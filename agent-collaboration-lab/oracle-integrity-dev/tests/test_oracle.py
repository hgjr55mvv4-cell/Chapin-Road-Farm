"""Executable tests assert both specificity and mutation rejection."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from implementations import IMPLEMENTATIONS
from truth_cases import CASES
from verify_oracle import evaluate_all


class TruthTableTests(unittest.TestCase):
    def test_public_truth_labels(self):
        self.assertEqual(len(CASES), 2)
        self.assertTrue(all(len(cases) >= 8 for cases in CASES.values()))
        self.assertEqual(len({name for name, _, _ in CASES['interval']}), 8)
        self.assertEqual(len({name for name, _, _ in CASES['first_seen']}), 8)

    def test_correct_variants_accepted(self):
        for family, variants in IMPLEMENTATIONS.items():
            for name, fn in variants['correct'].items():
                with self.subTest(family=family, name=name):
                    for case_name, args, expected in CASES[family]:
                        with self.subTest(case=case_name):
                            self.assertEqual(fn(*args), expected)

    def test_each_mutant_rejected_with_counterexample(self):
        for family, variants in IMPLEMENTATIONS.items():
            for name, fn in variants['incorrect'].items():
                with self.subTest(family=family, mutant=name):
                    self.assertTrue(any(fn(*args) != expected for _, args, expected in CASES[family]),
                                    'undetected mutant; oracle not adequate for this family')

    def test_runner_reports_full_sensitivity_and_specificity(self):
        report = evaluate_all()['summary']
        self.assertEqual(report['correct_accepted'], report['correct_total'])
        self.assertEqual(report['mutants_rejected'], report['mutants_total'])
        self.assertGreaterEqual(report['correct_total'], 4)
        self.assertGreaterEqual(report['mutants_total'], 6)


if __name__ == '__main__':
    unittest.main()
