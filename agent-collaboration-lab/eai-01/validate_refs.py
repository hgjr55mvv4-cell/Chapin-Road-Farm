"""Look up literal UTF-8 Git tree entries at an exact local commit."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys


EXIT = {"PRESENT": 0, "MISSING": 1, "INVALID_INPUT": 2, "EVIDENCE_UNAVAILABLE": 3}


class Unavailable(Exception):
    """Local Git could not provide the requested evidence."""


def unique_members(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON member")
        obj[key] = value
    return obj


def request(raw):
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_members)
    if not isinstance(data, dict) or data.keys() != {"commit", "paths"}:
        raise ValueError("expected an object with exactly commit and paths")
    pin = data["commit"]
    if not isinstance(pin, str) or not re.fullmatch(r"(?:[a-fA-F0-9]{40}|[a-fA-F0-9]{64})", pin):
        raise ValueError("expected a full hexadecimal commit ID")
    paths = data["paths"]
    if not isinstance(paths, list) or not paths:
        raise ValueError("expected a nonempty paths array")
    for i, path in enumerate(paths):
        if not isinstance(path, str) or "\0" in path or any(s in ("", ".", "..") for s in path.split("/")):
            raise ValueError(f"invalid repository path at index {i}")
        path.encode("utf-8")
    return pin.lower(), paths


def git_reader(repository):
    root = Path(repository)
    git_dir = root / ".git" if (root / ".git").exists() else root
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_NO_LAZY_FETCH="1", GIT_ALLOW_PROTOCOL="", LC_ALL="C")

    def git(*args):
        try:
            result = subprocess.run(
                ["git", "--no-replace-objects", f"--git-dir={git_dir.absolute()}", *args],
                env=env, capture_output=True, check=False)
        except OSError as exc:
            raise Unavailable("local Git could not run") from exc
        if result.returncode:
            raise Unavailable(f"Git could not complete {args[0]}")
        return result.stdout

    return git


def report(verdict, commit=None, rows=None, reason=None):
    result = {"scope": "git_tree_entry", "verdict": verdict, "commit": commit,
              "rows": [] if rows is None else rows}
    if reason is not None:
        result["reason"] = reason
    return result


def tree_entries(git, oid, *, root):
    # Git also accepts commits and tags as ls-tree arguments. Only the initial
    # lookup intentionally uses that feature; subtree edges require a tree.
    if not root and git("cat-file", "-t", oid).strip() != b"tree":
        raise Unavailable("subtree object has the wrong type")
    entries = {}
    for record in git("ls-tree", "-z", oid).split(b"\0"):
        if record:
            header, name = record.split(b"\t", 1)
            mode, kind, child = header.decode("ascii").split()
            if name in entries:
                entries[name] = None  # The directory supplies conflicting identities.
            else:
                entries[name] = {"mode": mode, "type": kind, "oid": child}
    return entries


def lookup(git, cache, commit, path):
    tree = commit
    parts = path.encode("utf-8").split(b"/")
    for i, name in enumerate(parts):
        if tree not in cache:
            try:
                cache[tree] = tree_entries(git, tree, root=(i == 0))
            except (Unavailable, ValueError):
                cache[tree] = None
        entries = cache[tree]
        if entries is None:
            return {"path": path, "status": "EVIDENCE_UNAVAILABLE", "unreadable_at": tree}
        if name not in entries:
            return {"path": path, "status": "MISSING"}
        entry = entries[name]
        if entry is None:
            return {"path": path, "status": "EVIDENCE_UNAVAILABLE", "ambiguous_at": tree}
        if i == len(parts) - 1:
            return {"path": path, "status": "PRESENT", **entry}
        if entry["type"] != "tree":
            return {"path": path, "status": "MISSING"}
        tree = entry["oid"]


def validate(repository, raw):
    try:
        pin, paths = request(raw)
        git = git_reader(repository)
        object_format = git("rev-parse", "--show-object-format=storage").strip()
        widths = {b"sha1": 40, b"sha256": 64}
        if object_format not in widths:
            raise Unavailable("unsupported Git storage format")
        if len(pin) != widths[object_format]:
            raise ValueError("ID width does not match the repository")
        if git("cat-file", "-t", pin).strip() != b"commit":
            raise ValueError("pin identifies a non-commit object")
    except (ValueError, RecursionError) as exc:
        return report("INVALID_INPUT", reason=str(exc))
    except (OSError, Unavailable) as exc:
        return report("EVIDENCE_UNAVAILABLE", reason=str(exc))

    cache = {}
    rows = [lookup(git, cache, pin, path) for path in paths]
    statuses = {row["status"] for row in rows}
    if "EVIDENCE_UNAVAILABLE" in statuses:
        return report("EVIDENCE_UNAVAILABLE", pin, rows)
    if "MISSING" in statuses:
        return report("MISSING", pin, rows)
    return report("PRESENT", pin, rows)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1]:
        result = validate(sys.argv[1], sys.stdin.buffer.read())
    else:
        result = report("INVALID_INPUT", reason="usage: python3 validate_refs.py REPOSITORY < request.json")
    print(json.dumps(result, ensure_ascii=True))
    sys.exit(EXIT[result["verdict"]])
