"""Follow-up Git-specific investigations using disposable local object stores."""
import os
import subprocess
import unittest

from dev_fixture import LocalRepo


class GitEdges(LocalRepo):
    def object(self, kind, payload):
        return subprocess.check_output(["git", "-C", self.repo, "hash-object", "-w", "-t", kind, "--stdin"],
                                       input=payload, env=self.env).decode().strip()

    def test_subtree_entry_with_a_commit_payload(self):
        tree = self.object("tree", b"40000 dir\0" + bytes.fromhex(self.pin))
        pin = self.git("commit-tree", tree, "-m", "synthetic inconsistent subtree")
        result, code = self.run_cli(pin=pin, paths=["dir", "dir/record", "missing"])
        self.assertEqual([r["status"] for r in result["rows"]], ["PRESENT", "EVIDENCE_UNAVAILABLE", "MISSING"])
        self.assertEqual((result["verdict"], result["commit"], code), ("EVIDENCE_UNAVAILABLE", pin, 3))

    def test_unavailable_root_tree(self):
        oid = self.git("rev-parse", "HEAD^{tree}")
        (self.repo / ".git/objects" / oid[:2] / oid[2:]).unlink()
        result, code = self.run_cli(paths=["a", "b"])
        self.assertEqual((result["verdict"], result["commit"], code), ("EVIDENCE_UNAVAILABLE", self.pin, 3))
        self.assertEqual([r["status"] for r in result["rows"]], ["EVIDENCE_UNAVAILABLE"] * 2)

    def test_partial_clone_never_contacts_configured_transport(self):
        # An instrumented, entirely local remote helper leaves a marker if called.
        marker = self.work / "contact"
        helper = self.work / "git-remote-observe"
        helper.write_text('#!/bin/sh\ntouch "$EAI_MARKER"\nexit 1\n')
        helper.chmod(0o755)
        self.git("config", "remote.origin.url", "observe::unused")
        self.git("config", "remote.origin.promisor", "true")
        self.git("config", "remote.origin.partialclonefilter", "blob:none")
        env = dict(self.env, PATH=str(self.work) + os.pathsep + os.environ["PATH"], EAI_MARKER=str(marker))
        # Positive control for the observer uses the local helper; no network destination exists.
        control_env = dict(env, GIT_ALLOW_PROTOCOL="observe")
        proc = subprocess.run(["git", "-C", self.repo, "cat-file", "-t", "1" * 40],
                              env=control_env, capture_output=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertTrue(marker.is_file())
        marker.unlink()
        result, code = self.run_cli(pin="1" * 40, env=control_env)
        self.assertEqual((result["verdict"], code), ("EVIDENCE_UNAVAILABLE", 3))
        self.assertFalse(marker.exists())

    def test_sha256_repository(self):
        other = self.work / "sha256"
        subprocess.run(["git", "init", "-q", "--object-format=sha256", other], check=True, env=self.env)
        subprocess.run(["git", "-C", other, "commit", "-qm", "empty", "--allow-empty"], check=True, env=self.env)
        pin = subprocess.check_output(["git", "-C", other, "rev-parse", "HEAD"], text=True, env=self.env).strip()
        result, code = self.run_cli(repo=other, pin=pin, paths=["absent"])
        self.assertEqual((len(pin), result["commit"], result["verdict"], code), (64, pin, "MISSING", 1))


if __name__ == "__main__":
    unittest.main()
