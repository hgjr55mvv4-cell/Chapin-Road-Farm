import sys, unittest, random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from loom import melody,intervals,ordered_similarity,histogram_similarity,absolute_pitch_similarity,evaluate,make_triplet

class LoomTests(unittest.TestCase):
    def test_interval_transposition_invariant(self):
        a=melody(60,[2,-3,1,3]);b=tuple(n+7 for n in a)
        self.assertEqual(intervals(a),intervals(b))
        self.assertEqual(ordered_similarity(a,b),1)
        self.assertEqual(absolute_pitch_similarity(a,b),0)
    def test_histogram_control_does_not_see_order(self):
        a=melody(60,[1,2,3,-2]);b=melody(65,[3,2,1,-2])
        self.assertEqual(histogram_similarity(a,b),1)
        self.assertLess(ordered_similarity(a,b),1)
    def test_no_label_filtering_for_null(self):
        class IdentityShuffle:
            def __init__(self):self.rng=random.Random(2)
            def choice(self,x):return self.rng.choice(x)
            def randint(self,a,b):return self.rng.randint(a,b)
            def shuffle(self,x):pass
        a,b,c,_=make_triplet(IdentityShuffle())
        self.assertEqual(ordered_similarity(a,c),1)
        self.assertEqual(histogram_similarity(a,c),1)
    def test_deterministic_replay(self):
        self.assertEqual(evaluate(11,12),evaluate(11,12))
    def test_results_valid_and_counts(self):
        z=evaluate()
        self.assertEqual(z['independent_generated_triplets'],64)
        self.assertEqual(z['ordered_detector']['true_positive_triplets'],64)
        self.assertEqual(z['histogram_control']['positive_mean'],1)
        self.assertEqual(z['histogram_control']['null_mean'],1)
        self.assertEqual(z['absolute_pitch_control']['positive_mean'],0)
        self.assertLessEqual(z['ordered_detector']['false_positive_triplets'],64)
    def test_bad_length_is_not_silently_scored(self):
        with self.assertRaises(ValueError):ordered_similarity([1],[2])
        with self.assertRaises(ValueError):histogram_similarity([1,2],[1,2,3])
    def test_zero_sets_rejected(self):
        with self.assertRaises(ValueError):evaluate(n=0)

if __name__=='__main__':unittest.main()
