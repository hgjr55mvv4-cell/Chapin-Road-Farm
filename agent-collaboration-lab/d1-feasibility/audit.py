"""D1 engineering preflight for declared agent manifests (stdlib-only).

This NEVER executes or authenticates a model, verifies blindness, or proves
the truth labels. SYNTHETIC_DEV can never qualify as prospective evidence.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

ARMS = ('S', 'P1', 'P2')
TRUTHS = ('valid', 'faulty', 'unknown')
DECISIONS = ('ACCEPT', 'REJECT', 'ABSTAIN')


def ratio(num, den):
    return num / den if den else None


def parallel(p1, p2):
    if p1 not in DECISIONS or p2 not in DECISIONS:
        raise ValueError('invalid decision')
    return 'REJECT' if 'REJECT' in (p1, p2) else (
        'ABSTAIN' if 'ABSTAIN' in (p1, p2) else 'ACCEPT')


def score(rows, arm):
    tally = Counter((r['truth'], r[arm]) for r in rows)
    va, vr, vu = (tally['valid', d] for d in DECISIONS)
    fa, fr, fu = (tally['faulty', d] for d in DECISIONS)
    n_valid, n_faulty = va + vr + vu, fa + fr + fu
    n_decided = va + vr + fa + fr
    return {
        'counts': {'valid_accepted': va, 'valid_rejected': vr,
                   'valid_abstained': vu, 'faulty_accepted': fa,
                   'faulty_rejected': fr, 'faulty_abstained': fu,
                   'known_truth': n_valid + n_faulty, 'decided_known_truth': n_decided,
                   'unknown_truth': sum(tally['unknown', d] for d in DECISIONS)},
        'rates': {
            'coverage_known_truth': ratio(n_decided, n_valid + n_faulty),
            'selective_error_decided': ratio(vr + fa, n_decided),
            'false_assurance_all_faulty': ratio(fa, n_faulty),
            'false_assurance_decided_faulty': ratio(fa, fa + fr),
            'false_rejection_all_valid': ratio(vr, n_valid),
            'false_rejection_decided_valid': ratio(vr, va + vr),
        },
    }


def check(m):
    issues = []
    def issue(x):
        issues.append(x)
    if not isinstance(m, dict):
        return {'status': 'BLOCKED', 'issues': ['manifest is not an object'],
                'scores': {}, 'warning': 'No authentication of provider calls'}
    synthetic = m.get('evidence_type') == 'SYNTHETIC_DEV'
    if m.get('protocol') != 'D1-FEASIBILITY-01-v0.1':
        issue('protocol mismatch')
    if m.get('evidence_type') not in ('SYNTHETIC_DEV', 'PROSPECTIVE_PILOT'):
        issue('invalid evidence_type')
    if not isinstance(m.get('frozen_spec_sha256'), str) or not m['frozen_spec_sha256']:
        issue('frozen specification reference missing')
    cap = m.get('token_cap_per_task')
    if type(cap) is not int or cap <= 0:
        issue('invalid equal opportunity token cap')
    agents = m.get('agents')
    if not isinstance(agents, dict):
        issue('agents not an object')
        agents = {}
    for arm in ARMS:
        a = agents.get(arm)
        if not isinstance(a, dict):
            issue(f'{arm}: missing agent')
            continue
        for field in ('model','input_manifest_sha256','artifact_sha256','execution_receipt_id'):
            if not isinstance(a.get(field), str) or not a[field]:
                issue(f'{arm}: missing {field}')
        for field in ('observable_tokens','human_handoffs'):
            if type(a.get(field)) is not int or a[field] < 0:
                issue(f'{arm}: invalid {field}')
    if all(isinstance(agents.get(a), dict) for a in ARMS):
        if len({agents[a].get('input_manifest_sha256') for a in ARMS}) != 1:
            issue('input manifest references differ')
        receipt_ids = [agents[a].get('execution_receipt_id') for a in ARMS]
        if len(set(receipt_ids)) != len(ARMS):
            issue('declared receipt IDs are not distinct')
        used = [agents[a].get('observable_tokens') for a in ARMS]
        if all(type(v) is int for v in used) and type(cap) is int and cap > 0:
            if used[0] > cap: issue('S observed use exceeds cap')
            if used[1] + used[2] > cap: issue('P combined observed use exceeds cap')
    candidates = m.get('candidates')
    if not isinstance(candidates, list) or not candidates:
        issue('no candidate rows')
        candidates = []
    ids, rows = [], []
    for n, row in enumerate(candidates):
        if not isinstance(row, dict):
            issue(f'candidate {n} is not an object')
            continue
        cid = row.get('id')
        if not isinstance(cid, str) or not cid.strip():
            issue(f'candidate {n}: missing id')
        ids.append(cid)
        truth = row.get('truth')
        if not isinstance(truth, str) or truth not in TRUTHS:
            issue(f'candidate {n}: invalid truth')
            continue
        if truth == 'unknown' and not row.get('ambiguity_ref'):
            issue(f'candidate {n}: unknown lacks ambiguity_ref')
        elif truth in ('valid','faulty') and not row.get('adjudication_ref'):
            issue(f'candidate {n}: truth lacks adjudication_ref')
        if any(not isinstance(row.get(a), str) or row[a] not in DECISIONS for a in ARMS):
            issue(f'candidate {n}: invalid decision')
            continue
        rows.append({**row, 'P': parallel(row['P1'], row['P2'])})
    if len(ids) != len(set(ids)):
        issue('duplicate candidate ids')
    if synthetic:
        issue('SYNTHETIC_DEV is not a model run or scientific evidence')
    elif not m.get('operator_approval_receipt'):
        issue('no operator-approval receipt for declared pilot')
    scores = {a: score(rows, a) for a in (*ARMS, 'P')} if rows else {}
    for arm in ('S', 'P'):
        if scores and scores[arm]['counts']['faulty_accepted']:
            issue(f'{arm} false-assured an adjudicated-faulty row; severity review required')
    return {
        'status': 'ENGINEERING_DEMO_NOT_MODEL_RUN' if synthetic else
                  ('BLOCKED' if issues else 'DECLARATIONS_COMPLETE_UNAUTHENTICATED'),
        'issues': issues, 'scores': scores,
        'warning': 'Declared receipt IDs, hash strings, source access and labels are not authenticated by this parser.'
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('manifest', type=Path)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    report = check(json.loads(args.manifest.read_text(encoding='utf-8')))
    encoded = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.out:
        args.out.write_text(encoded, encoding='utf-8')
    print(encoded, end='')
    if not report['scores']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
