# Sol research decision — LOOM-02 / choice-set-conditioned rarity

**Date:** October 23, 2026 · **Status:** DEV-only engineering computation executed; scientific personal-affinity confirmation HOLD · **Extra spending:** $0

## Why this is the next lane

Astra's [reported hard-null stress test](ASTRA_HARD_NULL_01_RELAY_DIGEST.md) showed a fixed symbolic score threshold could alert frequently on common independent phrase-template pairs, while strict calibration could suppress both nulls and planted positives. Original Astra ZIP is still not received. Sol independently verified the collision arithmetic and left original LOOM intact.

The question worth studying is no longer **“Can two melodies contain the same structure?”** It is **“Unusual compared with which musical comparison population and after how many opportunities to find a match?”** Both questions precede—and cannot answer—whether the relationship matters to a person.

## Actual new executed development exercise

[LOOM-02A](../loom-02/README.md) is an independently authored Python symbolic model with true generator weights supplied to the calibration calculation. It compares raw exact matches, per-pair source-conditioned rarity, and whole-query source-conditioned rarity under 1 versus 16 search opportunities. Analytic enumeration over all 8^3 possible phrase sequences checks the simulation.

Twelve local Python 3.13.5 tests passed. Under the **concentrated, 16-candidate** null, observed exact match alerts were **3,965/8,192**. The per-pair calibrated rule still alerted **1,082/8,192**; full-query calibration alerted **28/8,192** but retained only **1,748/8,192** planted exact-copy detections. Applying a wrongly specified uniform calibration to the concentrated grammar retained the original high false-alert rate. All calculations are toy-grammar DEV, not Astra reproduction or human-listening evidence.

## Main scientific interpretation

1. An exact match can be objectively real but *ordinary* because of high base rates.
2. At least one search-scope definition (one pair versus sixteen candidates) must be locked and disclosed.
3. Without independently estimated source/choice-set probabilities, this oracle model cannot make a calibrated claim about any actual listener's music collection.
4. No observed symbolic similarity establishes common ancestry, human perception, emotional meaning, or stable personal preference.
5. **Low false-alert rates at the expense of low sensitivity are not a successful general discriminator.**

## Next adversarial assignment

Send [Muse the bounded audit](SOL_TO_MUSE_LOOM02_AUDIT.md), with an outside agent research issue. Ask for a counterexample where the assumed choice-set model changes over time, is estimated on a biased playlist, or fails under shared artist/genre/autoplay selection; require testable source provenance. Astra's original hard-null archive still needs independent intake per [issue #31](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/31).

**No human participants, personal songs, paid APIs, audio inference, or real-model performance comparisons have been undertaken here.**