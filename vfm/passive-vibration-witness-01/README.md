# VFM-PASSIVE-VIBRATION-WITNESS-01
**Chapin Road Farm · VFM Field Mechanic · 2026-10-23**

**Status:** Simulation engineering preflight passed; physical build **NOT RUN**; fault diagnosis **NOT QUALIFIED**; field installation **HOLD**. Additional expenditure **$0**.

## Why
Test whether a battery-free mechanically frequency-biased witness might remember intermittent vibration as a visual event. An indicator cannot identify the failure that caused the motion. Any colored fluid in a future prototype belongs in a separately sealed indicator, **never in engine, hydraulic, transmission, fuel, coolant or other machine fluids**.

## Deliverables
- `sim.py`: stdlib Python synthetic base-excited single-degree-of-freedom resonator; impact, tuned peak and *hypothetical mechanical* 12-turning-point dwell arms.
- `test_sim.py`: 16 deterministic engineering checks, including two deliberately reproduced false-positive cases.
- `FROZEN_CONTRACT.md`: versioned parameters and selection rule committed before choosing synthetic confirmation fixtures.
- `confirm.py`: seeded 80-case internal simulation check. Running it creates `confirm_results.json`.
- `RESULTS.md`: complete 5-class metrics and failure analysis.
- `BENCH_PLAN.md`: physical falsification prerequisites and safety requirements.

## Reproduce
```sh
cd vfm/passive-vibration-witness-01
python sim.py
python -m unittest -v
python confirm.py
```

No dependencies outside Python 3.9+ standard library. A separate self-contained interactive iPad-friendly HTML simulator is delivered as part of the chat development package.

## Physical model
For mount acceleration `a(t)` the relative spring/mass displacement is `x'' + 2*zeta*omega0*x' + omega0^2*x = -a(t)`. Chosen illustrative design: resonance 90 Hz; damping ratio 0.055; displacement trip 0.15 mm; hypothetical dwell 12 consecutive above-threshold turning points; plain shock baseline 0.70g. **No real tractor/bearing frequency or acceleration is claimed.**

## Key limits
A normal machine operating with the same waveform activates the same witness. Large off-band vibrations can also trip it. The modeled dwell counter has **not been implemented as a no-power mechanical ratchet**. A simulation does not show a sticker exists. Avoid all actual machinery installations until independent guarded bench evidence, retention, temperature, orientation, mounting and adhesion testing. Never treat clear as safe-to-operate.

## Sources
- [SpotSee ShockWatch Label mechanics](https://spotsee.io/shockwatch-faqs/) — commercial passive liquid impact threshold, not narrow-band vibration.
- [ShockWatch 2](https://helpcenter.spotsee.io/knowledge/shockwatch-2-product-overview) — another single-use mechanical impact indicator; do not assume identical fluid design.
- [Chen et al. 2020 piezo-electrochromic visual vibration memory](https://doi.org/10.1016/j.jmat.2020.06.002) — experimental research, not qualified farm product.
- [Samimy & Rizzoni 1996 engine knock time-frequency variability](https://saemobilus.sae.org/papers/engine-knock-analysis-detection-using-time-frequency-analysis-960618).

**Provenance:** GPT-6 created and ran a local simulation. No independent audit, field recording, hardware inspection or material test took place. No reusable research policy promoted.