"""Black-box fixture shared by the two exposed DEV suites."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CLI = Path(__file__).with_name("validate_refs.py")


class LocalRepo(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name)
        self.repo = self.work / "repo"
        self.repo.mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME="DEV", GIT_COMMITTER_NAME="DEV",
                        GIT_AUTHOR_EMAIL="dev@example.invalid", GIT_COMMITTER_EMAIL="dev@example.invalid",
                        GIT_AUTHOR_DATE="2001-01-01T00:00:00Z", GIT_COMMITTER_DATE="2001-01-01T00:00:00Z",
                        GIT_ALLOW_PROTOCOL="", LC_ALL="C")
        self.git("init", "-q", "--object-format=sha1", "-b", "main")
        self.git("config", "core.autocrlf", "false")
        (self.repo / "record").write_bytes(b"evidence\n")
        self.git("add", "record")
        self.git("commit", "-qm", "first")
        self.pin = self.git("rev-parse", "HEAD")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", self.repo, *args], env=self.env, text=True).strip()

    def run_cli(self, *, raw=None, paths=None, pin=None, repo=None, env=None, cwd=None, options=()):
        if raw is None:
            raw = json.dumps({"commit": self.pin if pin is None else pin,
                              "paths": ["record"] if paths is None else paths}).encode()
        proc = subprocess.run([sys.executable, *options, CLI, self.repo if repo is None else repo],
                              input=raw, cwd=cwd, env=self.env if env is None else env, capture_output=True)
        self.assertEqual(proc.stderr, b"")
        return json.loads(proc.stdout), proc.returncode
