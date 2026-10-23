"""Three-way verifier scoring, including undefined rates, for engineering DEV.

Input: iterable of {'truth': 'valid'|'faulty'|'unknown',
'decision': 'ACCEPT'|'REJECT'|'ABSTAIN'}.
Unknown ground truth is tracked but not silently assigned to either class.
"""
from collections import Counter

TRUTHS = {'valid', 'faulty', 'unknown'}
DECISIONS = {'ACCEPT', 'REJECT', 'ABSTAIN'}


def _rate(num, den):
    return None if den == 0 else num / den


def conservative_parallel(first, second):
    """Illustrative fixed rule, not an established optimal aggregation policy."""
    if first not in DECISIONS or second not in DECISIONS:
        raise ValueError('Unknown verifier decision')
    if 'REJECT' in (first, second):
        return 'REJECT'
    if 'ABSTAIN' in (first, second):
        return 'ABSTAIN'
    return 'ACCEPT'


def evaluate(rows):
    counts = Counter()
    for row in rows:
        truth, decision = row['truth'], row['decision']
        if truth not in TRUTHS or decision not in DECISIONS:
            raise ValueError('Invalid truth or decision')
        counts[f'{truth}:{decision}'] += 1
    va = counts['valid:ACCEPT']
    vr = counts['valid:REJECT']
    vu = counts['valid:ABSTAIN']
    fa = counts['faulty:ACCEPT']
    fr = counts['faulty:REJECT']
    fu = counts['faulty:ABSTAIN']
    n_valid = va + vr + vu
    n_faulty = fa + fr + fu
    n_adjudicated = n_valid + n_faulty
    n_decided = va + vr + fa + fr
    n_unknown = sum(counts[f'unknown:{d}'] for d in DECISIONS)
    return {
        'counts': {
            'valid_accepted': va, 'valid_rejected': vr, 'valid_abstained': vu,
            'faulty_accepted': fa, 'faulty_rejected': fr, 'faulty_abstained': fu,
            'unresolved_truth': n_unknown, 'adjudicated': n_adjudicated,
            'decided': n_decided,
        },
        'rates': {
            'coverage': _rate(n_decided, n_adjudicated),
            'selective_error_among_decisions': _rate(vr + fa, n_decided),
            'false_assurance_all_faulty': _rate(fa, n_faulty),
            'false_assurance_decided_faulty': _rate(fa, fa + fr),
            'false_rejection_all_valid': _rate(vr, n_valid),
            'false_rejection_decided_valid': _rate(vr, va + vr),
            'abstention_valid': _rate(vu, n_valid),
            'abstention_faulty': _rate(fu, n_faulty),
        },
    }
