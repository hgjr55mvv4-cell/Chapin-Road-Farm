import csv
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
import wave
from sys import path as sys_path
sys_path.insert(0, str(Path(__file__).resolve().parents[1]))
from admission import audit, read_annotations, inspect_wav


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        wavepath = self.root / 'S-0001.wav'
        with wave.open(str(wavepath), 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(8000)
            w.writeframes(struct.pack('<' + 'h'*8000, *([500]*8000)))
        self.digest = hashlib.sha256(wavepath.read_bytes()).hexdigest()
        self.csv = self.root / 'poly.csv'
        self.csv.write_text('sound_name,class_name,start_perc,end_perc,start_time,end_time,event_length\n'
                            'S-0001.wav,Dog barkings and howlings,0,40,0.10,0.40,0.30\n')
        self.base = {'dataset':'DataSED', 'dataset_revision':'test-revision', 'candidates':[
            {'sound_name':'S-0001.wav','audio_sha256':self.digest,'split':'train',
             'provenance': {'lineage_status':'VERIFIED','original_recording_id':'upstream-one',
                           'evidence_ref':'synthetic-test-evidence','rights_status':'VERIFIED',
                           'rights_ref':'synthetic-test-rights','editing_history':'unchanged'},
             'independent_listening_checks': [
                {'decision':'EVENT_PRESENT','class_name':'Dog barkings and howlings',
                 'start_s':0.10,'end_s':0.40,'audio_sha256':self.digest,
                 'reviewer_id':'reviewer-A','receipt_ref':'synthetic-test-check'},
                {'decision':'CLASS_ABSENT_VERIFIED','class_name':'Vehicle idling',
                 'start_s':0.5,'end_s':0.8,'audio_sha256':self.digest,
                 'reviewer_id':'reviewer-A','receipt_ref':'synthetic-test-check'}]}]}

    def run_audit(self, obj=None):
        return audit(self.base if obj is None else obj, self.csv, self.root)

    def test_fixture_complete_is_admitted_as_software_fixture_only(self):
        a = self.run_audit()
        self.assertEqual(a['status'], 'ADMIT')
        self.assertEqual(a['admitted_candidates'], 1)

    def test_no_audio_is_blocked(self):
        (self.root/'S-0001.wav').unlink()
        self.assertEqual(self.run_audit()['status'], 'HOLD')

    def test_bad_hash_is_blocked(self):
        self.base['candidates'][0]['audio_sha256'] = '0'*64
        self.assertIn('AUDIO_HASH_MISMATCH', self.run_audit()['per_candidate'][0]['reasons'])

    def test_lineage_missing_is_blocked(self):
        self.base['candidates'][0]['provenance']['lineage_status'] = 'UNKNOWN'
        self.assertEqual(self.run_audit()['status'], 'HOLD')

    def test_missing_positive_review_blocked(self):
        self.base['candidates'][0]['independent_listening_checks'] = self.base['candidates'][0]['independent_listening_checks'][1:]
        self.assertIn('POSITIVE_LABELS_NOT_INDEPENDENTLY_VERIFIED', self.run_audit()['per_candidate'][0]['reasons'])

    def test_unlabeled_interval_is_not_verified_negative(self):
        self.base['candidates'][0]['independent_listening_checks'] = self.base['candidates'][0]['independent_listening_checks'][:1]
        self.assertIn('NO_VERIFIED_NEGATIVES', self.run_audit()['per_candidate'][0]['reasons'])

    def test_negative_cannot_overlap_positive(self):
        ch = self.base['candidates'][0]['independent_listening_checks'][1]
        ch.update({'class_name':'Dog barkings and howlings','start_s':0.2,'end_s':0.35})
        self.assertIn('NO_VERIFIED_NEGATIVES', self.run_audit()['per_candidate'][0]['reasons'])

    def test_source_leakage_blocks_both(self):
        cloned = json.loads(json.dumps(self.base['candidates'][0]))
        cloned['split'] = 'eval'
        self.base['candidates'].append(cloned)
        report = self.run_audit()
        self.assertEqual(report['status'],'HOLD')
        self.assertEqual(len(report['duplicate_train_eval_lineages']),1)
        self.assertTrue(all('TRAIN_EVAL_LINEAGE_LEAKAGE' in r['reasons'] for r in report['per_candidate']))

    def test_timestamp_outside_audio(self):
        self.csv.write_text('sound_name,class_name,start_time,end_time\nS-0001.wav,Dog barkings and howlings,0.9,1.7\n')
        self.assertIn('ANNOTATION_OUTSIDE_AUDIO', self.run_audit()['per_candidate'][0]['reasons'])

    def test_missing_columns_rejected(self):
        self.csv.write_text('filename,label,start,end\na,b,0,1\n')
        with self.assertRaises(ValueError): read_annotations(self.csv)

    def test_nan_time_is_rejected(self):
        self.csv.write_text('sound_name,class_name,start_time,end_time\nS-0001.wav,Dog,nan,1\n')
        spans, problems = read_annotations(self.csv)
        self.assertEqual(spans, {})
        self.assertEqual(len(problems),1)

    def test_audio_header_truncation_detected(self):
        wavepath = self.root/'S-0001.wav'
        truncated = wavepath.read_bytes()[:-100]
        wavepath.write_bytes(truncated)
        h = hashlib.sha256(truncated).hexdigest()
        self.assertEqual(inspect_wav(wavepath,h)[1], 'TRUNCATED_AUDIO')

    def test_negative_bad_hash_receipt_rejected(self):
        self.base['candidates'][0]['independent_listening_checks'][1]['audio_sha256']='a'*64
        self.assertIn('NO_VERIFIED_NEGATIVES',self.run_audit()['per_candidate'][0]['reasons'])

    def test_filename_path_traversal_rejected(self):
        self.base['candidates'][0]['sound_name'] = '../S-0001.wav'
        self.assertIn('BAD_FILE_NAME', self.run_audit()['per_candidate'][0]['reasons'])

if __name__ == '__main__': unittest.main()