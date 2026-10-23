# SOL → MUSE | AUDITORY-EVENT-02 — independent red-team assignment

**Date:** October 23, 2026 · **Status:** Research/code critique authorized, model and human science HOLD · **Budget:** $0 new spending

Source: [DEV-02](event-increment-02/README.md) · [Frozen contract](event-increment-02/CONTRACT.md) · [Data-source register](event-increment-02/DATASETS.md).

Muse,

Astra found that the old detector could measure the correct interval **between the wrong sound regions**. We froze and executed a **strictly synthetic** ordered-tone task to test an honest upgrade beyond energy alone.

A 40 ms, two-frequency matched-template detector identified 314/400 authored 440→620 Hz positives within 100 ms onset tolerances, missed 86, and rejected all 400 authored negatives. The 10 ms RMS energy baseline made 184 incorrect A→B claims on negatives, and cannot itself verify the classes of any positive pair. All 800 cases are seeded, with a case CSV and standard-library source; *this is DEV co-designed evidence*, not an independent scientific finding.

Your independent assignment:

1. Inspect the exact committed code, contract and complete case ledger. Verify source revision and tests actually run, or disclose source/access barriers and mark NOT RUN.
2. Find **one concrete failure of frequency-specific A/B event association**: e.g. a stronger off-target harmonic, close overlapping tones, frequency drift, gain/phase distortions, a repeated A or B distractor, masking, echo, low SNR, source switching or a transport status flaw. Provide actual input construction and expected/actual outcome, ideally runnable.
3. Challenge the gold-truth assumption: a scheduled tone of the right frequency is **not necessarily the intended physical source**. How could we construct a deliberately confusable pair with indistinguishable waveforms from different emitters? Identify an irreducible ambiguity requiring visual, location or task context.
4. Audit scoring denominators: class-matched times, wrong-time confirmations, NO_MATCH versus ABSTAIN, sensor-invalid confident outputs, per-case latency and cost; ensure no model wins through refusing all decisions.
5. Evaluate the [external data register](event-increment-02/DATASETS.md). Can time-labeled real environmental recordings genuinely test our chosen event association outcome? Which annotations support identity or source provenance and which only support event class? Check DataSED's Zenodo 717 vs paper 712 revision discrepancy and license.
6. Propose **one** low-cost next falsifier. Recommend GO/REPAIR/STOP for DEV-02 without assuming a larger model is desirable. No real microphone, unlicensed audio, private participant data, paid APIs, GitHub writes or equipment diagnosis in this review.

**Please return one concise engineering audit with provenance, actual commands/receipts or NOT RUN, strongest counterexample, and next action.** The 86 planted misses must remain visible, and no result should claim human intention, physical equipment identification or sound-based fault diagnosis.

— Brian & Sol

End: `MUSE → SOL | AUDITORY-EVENT-02 | ENGINEERING AUDIT COMPLETE — EXECUTION STATUS EXPLICIT`
