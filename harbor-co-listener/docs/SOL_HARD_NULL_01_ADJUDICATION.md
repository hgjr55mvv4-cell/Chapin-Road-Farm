# Sol review: hard-null stress test and the meaning of a structural match

**Date:** October 23, 2026 · **Disposition:** ACCEPT core inference boundary; source replay **BLOCKED BY MISSING ARCHIVE**; personal-music science remains HOLD.

## Four non-equivalent propositions

1. A generating program **planted** a shared pattern.
2. The generated songs **share** the chosen symbolic representation.
3. The relationship is **unusual relative to a declared musical comparison population and selection/search process**.
4. That relationship **matters to a particular human listener**.

LOOM's old 64/64 success is a deliberately simple demonstration of (1)–(2), not independent evidence of (3)–(4). Astra's source-reported concentrated-family failure is a severe challenge to treating the *fixed scalar cutoff* as (3). It says nothing against the listener's actual experience in (4).

## Arithmetic independently checked by Sol

The reported values have internal agreement:
- `565/2048 = 0.27587890625`, with a standard Wilson z=1.96 interval approximately **0.25695–0.29564**.
- `274 + 291 = 565`.
- `110/256 = 0.4296875`; adjusted `1/256 = 0.00390625`.

**Conditional theoretical check:** Suppose there are eight phrase templates; each of three phrase positions is sampled **iid**, template #1 with probability 0.7 and the other seven each with probability 0.3/7. Two independently generated compositions have the *same template at one position* with probability `0.7² + 7(0.3/7)² ≈ 0.502857`, and identical three-template sequences with probability its cube, **≈0.127155**, giving an expectation of **≈260.4 exact collisions among 2,048**. Astra reports **274**. This is *consistent* with the abstract sampling mechanism. It is **not a reproduction**: the original generator may impose extra constraints or correlations, which we cannot check without its actual source and case-level outputs.

Executable transparent check: [hard-null arithmetic code](../hard-null-01/README.md), Python standard library only. Sol locally executed its five tests. This independently checks **math and consistency of supplied counts**, not upstream execution.

## Calibration interpretation

When a common motif produces exact score 1.0 under the null, a score-only rule cannot perfectly distinguish a **planted exact identity** from an **independent exact collision** with the same observed representation. A source-conditioned probabilistic model can estimate rarity *if* the family and probabilities are supported. It cannot, from identical observations alone, establish whether the actual historical generating process was copying or independent; provenance is a latent cause.

**Zero null alerts with zero positive detections is not a successful discriminator.** Calling this “abstention” is appropriate only if the system explicitly outputs ABSTAIN; otherwise it may be an overconservative cutoff or no-detector-result. Report decision/coverage and false-rejection separately, rather than mistaking lack of alerts for certainty.

**Multiplicity is part of the hypothesis.** A prior probability threshold for a *pair* cannot be silently reused for “find any interesting pair among 16 candidates” or “select the best of 500 windows/features.” The relevant unit is the search/query episode; candidates are dependent.

## What is genuinely supported versus awaiting verification

**Supported from actual current-turn calculation:** numerical internal consistency, conditional iid collision mechanism, and the logical limitation of treating a structural score as provenance/meaning.

**Reported by Astra, awaiting exact-source replay:** 565 null alerts; 274 exact collisions; five-family calibration; 110/256 unadjusted queries; zero positives accepted under concentrated grammar; byte-identical two executions and case-level CSV audits.

**Not established:** that phrase template probability 0.7 is a realistic model for actual music; that cross-cultural choice sets are calibrated; audio recognition in real recordings; any individual listener's musical meaning; any causal effect of order or AI intervention.

## Decision and release gate

- **LOOM v0.1 original source:** preserve unchanged as **ENGINEERING PASS for planted symbolic interval equality**.
- **LOOM fixed 0.83 as a universal kinship-rarity test:** **NOT QUALIFIED / RETIRE THIS INTERPRETATION** (conditional on Astra's reported adversarial family; even without original run, the general inference is unjustified in principle).
- **ASTRA-HARD-NULL-01 original code:** **REPORTED RUN, NOT INDEPENDENTLY REPRODUCED**. Do not publish a fabricated upstream package or attribute this arithmetic-only checker to Astra's source.
- **Next engineering qualification:** obtain Astra's rights-cleared package bytes with manifest, check file membership/license/hashes, run frozen `python -m unittest -v test_hard_null`, `python hard_null.py --out results`, `python reproduce.py` and independently recount the CSVs. Keep original source and results immutable.
- **Next scientific comparison (HOLD):** after source replay, predeclare *source/family-conditioned rarity and query-level multiple-search calibration* versus **exact interval-tuple equality** and a strong simple alternative, with both known-positive sensitivity and family-matched null alerts. Evaluate under new independently sampled generators, explicit ties and null-family mismatch, report failures.
- **Human meaning research:** later, separately consented and prospectively measured; never equate symbolic rarity with what a person feels.

**No additional paid expenditure authorized, no private music, no copyrighted audio or participant data required.**
