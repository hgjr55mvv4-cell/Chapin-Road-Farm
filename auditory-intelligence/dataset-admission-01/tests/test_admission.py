import csv
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
import wave
from sys import path as sys_path
sys_path.insert(0, str(Path(__file__).resolve().parents[1]))
from admission import audit, read_annotations, inspect_wav


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        wavepath = self.root / 'S-0001.wav'
        with wave.open(str(wavepath), 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(8000)
            w.writeframes(struct.pack('<' + 'h'*8000, *([500]*8000)))
        self.digest = hashlib.sha256(wavepath.read_bytes()).hexdigest()
        self.csv = self.root / 'poly.csv'
        self.csv.write_text('sound_name,class_name,start_perc,end_perc,start_time,end_time,event_length\n'
                            'S-0001.wav,Dog barkings and howlings,0,40,0.10,0.40,0.30\n')
        self.base = {'dataset':'DataSED', 'dataset_revision':'test-revision', 'candidates':[
            {'sound_name':'S-0001.wav','audio_sha256':self.digest,'split':'train',
             'provenance': {'lineage_status':'VERIFIED','original_recording_id':'upstream-one',
                           'evidence_ref':'synthetic-test-evidence','rights_status':'VERIFIED',
                           'rights_ref':'synthetic-test-rights','editing_history':'unchanged'},
             'independent_listening_checks': [
                {'decision':'EVENT_PRESENT','class_name':'Dog barkings and howlings',
                 'start_s':0.10,'end_s':0.40,'audio_sha256':self.digest,
                 'reviewer_id':'reviewer-A','receipt_ref':'synthetic-test-check'},
                {'decision':'CLASS_ABSENT_VERIFIED','class_name':'Vehicle idling',
                 'start_s':0.5,'end_s':0.8,'audio_sha256':self.digest,
                 'reviewer_id':'reviewer-A','receipt_ref':'synthetic-test-check'}]}]}

    def run_audit(self, obj=None):
        return audit(self.base if obj is None else obj, self.csv, self.root)

    def test_fixture_complete_is_admitted_as_software_fixture_only(self):
        a = self.run_audit()
        self.assertEqual(a['status'], 'ADMIT')
        self.assertEqual(a['admitted_candidates'], 1)

    def test_no_audio_is_blocked(self):
        (self.root/'S-0001.wav').unlink()
        self.assertEqual(self.run_audit()['status'], 'HOLD')

    def test_bad_hash_is_blocked(self):
        self.base['candidates'][0]['audio_sha256'] = '0'*64
        self.assertIn('AUDIO_HASH_MISMATCH', self.run_audit()['per_candidate'][0]['reasons'])

    def test_lineage_missing_is_blocked(self):
        self.base['candidates'][0]['provenance']['lineage_status'] = 'UNKNOWN'
        self.assertEqual(self.run_audit()['status'], 'HOLD')

    def test_missing_positive_review_blocked(self):
        self.base['candidates'][0]['independent_listening_checks'] = self.base['candidates'][0]['independent_listening_checks'][1:]
        self.assertIn('POSITIVE_LABELS_NOT_INDEPENDENTLY_VERIFIED', self.run_audit()['per_candidate'][0]['reasons'])

    def test_unlabeled_interval_is_not_verified_negative(self):
        self.base['candidates'][0]['independent_listening_checks'] = self.base['candidates'][0]['independent_listening_checks'][:1]
        self.assertIn('NO_VERIFIED_NEGATIVES', self.run_audit()['per_candidate'][0]['reasons'])

    def test_negative_cannot_overlap_positive(self):
        ch = self.base['candidates'][0]['independent_listening_checks'][1]
        ch.update({'class_name':'Dog barkings and howlings','start_s':0.2,'end_s':0.35})
        self.assertIn('NO_VERIFIED_NEGATIVES', self.run_audit()['per_candidate'][0]['reasons'])

    def test_source_leakage_blocks_both(self):
        cloned = json.loads(json.dumps(self.base['candidates'][0]))
        cloned['split'] = 'eval'
        self.base['candidates'].append(cloned)
        report = self.run_audit()
        self.assertEqual(report['status'],'HOLD')
        self.assertEqual(len(report['duplicate_train_eval_lineages']),1)
        self.assertTrue(all('TRAIN_EVAL_LINEAGE_LEAKAGE' in r['reasons'] for r in report['per_candidate']))

    def add_alias(self, name, split):
        source = self.base['candidates'][0]
        clone = json.loads(json.dumps(source))
        clone.update(sound_name=name, split=split)
        clone['provenance']['original_recording_id'] = name
        (self.root / name).write_bytes((self.root / source['sound_name']).read_bytes())
        with self.csv.open('a') as f:
            f.write(f'{name},Dog barkings and howlings,0,40,0.10,0.40,0.30\n')
        self.base['candidates'].append(clone)
        return clone

    def test_same_audio_across_splits_holds_all_aliases(self):
        self.add_alias('second-train.wav', 'train')
        self.add_alias('renamed-eval.wav', 'eval')
        report = self.run_audit()
        self.assertEqual(report['status'], 'HOLD')
        self.assertEqual(report['admitted_candidates'], 0)
        self.assertEqual(report['duplicate_train_eval_lineages'], [])
        for row in report['per_candidate']:
            self.assertEqual(row['status'], 'HOLD')
            self.assertIn('TRAIN_EVAL_AUDIO_HASH_LEAKAGE', row['reasons'])
            self.assertEqual(row['positive_spans_verified'], [])
            self.assertEqual(row['negative_spans_verified'], [])

    def test_duplicate_audio_in_one_split_is_not_cross_split_leakage(self):
        self.add_alias('also-train.wav', 'train')
        self.assertEqual(self.run_audit()['status'], 'ADMIT')

    def test_unverified_digest_does_not_hold_an_independent_candidate(self):
        alias = self.add_alias('eval.wav', 'eval')
        # Valid PCM, different samples, but still declares the first file's hash.
        path = self.root / alias['sound_name']
        data = path.read_bytes()
        path.write_bytes(data[:-2] + b'\x00\x00')
        train, evaluation = self.run_audit()['per_candidate']
        self.assertEqual(train['status'], 'ADMIT')
        self.assertIn('AUDIO_HASH_MISMATCH', evaluation['reasons'])
        self.assertNotIn('TRAIN_EVAL_AUDIO_HASH_LEAKAGE', evaluation['reasons'])

        # Once all references match the distinct file, both splits can pass.
        alias['audio_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        for check in alias['independent_listening_checks']:
            check['audio_sha256'] = alias['audio_sha256']
        self.assertEqual(self.run_audit()['admitted_candidates'], 2)

    def test_timestamp_outside_audio(self):
        self.csv.write_text('sound_name,class_name,start_time,end_time\nS-0001.wav,Dog barkings and howlings,0.9,1.7\n')
        self.assertIn('ANNOTATION_OUTSIDE_AUDIO', self.run_audit()['per_candidate'][0]['reasons'])

    def test_missing_columns_rejected(self):
        self.csv.write_text('filename,label,start,end\na,b,0,1\n')
        with self.assertRaises(ValueError): read_annotations(self.csv)

    def test_short_csv_row_yields_a_line_numbered_hold(self):
        with self.csv.open('a') as f:
            f.write('S-0001.wav\n')
        report = self.run_audit()
        self.assertEqual(report['status'], 'HOLD')
        self.assertEqual(report['admitted_candidates'], 0)
        self.assertIn('INVALID_ANNOTATION_ROW', report['per_candidate'][0]['reasons'])
        self.assertEqual(report['unverified_annotation_rows'],
                         [{'line': 3, 'reason': 'INVALID_ANNOTATION_ROW', 'sound_name': 'S-0001.wav'}])

    def test_unattributable_row_holds_dataset_without_assigning_it_to_a_clip(self):
        with self.csv.open('a') as f:
            f.write(',unknown class\n')
        report = self.run_audit()
        self.assertEqual(report['status'], 'HOLD')
        self.assertEqual(report['per_candidate'][0]['status'], 'ADMIT')
        self.assertEqual(report['unverified_annotation_rows'],
                         [{'line': 3, 'reason': 'INVALID_ANNOTATION_ROW'}])

    def test_nan_time_is_rejected(self):
        self.csv.write_text('sound_name,class_name,start_time,end_time\nS-0001.wav,Dog,nan,1\n')
        spans, problems = read_annotations(self.csv)
        self.assertEqual(spans, {})
        self.assertEqual(len(problems),1)

    def test_audio_header_truncation_detected(self):
        wavepath = self.root/'S-0001.wav'
        truncated = wavepath.read_bytes()[:-100]
        wavepath.write_bytes(truncated)
        h = hashlib.sha256(truncated).hexdigest()
        self.assertEqual(inspect_wav(wavepath,h)[1], 'TRUNCATED_AUDIO')

    def test_negative_bad_hash_receipt_rejected(self):
        self.base['candidates'][0]['independent_listening_checks'][1]['audio_sha256']='a'*64
        self.assertIn('NO_VERIFIED_NEGATIVES',self.run_audit()['per_candidate'][0]['reasons'])

    def test_filename_path_traversal_rejected(self):
        self.base['candidates'][0]['sound_name'] = '../S-0001.wav'
        self.assertIn('BAD_FILE_NAME', self.run_audit()['per_candidate'][0]['reasons'])

if __name__ == '__main__': unittest.main()
