"""DEV counterexamples: newly authored mutants survive old test cases yet violate contract.

This is deliberately exposed engineering material, not blinded model evidence.
It does not modify historical truth_cases.py or original receipts.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from truth_cases import CASES
from implementations import IMPLEMENTATIONS


def bad_nonnegative_overlap(a, b):
    """Wrong: silently clips start of overlap to 0, assuming nonnegative time."""
    return max(0, a[0], b[0]) < min(a[1], b[1])


def bad_case_insensitive_dedup(items):
    """Wrong: accidentally case-folds distinct string keys."""
    seen = set()
    result = []
    for key, payload in items:
        lower = key.casefold()
        if lower not in seen:
            seen.add(lower)
            result.append((key, payload))
    return result


class ShadowMutantTests(unittest.TestCase):
    def test_negative_interval_mutant_fools_original_cases(self):
        for name, args, expected in CASES['interval']:
            with self.subTest(name=name):
                self.assertEqual(bad_nonnegative_overlap(*args), expected)

    def test_new_negative_interval_valid_counterexample(self):
        args = ((-8, -4), (-6, -2))
        expected = True
        self.assertFalse(bad_nonnegative_overlap(*args))
        for name, fn in IMPLEMENTATIONS['interval']['correct'].items():
            with self.subTest(implementation=name):
                self.assertEqual(fn(*args), expected)

    def test_case_fold_mutant_fools_original_cases(self):
        for name, args, expected in CASES['first_seen']:
            with self.subTest(name=name):
                self.assertEqual(bad_case_insensitive_dedup(*args), expected)

    def test_new_case_sensitive_keys_valid_counterexample(self):
        args = ([('A', 1), ('a', 2)],)
        expected = [('A', 1), ('a', 2)]
        self.assertEqual(bad_case_insensitive_dedup(*args), [('A', 1)])
        for name, fn in IMPLEMENTATIONS['first_seen']['correct'].items():
            with self.subTest(implementation=name):
                self.assertEqual(fn(*args), expected)


if __name__ == '__main__':
    unittest.main()
