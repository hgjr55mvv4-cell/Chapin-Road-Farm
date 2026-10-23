import unittest
from audio_dev import render, observe, decide, gap_band, evaluate

class AuditoryDevTests(unittest.TestCase):
    def test_short_gap_recovery(self):
        obs = observe(render(.12))
        self.assertEqual(obs.sensor_status, 'OK')
        self.assertAlmostEqual(obs.gap_s, .12, delta=.02)

    def test_long_gap_recovery(self):
        obs = observe(render(.68))
        self.assertEqual(obs.sensor_status, 'OK')
        self.assertAlmostEqual(obs.gap_s, .68, delta=.02)

    def test_identical_text_unequal_timing(self):
        a,b = evaluate()['cases']
        self.assertEqual(a['external_transcript'], b['external_transcript'])
        self.assertNotEqual(a['audio_activity_action'], b['audio_activity_action'])
        self.assertEqual(a['transcript_only_action'], b['transcript_only_action'])

    def test_timestamp_baseline_as_strong_as_audio_in_clean_cases(self):
        for row in evaluate()['cases']:
            self.assertEqual(row['audio_activity_action'], row['transcript_with_gold_timestamps_action'])

    def test_missing_or_unreadable(self):
        self.assertEqual(observe(None).sensor_status, 'MISSING')
        self.assertEqual(observe(b'not a wave').sensor_status, 'UNREADABLE')

    def test_clipped_audio_cannot_justify_action(self):
        obs = observe(render(.12, amplitude=3.))
        self.assertEqual(obs.sensor_status, 'CLIPPED')
        self.assertIsNone(obs.gap_s)
        self.assertEqual(decide(text='turn', gap_s=obs.gap_s, sensor_status=obs.sensor_status),
                         'ABSTAIN_REQUEST_CLEAR_SAMPLE')

    def test_loud_background_is_not_discrete_event(self):
        obs = observe(render(.12, noise=.28))
        self.assertEqual(obs.sensor_status, 'BACKGROUND_UNRELIABLE')
        self.assertIsNone(obs.gap_s)

    def test_one_event_insufficient(self):
        obs = observe(render(.68, omit_second=True))
        self.assertEqual(obs.sensor_status, 'INSUFFICIENT_EVENTS')
        self.assertIsNone(obs.gap_s)

    def test_explicit_correction_is_text_sufficient(self):
        self.assertEqual(decide(text='No, I meant the other path.', gap_s=None),
                         'CONFIRM_EXPLICIT_CORRECTION')

    def test_midband_ambiguous(self):
        self.assertEqual(gap_band(.40), 'AMBIGUOUS')
        self.assertEqual(decide(text='hello', gap_s=.4), 'WAIT')

    def test_deterministic(self):
        self.assertEqual(render(.12,seed=11), render(.12,seed=11))
        self.assertEqual(evaluate(), evaluate())

    def test_report_restricts_its_own_claims(self):
        report = evaluate()
        self.assertEqual(report['status'], 'EXPOSED_ENGINEERING_DEV')
        self.assertTrue(all(not c['waveform_is_real_speech'] for c in report['cases']))
        self.assertTrue(all(c['gap_absolute_error_s'] <= .02 for c in report['cases']))

if __name__=='__main__':unittest.main()
