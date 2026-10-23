import copy
import json
import sys
import unittest
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from audit import check, parallel
demo = json.loads((root / 'examples/synthetic_only.json').read_text(encoding='utf-8'))


class IntakeTests(unittest.TestCase):
    def trial(self):
        return copy.deepcopy(demo)

    def test_demo_is_not_real_inference(self):
        report = check(self.trial())
        self.assertEqual(report['status'], 'ENGINEERING_DEMO_NOT_MODEL_RUN')
        self.assertTrue(any('SYNTHETIC_DEV' in x for x in report['issues']))
        self.assertEqual(report['scores']['S']['rates']['coverage_known_truth'], .75)
        self.assertEqual(report['scores']['P']['counts']['valid_rejected'], 1)
        self.assertEqual(report['scores']['P']['counts']['unknown_truth'], 1)

    def test_predeclared_aggregation(self):
        self.assertEqual(parallel('ACCEPT','REJECT'), 'REJECT')
        self.assertEqual(parallel('ABSTAIN','ACCEPT'), 'ABSTAIN')
        self.assertEqual(parallel('ACCEPT','ACCEPT'), 'ACCEPT')

    def test_budget_cap_overrun(self):
        f = self.trial()
        f['agents']['P2']['observable_tokens'] += 1
        self.assertTrue(any('exceeds cap' in e for e in check(f)['issues']))

    def test_budget_opportunity_not_equal_realized_usage(self):
        f = self.trial()
        f['agents']['S']['observable_tokens'] = 10
        self.assertFalse(any('exceeds cap' in e for e in check(f)['issues']))

    def test_unknown_requires_dispute_ref(self):
        f = self.trial()
        del f['candidates'][-1]['ambiguity_ref']
        self.assertTrue(any('ambiguity_ref' in e for e in check(f)['issues']))

    def test_duplicate_ids(self):
        f = self.trial()
        f['candidates'][0]['id'] = f['candidates'][1]['id']
        self.assertTrue(any('duplicate candidate' in e for e in check(f)['issues']))

    def test_invalid_unhashable_truth_is_flagged(self):
        f = self.trial()
        f['candidates'][0]['truth'] = []
        self.assertTrue(any('invalid truth' in e for e in check(f)['issues']))

    def test_fake_pilot_authorization_missing(self):
        f = self.trial()
        f['evidence_type'] = 'PROSPECTIVE_PILOT'
        self.assertEqual(check(f)['status'], 'BLOCKED')
        self.assertTrue(any('operator-approval' in e for e in check(f)['issues']))

    def test_duplicate_receipts(self):
        f = self.trial()
        f['agents']['P2']['execution_receipt_id'] = f['agents']['P1']['execution_receipt_id']
        self.assertTrue(any('not distinct' in e for e in check(f)['issues']))

    def test_critical_false_accept_flagged(self):
        f = self.trial()
        f['candidates'][2]['S'] = 'ACCEPT'
        self.assertTrue(any('false-assured' in e for e in check(f)['issues']))

    def test_all_abstain_cannot_claim_zero_decided_error(self):
        f = self.trial()
        for row in f['candidates']:
            for arm in ('S','P1','P2'):
                row[arm] = 'ABSTAIN'
        r = check(f)['scores']['S']['rates']
        self.assertEqual(r['coverage_known_truth'], 0)
        self.assertIsNone(r['selective_error_decided'])


if __name__ == '__main__':
    unittest.main()
