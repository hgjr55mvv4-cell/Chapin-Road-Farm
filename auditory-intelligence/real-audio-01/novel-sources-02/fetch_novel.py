#!/usr/bin/env python3
"""Download only frozen, individually CC0 novel ESC-10 source WAVs for DEV."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from fetch_clips import get  # original downloader's pinned ESC-50 commit and limits
FROZEN_MANIFEST_SHA256 = "bb6d17f2fb8f81db7b74f45ea0120716433263bf8edf088bdb0b83524de38b11"


def main() -> None:
    manifest_path = HERE / "selected_sources.json"
    raw = manifest_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != FROZEN_MANIFEST_SHA256:
        raise ValueError("New source selection manifest is not frozen")
    manifest = json.loads(raw)
    if manifest["dataset_commit"] != "33c8ce9eb2cf0b1c2f8bcf322eb349b6be34dbb6":
        raise ValueError("Dataset commit mismatch")
    chosen = manifest["new_eval_sources"]
    if len(chosen) != 15:
        raise ValueError("Wrong number of selected recordings")
    metadata = {r["filename"]: r for r in
                csv.DictReader(get("meta/esc50.csv").decode("utf8").splitlines())}
    licensing = get("LICENSE").decode("utf8").splitlines()
    folder = Path("clip_cache_new")
    folder.mkdir(exist_ok=True)
    checksums = {}
    for source in chosen:
        filename = source["filename"]
        if not re.fullmatch(r"[2-5]-\d+-[A-Z]-\d+\.wav", filename):
            raise ValueError("Malformed source filename: " + filename)
        row = metadata.get(filename)
        if (not row or row["category"] != source["category"]
            or row["esc10"] != "True"
            or row["src_file"] != source["source_id"]
            or int(row["fold"]) != source["fold"]):
            raise ValueError("Pinned ESC-10 class/identity/fold mismatch: " + filename)
        ogg = re.sub(r"-\d+\.wav$", ".ogg", filename)
        entries = [x for x in licensing if x.startswith("- [" + ogg + "]")]
        if (len(entries) != 1 or
            not entries[0].endswith("by " + source["author"] + " [CC0]")):
            raise ValueError("Original-source CC0 attribution not proven: " + filename)
        wav = get("audio/" + filename)
        if len(wav) != 441044 or wav[:4] != b"RIFF":
            raise ValueError("Unexpected real ESC-10 WAV size/signature: " + filename)
        (folder / filename).write_bytes(wav)
        checksums[filename] = hashlib.sha256(wav).hexdigest()
        print("NOVEL_SOURCE_VERIFIED", filename, source["source_id"],
              source["author"], checksums[filename])
    print("NOVEL_SOURCE_LICENSED_COUNT", len(checksums))
    print("NOVEL_SOURCE_DOWNLOADED_SHA256:", json.dumps(checksums, sort_keys=True))


if __name__ == "__main__":
    main()
