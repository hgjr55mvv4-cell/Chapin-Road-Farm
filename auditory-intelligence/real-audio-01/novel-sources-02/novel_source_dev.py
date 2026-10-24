#!/usr/bin/env python3
"""Held-out ESC-10 source-ID expansion; engineered slot-label association only.

The baseline real_audio algorithms, fixed prototypes, normalization, slots,
excerpt selector, and thresholds are imported unchanged. This is not
natural acoustic event localization, human perception, or source-object ID.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from real_audio import (  # noqa: E402
    CATEGORIES, ENERGY_THRESHOLD, LENGTH, RATE, SLOTS,
    classify, decode, excerpt, mix, rms, train,
)

FROZEN_MANIFEST_SHA256 = "bb6d17f2fb8f81db7b74f45ea0120716433263bf8edf088bdb0b83524de38b11"
DATASET_COMMIT = "33c8ce9eb2cf0b1c2f8bcf322eb349b6be34dbb6"
FROZEN_ALGORITHM_SHA256 = "3dc01418d91546e373b21520b25f22b4ae4909070df2903a70d54da479c3e014"
SCHEDULES = (
    ("dog", "chainsaw"),
    ("chainsaw", "dog"),
    ("dog", "dog"),
    ("chainsaw", "chainsaw"),
)
GAIN = 0.50
METHODS = ("energy", "zcr", "multiband")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def plan(manifest_path: Path, original_manifest_path: Path) -> tuple[dict, dict, list[dict]]:
    raw = manifest_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == FROZEN_MANIFEST_SHA256,
            "Frozen source selection changed; new candidate version required")
    document = json.loads(raw)
    require(document["dataset_commit"] == DATASET_COMMIT, "Dataset commit drift")
    original = json.loads(original_manifest_path.read_text())
    originals = original["sources"]
    train_sources = [r for r in originals if r["role"] == "train"]
    require(document["train_sources"] == train_sources and len(train_sources) == 4,
            "Training sources changed")
    eval_sources = document["new_eval_sources"]
    require(len(eval_sources) == 15, "Expected fifteen new held-out recordings")
    require(all(x["role"] == "eval" and x["license"] == "CC0" for x in eval_sources),
            "Invalid evaluation source role/license")
    all_sources = train_sources + eval_sources
    require(len({x["filename"] for x in all_sources}) == 19,
            "Duplicate WAV filename")
    require(len({x["source_id"] for x in all_sources}) == 19,
            "Repeated Freesound source identity")
    require(not ({x["source_id"] for x in eval_sources} &
                 {x["source_id"] for x in originals}),
            "New evaluation source identity overlaps original ten-source study")
    held = {cat: [x for x in eval_sources if x["category"] == cat]
            for cat in ("dog", "chainsaw", "rain")}
    require(all(len(v) == 5 for v in held.values()), "Not five source IDs per class")
    require(sorted(x["fold"] for x in held["dog"]) == [2, 2, 3, 4, 5],
            "Dog fold allocation drift")
    require(sorted(x["fold"] for x in held["rain"]) == [2, 2, 3, 4, 5],
            "Rain fold allocation drift")
    require(sorted(x["fold"] for x in held["chainsaw"]) == [4, 4, 4, 5, 5],
            "Chainsaw fold allocation drift")
    triples = []
    for d, c, r in product(range(5), repeat=3):
        triples.append({"indices": [d, c, r],
                        "filenames": {k: held[k][idx]["filename"]
                                      for k, idx in (("dog", d), ("chainsaw", c), ("rain", r))}})
    require(len(triples) == 125 and len({tuple(g["indices"]) for g in triples}) == 125,
            "Crossed sampling plan changed")
    return document, held, triples


def verify_and_excerpt(path: Path, sha: str | None) -> tuple[list[float], float, str]:
    if not path.is_file():
        raise FileNotFoundError("ACTUAL WAV REQUIRED; NO SYNTHETIC FALLBACK: " + str(path))
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if sha is not None:
        require(actual == sha, "Original pinned source SHA mismatch: " + path.name)
    segment, offset = excerpt(decode(path))
    return segment, offset, actual


def predict(slots: list[list[float]], prototypes: dict) -> dict:
    results = {}
    for method in METHODS:
        if method == "energy":
            labels = tuple("active" if rms(v) >= ENERGY_THRESHOLD else "none"
                           for v in slots)
            matched = labels == ("active", "active")
        else:
            labels = tuple(classify(v, prototypes, method) for v in slots)
            matched = labels == ("dog", "chainsaw")
        results[method] = {"labels": list(labels), "matched": matched}
    return results


def measure(rows: list[dict]) -> dict:
    positives = [x for x in rows if x["positive"]]
    negatives = [x for x in rows if not x["positive"]]
    return {method: {
        "positive_hits": sum(x["predictions"][method]["matched"] for x in positives),
        "positive_cases": len(positives),
        "false_alerts": sum(x["predictions"][method]["matched"] for x in negatives),
        "negative_cases": len(negatives),
        "rows_with_abstention": sum(
            "abstain" in x["predictions"][method]["labels"] for x in rows),
        "constructed_rows": len(rows),
    } for method in METHODS}


def evaluate(manifest: Path, original_manifest: Path, original_audio_dir: Path,
             new_audio_dir: Path, original_hash_receipt: Path) -> dict:
    require(hashlib.sha256((ROOT / "real_audio.py").read_bytes()).hexdigest() == FROZEN_ALGORITHM_SHA256,
            "Frozen algorithm source changed; new candidate version required")
    document, held, triples = plan(manifest, original_manifest)
    original_shas = json.loads(original_hash_receipt.read_text())
    records = document["train_sources"] + document["new_eval_sources"]
    data = {}
    for record in records:
        filename = record["filename"]
        path = (original_audio_dir if record["role"] == "train"
                else new_audio_dir) / filename
        sha = original_shas[filename] if record["role"] == "train" else None
        data[filename] = verify_and_excerpt(path, sha)
    prototypes = train(data, {r["filename"]: r for r in records})
    all_rows = []
    group_scores = []
    for group in triples:
        files = group["filenames"]
        heldout = {c: data[files[c]][0] for c in CATEGORIES}
        background = data[files["rain"]][0]
        local = []
        for schedule in SCHEDULES:
            wav, clipped = mix(schedule, heldout, background, GAIN)
            require(clipped == 0, "Clipped constructed audio")
            windows = [wav[int(t * RATE):int((t + LENGTH) * RATE)] for t in SLOTS]
            row = {"indices": group["indices"], "source_filenames": files,
                   "schedule": list(schedule), "gain": GAIN,
                   "positive": schedule == ("dog", "chainsaw"),
                   "predictions": predict(windows, prototypes)}
            local.append(row)
            all_rows.append(row)
        group_scores.append({"indices": group["indices"], "source_filenames": files,
                             "scores": measure(local)})
    require(len(all_rows) == 500 and len(group_scores) == 125,
            "Unexpected experiment row count")
    source_summaries = {}
    for category in ("dog", "chainsaw", "rain"):
        source_summaries[category] = []
        for record in held[category]:
            filename = record["filename"]
            selected = [x for x in all_rows if x["source_filenames"][category] == filename]
            require(len(selected) == 100, "Source reuse or missing cases: " + filename)
            source_summaries[category].append({
                "filename": filename,
                "source_id": record["source_id"],
                "fold": record["fold"],
                "scores": measure(selected),
            })
    return {
        "research_id": "AUDITORY-NOVEL-SOURCES-DEV-02",
        "status": "EXPOSED_ENGINEERING_DEV",
        "baseline_sha256": hashlib.sha256((ROOT / "real_audio.py").read_bytes()).hexdigest(),
        "selection_manifest_sha256": FROZEN_MANIFEST_SHA256,
        "dataset_commit": DATASET_COMMIT,
        "design": {
            "new_unique_freesound_eval_source_ids": 15,
            "per_class_eval_source_ids": 5,
            "crossed_source_triples": 125,
            "constructed_rows": 500,
            "positive_rows": 125,
            "negative_rows": 375,
            "gain": GAIN,
            "independent_crosses_claim": False,
            "frozen_methods": True,
            "oracle_slot_boundaries": True,
        },
        "sources": [{
            "filename": r["filename"], "category": r["category"],
            "role": r["role"], "source_id": r["source_id"],
            "sha256": data[r["filename"]][2],
            "peak_excerpt_offset_s": data[r["filename"]][1]
        } for r in records],
        "method_totals": measure(all_rows),
        "source_summaries": source_summaries,
        "crossed_group_scores": group_scores,
        "constructed_rows": all_rows,
        "nonclaims": document["nonclaims"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(HERE / "selected_sources.json"))
    parser.add_argument("--original-manifest", default="sources.json")
    parser.add_argument("--original-audio-dir", default="clip_cache")
    parser.add_argument("--new-audio-dir", default="clip_cache_new")
    parser.add_argument("--original-hashes", default="receipts/source_sha256.json")
    parser.add_argument("--out", default="novel_source_results.json")
    args = parser.parse_args()
    result = evaluate(Path(args.manifest), Path(args.original_manifest),
                      Path(args.original_audio_dir), Path(args.new_audio_dir),
                      Path(args.original_hashes))
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("NOVEL_SOURCE_DESIGN:", json.dumps(result["design"], sort_keys=True))
    print("NOVEL_SOURCE_METHOD_TOTALS:", json.dumps(result["method_totals"], sort_keys=True))
    for category in ("dog", "chainsaw", "rain"):
        for record in result["source_summaries"][category]:
            print("NOVEL_SOURCE_ROW:", json.dumps({"category": category, **record},
                                                  sort_keys=True))
    print("NOVEL_SOURCE_BYTE_SHA256:", json.dumps(
        {s["filename"]: s["sha256"] for s in result["sources"]}, sort_keys=True))


if __name__ == "__main__":
    main()
