"""DataSED candidate gate. Evidence checker, NOT an audio event detector.

Requires explicit provenance, actual audio bytes, and independent listening receipts.
No label absence is treated as evidence of silence or absence of a class.
"""
import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
import wave

REQUIRED_COLUMNS = ('sound_name', 'class_name', 'start_time', 'end_time')
TOLERANCE_S = 0.5


def _finite_number(value):
    try:
        out = float(value)
        return out if math.isfinite(out) else None
    except (TypeError, ValueError):
        return None


def read_annotations(csv_path):
    """Read exact observed DataSED time-label schema; record all ambiguous rows."""
    with Path(csv_path).open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not set(REQUIRED_COLUMNS).issubset(reader.fieldnames):
            raise ValueError('Missing required time-label columns')
        spans = defaultdict(list)
        problems = []
        for n, row in enumerate(reader, start=2):
            name = row['sound_name'].strip()
            cls = row['class_name'].strip()
            a, b = _finite_number(row['start_time']), _finite_number(row['end_time'])
            if not name or not cls or a is None or b is None or a < 0 or b <= a:
                problems.append({'line': n, 'reason': 'INVALID_ANNOTATION_ROW'})
                continue
            spans[name].append({'class_name': cls, 'start_s': a, 'end_s': b})
    for items in spans.values():
        items.sort(key=lambda x: (x['start_s'], x['end_s'], x['class_name']))
    return dict(spans), problems


def inspect_wav(path, expected_sha256):
    p = Path(path)
    if not p.is_file():
        return None, 'MISSING_AUDIO'
    if p.stat().st_size > 64 * 1024 * 1024:
        return None, 'AUDIO_TOO_LARGE_FOR_BOUNDED_ADMISSION'
    data = p.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64 or digest.lower() != expected_sha256.lower():
        return None, 'AUDIO_HASH_MISMATCH'
    try:
        with wave.open(str(p), 'rb') as w:
            n = w.getnframes(); sr = w.getframerate()
            if not sr or n <= 0 or w.getcomptype() != 'NONE':
                return None, 'UNSUPPORTED_AUDIO'
            expected_bytes = n * w.getnchannels() * w.getsampwidth()
            raw = w.readframes(n)
            if len(raw) != expected_bytes:
                return None, 'TRUNCATED_AUDIO'
            duration = n / sr
    except (wave.Error, EOFError, OSError, ValueError):
        return None, 'UNREADABLE_AUDIO'
    return {'sha256': digest, 'duration_s': duration, 'sample_rate_hz': sr}, None


def _valid_provenance(rec):
    prov = rec.get('provenance') or {}
    return (prov.get('lineage_status') == 'VERIFIED'
            and isinstance(prov.get('original_recording_id'), str)
            and bool(prov['original_recording_id'].strip())
            and isinstance(prov.get('evidence_ref'), str)
            and bool(prov['evidence_ref'].strip())
            and prov.get('rights_status') == 'VERIFIED'
            and isinstance(prov.get('rights_ref'), str)
            and bool(prov['rights_ref'].strip())
            and isinstance(prov.get('editing_history'), str)
            and bool(prov['editing_history'].strip()))


def _confirmed_positive(check, span, digest, duration):
    if not isinstance(check, dict) or check.get('decision') != 'EVENT_PRESENT':
        return False
    if check.get('audio_sha256') != digest or not check.get('reviewer_id') or not check.get('receipt_ref'):
        return False
    a, b = _finite_number(check.get('start_s')), _finite_number(check.get('end_s'))
    if a is None or b is None or a < 0 or b <= a or b > duration:
        return False
    return (check.get('class_name') == span['class_name'] and
            abs(a - span['start_s']) <= TOLERANCE_S and
            abs(b - span['end_s']) <= TOLERANCE_S)


def _confirmed_negative(check, spans, digest, duration):
    if not isinstance(check, dict) or check.get('decision') != 'CLASS_ABSENT_VERIFIED':
        return False
    if check.get('audio_sha256') != digest or not check.get('reviewer_id') or not check.get('receipt_ref'):
        return False
    cls = check.get('class_name')
    a, b = _finite_number(check.get('start_s')), _finite_number(check.get('end_s'))
    if not cls or a is None or b is None or a < 0 or b <= a or b > duration:
        return False
    # Any overlapping positive source label blocks an unambiguous negative.
    if any(s['class_name'] == cls and a < s['end_s'] and b > s['start_s'] for s in spans):
        return False
    return True


def audit(manifest, labels_csv, audio_dir):
    if manifest.get('dataset') != 'DataSED' or not isinstance(manifest.get('dataset_revision'), str):
        raise ValueError('Expected named DataSED revision')
    spans_by_clip, annotation_errors = read_annotations(labels_csv)
    records = manifest.get('candidates')
    if not isinstance(records, list) or not records:
        raise ValueError('No explicit candidate records')
    outcomes = []
    lineage_by_split = defaultdict(set)
    for rec in records:
        name = rec.get('sound_name', '')
        split = rec.get('split')
        reasons = []
        if not name or '/' in name or '\\' in name or not name.lower().endswith('.wav'):
            reasons.append('BAD_FILE_NAME')
        if split not in ('train', 'eval'):
            reasons.append('BAD_SPLIT')
        if not _valid_provenance(rec):
            reasons.append('UNVERIFIED_LINEAGE_OR_RIGHTS')
        observed, error = (inspect_wav(Path(audio_dir) / name, rec.get('audio_sha256'))
                           if 'BAD_FILE_NAME' not in reasons else (None, 'BAD_FILE_NAME'))
        if error:
            reasons.append(error)
        spans = spans_by_clip.get(name, [])
        if not spans:
            reasons.append('NO_POSITIVE_TIME_LABELS')
        if observed and any(s['end_s'] > observed['duration_s'] for s in spans):
            reasons.append('ANNOTATION_OUTSIDE_AUDIO')
        checks = rec.get('independent_listening_checks') or []
        pos, neg = [], []
        if observed:
            for s in spans:
                if s['end_s'] <= observed['duration_s'] and any(
                        _confirmed_positive(ch, s, observed['sha256'], observed['duration_s'])
                        for ch in checks):
                    pos.append(s)
            for ch in checks:
                if _confirmed_negative(ch, spans, observed['sha256'], observed['duration_s']):
                    neg.append({'class_name': ch['class_name'], 'start_s': ch['start_s'],
                                'end_s': ch['end_s']})
        if spans and len(pos) != len(spans):
            reasons.append('POSITIVE_LABELS_NOT_INDEPENDENTLY_VERIFIED')
        if not neg:
            reasons.append('NO_VERIFIED_NEGATIVES')
        if _valid_provenance(rec) and split in ('train', 'eval'):
            lineage_by_split[rec['provenance']['original_recording_id']].add(split)
        outcomes.append({'sound_name': name, 'split': split,
                         'status': 'ADMIT' if not reasons else 'HOLD',
                         'reasons': sorted(set(reasons)),
                         'positive_spans_verified': pos if not reasons else [],
                         'negative_spans_verified': neg if not reasons else [],
                         'n_positive_labels_in_source': len(spans),
                         'audio_observed': observed is not None})
    duplicate_lineage = sorted(k for k, v in lineage_by_split.items() if len(v) > 1)
    if duplicate_lineage:
        for rec, result in zip(records, outcomes):
            if (rec.get('provenance') or {}).get('original_recording_id') in duplicate_lineage:
                result['status'] = 'HOLD'
                result['reasons'] = sorted(set(result['reasons'] + ['TRAIN_EVAL_LINEAGE_LEAKAGE']))
                result['positive_spans_verified'] = []
                result['negative_spans_verified'] = []
    summary = {
        'gate': 'AUDITORY_DATASED_ADMISSION_01_v0.1',
        'status': 'ADMIT' if outcomes and all(x['status'] == 'ADMIT' for x in outcomes)
                  and not annotation_errors else 'HOLD',
        'dataset': manifest['dataset'],
        'dataset_revision': manifest['dataset_revision'],
        'total_candidates': len(outcomes),
        'admitted_candidates': sum(x['status'] == 'ADMIT' for x in outcomes),
        'unverified_annotation_rows': annotation_errors,
        'duplicate_train_eval_lineages': duplicate_lineage,
        'per_candidate': outcomes,
        'research_limits': [
            'Independently listening-verified event labels require external human evidence and are NOT produced by this checker.',
            'No annotation row never implies an event was absent.',
            'Human-written provenance fields are claims to audit, not automatically authenticated by this script.',
            'Metadata admission cannot establish that a model understands a physical emitter or machine failure.',
        ],
    }
    return summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', required=True)
    p.add_argument('--annotations', required=True)
    p.add_argument('--audio-dir', required=True)
    p.add_argument('--out', default='admission_report.json')
    args = p.parse_args()
    result = audit(json.loads(Path(args.manifest).read_text()), args.annotations, args.audio_dir)
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': result['status'], 'admitted_candidates': result['admitted_candidates'],
                      'total_candidates': result['total_candidates'],
                      'duplicate_train_eval_lineages': result['duplicate_train_eval_lineages']}, sort_keys=True))
    raise SystemExit(0 if result['status'] == 'ADMIT' else 2)

if __name__ == '__main__':
    main()