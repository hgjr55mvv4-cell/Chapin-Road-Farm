#!/usr/bin/env python3
"""Passive Vibration Witness -- deterministic, synthetic proof of concept.

This is a phenomenological base-excited single-degree-of-freedom resonator.
Threshold and run-length counters are ABSTRACT detectors, not a qualified latch.
No real engine, noise recording, adhesive, material, or spring has been tested.
Standard library only. Python 3.9+.
"""
from dataclasses import dataclass, asdict
from typing import Optional
import math
import json
import argparse

G = 9.80665

@dataclass(frozen=True)
class Design:
    natural_hz: float = 90.0
    damping_ratio: float = 0.055
    trip_mm: float = 0.15
    extrema_required: int = 12
    shock_threshold_g: float = 0.70
    fs_hz: int = 8000

@dataclass(frozen=True)
class Event:
    label: str
    kind: str
    frequency_hz: float = 90.0
    amplitude_g: float = 0.6
    duration_s: float = 0.4
    onset_s: float = 0.15
    total_s: float = 0.70
    impulse_width_s: float = 0.002
    background_hz: float = 0.0
    background_g: float = 0.0


def acceleration(t: float, event: Event) -> float:
    a = 0.0
    if event.background_hz > 0:
        a += event.background_g * G * math.sin(2 * math.pi * event.background_hz * t)
    if event.onset_s <= t < event.onset_s + event.duration_s:
        elapsed = t - event.onset_s
        if event.kind == 'sine':
            a += event.amplitude_g * G * math.sin(2 * math.pi * event.frequency_hz * elapsed)
        elif event.kind == 'impulse':
            if elapsed < event.impulse_width_s:
                a += event.amplitude_g * G * math.sin(math.pi * elapsed / event.impulse_width_s)
        elif event.kind == 'chirp':
            # linear sweep from frequency_hz to 1.65 * frequency_hz
            rate = event.frequency_hz * 0.65 / event.duration_s
            phase = 2 * math.pi * (event.frequency_hz * elapsed + 0.5 * rate * elapsed * elapsed)
            a += event.amplitude_g * G * math.sin(phase)
        elif event.kind == 'none':
            pass
        else:
            raise ValueError(event.kind)
    return a


def run(event: Event, design: Design = Design(), collect_trace=False) -> dict:
    if design.natural_hz <= 0 or not 0 < design.damping_ratio < 1 or design.fs_hz < design.natural_hz * 25 or design.extrema_required < 1:
        raise ValueError('Invalid resonator design / undersampled simulation')
    dt = 1 / design.fs_hz
    omega = 2 * math.pi * design.natural_hz
    x = v = old_v = 0.0
    peak_disp = peak_acc = 0.0
    plain_tripped = tuned_tripped = dwell_tripped = False
    tuned_trigger_time = dwell_trigger_time = None
    streak = 0
    strongest_streak = 0
    trace = []
    n = int(event.total_s * design.fs_hz)
    for i in range(n):
        t = i * dt
        a = acceleration(t, event)
        peak_acc = max(peak_acc, abs(a) / G)
        if abs(a) >= design.shock_threshold_g * G:
            plain_tripped = True
        # Semi-implicit Euler for base-excited 2nd order damped resonator
        old_v = v
        v += dt * (-2 * design.damping_ratio * omega * v - omega * omega * x - a)
        x += dt * v
        peak_disp = max(peak_disp, abs(x))
        if abs(x) >= design.trip_mm / 1000:
            if not tuned_tripped:
                tuned_trigger_time = t
            tuned_tripped = True
        # Approximate alternating turning-point latch requirements; not physical ratchet evidence.
        if (old_v > 0 and v <= 0) or (old_v < 0 and v >= 0):
            if abs(x) >= design.trip_mm / 1000:
                streak += 1
            else:
                streak = 0
            strongest_streak = max(strongest_streak, streak)
            if streak >= design.extrema_required and not dwell_tripped:
                dwell_tripped = True
                dwell_trigger_time = t
        if collect_trace and i % 8 == 0:
            trace.append((round(t,5), round(a / G,5), round(x * 1000,5)))
    return {'event': event.label, 'event_kind': event.kind, 'plain_impact': plain_tripped,
            'tuned_peak': tuned_tripped, 'tuned_dwell': dwell_tripped,
            'peak_input_g': round(peak_acc, 5), 'peak_displacement_mm': round(peak_disp * 1000, 5),
            'max_consecutive_extrema': strongest_streak,
            'peak_trigger_s': None if tuned_trigger_time is None else round(tuned_trigger_time,5),
            'dwell_trigger_s': None if dwell_trigger_time is None else round(dwell_trigger_time,5),
            **({'trace': trace} if collect_trace else {})}


def cases():
    # All entirely synthetic, selected for engineering exploration, NOT confirmatory field evidence.
    return [
        Event('quiet_90hz_0.1g', 'sine', amplitude_g=0.1),
        Event('target_90hz_0.6g', 'sine', amplitude_g=0.6),
        Event('target_90hz_0.9g', 'sine', amplitude_g=0.9),
        Event('offband_45hz_0.6g', 'sine', frequency_hz=45, amplitude_g=0.6),
        Event('offband_150hz_0.6g', 'sine', frequency_hz=150, amplitude_g=0.6),
        Event('normal_onband_90hz_0.6g', 'sine', amplitude_g=0.6),
        Event('target_short_90hz_0.6g', 'sine', amplitude_g=0.6, duration_s=0.015),
        Event('broad_impact_5g', 'impulse', amplitude_g=5, duration_s=0.002),
        Event('broad_impact_10g', 'impulse', amplitude_g=10, duration_s=0.002),
        Event('sweep_60hz_up', 'chirp', frequency_hz=60, amplitude_g=0.6, duration_s=0.4),
        Event('mixed_90hz_target_on_40hz', 'sine', frequency_hz=90, amplitude_g=0.6,
              background_hz=40, background_g=0.3),
        Event('offband_high_amplitude_45hz_3g', 'sine', frequency_hz=45, amplitude_g=3),
        Event('offband_overload_45hz_4g', 'sine', frequency_hz=45, amplitude_g=4),
        Event('no_signal', 'none', amplitude_g=0),
    ]


def main():
    p=argparse.ArgumentParser(description='Software-only passive resonant witness simulator')
    p.add_argument('--json', default=None, help='Save deterministic example outputs as JSON')
    p.add_argument('--trace', action='store_true', help='Include decimated traces (large output)')
    args=p.parse_args()
    output={'status':'SIMULATION_ONLY_NOT_PHYSICALLY_VALIDATED', 'design': asdict(Design()),
            'results': [run(case, collect_trace=args.trace) for case in cases()]}
    payload=json.dumps(output,indent=2)
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f: f.write(payload+'\n')
    else:
        print(payload)

if __name__ == '__main__':
    main()
