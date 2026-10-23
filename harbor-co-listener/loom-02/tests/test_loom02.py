import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from loom02 import (FAMILIES, source_probability, any_exact_probability_given_source,
                    analytical_rates, choose_alert, simulate, report)

class Loom02Tests(unittest.TestCase):
    def test_analytical_template_mass(self):
        self.assertAlmostEqual(sum(source_probability((i,j,k),FAMILIES['concentrated'])
                                   for i in range(8) for j in range(8) for k in range(8)),1.0)
    def test_expected_collision_rate(self):
        p = sum(w*w for w in FAMILIES['concentrated'])**3
        observed_analytic = analytical_rates(FAMILIES['concentrated'],FAMILIES['concentrated'],1)
        self.assertAlmostEqual(observed_analytic['raw_exact']['null_alert_probability'],p)
        self.assertGreater(p, .12)
    def test_source_conditioning_rejects_common_triple(self):
        common=(0,0,0)
        rare=(1,1,1)
        self.assertAlmostEqual(source_probability(common,FAMILIES['concentrated']),.7**3)
        self.assertGreater(any_exact_probability_given_source(common,FAMILIES['concentrated'],16),.05)
        self.assertLess(any_exact_probability_given_source(rare,FAMILIES['concentrated'],16),.05)
        self.assertFalse(choose_alert(common,[common],FAMILIES['concentrated'],1)['query_calibrated'])
        self.assertTrue(choose_alert(rare,[rare],FAMILIES['concentrated'],1)['query_calibrated'])
    def test_query_search_scope_increases_chance(self):
        source=(0,0,1)
        pair=any_exact_probability_given_source(source,FAMILIES['concentrated'],1)
        query=any_exact_probability_given_source(source,FAMILIES['concentrated'],16)
        self.assertLess(pair,.05)
        self.assertGreater(query,.05)
    def test_matched_query_fpr_is_bounded_analytically(self):
        for family,w in FAMILIES.items():
            for m in (1,16):
                a=analytical_rates(w,w,m)['query_calibrated']
                self.assertLessEqual(a['null_alert_probability'],.05+1e-12)
                self.assertLessEqual(a['planted_detection_probability'],1)
    def test_concentrated_raw_exceeds_alpha(self):
        w=FAMILIES['concentrated']
        for m in (1,16):
            self.assertGreater(analytical_rates(w,w,m)['raw_exact']['null_alert_probability'],.05)
    def test_wrong_family_query_can_exceed_target(self):
        a=analytical_rates(FAMILIES['concentrated'],FAMILIES['uniform'],16)
        self.assertGreater(a['query_calibrated']['null_alert_probability'],.05)
    def test_planted_exact_positive_is_detected_by_raw(self):
        w=FAMILIES['concentrated']
        z=simulate(w,w,16,24,345)
        self.assertEqual(z['raw_exact']['positive_detections'],24)
    def test_seed_reproducible(self):
        w=FAMILIES['concentrated']
        self.assertEqual(simulate(w,w,16,30,123),simulate(w,w,16,30,123))
    def test_no_silent_search_scope_change(self):
        with self.assertRaises(ValueError):
            choose_alert((0,1,2),[(0,1,2)],FAMILIES['uniform'],16)
    def test_invalid_source_and_weights(self):
        with self.assertRaises(ValueError):source_probability((0,1),FAMILIES['uniform'])
        with self.assertRaises(ValueError):source_probability((True,0,1),FAMILIES['uniform'])
        with self.assertRaises(ValueError):source_probability((0,1,2),[.1]*8)
    def test_report_has_expected_query_denominators(self):
        r=report(20,10)
        self.assertEqual(len(r['scenarios']),6)
        self.assertTrue(all(x['queries_per_condition']==20 for x in r['scenarios']))

if __name__=='__main__': unittest.main()
