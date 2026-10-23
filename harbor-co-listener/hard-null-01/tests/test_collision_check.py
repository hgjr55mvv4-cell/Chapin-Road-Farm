import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from collision_check import collision_probability, wilson_interval, summary

class CollisionCheckTests(unittest.TestCase):
    def test_simple_independent_collision(self):
        self.assertAlmostEqual(collision_probability([.5,.5],3),.125)
    def test_concentrated_three_phrases(self):
        p=.7**2 + 7*(.3/7)**2
        self.assertAlmostEqual(collision_probability([.7]+[.3/7]*7,3),p**3)
    def test_expected_collisions(self):
        d=summary()
        self.assertTrue(d['internal_consistency'])
        self.assertEqual(d['reported']['null_alerts'],565)
        self.assertAlmostEqual(d['expected_exact_collisions_in_2048'],260.4136967463556)
    def test_wilson(self):
        lo,hi=wilson_interval(565,2048)
        self.assertTrue(.256<lo<.258)
        self.assertTrue(.295<hi<.297)
    def test_invalid_inputs(self):
        for values,n in [([.7,.7],3),([-.1,1.1],2),([],3),([1.0],0)]:
            with self.subTest(values=values,n=n):
                with self.assertRaises(ValueError):collision_probability(values,n)
        with self.assertRaises(ValueError):wilson_interval(9,8)

if __name__=='__main__':unittest.main()
