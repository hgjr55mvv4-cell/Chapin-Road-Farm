"""Contract-driven CLI tests. Expected values are independent of the validator."""
import json
import os
import subprocess
import unittest

from dev_fixture import LocalRepo


class ContractTests(LocalRepo):
    def expect(self, verdict, code, **kwargs):
        result, status = self.run_cli(**kwargs)
        self.assertEqual((result["verdict"], status), (verdict, code))
        return result

    def test_present_identity_and_ordinary_missing(self):
        result = self.expect("PRESENT", 0, pin=self.pin.upper())
        self.assertEqual(result["commit"], self.pin)
        self.assertEqual(result["rows"], [{"path": "record", "status": "PRESENT", "mode": "100644",
                                          "type": "blob", "oid": self.git("rev-parse", "HEAD:record")}])
        self.expect("MISSING", 1, paths=["Record"])

    def test_uses_commit_not_worktree_index_or_current_head(self):
        (self.repo / "record").unlink()
        (self.repo / "next").touch()
        self.git("add", "-A")
        (self.repo / "untracked").touch()
        paths = ["record", "next", "untracked"]
        before = self.expect("MISSING", 1, paths=paths)
        self.git("commit", "-qm", "second")
        after = self.expect("MISSING", 1, paths=paths, pin=self.git("rev-parse", "HEAD"))
        self.assertEqual([r["status"] for r in before["rows"]], ["PRESENT", "MISSING", "MISSING"])
        self.assertEqual([r["status"] for r in after["rows"]], ["MISSING", "PRESENT", "MISSING"])
        self.assertEqual(self.expect("MISSING", 1, paths=paths), before)

    def test_exact_literal_names_and_collisions(self):
        for name in ["a*", "ab", ":(glob)a?", "-q", "x\ny", "x\ty", "a\\b", " é "]:
            (self.repo / name).touch()
        self.git("add", ".")
        self.git("commit", "-qm", "literals")
        paths = ["a*", "a?", ":(glob)a?", "-q", "x\ny", "x\ty", "a\\b", " é ", "é"]
        rows = self.expect("MISSING", 1, pin=self.git("rev-parse", "HEAD"), paths=paths)["rows"]
        self.assertEqual([r["path"] for r in rows], paths)
        self.assertEqual([r["status"] for r in rows], ["PRESENT", "MISSING"] + ["PRESENT"] * 6 + ["MISSING"])

    def test_input_contract(self):
        for paths in ([], None, "record", {}, [0], [False], ["record", []], [""],
                      ["/record"], ["./record"], ["a//b"], ["a/../b"], ["record/"], ["a\0b"],
                      ["\ud800"]):
            with self.subTest(paths=paths):
                raw = json.dumps({"commit": self.pin, "paths": paths}).encode()
                result = self.expect("INVALID_INPUT", 2, raw=raw)
                self.assertEqual((result["commit"], result["rows"]), (None, []))
        for raw in (b"", b"[", b"{}", b"[]", b"\xff", b'{"paths":0,"paths":1}', b"{} {}"):
            with self.subTest(raw=raw):
                self.expect("INVALID_INPUT", 2, raw=raw)

    def test_duplicate_paths_preserve_each_occurrence(self):
        rows = self.expect("PRESENT", 0, paths=["record", "record"])["rows"]
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], rows[1])

    def test_bad_pin_or_known_wrong_object_type(self):
        self.git("tag", "-am", "tag", "annotated")
        for pin in ("HEAD", self.pin[:8], self.pin + "^", "z" * 40, "0" * 64,
                    self.git("rev-parse", "HEAD:record"), self.git("rev-parse", "HEAD^{tree}"),
                    self.git("rev-parse", "annotated")):
            with self.subTest(pin=pin):
                self.expect("INVALID_INPUT", 2, pin=pin)
        self.expect("EVIDENCE_UNAVAILABLE", 3, pin="0" * 40)

    def test_repository_selection(self):
        folder = self.repo / "nested"
        folder.mkdir()
        self.expect("EVIDENCE_UNAVAILABLE", 3, repo=folder)
        self.expect("EVIDENCE_UNAVAILABLE", 3, repo=self.work / "absent")
        self.expect("PRESENT", 0, repo=self.repo / ".git")
        worktree = self.work / "linked"
        self.git("worktree", "add", "--quiet", "--detach", str(worktree))
        self.expect("PRESENT", 0, repo=worktree)
        bare = self.work / "bare"
        subprocess.run(["git", "clone", "--quiet", "--bare", "--local", self.repo, bare],
                       env=self.env, check=True)
        self.expect("PRESENT", 0, repo=bare)

    def test_tree_symlink_gitlink_and_non_directory_traversal(self):
        (self.repo / "dir").mkdir()
        (self.repo / "dir" / "leaf").touch()
        (self.repo / "link").symlink_to("dir")
        self.git("add", ".")
        self.git("update-index", "--add", "--cacheinfo", "160000," + self.pin + ",sub")
        self.git("commit", "-qm", "kinds")
        paths = ["dir", "dir/leaf", "link", "sub", "record/x", "link/leaf", "sub/record"]
        rows = self.expect("MISSING", 1, paths=paths, pin=self.git("rev-parse", "HEAD"))["rows"]
        self.assertEqual([r.get("mode") for r in rows], ["040000", "100644", "120000", "160000", None, None, None])
        self.assertEqual([r["status"] for r in rows], ["PRESENT"] * 4 + ["MISSING"] * 3)

    def test_missing_subtree_and_leaf_object_have_different_meanings(self):
        (self.repo / "dir").mkdir()
        (self.repo / "dir" / "leaf").touch()
        self.git("add", "dir")
        self.git("commit", "-qm", "subtree")
        pin = self.git("rev-parse", "HEAD")
        for rev in ("HEAD:dir", "HEAD:record"):
            oid = self.git("rev-parse", rev)
            (self.repo / ".git/objects" / oid[:2] / oid[2:]).unlink()
        self.expect("PRESENT", 0, paths=["record", "dir"], pin=pin)
        result = self.expect("EVIDENCE_UNAVAILABLE", 3, pin=pin, paths=["absent", "dir/leaf", "record"])
        self.assertEqual(result["commit"], pin)
        self.assertEqual([r["status"] for r in result["rows"]], ["MISSING", "EVIDENCE_UNAVAILABLE", "PRESENT"])

    def test_replacements_and_environment_do_not_redirect_lookup(self):
        (self.repo / "record").unlink()
        self.git("add", "-u")
        self.git("commit", "-qm", "removed")
        self.git("replace", self.pin, self.git("rev-parse", "HEAD"))
        env = dict(self.env, GIT_DIR=str(self.work / "absent"), GIT_OBJECT_DIRECTORY=str(self.work))
        self.expect("PRESENT", 0, env=env)

    def test_unavailable_git(self):
        self.expect("EVIDENCE_UNAVAILABLE", 3, env=dict(self.env, PATH=str(self.work)))


if __name__ == "__main__":
    unittest.main()
