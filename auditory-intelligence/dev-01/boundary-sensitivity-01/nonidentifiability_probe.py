#!/usr/bin/env python3
"""Non-identifiability probe for AUDITORY-DEV-01; synthetic engineering only.

Pairs one physical interpretation (a first tone continues 80 ms below the
fixed RMS threshold) with another (the first tone truly ends 80 ms earlier).
Both can produce the same measured intervals, gap, band, and illustrative action.
This is not speech, perception, or turn-taking research.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
from pathlib import Path
import random
import struct
import sys
import wave

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASELINE))
from audio_dev import (  # noqa: E402
    AMPLITUDE, FIRST, FRAME_SAMPLES, SAMPLE_RATE, SILENCE_RMS_MAX,
    TONES, decide, gap_band, observe,
)

BASELINE_SHA256 = "ec824b080e73209c05053bed259c1105c93d9c1d009f88a5272fdb9dea41c021"
SECOND_START_S = 1.10
SECOND_DURATION_S = 0.42
DURATION_S = SECOND_START_S + 0.62
TAIL_START_S = 0.54
TEXT = "Synthetic timing example; no spoken language."


def synth(first_end_s: float, tail_factor: float = 1.0) -> bytes:
    """Generate like the public boundary probe, but allow the first end to move."""
    spans = ((FIRST[0], first_end_s, TONES[0]),
             (SECOND_START_S, SECOND_START_S + SECOND_DURATION_S, TONES[1]))
    rng = random.Random(42)
    pcm = bytearray()
    for i in range(int(DURATION_S * SAMPLE_RATE)):
        t = i / SAMPLE_RATE
        sample = rng.uniform(-0.008, 0.008)
        for start, stop, frequency in spans:
            if start <= t < stop:
                scale = tail_factor if frequency == TONES[0] and t >= TAIL_START_S else 1.0
                sample += AMPLITUDE * scale * math.sin(2 * math.pi * frequency * (t - start))
        pcm += struct.pack("<h", round(max(-1.0, min(1.0, sample)) * 32767))
    out = io.BytesIO()
    with wave.open(out, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm)
    return out.getvalue()


def tail_region_rms(wav_bytes: bytes) -> list[float]:
    with wave.open(io.BytesIO(wav_bytes), "rb") as wav:
        samples = struct.unpack("<" + str(wav.getnframes()) + "h",
                                wav.readframes(wav.getnframes()))
    first = round(TAIL_START_S * SAMPLE_RATE / FRAME_SAMPLES)
    last = round(FIRST[1] * SAMPLE_RATE / FRAME_SAMPLES)
    return [
        math.sqrt(sum((s / 32767.0) ** 2 for s in samples[k * FRAME_SAMPLES:(k + 1) * FRAME_SAMPLES])
                  / FRAME_SAMPLES)
        for k in range(first, last)
    ]


def case(name: str, first_end_s: float, tail_factor: float) -> dict:
    wav_bytes = synth(first_end_s, tail_factor)
    observation = observe(wav_bytes)
    programmed_gap_s = round(SECOND_START_S - first_end_s, 3)
    programmed_action = decide(text=TEXT, gap_s=programmed_gap_s)
    measured_action = decide(text=TEXT, gap_s=observation.gap_s,
                             sensor_status=observation.sensor_status)
    rms = tail_region_rms(wav_bytes)
    return {
        "case": name,
        "first_tone_programmed_end_s": first_end_s,
        "second_tone_programmed_start_s": SECOND_START_S,
        "programmed_gap_s": programmed_gap_s,
        "tail_amplitude_factor_after_0_54_s": tail_factor if first_end_s > TAIL_START_S else None,
        "wav_sha256": hashlib.sha256(wav_bytes).hexdigest(),
        "sensor_status": observation.sensor_status,
        "energy_intervals_s": [list(interval) for interval in observation.active_intervals_s],
        "energy_gap_s": observation.gap_s,
        "energy_gap_band": gap_band(observation.gap_s),
        "tail_region_0_54_to_0_62_rms_min": round(min(rms), 6),
        "tail_region_0_54_to_0_62_rms_max": round(max(rms), 6),
        "illustrative_programmed_gap_action": programmed_action,
        "illustrative_energy_action": measured_action,
        "action_differs_from_programmed_gap": measured_action != programmed_action,
    }


def evaluate() -> dict:
    actual_sha = hashlib.sha256((BASELINE / "audio_dev.py").read_bytes()).hexdigest()
    cases = [
        case("attenuated_tail_programmed_gap_0.48", FIRST[1], 0.1),
        case("true_short_boundary_programmed_gap_0.56", TAIL_START_S, 1.0),
    ]
    same_observation = (
        cases[0]["sensor_status"] == cases[1]["sensor_status"] and
        cases[0]["energy_intervals_s"] == cases[1]["energy_intervals_s"] and
        cases[0]["energy_gap_s"] == cases[1]["energy_gap_s"] and
        cases[0]["energy_gap_band"] == cases[1]["energy_gap_band"] and
        cases[0]["illustrative_energy_action"] == cases[1]["illustrative_energy_action"]
    )
    return {
        "research_id": "AUDITORY-BOUNDARY-NONIDENTIFIABILITY-DEV-01",
        "status": "EXPOSED_ENGINEERING_DEV",
        "claim_challenged": "One measured energy gap/action is sufficient to infer the programmed physical boundary.",
        "baseline_audio_dev_sha256": actual_sha,
        "energy_threshold_rms": SILENCE_RMS_MAX,
        "frame_duration_ms": FRAME_SAMPLES * 1000 // SAMPLE_RATE,
        "same_energy_observation": same_observation,
        "same_illustrative_energy_action": cases[0]["illustrative_energy_action"] == cases[1]["illustrative_energy_action"],
        "wav_bytes_identical_between_cases": cases[0]["wav_sha256"] == cases[1]["wav_sha256"],
        "cases": cases,
        "interpretation": (
            "The same detector output is consistent with at least two programmed physical histories: "
            "a 0.48 s programmed gap whose first tone continues below threshold until 0.62 s, and a true "
            "first-tone end at 0.54 s with a 0.56 s programmed gap. The fixed RMS threshold collapses these "
            "distinct signals into the same measured boundary and downstream illustrative action. Human perception "
            "was not measured."
        ),
        "nonclaims": [
            "Generated pure tones, not speech, field audio, or a listening participant.",
            "Programmed synthesizer boundaries are not perceptual ground truth.",
            "The detector measures an RMS-threshold boundary, not a unique physical event identity.",
            "The illustrative routing action is not a validated human turn-taking policy.",
            "This exposed development counterexample is not independent scientific confirmation.",
        ],
    }


def check(report: dict, generated: bytes) -> None:
    def require(condition: bool, reason: str) -> None:
        if not condition:
            raise RuntimeError(reason)

    require(report["baseline_audio_dev_sha256"] == BASELINE_SHA256,
            "Original detector changed")
    require(len(report["cases"]) == 2, "Expected exactly two paired cases")
    require(report["same_energy_observation"] is True,
            "Paired cases no longer share the same energy observation")
    require(report["same_illustrative_energy_action"] is True,
            "Paired cases no longer share the same illustrative action")
    require(report["wav_bytes_identical_between_cases"] is False,
            "Nonzero attenuated-tail case unexpectedly matches the true short-boundary bytes")
    for row in report["cases"]:
        require(row["sensor_status"] == "OK", str(row))
        require(row["energy_gap_s"] == 0.56, str(row))
        require(row["energy_gap_band"] == "LONG", str(row))
        require(row["illustrative_energy_action"] == "READY_NOT_OBLIGATED_TO_REPLY", str(row))
        require(row["tail_region_0_54_to_0_62_rms_max"] < SILENCE_RMS_MAX, str(row))
    require(report["cases"][0]["action_differs_from_programmed_gap"] is True,
            "Attenuated-tail case should flip the programmed-gap action")
    require(report["cases"][1]["action_differs_from_programmed_gap"] is False,
            "True short-boundary control should match its programmed-gap action")
    expected_receipt = (HERE / "receipts" / "nonidentifiability_observed.json").read_bytes()
    require(expected_receipt == generated, "Generated JSON differs from committed receipt")


def main() -> int:
    report = evaluate()
    output = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if "--check" in sys.argv[1:]:
        check(report, output)
        print("PASS: same measured boundary/action from two programmed physical histories", file=sys.stderr)
    elif sys.argv[1:]:
        raise SystemExit("Usage: python3 nonidentifiability_probe.py [--check]")
    sys.stdout.buffer.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
