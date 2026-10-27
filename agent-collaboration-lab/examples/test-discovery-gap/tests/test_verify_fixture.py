"""Fail-closed regression checks for the public test-discovery receipt runner."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_verifier(root, optimized=False, optimized_env=False):
    command = [sys.executable]
    if optimized:
        command.append('-O')
    command.append(str(root / 'verify_fixture.py'))
    env = None
    if optimized_env:
        env = os.environ.copy()
        env['PYTHONOPTIMIZE'] = '1'
    return subprocess.run(command, text=True, capture_output=True, env=env)


class VerifierIntegrityTests(unittest.TestCase):
    def assert_rejected(self, root):
        for optimized, optimized_env in ((False, False), (True, False), (False, True)):
            with self.subTest(optimized=optimized, optimized_env=optimized_env):
                result = run_verifier(root, optimized, optimized_env)
                transcript = result.stdout + result.stderr
                self.assertNotEqual(result.returncode, 0, transcript)
                self.assertNotIn('VERIFICATION_PASS', transcript)
                self.assertIn('ValueError', transcript)

    def test_valid_fixture_passes_normal_and_optimized(self):
        for optimized, optimized_env in ((False, False), (True, False), (False, True)):
            with self.subTest(optimized=optimized, optimized_env=optimized_env):
                result = run_verifier(ROOT, optimized, optimized_env)
                transcript = result.stdout + result.stderr
                self.assertEqual(result.returncode, 0, transcript)
                self.assertIn('VERIFICATION_PASS', transcript)

    def test_failed_repaired_suite_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / 'fixture'
            shutil.copytree(ROOT, copied)
            test_file = copied / 'good/test_checks.py'
            source = test_file.read_text(encoding='utf-8')
            original = 'self.assertTrue(validate_age(25))'
            self.assertIn(original, source)
            test_file.write_text(
                source.replace(original, 'self.assertFalse(validate_age(25))', 1),
                encoding='utf-8',
            )
            self.assert_rejected(copied)

    def test_failed_direct_check_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / 'fixture'
            shutil.copytree(ROOT, copied)
            test_file = copied / 'bad/test_checks.py'
            source = test_file.read_text(encoding='utf-8')
            original = 'return type(value) is int and 0 <= value <= 130'
            self.assertIn(original, source)
            test_file.write_text(source.replace(original, 'return True', 1), encoding='utf-8')
            self.assert_rejected(copied)

    def test_missing_execution_marker_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            copied = Path(tmp) / 'fixture'
            shutil.copytree(ROOT, copied)
            test_file = copied / 'bad/test_checks.py'
            source = test_file.read_text(encoding='utf-8')
            original = "    print('DIRECT_CHECKS_EXECUTED=2')\n"
            self.assertIn(original, source)
            test_file.write_text(source.replace(original, '', 1), encoding='utf-8')
            self.assert_rejected(copied)


if __name__ == '__main__':
    unittest.main()
