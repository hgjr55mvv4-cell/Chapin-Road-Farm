"""Check executable oracle rejection/acceptance on documented mutation probes.

Runs no model inference. Standard-library only. Exits nonzero on any contract failure.
"""
import json
import platform
import sys
from implementations import IMPLEMENTATIONS
from truth_cases import CASES


# The public DEV receipt covers these implementations and eight named cases per family.
PUBLISHED_VARIANTS = {
    'interval': {'correct': {'max_min', 'direct'},
                 'incorrect': {'touch_counts', 'containment_only', 'inclusive_end'}},
    'first_seen': {'correct': {'set_append', 'reverse_dict'},
                   'incorrect': {'last_wins', 'sort_keys', 'adjacent_only'}},
}


def coverage_issues():
    issues = []
    for family in sorted(PUBLISHED_VARIANTS.keys() | IMPLEMENTATIONS.keys() | CASES.keys()):
        cases = CASES.get(family, ())
        minimum = 8 if family in PUBLISHED_VARIANTS else 1
        names = [name for name, _, _ in cases]
        if len(names) < minimum or len(set(names)) != len(names):
            issues.append(f'{family}: expected at least {minimum} cases with distinct names')
        for group in ('correct', 'incorrect'):
            variants = IMPLEMENTATIONS.get(family, {}).get(group, {})
            required = PUBLISHED_VARIANTS.get(family, {}).get(group, set())
            missing = sorted(required.difference(variants))
            if missing:
                issues.append(f'{family}/{group}: missing {", ".join(missing)}')
            elif not variants:
                issues.append(f'{family}/{group}: no implementations')
            for name, fn in variants.items():
                if not callable(fn):
                    issues.append(f'{family}/{group}: {name} is not callable')
    return issues


def evaluate_all():
    report = {'python': platform.python_version(), 'platform': sys.platform, 'families': {}, 'summary': {}}
    issues = coverage_issues()
    if issues:
        report['coverage_issues'] = issues
        report['summary'] = {
            'correct_accepted': 0, 'correct_total': 0,
            'mutants_rejected': 0, 'mutants_total': 0,
            'mutation_detection': 'INCOMPLETE', 'correct_acceptance': 'INCOMPLETE',
        }
        return report
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
