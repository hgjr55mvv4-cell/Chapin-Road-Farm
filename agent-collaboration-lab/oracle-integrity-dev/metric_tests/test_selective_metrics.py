import unittest
from selective_metrics import evaluate, conservative_parallel


class MetricsTests(unittest.TestCase):
    def test_explicit_denominators_and_abstention(self):
        rows = ([{'truth': 'valid', 'decision': d} for d in
                 ['ACCEPT', 'ACCEPT', 'REJECT', 'ABSTAIN']] +
                [{'truth': 'faulty', 'decision': d} for d in
                 ['REJECT', 'REJECT', 'REJECT', 'ACCEPT', 'ACCEPT',
                  'ABSTAIN', 'ABSTAIN', 'ABSTAIN']] +
                [{'truth': 'unknown', 'decision': 'REJECT'}])
        data = evaluate(rows)
        self.assertEqual(data['counts']['adjudicated'], 12)
        self.assertEqual(data['counts']['unresolved_truth'], 1)
        self.assertEqual(data['rates']['coverage'], 8 / 12)
        self.assertEqual(data['rates']['false_assurance_all_faulty'], 2 / 8)
        self.assertEqual(data['rates']['false_assurance_decided_faulty'], 2 / 5)
        self.assertEqual(data['rates']['false_rejection_decided_valid'], 1 / 3)
        self.assertEqual(data['rates']['selective_error_among_decisions'], 3 / 8)

    def test_all_abstain_is_not_false_assurance_zero_quality(self):
        out = evaluate([{'truth':'faulty','decision':'ABSTAIN'},
                        {'truth':'valid','decision':'ABSTAIN'}])
        self.assertEqual(out['rates']['coverage'], 0)
        self.assertIsNone(out['rates']['false_assurance_decided_faulty'])
        self.assertIsNone(out['rates']['selective_error_among_decisions'])

    def test_empty_population_is_unknown_not_zero(self):
        data = evaluate([])
        self.assertIsNone(data['rates']['coverage'])
        self.assertIsNone(data['rates']['false_assurance_all_faulty'])

    def test_conservative_aggregation_can_falsely_reject(self):
        self.assertEqual(conservative_parallel('ACCEPT','ACCEPT'),'ACCEPT')
        self.assertEqual(conservative_parallel('ABSTAIN','ACCEPT'),'ABSTAIN')
        self.assertEqual(conservative_parallel('ABSTAIN','REJECT'),'REJECT')
        self.assertEqual(conservative_parallel('REJECT','ACCEPT'),'REJECT')
        with self.assertRaises(ValueError):
            conservative_parallel('YES', 'REJECT')

    def test_invalid_truth_labels_raise(self):
        with self.assertRaises(ValueError):
            evaluate([{'truth':'maybe','decision':'ACCEPT'}])


if __name__ == '__main__':
    unittest.main()
