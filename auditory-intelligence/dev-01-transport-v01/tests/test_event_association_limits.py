"""EXPECTED-FAILURE OF EVENT MEANING: records present blind spots as passing tests.

No source-association improvement is claimed. Two measured regions can be
fragments or distractors, not the intended pair of acoustic events.
"""
import math
import struct
import unittest
from audio_dev import SAMPLE_RATE, observe, render


class AssociationLimits(unittest.TestCase):
    def test_single_burst_fragmented_into_two_regions(self):
        wav=bytearray(render(.68,omit_second=True))
        for i in range(round(.34*SAMPLE_RATE),round(.42*SAMPLE_RATE)):
            struct.pack_into('<h',wav,44+2*i,0)
        result=observe(bytes(wav))
        self.assertEqual(result.sensor_status,'OK')
        self.assertEqual(result.gap_s,.08)
        self.assertEqual(result.event_association_status,'UNVERIFIED')
        # Only one intended event despite two measured activity regions.

    def test_distractor_replaces_quiet_intended_target(self):
        wav=bytearray(render(.68))
        for i in range(round(1.30*SAMPLE_RATE),round(1.72*SAMPLE_RATE)):
            old=struct.unpack_from('<h',wav,44+2*i)[0]
            struct.pack_into('<h',wav,44+2*i,round(old*.06))
        for i in range(round(.80*SAMPLE_RATE),round(1.04*SAMPLE_RATE)):
            value=round(.5*math.sin(2*math.pi*310*(i/SAMPLE_RATE-.8))*32767)
            struct.pack_into('<h',wav,44+2*i,value)
        result=observe(bytes(wav))
        self.assertEqual(result.sensor_status,'OK')
        self.assertEqual(result.gap_s,.18)
        self.assertEqual(result.event_association_status,'UNVERIFIED')
        # Intentional second event still began after .68 s, not .18 s.

if __name__=='__main__':unittest.main()
