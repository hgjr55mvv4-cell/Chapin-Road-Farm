#!/usr/bin/env python3
"""Deterministic engineering-unit checks, not physical device validation."""
import unittest
from sim import Design, Event, run, cases


class ResonatorTests(unittest.TestCase):
    def setUp(self):
        self.d=Design()
        self.by_name={e.label:run(e) for e in cases()}

    def test_zero_input_cannot_latch(self):
        r=self.by_name['no_signal']; self.assertFalse(any(r[k] for k in ('plain_impact','tuned_peak','tuned_dwell')))

    def test_quiet_input_cannot_latch(self):
        self.assertFalse(self.by_name['quiet_90hz_0.1g']['tuned_dwell'])

    def test_resonant_event_detected(self):
        self.assertTrue(self.by_name['target_90hz_0.6g']['tuned_dwell'])

    def test_resonant_input_below_shock_threshold(self):
        self.assertFalse(self.by_name['target_90hz_0.6g']['plain_impact'])

    def test_off_band_45hz_rejected_at_equal_amplitude(self):
        self.assertFalse(self.by_name['offband_45hz_0.6g']['tuned_peak'])

    def test_off_band_150hz_rejected_at_equal_amplitude(self):
        self.assertFalse(self.by_name['offband_150hz_0.6g']['tuned_peak'])

    def test_short_pulse_is_dismissed(self):
        self.assertFalse(self.by_name['target_short_90hz_0.6g']['tuned_dwell'])

    def test_high_impact_trips_peak_but_not_dwell(self):
        r=self.by_name['broad_impact_10g']; self.assertTrue(r['tuned_peak']); self.assertFalse(r['tuned_dwell'])

    def test_chirp_trips_peak_but_not_dwell(self):
        r=self.by_name['sweep_60hz_up']; self.assertTrue(r['tuned_peak']); self.assertFalse(r['tuned_dwell'])

    def test_large_off_band_vibration_false_triggers(self):
        # Negative result: large off-band acceleration overcomes resonance rejection.
        self.assertTrue(self.by_name['offband_overload_45hz_4g']['tuned_dwell'])

    def test_healthy_onband_is_indistinguishable(self):
        # No physical basis for assigning the same waveform two different fault labels.
        normal=self.by_name['normal_onband_90hz_0.6g']; fault=self.by_name['target_90hz_0.6g']
        self.assertEqual([normal[k] for k in ('tuned_peak','tuned_dwell','peak_displacement_mm')],
                         [fault[k] for k in ('tuned_peak','tuned_dwell','peak_displacement_mm')])

    def test_same_event_is_deterministic(self):
        e=Event('duplicate','sine',amplitude_g=.75)
        self.assertEqual(run(e),run(e))

    def test_traces_are_decimated(self):
        r=run(Event('trace','sine'), collect_trace=True)
        self.assertTrue(len(r['trace'])>50)
        self.assertTrue(all(len(v)==3 for v in r['trace']))

    def test_invalid_high_frequency_raises(self):
        with self.assertRaises(ValueError):
            run(Event('bad','sine'), Design(natural_hz=1000,fs_hz=8000))

    def test_no_state_leak_after_trigger(self):
        a=run(Event('latch','sine',amplitude_g=.9))
        b=run(Event('separate','none'))
        self.assertTrue(a['tuned_dwell']); self.assertFalse(b['tuned_dwell'])

    def test_numerical_convergence_8k_to_16k(self):
        e=Event('convergence','sine',amplitude_g=.8)
        low=run(e,Design(fs_hz=8000))['peak_displacement_mm']
        high=run(e,Design(fs_hz=16000))['peak_displacement_mm']
        self.assertLess(abs(low-high)/high,.015)

if __name__=='__main__': unittest.main(verbosity=2)
