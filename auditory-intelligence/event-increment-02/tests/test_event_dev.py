import io
import struct
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from event_dev import (pair_cases, _read, _synth, Event, A, B, energy, frequency,
                       evaluate, score, MAX_BYTES, RATE)

class EventIncrementTests(unittest.TestCase):
    def test_positives_schedule_A_followed_by_B(self):
        for i in range(18):
            p,n=pair_cases(i)
            self.assertTrue(p.intended_positive)
            self.assertFalse(n.intended_positive)
            self.assertLess(p.a.end, p.b.start)
            self.assertEqual(p.wav[:40], n.wav[:40])

    def test_clean_frequency_recovers_target_times(self):
        p,n=pair_cases(3)
        output=frequency(p.wav)
        self.assertEqual(output['decision'], 'MATCH_A_THEN_B')
        a,b=output['selected']
        self.assertLess(abs(a[0]-p.a.start), .1)
        self.assertLess(abs(b[0]-p.b.start), .1)
        self.assertEqual(output['identity_scope'], 'SYNTHETIC_TONE_CLASSES_ONLY')

    def test_energy_uses_only_regions_not_tone_classes(self):
        p,n=pair_cases(3)
        result=energy(p.wav)
        if result['decision']=='MATCH_A_THEN_B':
            self.assertEqual(result['event_identity'],'UNVERIFIED')
            self.assertNotIn('selected', result)

    def test_intended_second_tone_omitted(self):
        _,n=pair_cases(0)
        self.assertEqual(n.perturbation, 'intended_B_absent')
        self.assertNotEqual(frequency(n.wav)['decision'],'MATCH_A_THEN_B')

    def test_wrong_C_instead_of_B(self):
        _,n=pair_cases(1)
        self.assertEqual(n.perturbation, 'B_replaced_by_C')
        self.assertNotEqual(frequency(n.wav)['decision'],'MATCH_A_THEN_B')

    def test_reversed_order_is_negative(self):
        _,n=pair_cases(2)
        self.assertEqual(n.perturbation,'B_precedes_A')
        self.assertNotEqual(frequency(n.wav)['decision'],'MATCH_A_THEN_B')

    def test_null_text_has_no_tone_labels(self):
        self.assertEqual('A then B' in 'Please listen to the signal.', False)

    def test_identical_prefix_with_different_future(self):
        p,n=pair_cases(0)
        cutoff=int(.9*RATE)*2+44
        self.assertEqual(p.wav[:cutoff],n.wav[:cutoff])
        self.assertNotEqual(p.wav,n.wav)

    def test_riff_truncation_rejected(self):
        p,_=pair_cases(3)
        self.assertNotEqual(_read(p.wav[:-1600])[0],'OK')
        self.assertEqual(frequency(p.wav[:-1600])['decision'],'ABSTAIN')

    def test_inflated_data_length_rejected(self):
        p,_=pair_cases(3)
        malformed=bytearray(p.wav)
        struct.pack_into('<I',malformed,40,struct.unpack_from('<I',malformed,40)[0]+800)
        self.assertNotEqual(_read(bytes(malformed))[0],'OK')

    def test_clipping_rejected(self):
        p,_=pair_cases(3)
        altered=bytearray(p.wav)
        for i in range(200,210):struct.pack_into('<h',altered,44+i*2,32767)
        self.assertEqual(_read(bytes(altered))[0],'CLIPPED')
        self.assertEqual(frequency(bytes(altered))['decision'],'ABSTAIN')

    def test_oversize_input_rejected(self):
        self.assertEqual(_read(b'0'*(MAX_BYTES+1))[0],'TOO_LARGE')

    def test_missing_input_abstains(self):
        self.assertEqual(frequency(None)['decision'],'ABSTAIN')

    def test_fragmented_source_rms_not_proof_of_two_sources(self):
        e=Event(A,.30,.95,.40,dropout=(.53,.61))
        out=energy(_synth((e,),0.001,99))
        self.assertIn(out['decision'],('ABSTAIN','MATCH_A_THEN_B'))
        if out['decision']=='MATCH_A_THEN_B':
            self.assertEqual(out['event_identity'],'UNVERIFIED')

    def test_classwise_gap_bridging(self):
        p,_=pair_cases(0)
        result=frequency(p.wav)
        if result['decision']=='MATCH_A_THEN_B':
            self.assertEqual(len(result['selected']),2)
            self.assertLess(abs(result['selected'][0][0]-p.a.start),.1)

    def test_fixed_generator_replay(self):
        a,b=pair_cases(22,20261023),pair_cases(22,20261023)
        self.assertEqual(a[0].wav,b[0].wav)
        self.assertEqual(a[1].wav,b[1].wav)

    def test_scoring_distinguishes_wrong_from_unverified(self):
        p,_=pair_cases(3)
        s=score([p],energy)['counts']
        self.assertEqual(s['wrong_time_positive'],0)
        self.assertEqual(s['unverified_identity_positive'],s['match_on_positive'])

    def test_evaluation_small_coherent(self):
        x=evaluate(9,20261023)
        self.assertEqual(x['matched_pair_scenarios'],9)
        self.assertEqual(x['energy']['counts']['positives'],9)
        self.assertEqual(x['frequency']['counts']['negatives'],9)
        self.assertEqual(x['status'],'EXPOSED_SYNTHETIC_ENGINEERING_ONLY')

if __name__=='__main__': unittest.main()
