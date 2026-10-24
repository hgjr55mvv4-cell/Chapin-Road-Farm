#!/usr/bin/env python3
"""Public synthetic boundary-sensitivity probe; not speech or perception research."""
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
    TONES, decide, gap_band, observe, render,
)

BASELINE_SHA256 = "ec824b080e73209c05053bed259c1105c93d9c1d009f88a5272fdb9dea41c021"
PROGRAMMED_GAP_S = 0.48
TAIL_S = 0.08
FACTORS = (1.0, 0.5, 0.3, 0.1, 0.0)
TEXT = "Synthetic timing example; no spoken language."


def render_with_tail_factor(factor: float) -> bytes:
    """Match audio_dev.render except for the first tone's final 80 ms."""
    second_start = FIRST[1] + PROGRAMMED_GAP_S
    spans = ((FIRST[0], FIRST[1], TONES[0]),
             (second_start, second_start + 0.42, TONES[1]))
    rng = random.Random(42)
    pcm = bytearray()
    for i in range(int((second_start + 0.62) * SAMPLE_RATE)):
        t = i / SAMPLE_RATE
        sample = rng.uniform(-0.008, 0.008)
        for start, stop, frequency in spans:
            if start <= t < stop:
                scale = factor if frequency == TONES[0] and t >= FIRST[1] - TAIL_S else 1.0
                sample += AMPLITUDE * scale * math.sin(2 * math.pi * frequency * (t - start))
        pcm += struct.pack("<h", round(max(-1.0, min(1.0, sample)) * 32767))
    out = io.BytesIO()
    with wave.open(out, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm)
    return out.getvalue()


def tail_frame_rms(wav_bytes: bytes) -> list[float]:
    with wave.open(io.BytesIO(wav_bytes), "rb") as wav:
        samples = struct.unpack("<" + str(wav.getnframes()) + "h",
                                wav.readframes(wav.getnframes()))
    first = round((FIRST[1] - TAIL_S) * SAMPLE_RATE / FRAME_SAMPLES)
    last = round(FIRST[1] * SAMPLE_RATE / FRAME_SAMPLES)
    return [
        math.sqrt(sum((s / 32767.0) ** 2 for s in samples[k * FRAME_SAMPLES:(k + 1) * FRAME_SAMPLES])
                  / FRAME_SAMPLES)
        for k in range(first, last)
    ]


def evaluate() -> dict:
    actual_sha = hashlib.sha256((BASELINE / "audio_dev.py").read_bytes()).hexdigest()
    cases = []
    for factor in FACTORS:
        wav_bytes = render_with_tail_factor(factor)
        observation = observe(wav_bytes)
        measured_action = decide(text=TEXT, gap_s=observation.gap_s,
                                 sensor_status=observation.sensor_status)
        rms = tail_frame_rms(wav_bytes)
        cases.append({
            "tail_amplitude_factor": factor,
            "sensor_status": observation.sensor_status,
            "energy_intervals_s": [list(interval) for interval in observation.active_intervals_s],
            "energy_gap_s": observation.gap_s,
            "energy_minus_programmed_gap_s": (round(observation.gap_s - PROGRAMMED_GAP_S, 3)
                                              if observation.gap_s is not None else None),
            "energy_gap_band": gap_band(observation.gap_s),
            "illustrative_energy_action": measured_action,
            "action_differs_from_programmed_gap": measured_action != decide(
                text=TEXT, gap_s=PROGRAMMED_GAP_S),
            "attenuated_tail_rms_min": round(min(rms), 6),
            "attenuated_tail_rms_max": round(max(rms), 6),
        })
    return {
        "research_id": "AUDITORY-BOUNDARY-DEV-01",
        "status": "EXPOSED_ENGINEERING_DEV",
        "baseline_audio_dev_sha256": actual_sha,
        "baseline_control_wav_identical": render_with_tail_factor(1.0) == render(PROGRAMMED_GAP_S),
        "programmed_first_tone_end_s": FIRST[1],
        "programmed_second_tone_start_s": round(FIRST[1] + PROGRAMMED_GAP_S, 3),
        "programmed_gap_s": PROGRAMMED_GAP_S,
        "modified_tail_start_s": round(FIRST[1] - TAIL_S, 3),
        "energy_threshold_rms": SILENCE_RMS_MAX,
        "frame_duration_ms": FRAME_SAMPLES * 1000 // SAMPLE_RATE,
        "illustrative_programmed_gap_action": decide(text=TEXT, gap_s=PROGRAMMED_GAP_S),
        "perceptual_event_boundary": "NOT MEASURED",
        "cases": cases,
        "nonclaims": [
            "Generated pure tones, not speech, field audio, or a listening participant.",
            "Programmed synthesizer boundaries are not perceptual ground truth.",
            "The detector measures an RMS-threshold boundary, not a physical event identity.",
            "The illustrative routing action is not a validated human turn-taking policy.",
            "This exposed development counterexample is not independent scientific confirmation.",
        ],
    }


def check(report: dict, generated: bytes) -> None:
    """Explicit validation, including when Python is run with -O."""
    def require(condition: bool, reason: str) -> None:
        if not condition:
            raise RuntimeError(reason)

    require(report["baseline_audio_dev_sha256"] == BASELINE_SHA256,
            "Original detector changed")
    require(report["baseline_control_wav_identical"],
            "Control no longer matches original generator")
    expected = (
        (0.48, "WAIT", False),
        (0.48, "WAIT", False),
        (0.48, "WAIT", False),
        (0.56, "READY_NOT_OBLIGATED_TO_REPLY", True),
        (0.56, "READY_NOT_OBLIGATED_TO_REPLY", True),
    )
    require(len(report["cases"]) == len(expected), "Unexpected case count")
    for case, (gap, action, differs) in zip(report["cases"], expected):
        require(case["sensor_status"] == "OK", str(case))
        require(case["energy_gap_s"] == gap, str(case))
        require(case["illustrative_energy_action"] == action, str(case))
        require(case["action_differs_from_programmed_gap"] is differs, str(case))
    require(report["cases"][3]["attenuated_tail_rms_max"] < SILENCE_RMS_MAX,
            "Attenuated tail no longer falls below threshold")
    expected_receipt = (HERE / "receipts" / "observed.json").read_bytes()
    require(expected_receipt == generated, "Generated JSON differs from committed receipt")

def main() -> int:
    report = evaluate()
    output = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if "--check" in sys.argv[1:]:
        check(report, output)
        print("PASS: unchanged detector, five paired synthetic cases, receipt byte match", file=sys.stderr)
    elif sys.argv[1:]:
        raise SystemExit("Usage: python3 verify.py [--check]")
    sys.stdout.buffer.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
