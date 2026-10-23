"""Sol-authored transport tests, NOT Astra's as-yet-unreceived patch."""
import io
import struct
import unittest
import wave
from audio_dev import observe, render, MAX_WAV_BYTES


class TransportRegressions(unittest.TestCase):
    def test_truncated_declared_frames_not_ok(self):
        wav_bytes = render(.12)[:-3200]
        with wave.open(io.BytesIO(wav_bytes),'rb') as wav:
            n = wav.getnframes()
            actual = len(wav.readframes(n)) // wav.getsampwidth()
        self.assertLess(actual,n)
        self.assertNotEqual(observe(wav_bytes).sensor_status,'OK')
        self.assertIsNone(observe(wav_bytes).gap_s)

    def test_inflated_riff_size_not_ok(self):
        buf = bytearray(render(.12))
        struct.pack_into('<I',buf,4,struct.unpack_from('<I',buf,4)[0]+1600)
        self.assertNotEqual(observe(bytes(buf)).sensor_status,'OK')
        self.assertIsNone(observe(bytes(buf)).gap_s)

    def test_inflated_data_length_not_ok(self):
        buf=bytearray(render(.12))
        # The frozen generator's simple 44-byte PCM header: data size at offset 40.
        struct.pack_into('<I',buf,40,struct.unpack_from('<I',buf,40)[0]+1600)
        self.assertNotEqual(observe(bytes(buf)).sensor_status,'OK')
        self.assertIsNone(observe(bytes(buf)).gap_s)

    def test_size_cap_precedes_parsing(self):
        wav_bytes=render(.12)
        over=wav_bytes+b'X'*(MAX_WAV_BYTES+1-len(wav_bytes))
        self.assertEqual(observe(over).sensor_status,'TOO_LARGE')
        self.assertIsNone(observe(over).gap_s)

    def test_unexpected_trailing_bytes_not_ok(self):
        self.assertNotEqual(observe(render(.12)+b'extraneous bytes').sensor_status,'OK')

    def test_clean_capture_still_unverified_event_identity(self):
        result=observe(render(.68))
        self.assertEqual(result.sensor_status,'OK')
        self.assertAlmostEqual(result.gap_s,.68,delta=.02)
        self.assertEqual(result.event_association_status,'UNVERIFIED')

if __name__=='__main__':unittest.main()
