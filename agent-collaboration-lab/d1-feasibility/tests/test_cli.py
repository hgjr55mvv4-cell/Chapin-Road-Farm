import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / 'examples/synthetic_only.json'


class ExitStatusTests(unittest.TestCase):
    def run_manifest(self, manifest, code, status):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'
            output = Path(tmp) / 'report.json'
            path.write_text(json.dumps(manifest), encoding='utf-8')
            run = subprocess.run([sys.executable, str(ROOT / 'audit.py'), str(path),
                                  '--out', str(output)], capture_output=True)
            self.assertEqual(run.stderr, b'')
            self.assertEqual(run.stdout, output.read_bytes())
            report = json.loads(run.stdout)
            self.assertEqual(report['status'], status)
            self.assertEqual(run.returncode, code)
            return report

    def setUp(self):
        self.manifest = json.loads(DEMO.read_bytes())

    def test_clean_demo(self):
        self.run_manifest(self.manifest, 0, 'ENGINEERING_DEMO_NOT_MODEL_RUN')

    def test_scored_blocked_report_stops_a_caller(self):
        self.manifest['evidence_type'] = 'PROSPECTIVE_PILOT'
        report = self.run_manifest(self.manifest, 2, 'BLOCKED')
        self.assertTrue(report['scores'])
        self.assertIn('no operator-approval receipt for declared pilot', report['issues'])

    def test_unscored_report(self):
        self.run_manifest({}, 2, 'BLOCKED')

    def test_demo_with_overrun_keeps_scores_and_signals_failure(self):
        self.manifest['token_cap_per_task'] = 1
        report = self.run_manifest(self.manifest, 2, 'ENGINEERING_DEMO_NOT_MODEL_RUN')
        self.assertTrue(report['scores'])
        self.assertIn('P combined observed use exceeds cap', report['issues'])

    def test_complete_declarations_are_still_unauthenticated(self):
        self.manifest['evidence_type'] = 'PROSPECTIVE_PILOT'
        self.manifest['operator_approval_receipt'] = 'MOCK-ONLY-NO-REAL-AUTHORIZATION'
        self.run_manifest(self.manifest, 0, 'DECLARATIONS_COMPLETE_UNAUTHENTICATED')
