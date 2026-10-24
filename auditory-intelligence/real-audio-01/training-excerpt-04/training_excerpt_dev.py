#!/usr/bin/env python3
"""Training-excerpt sensitivity with the 500 evaluation mixtures unchanged.

T0 reproduces PR #69. T1/T2/T3 change only which 0.8s interval supplies
the four *training* exemplars before the original fixed train() runs.
Clip-level labels do not validate the selected interval's audible content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "novel-sources-02"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT))
from real_audio import (  # noqa: E402
    LENGTH, NORM_PEAK, RATE, SLOTS, classify, decode, excerpt, mix, rms, train,
)
from novel_source_dev import (  # noqa: E402
    GAIN, METHODS, evaluate as baseline_evaluate, measure, plan,
    predict as baseline_predict, verify_and_excerpt,
)

FROZEN_CONTRACT_SHA256 = "54b3717be2004da81d65074f5b5b2d394995212f191c7d60408278fcbeb8a4ff"
FROZEN_BASELINE_RECEIPT_SHA256 = "b11e089a5a039d37043b5d2e2735ff0fdbb97c24849d1ed1f11820662b3a5f9e"
FROZEN_ALGORITHM_SHA256 = "3dc01418d91546e373b21520b25f22b4ae4909070df2903a70d54da479c3e014"
FROZEN_SELECTION_SHA256 = "bb6d17f2fb8f81db7b74f45ea0120716433263bf8edf088bdb0b83524de38b11"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def normalized_fixed_window(samples: list[float], offset_s: float) -> tuple[list[float], dict]:
    start = round(offset_s * RATE)
    length = int(LENGTH * RATE)
    require(0 <= start and start + length <= len(samples),
            "Frozen training excerpt out of bounds")
    window = samples[start:start + length]
    peak = max(abs(v) for v in window)
    require(peak >= .002, "Frozen training excerpt too quiet; no rerolls")
    return ([v / peak * NORM_PEAK for v in window],
            {"offset_s": offset_s, "raw_peak": round(peak, 8),
             "raw_rms": round(rms(window), 8)})


def frozen_inputs(contract: Path, baseline_receipt: Path,
                  original_manifest: Path, expanded_manifest: Path) -> tuple[dict, dict, dict]:
    require(hashlib.sha256(contract.read_bytes()).hexdigest() == FROZEN_CONTRACT_SHA256,
            "Training-excerpt contract changed; requires new candidate")
    require(hashlib.sha256(baseline_receipt.read_bytes()).hexdigest() ==
            FROZEN_BASELINE_RECEIPT_SHA256, "PR69 evidence receipt changed")
    require(hashlib.sha256((ROOT / "real_audio.py").read_bytes()).hexdigest() ==
            FROZEN_ALGORITHM_SHA256, "Original acoustic algorithm changed")
    require(hashlib.sha256(expanded_manifest.read_bytes()).hexdigest() ==
            FROZEN_SELECTION_SHA256, "PR69 source selection changed")
    contract_data = json.loads(contract.read_text())
    receipt = json.loads(baseline_receipt.read_text())
    document, held, _ = plan(expanded_manifest, original_manifest)
    require(contract_data["baseline_ci_source_receipt_sha256"] ==
            FROZEN_BASELINE_RECEIPT_SHA256, "Receipt provenance mismatch")
    require(contract_data["source_manifest_sha256"] ==
            FROZEN_SELECTION_SHA256, "Source-selection contract mismatch")
    require(contract_data["baseline_real_audio_sha256"] ==
            FROZEN_ALGORITHM_SHA256, "Algorithm contract mismatch")
    require(len(document["train_sources"]) == 4 and
            len(document["new_eval_sources"]) == 15, "Frozen source counts changed")
    return contract_data, receipt, document


def verify_original_outputs(actual: dict, ci: dict) -> None:
    require(actual["design"]["constructed_rows"] == 500 and
            actual["method_totals"] == ci["method_totals"],
            "Original PR69 500-case method totals not reproduced")
    expected_shas = ci["new_eval_wav_sha256s"]
    actual_shas = {r["filename"]: r["sha256"] for r in actual["sources"]}
    require(len(expected_shas) == 15, "Unexpected PR69 source receipt cardinality")
    for filename, sha in expected_shas.items():
        require(actual_shas.get(filename) == sha, "PR69 WAV SHA mismatch: " + filename)
    for report in ci["per_source_summaries"]:
        found = next((r for r in actual["source_summaries"][report["category"]]
                      if r["filename"] == report["filename"]), None)
        require(found is not None and found["scores"] == report["scores"],
                "PR69 per-source scores no longer reproduce: " + report["filename"])


def evaluate(original_dir: Path, new_dir: Path, contract_path: Path,
             expanded_manifest: Path, old_manifest: Path,
             original_hash_receipt: Path, ci_receipt_path: Path) -> dict:
    contract, ci, manifest = frozen_inputs(
        contract_path, ci_receipt_path, old_manifest, expanded_manifest)
    original_result = baseline_evaluate(expanded_manifest, old_manifest,
                                        original_dir, new_dir, original_hash_receipt)
    verify_original_outputs(original_result, ci)
    records = manifest["train_sources"] + manifest["new_eval_sources"]
    indexed = {r["filename"]: r for r in records}
    original_shas = json.loads(original_hash_receipt.read_text())
    old_segments = {}
    new_segments = {}
    all_raw_train = {}
    for r in manifest["train_sources"]:
        fn = r["filename"]
        old_segments[fn] = verify_and_excerpt(original_dir / fn, original_shas[fn])
        all_raw_train[fn] = decode(original_dir / fn)
    for r in manifest["new_eval_sources"]:
        fn = r["filename"]
        new_segments[fn] = verify_and_excerpt(new_dir / fn, ci["new_eval_wav_sha256s"][fn])
    t0_prototypes = train({**old_segments, **new_segments}, indexed)

    # Precommitted offsets and source IDs: never reroll on low-energy windows.
    offsets = contract["training_offsets_seconds"]
    require(set(offsets) == {r["source_id"] for r in manifest["train_sources"]},
            "Training-offset source identity mismatch")
    alternate_prototypes = {}
    training_measurements = {}
    for arm in (1, 2, 3):
        trained = dict(new_segments)
        report = []
        for r in manifest["train_sources"]:
            fn, sid = r["filename"], r["source_id"]
            positions = offsets[sid]
            require(len(positions) == 3, "Three frozen starts required per source")
            interval, stats = normalized_fixed_window(all_raw_train[fn], positions[arm - 1])
            trained[fn] = (interval, stats["offset_s"], old_segments[fn][2])
            report.append({"source_id": sid, "filename": fn,
                           "peak_offset_t0_s": old_segments[fn][1],
                           "coincides_with_t0": stats["offset_s"] == old_segments[fn][1],
                           **stats})
        alternate_prototypes["T" + str(arm)] = train(trained, indexed)
        training_measurements["T" + str(arm)] = report

    rows_by_arm = {"T0": original_result["constructed_rows"]}
    for arm in ("T1", "T2", "T3"):
        rows_by_arm[arm] = []
    baseline_rows = original_result["constructed_rows"]
    for old in baseline_rows:
        files = old["source_filenames"]
        events = {c: new_segments[files[c]][0] for c in ("dog", "chainsaw")}
        rain = new_segments[files["rain"]][0]
        schedule = tuple(old["schedule"])
        waveform, clipped = mix(schedule, events, rain, GAIN)
        require(clipped == 0, "Newly reconstructed evaluation mixture clipped")
        slots = [waveform[int(t * RATE):int((t + LENGTH) * RATE)] for t in SLOTS]
        require(baseline_predict(slots, t0_prototypes) == old["predictions"],
                "The 500 PR69 evaluation mixtures changed")
        for arm, prototypes in alternate_prototypes.items():
            outcomes = {}
            for method in METHODS:
                if method == "energy":
                    outcomes[method] = old["predictions"][method]
                else:
                    labels = [classify(v, prototypes, method) for v in slots]
                    outcomes[method] = {
                        "labels": labels, "matched": labels == ["dog", "chainsaw"]}
            rows_by_arm[arm].append({
                "indices": old["indices"], "source_filenames": files,
                "schedule": old["schedule"], "gain": old["gain"],
                "positive": old["positive"], "predictions": outcomes})
    require(all(len(v) == 500 for v in rows_by_arm.values()),
            "Each of four training arms must score the same 500 mixtures")

    totals = {arm: measure(rows) for arm, rows in rows_by_arm.items()}
    by_dog = {}
    flips = {}
    for arm, rows in rows_by_arm.items():
        by_dog[arm] = []
        for r in (x for x in manifest["new_eval_sources"] if x["category"] == "dog"):
            selected = [x for x in rows if x["source_filenames"]["dog"] == r["filename"]]
            require(len(selected) == 100, "Missing dog-source cases")
            by_dog[arm].append({"source_id": r["source_id"],
                                "filename": r["filename"],
                                "scores": measure(selected)})
        if arm != "T0":
            flips[arm] = {}
            for method in METHODS:
                flips[arm][method] = {
                    "matched_prediction_changed": sum(
                        x["predictions"][method]["matched"] != y["predictions"][method]["matched"]
                        for x, y in zip(baseline_rows, rows)),
                    "labels_changed": sum(
                        x["predictions"][method]["labels"] != y["predictions"][method]["labels"]
                        for x, y in zip(baseline_rows, rows)),
                    "abstention_presence_changed": sum(
                        ("abstain" in x["predictions"][method]["labels"]) !=
                        ("abstain" in y["predictions"][method]["labels"])
                        for x, y in zip(baseline_rows, rows)),
                }
    return {
        "research_id": "AUDITORY-TRAIN-EXCERPT-DEV-04",
        "status": "EXPOSED_ENGINEERING_DEV",
        "frozen_contract_sha256": FROZEN_CONTRACT_SHA256,
        "base_pr69_receipt_sha256": FROZEN_BASELINE_RECEIPT_SHA256,
        "algorithm_sha256": FROZEN_ALGORITHM_SHA256,
        "source_manifest_sha256": FROZEN_SELECTION_SHA256,
        "design": {
            "distinct_evaluation_source_ids": 15,
            "original_training_source_ids": 4,
            "identical_constructed_eval_rows_per_arm": 500,
            "training_arms": ["T0", "T1", "T2", "T3"],
            "precommitted_training_window_starts": True,
            "training_source_excerpt_only_changed": True,
            "original_pr69_baseline_reproduced": True,
            "actual_event_labels_in_training_windows": "UNKNOWN",
        },
        "source_sha256": {r["filename"]: r["sha256"]
                          for r in original_result["sources"]},
        "training_measurements": training_measurements,
        "method_totals_by_arm": totals,
        "per_dog_source_scores_by_arm": by_dog,
        "paired_changes_vs_T0": flips,
        "rows_by_arm": rows_by_arm,
        "nonclaims": contract["interpretation_limits"],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--contract", default=str(HERE / "frozen_contract.json"))
    p.add_argument("--old-manifest", default="sources.json")
    p.add_argument("--expanded-manifest", default=str(PARENT / "selected_sources.json"))
    p.add_argument("--old-audio-dir", default="clip_cache")
    p.add_argument("--new-audio-dir", default="clip_cache_new")
    p.add_argument("--original-hashes", default="receipts/source_sha256.json")
    p.add_argument("--ci-receipt", default=str(PARENT / "receipts/ci_source_summary_2026-10-24.json"))
    p.add_argument("--out", default="training_excerpt_results.json")
    a = p.parse_args()
    result = evaluate(Path(a.old_audio_dir), Path(a.new_audio_dir),
                      Path(a.contract), Path(a.expanded_manifest),
                      Path(a.old_manifest), Path(a.original_hashes), Path(a.ci_receipt))
    Path(a.out).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print("TRAIN_EXCERPT_DESIGN:", json.dumps(result["design"], sort_keys=True))
    print("TRAIN_EXCERPT_TOTALS:", json.dumps(result["method_totals_by_arm"], sort_keys=True))
    print("TRAIN_EXCERPT_FLIPS:", json.dumps(result["paired_changes_vs_T0"], sort_keys=True))
    print("TRAIN_EXCERPT_DOG_SCORES:", json.dumps(result["per_dog_source_scores_by_arm"], sort_keys=True))
    print("TRAIN_EXCERPT_MEASUREMENTS:", json.dumps(result["training_measurements"], sort_keys=True))


if __name__ == "__main__":
    main()
