# LOOM-02A — synthetic choice-set / rarity test (DEV contract v0.1)

**Date:** 2026-10-23. **Status:** ENGINEERING DEV / publicly exposed; not prospective scientific confirmation.

## Question

Under a known independent generative grammar, can an exact structural-match rule distinguish a rare match from a routine coincidence **at a query-level search scope**? How does wrong-grammar calibration invalidate that result?

## Frozen within this engineering demonstration

- Each symbolic song contains **three independent phrase-template indices** in `0..7`, no audio, no durations, no motif alignment, no listener.
- Two families: **uniform** (all templates 1/8); **concentrated** (one template weight 0.7 and seven templates each 0.3/7).
- A null query samples one source and `m` *independent* candidate songs from the same true family; a planted query samples the source and independently draws `m-1` other candidates, placing an **exact source copy** at a randomly selected slot. Other chance collisions are not filtered.
- Evaluate `m=1` and `m=16`, `8,192` null queries and `8,192` planted queries for each scenario, fixed seed `20261023`. **Queries**, not 16 pairs within a query, are the experimental denominator.
- **Rule R0:** alert whenever any candidate exactly matches source.
- **Rule R1:** alert only if R0 and the **single-pair** probability of a random candidate equaling that source, `q(source)`, is ≤ 0.05.
- **Rule R2:** alert only if R0 and the **query-level** chance `1-(1-q(source))^m` is ≤ 0.05. It is a source-conditioned exact-match rarity flag, not a claim of shared ancestry.
- Compare (A) correctly specified known family and (B) wrongly calibrated **uniform** family applied to **concentrated** music. The calibrator is deliberately given **oracle** knowledge of the grammar; no estimation/learning occurred.
- Predefined `alpha=0.05` is an engineering illustration, chosen with knowledge of Astra's reported prior run, not an independent confirmatory threshold. Output also includes **exact analytical rates** over all 512 possible source sequences.
- All metrics show null-alert probability and planted detection probability separately. `0` detection is not a successful discriminator even if null alerts are 0.

## Data and separation

The null and planted streams are seeded separately and never filtered after observing scores. Analytical probabilities are calculated from the grammar, not from output labels. The two calibration models are knowingly correct or intentionally misspecified. **This demonstration is not blinded, independent, or representative of actual music.**

## Primary stopping interpretation

If the assumed grammar is wrong, or actual number of searched candidates is unknown, no fixed rarity guarantee is established. No population-level or human-musical-meaning conclusion follows from simulation. If grammar distribution cannot be estimated in a future legitimate study from an independent sample, do not promote the oracle-calibrated result as field-ready.
