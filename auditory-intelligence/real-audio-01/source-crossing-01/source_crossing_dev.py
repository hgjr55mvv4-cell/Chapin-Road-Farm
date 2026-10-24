#!/usr/bin/env python3
"""Cross the six existing held-out ESC-10 sources; exposed engineering DEV only.

This is a nuisance-factor diagnostic, not six new independent recordings.
The original detector, source excerpts, and trained prototypes are unchanged.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from real_audio import (
    CATEGORIES, ENERGY_THRESHOLD, LENGTH, RATE, SLOTS,
    classify, decode, excerpt, mix, rms, train,
)

SCHEDULES = (
    ("dog", "chainsaw"), ("chainsaw", "dog"), ("dog", "dog"),
    ("chainsaw", "chainsaw"), ("dog", "none"), ("none", "chainsaw"),
    ("none", "none"), ("chainsaw", "none"),
)
GAINS = (0.25, 0.50, 0.85)
METHODS = ("energy", "zcr", "multiband")
EXPECTED_SHA_FILE = "receipts/source_sha256.json"
EXISTING_CASES_FILE = "receipts/real_case_decisions.csv"


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def plan_sources(document: dict) -> tuple[dict, list[dict]]:
    """Freeze all eight crosses in the manifest's fold-2 then fold-3 order."""
    records = document["sources"]
    require(len(records) == 10, "Expected exact original 10-recording manifest")
    require(len({r["filename"] for r in records}) == 10, "Duplicate filename")
    require(len({r["source_id"] for r in records}) == 10,
            "Source identity reused, including across classes or folds")
    require({r["role"] for r in records} == {"train", "eval"}, "Unknown source role")
    require(sum(r["role"] == "train" for r in records) == 4, "Training set changed")
    held = {}
    for category in ("dog", "chainsaw", "rain"):
        items = sorted((r for r in records if r["role"] == "eval" and
                        r["category"] == category), key=lambda r: r["filename"])
        require(len(items) == 2, f"Expected two eval recordings: {category}")
        require(tuple(int(r["filename"][0]) for r in items) == (2, 3),
                f"Evaluation fold order changed for {category}")
        held[category] = items
    groups = []
    for d, c, r in product(range(2), repeat=3):
        selected = {
            "dog": held["dog"][d]["filename"],
            "chainsaw": held["chainsaw"][c]["filename"],
            "rain": held["rain"][r]["filename"],
        }
        groups.append({"cross_index": [d, c, r], "sources": selected})
    require(len(groups) == 8, "Crossed plan did not yield eight groups")
    return held, groups


def validate_audio(records: list[dict], audio_dir: Path, receipt: Path) -> dict:
    expected = json.loads(receipt.read_text())
    require(set(expected) == {r["filename"] for r in records},
            "Source hash receipt does not match manifest filenames")
    data = {}
    for r in records:
        path = audio_dir / r["filename"]
        if not path.is_file():
            raise FileNotFoundError("ACTUAL ESC-10 WAV REQUIRED: " + str(path))
        source_sha = hashlib.sha256(path.read_bytes()).hexdigest()
        require(source_sha == expected[r["filename"]],
                "Pinned source SHA-256 mismatch: " + r["filename"])
        segment, offset = excerpt(decode(path))
        data[r["filename"]] = (segment, offset, source_sha)
    return data


def predictions(windows: list[list[float]], prototypes: dict) -> dict:
    outputs = {}
    for name in METHODS:
        if name == "energy":
            labels = tuple("active" if rms(s) >= ENERGY_THRESHOLD else "none"
                           for s in windows)
            matched = labels == ("active", "active")
        else:
            labels = tuple(classify(s, prototypes, name) for s in windows)
            matched = labels == ("dog", "chainsaw")
        outputs[name] = {"labels": list(labels), "matched": matched}
    return outputs


def verify_diagonal(rows: list[dict], receipt: Path) -> None:
    """The original two paired source groups must reproduce all 48 ledger rows."""
    with receipt.open(newline="") as handle:
        archived = list(csv.DictReader(handle))
    require(len(archived) == 48, "Original ledger row count changed")
    expected = {
        (int(row["source_group"]), row["slots"], float(row["gain"])): row
        for row in archived
    }
    require(len(expected) == 48, "Duplicate original ledger key")
    diagonal = [r for r in rows if len(set(r["cross_index"])) == 1]
    require(len(diagonal) == 48, "Unexpected number of diagonal control rows")
    for case in diagonal:
        key = (case["cross_index"][0], ">".join(case["slot_sources"]), case["gain"])
        saved = expected.get(key)
        require(saved is not None, "Missing original ledger row: " + str(key))
        require(int(saved["truth"]) == int(case["planted_positive"]),
                "Original truth differs: " + str(key))
        for method, values in case["predictions"].items():
            require(int(saved[method + "_alert"]) == int(values["matched"]),
                    f"Original {method} alert differs: {key}")
            if method != "energy":
                require(saved[method + "_labels"] == ">".join(values["labels"]),
                        f"Original {method} labels differ: {key}")


def evaluate(audio_dir: Path, manifest: Path, sha_receipt: Path,
             case_receipt: Path) -> dict:
    document = json.loads(manifest.read_text())
    records = document["sources"]
    held, groups = plan_sources(document)
    data = validate_audio(records, audio_dir, sha_receipt)
    indexed = {r["filename"]: r for r in records}
    prototypes = train(data, indexed)
    all_rows = []
    summaries = []
    for group in groups:
        files = group["sources"]
        heldout = {c: data[files[c]][0] for c in CATEGORIES}
        background = data[files["rain"]][0]
        local = []
        for schedule in SCHEDULES:
            for gain in GAINS:
                wav, clipped = mix(schedule, heldout, background, gain)
                require(clipped == 0, "Clipped constructed waveform")
                windows = [wav[int(t * RATE):int((t + LENGTH) * RATE)] for t in SLOTS]
                values = predictions(windows, prototypes)
                row = {
                    "cross_index": group["cross_index"],
                    "source_filenames": files,
                    "slot_sources": list(schedule),
                    "gain": gain,
                    "planted_positive": schedule == ("dog", "chainsaw"),
                    "predictions": values,
                }
                all_rows.append(row)
                local.append(row)
        score = {}
        for method in METHODS:
            pos = [r for r in local if r["planted_positive"]]
            neg = [r for r in local if not r["planted_positive"]]
            score[method] = {
                "positive_hits_of_3": sum(r["predictions"][method]["matched"] for r in pos),
                "false_alerts_of_21": sum(r["predictions"][method]["matched"] for r in neg),
                "abstaining_queries_of_24": sum(
                    "abstain" in r["predictions"][method]["labels"] for r in local),
            }
        summaries.append({"cross_index": group["cross_index"],
                          "source_filenames": files, "scores": score})
    require(len(all_rows) == 192 and len(summaries) == 8,
            "Expected eight crosses, 24 rows per cross")
    verify_diagonal(all_rows, case_receipt)
    return {
        "research_id": "AUDITORY-SOURCE-CROSSING-DEV-01",
        "status": "EXPOSED_ENGINEERING_DEV",
        "provenance": document["provenance"],
        "design": {
            "distinct_eval_recordings": 6,
            "crossed_configurations": 8,
            "constructed_rows": 192,
            "positive_rows": 24,
            "negative_rows": 168,
            "independent_source_count_does_not_increase": True,
            "diagonal_original_48_rows_reproduced": True,
            "thresholds_and_prototypes_unchanged": True,
        },
        "source_hashes": {r["filename"]: data[r["filename"]][2] for r in records},
        "groups": summaries,
        "rows": all_rows,
        "nonclaims": [
            "Eight combinations are not eight statistically independent recordings.",
            "Only six unique held-out source recordings are used repeatedly.",
            "Class tags are clip-level labels, not annotated natural event onsets.",
            "The experimenter supplies the slot boundaries and selects peak-energy excerpts.",
            "No physical-source identity, machine diagnosis, or population generalization established.",
            "Development cases only; prospective scientific confirmation remains HOLD.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-dir", default="clip_cache")
    parser.add_argument("--manifest", default="sources.json")
    parser.add_argument("--hash-receipt", default=EXPECTED_SHA_FILE)
    parser.add_argument("--case-receipt", default=EXISTING_CASES_FILE)
    parser.add_argument("--out", default="crossed_results.json")
    args = parser.parse_args()
    result = evaluate(Path(args.audio_dir), Path(args.manifest),
                      Path(args.hash_receipt), Path(args.case_receipt))
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("CROSSING_DESIGN:", json.dumps(result["design"], sort_keys=True))
    for group in result["groups"]:
        print("CROSSING_GROUP:", json.dumps(group, sort_keys=True))


if __name__ == "__main__":
    main()
