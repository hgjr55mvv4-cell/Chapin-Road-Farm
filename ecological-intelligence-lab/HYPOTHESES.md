# Falsifiable hypotheses

**Status:** DESIGN ONLY. No hypothesis below has been tested. Each carries its falsifier; a falsified hypothesis is a result, not an embarrassment.

## H1 — Dependency representation improves decision utility

On synthetic socio-ecological vignettes with planted causal structure, an agent that explicitly represents dependencies before choosing an action achieves higher realized utility (under the ground-truth causal model) than a strong-simple baseline at equal compute.

- **Falsifier:** utility difference ≤ 0, or the win disappears when the baseline receives the same case facts in a different order (order effect, not representation effect).
- **Test:** EIL-DEV-01.

## H2 — Consequence simulation improves restraint calibration

Explicit second-order consequence enumeration reduces **both** harmful actions (acting when restraint was correct) **and** harmful omissions (restraining when action was correct), rather than trading one error for the other.

- **Falsifier:** total error rate unchanged, or one error type falls while the other rises by as much.
- **Test:** EIL-DEV-01 (primary), EIL-DEV-03 (restraint matrix).

## H3 — Collective adjudication beats strong single only at compute parity

Independent-parallel agents with adjudication beat a strong single agent on vignettes with planted shared misconceptions, when total compute (tokens) is held equal.

- **Falsifier:** no win at compute parity, or the group amplifies the planted misconception (group error rate ≥ best single-agent error rate).
- **Test:** EIL-DEV-02. Method by reference to the Agent Collaboration Lab protocol (COLLAB-REVIEW-DEV-01); EIL contributes only vignettes and misconception cases.

## H4 — Ecological language is not ecological understanding

Style-only variants of the same recommendation (ecological rhetoric added or removed, content unchanged) score differently on "ecologicalness" ratings but identically on decision utility.

- **Falsifier for language-as-understanding:** if style changes utility, the "style" manipulation leaked content and the test must be redesigned; if raters cannot distinguish style from content, the rating instrument is invalid and must be replaced before any language claim is made.
- **Test:** style controls inside EIL-DEV-01 and EIL-DEV-03. "Ecologicalness" ratings are a diagnostic, never an outcome metric.

## H5 — Calibration, not hedging

A candidate that states calibrated confidence (confidence predicting correctness, measured by Brier score) beats a baseline that hedges vaguely, and the gain comes from discrimination (confident when right, uncertain when wrong), not from blanket uncertainty statements.

- **Falsifier:** Brier score no better than baseline, or the gain vanishes when vague statements are scored as non-answers.
- **Test:** EIL-DEV-01 (secondary), EIL-DEV-03 (calibration by factorial cell).

## What is NOT hypothesized

- No claim that any model possesses ecological concern, subjective experience, or moral agency.
- No claim that collective intelligence generalizes beyond the tested vignette families.
- No claim about real-world ecological outcomes (EIL-04 is parked).
- No claim that "ecological intelligence" is a general factor, trait, or measurable kind — see `FOUNDING_QUESTIONS.md` for the rejection of the unitary construct and its retirement condition.
