"""Apply inherited operations with contract-specific expectations, through actual CLIs."""
import io
import json
import subprocess
import sys
import unittest

from dev_fixture import LocalRepo
from operations import (duplicate_evidence, empty_evidence, require_consistent_exit,
                        suppress_required_check, unexpected_type)

# Transcribed from CONTRACT.md. Never import the CLI's exit map.
EXPECTED_EXIT = {"PRESENT": 0, "MISSING": 1, "INVALID_INPUT": 2, "EVIDENCE_UNAVAILABLE": 3}


class InheritedTests(LocalRepo):
    def test_empty_evidence(self):
        report, code = self.run_cli(paths=empty_evidence(["record"]))
        self.assertEqual((report["verdict"], report["rows"], code), ("INVALID_INPUT", [], 2))

    def test_type_substitutions(self):
        data = {"commit": self.pin, "paths": ["record"]}
        for key, value in (("paths", {"0": "record"}), ("paths", "record"), ("commit", [self.pin])):
            with self.subTest(key=key, value=value):
                changed = unexpected_type(data, key, value)
                report, code = self.run_cli(raw=json.dumps(changed).encode())
                self.assertEqual((report["verdict"], report["rows"], code), ("INVALID_INPUT", [], 2))

    def test_duplicate_lookup_can_remove_the_only_missing_item(self):
        original = ["record", "absent"]
        changed = duplicate_evidence(original, 0, 1)
        before, before_code = self.run_cli(paths=original)
        after, after_code = self.run_cli(paths=changed)
        self.assertEqual((before["verdict"], before_code), ("MISSING", 1))
        self.assertEqual((after["verdict"], after_code), ("PRESENT", 0))
        self.assertEqual([r["path"] for r in after["rows"]], ["record", "record"])

    def test_same_duplicate_operation_on_distinct_git_transaction_refs(self):
        self.git("branch", "second", self.pin)
        refs = ["refs/heads/main", "refs/heads/second"]
        for inputs, expected_success in ((refs, True), (duplicate_evidence(refs, 0, 1), False)):
            with self.subTest(refs=inputs):
                checks = "".join(f"verify {ref} {self.pin}\n" for ref in inputs)
                proc = subprocess.run(["git", "-C", self.repo, "update-ref", "--stdin"],
                                      input=checks, text=True, capture_output=True, env=self.env)
                self.assertEqual(proc.returncode == 0, expected_success)
                if not expected_success:
                    self.assertIn("multiple updates", proc.stderr)

    def test_required_check_suppression_on_unittest_only(self):
        # The artifact lookup has no required-check runner interface.
        class Example(unittest.TestCase):
            def test_required(self):
                self.fail("control check ran")

        def run():
            return unittest.TextTestRunner(stream=io.StringIO()).run(Example("test_required"))

        baseline = run()
        self.assertEqual((baseline.testsRun, len(baseline.failures)), (1, 1))
        Example.test_required = suppress_required_check(Example.test_required)
        observed = run()
        self.assertEqual((observed.testsRun, len(observed.skipped), observed.wasSuccessful()), (1, 1, True))

    def test_status_agreement_for_each_real_process_outcome(self):
        for kwargs, expected in (({}, "PRESENT"), ({"paths": ["absent"]}, "MISSING"),
                                 ({"paths": []}, "INVALID_INPUT"), ({"pin": "0" * 40}, "EVIDENCE_UNAVAILABLE")):
            with self.subTest(expected=expected):
                report, code = self.run_cli(**kwargs)
                self.assertEqual(report["verdict"], expected)
                require_consistent_exit(report["verdict"], code, EXPECTED_EXIT)

    def test_status_observer_detects_disagreement_but_accepts_consistent_error(self):
        # Explicitly seeded shell controls. Neither is an observed lookup defect.
        proc = subprocess.run([sys.executable, "-c", """print('{"verdict":"MISSING"}')"""],
                              capture_output=True, check=True)
        with self.assertRaises(AssertionError):
            require_consistent_exit(json.loads(proc.stdout)["verdict"], proc.returncode, EXPECTED_EXIT)
        require_consistent_exit("PRESENT", 0, EXPECTED_EXIT)  # Could be wrong about the path.


if __name__ == "__main__":
    unittest.main()
