#!/usr/bin/env python3
"""Sensing-only eligibility inventory for a BLOCKED training-excerpt experiment.

Records raw peak/RMS of all fixed-grid 0.8s windows from original public WAVs.
This does not test if any window contains an audible labeled class event.
Does not modify, reselect or retry the frozen DEV-04 training offsets.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from real_audio import LENGTH, RATE, decode, excerpt, rms  # noqa: E402

CONTRACT_SHA = "54b3717be2004da81d65074f5b5b2d394995212f191c7d60408278fcbeb8a4ff"


def main() -> None:
    contract_file = HERE / "frozen_contract.json"
    if hashlib.sha256(contract_file.read_bytes()).hexdigest() != CONTRACT_SHA:
        raise ValueError("Original failed DEV-04 contract not preserved")
    contract = json.loads(contract_file.read_text())
    manifest = json.loads((ROOT / "novel-sources-02" / "selected_sources.json").read_text())
    old_shas = json.loads((ROOT / "receipts" / "source_sha256.json").read_text())
    ci = json.loads((ROOT / "novel-sources-02" / "receipts" /
                     "ci_source_summary_2026-10-24.json").read_text())
    records = manifest["train_sources"] + manifest["new_eval_sources"]
    if len(records) != 19:
        raise ValueError("Expected 19 public source WAVs")
    result = []
    for source in records:
        filename = source["filename"]
        path = ROOT / ("clip_cache" if source["role"] == "train"
                       else "clip_cache_new") / filename
        if not path.is_file():
            raise FileNotFoundError("Real public WAV missing: " + filename)
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = (old_shas[filename] if source["role"] == "train"
                    else ci["new_eval_wav_sha256s"][filename])
        if sha != expected:
            raise ValueError("WAV SHA-256 mismatch: " + filename)
        samples = decode(path)
        window_length = int(LENGTH * RATE)
        starts = list(range(0, len(samples) - window_length + 1, RATE // 4))
        if len(starts) != 17:
            raise ValueError("Unexpected window count from actual source: " + filename)
        windows = []
        for idx, start in enumerate(starts):
            w = samples[start:start + window_length]
            peak = max(abs(x) for x in w)
            windows.append({
                "grid_index": idx,
                "offset_s": round(start / RATE, 2),
                "peak": round(peak, 8),
                "rms": round(rms(w), 8),
                "valid_under_original_peak_rule": peak >= .002,
            })
        _, original_offset = excerpt(samples)
        alternative = []
        if source["role"] == "train":
            positions = contract["training_offsets_seconds"][source["source_id"]]
            by_offset = {w["offset_s"]: w for w in windows}
            for arm, offset in enumerate(positions, 1):
                alternative.append({"arm": "T" + str(arm), **by_offset[offset]})
        row = {
            "filename": filename, "source_id": source["source_id"],
            "category": source["category"], "role": source["role"],
            "wav_sha256": sha,
            "peak_excerpt_original_offset_s": original_offset,
            "eligible_windows_of_17": sum(w["valid_under_original_peak_rule"] for w in windows),
            "precommitted_train_offsets": alternative,
            "all_windows": windows,
            "event_content_ground_truth": "UNKNOWN",
        }
        result.append(row)
        print("EXCERPT_ELIGIBILITY_SOURCE:", json.dumps({
            k: row[k] for k in ("filename", "source_id", "category", "role",
                               "peak_excerpt_original_offset_s", "eligible_windows_of_17",
                               "precommitted_train_offsets")
        }, sort_keys=True))
    summary = {
        "recordings": len(result),
        "training_recordings": 4,
        "new_evaluation_recordings": 15,
        "grid_windows_total": len(result) * 17,
        "grid_windows_valid_under_peak_rule": sum(x["eligible_windows_of_17"] for x in result),
        "invalid_precommitted_training_windows": [
            {"source_id": row["source_id"], "filename": row["filename"],
             "arm": window["arm"], "offset_s": window["offset_s"],
             "peak": window["peak"], "rms": window["rms"]}
            for row in result for window in row["precommitted_train_offsets"]
            if not window["valid_under_original_peak_rule"]],
        "this_is_not_an_event_presence_annotation": True,
    }
    report = {
        "research_id": "AUDITORY-EXCERPT-ELIGIBILITY-SENSE-01",
        "status": "EXPOSED_ENGINEERING_DEV_SENSOR_ONLY",
        "blocked_experiment": "AUDITORY-TRAIN-EXCERPT-DEV-04-v0.1",
        "frozen_contract_sha256": CONTRACT_SHA,
        "summary": summary,
        "source_windows": result,
        "nonclaims": [
            "An RMS/peak-eligible interval need not contain the stated dog/chainsaw event.",
            "An ineligible interval is low-amplitude, not proof of semantic absence.",
            "No training selection was changed, no rerolls were performed.",
            "Original training-excerpt DEV-04-v0.1 remains BLOCKED.",
        ],
    }
    (ROOT / "excerpt_eligibility_results.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("EXCERPT_ELIGIBILITY_SUMMARY:", json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
