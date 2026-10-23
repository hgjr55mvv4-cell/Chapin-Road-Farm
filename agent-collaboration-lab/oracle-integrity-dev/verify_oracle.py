"""Check executable oracle rejection/acceptance on documented mutation probes.

Runs no model inference. Standard-library only. Exits nonzero on any contract failure.
"""
import json
import platform
import sys
from implementations import IMPLEMENTATIONS
from truth_cases import CASES


def evaluate_all():
    report = {'python': platform.python_version(), 'platform': sys.platform, 'families': {}, 'summary': {}}
    for family, variants in IMPLEMENTATIONS.items():
        records = []
        for expected_label in ('correct', 'incorrect'):
            for name, fn in variants[expected_label].items():
                failed = []
                for case_name, args, expected in CASES[family]:
                    try:
                        actual = fn(*args)
                        if actual != expected:
                            failed.append(case_name)
                    except Exception as exc:
                        failed.append(f'{case_name}: {type(exc).__name__}')
                predicted_correct = len(failed) == 0
                should_be_correct = expected_label == 'correct'
                records.append(dict(name=name, expected_correct=should_be_correct,
                                    accepted=predicted_correct, cases_failed=failed))
        report['families'][family] = dict(num_truth_cases=len(CASES[family]), implementations=records)
    allrecords = [r for v in report['families'].values() for r in v['implementations']]
    good = [r for r in allrecords if r['expected_correct']]
    mutants = [r for r in allrecords if not r['expected_correct']]
    report['summary'] = {
        'correct_accepted': sum(r['accepted'] for r in good),
        'correct_total': len(good),
        'mutants_rejected': sum(not r['accepted'] for r in mutants),
        'mutants_total': len(mutants),
        'mutation_detection': 'PASS' if all(not r['accepted'] for r in mutants) else 'FAIL',
        'correct_acceptance': 'PASS' if all(r['accepted'] for r in good) else 'FAIL',
    }
    return report


if __name__ == '__main__':
    report = evaluate_all()
    print(json.dumps(report, indent=2))
    good = report['summary']
    if good['mutation_detection'] != 'PASS' or good['correct_acceptance'] != 'PASS':
        sys.exit(1)
