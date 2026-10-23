"""Finite-domain and seeded metamorphic DEV checks. Not proof or unseen science."""
import itertools, random, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from implementations import overlapping_half_open_a, overlapping_half_open_b, first_by_key_a, first_by_key_b
SEED=20261023
KEYS=['A','a','a ','','\u00e9','e\u0301','Z','z']
def interval_ref(a,b):
    # Integer endpoints: independent unit-grid coverage on bounded test domain.
    return bool(set(range(*a)).intersection(range(*b)))
def dedup_ref(items):
    out=[]
    for key,payload in items:
        if not any(k==key for k,_ in out): out.append((key,payload))
    return out
def bad_strip(items):
    seen=set();out=[]
    for k,v in items:
        if k.strip() not in seen:
            seen.add(k.strip());out.append((k,v))
    return out
def bad_normalize(items):
    import unicodedata
    seen=set();out=[]
    for k,v in items:
        norm=unicodedata.normalize('NFC',k)
        if norm not in seen: seen.add(norm);out.append((k,v))
    return out
class PropertyDevTests(unittest.TestCase):
    interval_pairs=0;dedup_sequences=0
    def test_interval_finite_enumeration(self):
        iv=[(a,b) for a in range(-4,5) for b in range(a,5)]
        for a in iv:
            for b in iv:
                expected=interval_ref(a,b)
                self.assertEqual(overlapping_half_open_a(a,b),expected,(a,b))
                self.assertEqual(overlapping_half_open_b(a,b),expected,(a,b))
                self.assertEqual(overlapping_half_open_a(a,b),overlapping_half_open_a(b,a))
                self.__class__.interval_pairs+=1
    def test_seeded_translation_invariance(self):
        rng=random.Random(SEED)
        for _ in range(1000):
            a=tuple(sorted([rng.randint(-100,100),rng.randint(-100,100)]))
            b=tuple(sorted([rng.randint(-100,100),rng.randint(-100,100)]))
            shift=rng.randint(-500,500)
            correct=overlapping_half_open_a(a,b)
            self.assertEqual(correct,overlapping_half_open_a(
                (a[0]+shift,a[1]+shift),(b[0]+shift,b[1]+shift)))
            self.assertEqual(correct,overlapping_half_open_b(a,b))
    def test_dedup_short_sequence_enumeration(self):
        alphabet=[(k,v) for k in KEYS for v in (0,1)]
        for n in range(4):
            for seq in itertools.product(alphabet,repeat=n):
                items=list(seq); expected=dedup_ref(items)
                self.assertEqual(first_by_key_a(items),expected,items)
                self.assertEqual(first_by_key_b(items),expected,items)
                self.assertEqual(first_by_key_a(expected),expected)
                self.__class__.dedup_sequences+=1
    def test_whitespace_and_unicode_mutation_witnesses(self):
        for bad,items in [(bad_strip,[('a',1),('a ',2)]),
                          (bad_normalize,[('\u00e9',1),('e\u0301',2)])]:
            expected=dedup_ref(items)
            self.assertNotEqual(bad(items),expected)
            self.assertEqual(first_by_key_a(items),expected)
            self.assertEqual(first_by_key_b(items),expected)
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(PropertyDevTests))
    print(f'RECEIPT interval_pairs={PropertyDevTests.interval_pairs} '
          f'dedup_sequences={PropertyDevTests.dedup_sequences} '
          f'shifted_intervals=1000 seed={SEED} tests_run={result.testsRun} '
          f'failures={len(result.failures)} errors={len(result.errors)}')
    if not result.wasSuccessful():sys.exit(1)
