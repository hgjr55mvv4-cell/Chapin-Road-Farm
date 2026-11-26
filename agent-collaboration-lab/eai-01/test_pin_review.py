"""Sol's EAI-01 review probes. Exercise a real CLI against local objects and refs."""
import hashlib
import subprocess
import unittest

from dev_fixture import LocalRepo


class PinReview(LocalRepo):
    def git_bytes(self, *args, data=None, check=True):
        return subprocess.run(["git", "-C", self.repo, *args], env=self.env,
                              input=data, capture_output=True, check=check)

    def hash_commit_bytes(self, fmt, payload):
        header = b"commit " + str(len(payload)).encode("ascii") + b"\0"
        return hashlib.new(fmt, header + payload).hexdigest()

    def check_literal_pin(self, fmt):
        pin = self.git("rev-parse", "HEAD")
        raw = self.git_bytes("cat-file", "commit", pin).stdout
        self.assertEqual(self.hash_commit_bytes(fmt, raw), pin)
        blob = self.git("rev-parse", "HEAD:record")
        (self.repo / "record").rename(self.repo / "other")
        self.git("add", "-A")
        self.git("commit", "-qm", "different tree")
        alternate = self.git("rev-parse", "HEAD")
        self.assertNotEqual(alternate, pin)
        absent = "1" * len(pin)
        self.assertNotEqual(self.git_bytes("cat-file", "-e", absent, check=False).returncode, 0)

        # A fully qualified ref lookup is the positive control for each name.
        for name in (pin, absent, blob):
            for namespace in ("heads", "tags"):
                ref = f"refs/{namespace}/{name}"
                self.git("update-ref", ref, alternate)
                self.assertEqual(self.git("rev-parse", "--verify", ref), alternate)

        result, code = self.run_cli(pin=pin.upper(), paths=["record"])
        self.assertEqual((result["commit"], result["verdict"], result["rows"][0]["oid"], code),
                         (pin, "PRESENT", blob, 0))
        result, code = self.run_cli(pin=pin, paths=["record", "other"])
        self.assertEqual((result["commit"], result["verdict"], code), (pin, "MISSING", 1))
        self.assertEqual([(r["path"], r["status"], r.get("oid")) for r in result["rows"]],
                         [("record", "PRESENT", blob), ("other", "MISSING", None)])
        result, code = self.run_cli(pin=absent, paths=["other"])
        self.assertEqual((result["commit"], result["verdict"], result["rows"], code),
                         (None, "EVIDENCE_UNAVAILABLE", [], 3))
        result, code = self.run_cli(pin=blob, paths=["other"])
        self.assertEqual((result["commit"], result["verdict"], result["rows"], code),
                         (None, "INVALID_INPUT", [], 2))

    def test_full_width_sha1_refs_do_not_supply_objects(self):
        self.check_literal_pin("sha1")

    def test_full_width_sha256_refs_do_not_supply_objects(self):
        self.repo = self.work / "sha256"
        self.repo.mkdir()
        self.git("init", "-q", "--object-format=sha256", "-b", "main")
        (self.repo / "record").write_bytes(b"evidence\n")
        self.git("add", "record")
        self.git("commit", "-qm", "first")
        self.check_literal_pin("sha256")

    def test_malformed_root_header_names_blob_commit_or_tag(self):
        self.git("tag", "-am", "annotated", "annotated", self.pin)
        old = self.git_bytes("cat-file", "commit", self.pin).stdout
        _, newline, tail = old.partition(b"\n")
        for kind, target in (("blob", self.git("rev-parse", "HEAD:record")), ("commit", self.pin),
                             ("tag", self.git("rev-parse", "annotated"))):
            with self.subTest(root_type=kind):
                self.assertEqual(self.git("cat-file", "-t", target), kind)
                raw = b"tree " + target.encode() + newline + tail
                pin = self.git_bytes("hash-object", "--literally", "-w", "-t", "commit", "--stdin",
                                     data=raw).stdout.decode().strip()
                self.assertEqual(self.hash_commit_bytes("sha1", raw), pin)
                self.assertEqual(self.git("cat-file", "-t", pin), "commit")
                listing = self.git_bytes("ls-tree", "--full-tree", "-z", pin, check=False)
                self.assertNotEqual(listing.returncode, 0)
                self.assertEqual(listing.stdout, b"")
                result, code = self.run_cli(pin=pin, paths=["record", "absent"])
                self.assertEqual((result["commit"], result["verdict"], code), (pin, "EVIDENCE_UNAVAILABLE", 3))
                self.assertEqual([(r["path"], r["status"]) for r in result["rows"]],
                                 [("record", "EVIDENCE_UNAVAILABLE"), ("absent", "EVIDENCE_UNAVAILABLE")])


if __name__ == "__main__":
    unittest.main()
