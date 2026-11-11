# DEV design freeze PVW-01 v0.1 — 2026-10-23
**Stage:** synthetic software engineering only. **Frozen `sim.py` SHA-256:** `e17a6812c02badf41efcc6afe2401ab929a09fd0c5137ceb2fd960898f474062`. **Budget:** $0. Any material change to this source/parameters creates a new version and new cases.

### Candidate vs incumbent
- Baseline `plain_impact`: instantaneous |base acceleration| >=0.70g.
- Simpler comparator `tuned_peak`: relative resonator displacement >=0.15mm.
- Challenger `tuned_dwell`: 12 sequential above-threshold turning points, for a proposed single-use visible witness. **The repeated-cycle latch is hypothetical**; no physical passive accumulator has been made.
- 90 Hz resonance, 0.055 damping, 8000 Hz discrete integration; all illustrative, not measured.

### Trigger, action, scope, success
Trigger: sustained tuned-band base vibration on a single axis. Action: theoretical one-bit irreversible flag. Scope: event exposure only, not condition, fault identity or clearance to operate.

Fixed confirmation case selection rule before seed selection: generate 16 samples in each of five classes—(1) on-band 89–91Hz, .8–1.0g, .30–.50s; (2) off-band 43–47Hz or 148–152Hz, .60–1.0g; (3) impacts 5–12g, 2ms; (4) overload 43–47Hz, 3.5–5g; (5) healthy matched inputs from class (1), with different labels. Use one post-freeze seeded batch without re-tuning. Same input must always yield same response regardless of human fault label.

DEV vibration witness pass gate: at least 15/16 sustained on-band triggers, at most 1/16 ordinary off-band, at most 1/16 impact, better impact rejection than tuned-peak with equal on-band sensitivity. Report overload and matched healthy errors explicitly. **Absolute fault diagnosis safety floor: UNKNOWN/NOT QUALIFIED** regardless of passing software gates.

Falsifiers: healthy normal vibration in same band, high-amplitude off-band events, frequency drift with RPM, mounting variation, thermal stress, persistent memory failure, short impacts, no viable cheap mechanical repeat-cycle latch. Bench/field qualification **HOLD**. Cost ceiling no paid API or purchases; persistent complexity must later compete with simple peak latch.

This is not an Ω-ARENA promotion of any reusable procedural policy. Synthetic results cannot validate real mechanical performance.