"""Verify archived real-audio case JSON and CSV without relying on Python assertions.

Results JSON is produced ONLY after ten actual WAV clips were downloaded and validated.
No test-fixture or mocked-results fallback is permitted for research evaluation.
"""
import csv
import hashlib
import json
from pathlib import Path

ORIGINAL_JSON_SHA = "4ccc41912a9a0ba05790828a989b3efffe8874e873124b479fbc0e5da5c35d0c"
ORIGINAL_CSV_SHA = "c5f14b064d8f2d05ea71520c182cdf0fe8e14b4f1d836ec20b0de6b4345b27ad"


def require(condition, message):
    """Remain fail-closed when run with python -O / PYTHONOPTIMIZE."""
    if not condition:
        raise ValueError(message)


def main():
    jf = Path("results.json")
    cf = Path("receipts/real_case_decisions.csv")
    require(hashlib.sha256(jf.read_bytes()).hexdigest() == ORIGINAL_JSON_SHA,
            "Original result changed; create a versioned receipt instead of overwriting")
    require(hashlib.sha256(cf.read_bytes()).hexdigest() == ORIGINAL_CSV_SHA,
            "Case-ledger bytes do not match published source")
    data = json.loads(jf.read_text())
    with cf.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == len(data["rows"]) == 48,
            "Expected 48 identical result and receipt rows")
    for i, (saved, new) in enumerate(zip(rows, data["rows"])):
        require(int(saved["source_group"]) == new["source_group"], f"Row {i}: source group mismatch")
        require(saved["slots"] == ">".join(new["slot_sources"]), f"Row {i}: source slots mismatch")
        require(float(saved["gain"]) == new["gain"], f"Row {i}: gain mismatch")
        require(int(saved["truth"]) == int(new["planted_dog_then_chainsaw"]),
                f"Row {i}: planted truth mismatch")
        for method in ("energy", "zcr", "multiband"):
            require(int(saved[method + "_alert"]) == int(new["predictions"][method]["matched"]),
                    f"Row {i}: {method} alert mismatch")
            if method != "energy":
                require(saved[method + "_labels"] == ">".join(new["predictions"][method]["labels"]),
                        f"Row {i}: {method} labels mismatch")
    for method in ("energy", "zcr", "multiband"):
        counts = data["methods"][method]
        require(counts["true_A_then_B"] + counts["miss_A_then_B"] == 6,
                f"{method}: positive denominator mismatch")
        require(counts["false_A_then_B"] + counts["true_no_match"] == 42,
                f"{method}: negative denominator mismatch")
    print("VERIFIED_FULL_SOURCE_RESULT_HASH_AND_ALL_48_CASE_ROWS")


if __name__ == "__main__":
    main()
