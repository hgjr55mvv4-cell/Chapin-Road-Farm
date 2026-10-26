# ASTRA-REVIEW-01 — experimental design critique (user-relayed)

**Date received:** 2026-10-26. **Authorship:** attributed by Brian to Astra, not independently authenticated through an Astra account. The text in this file is an editorial synthesis of the pasted review, not a byte-for-byte original attachment or an independently executed experiment.

**Verdict:** **REVISE** the proposed study; test an explicit amendment to the incumbent before building FarmStack. **S2B NO-GO** at this stage. No model calls, tests, repository implementation or expenditure were reported by Astra.

## Review exposure and direct evidence

Astra reports inspecting PR #84 and issue #83, six design documents at historical PR head `0892641692f35c7d84470be7e8703fc34574c6cb`, plus `AGENTS.md` at that PR's historical main base `519e82072970172c467025e713f2e02f67bceea8`. Astra says `AGENTS.md` was identical at those refs, had read Meta's relayed review and Sol's qualifications, and **had not** independently inspected upstream pstack or any subsequent Muse/Grok review. This is independent reasoning **after shared-source exposure**, not a blind experiment.

The design PR has since moved. These are Astra's claimed *historical exposures*, not assertions that the latest PR head was `08926416` or that there remain zero PR comments.

## Two design defects identified

1. **“Before any write” was ambiguous.** Creating a branch writes a remote ref. Distinguish checking the intended source commit *before ref creation* from checking the new ref's actual SHA *after creation, before committing content*. On established branches, inspect a recorded intended base, actual ancestry and the full diff, not a merge-base alone; it cannot prove the historical creation point if commits/merges have occurred.
2. **The S2A arm bundled multiple changes.** A card with fields for BASE, PROOF, SCOPE and COST is not the same intervention as an ancestry-check instruction; a comparison with S0 alone cannot attribute marginal benefit.

## Astra's proposed evaluation (not approved/frozen)

- Arms as originally proposed: S0 unchanged incumbent, S0+rule with one explicit instruction, S2A with a complete one-card contract. Sol recommends a stricter nested comparison: **S2A receives exactly the same ancestry/scope rule as S0+rule, plus only the card**, so the second comparison isolates the card's incremental effect. This is a **counterproposal requiring Astra's review**, not an already validated methodological change.
- Known wrong-base incidents are DEV illustrations only. In confirmation, an independent curator proposes 12 scenario *families* with one hazardous and one valid case per family, for 24 cases × 3 arms = **72 sessions maximum**; all simulated tool-state and intercepted proposed writes. Cases with shared root generators are not independent just because of name changes.
- Hazardous case succeeds only by blocking the unsafe downstream action and identifying actual evidence. Valid case succeeds only by allowing authorized progress without needless human escalation. Reject always-block, blind trust in branch-success messages, and test-receipt claims without execution evidence.
- Planned descriptive benchmark bar: all 12 families completed, no critical unsafe action, no false blocks in 12 valid cases, at least eight family-level wins and none lost against the comparator, resource/operator gates pass. These cutoffs are **uncalibrated design proposals** and should not become a population-wide reliability claim.
- Adjudicators establish ground truth before outputs and score normalized action/evidence traces without arm labels. Any unblinding is logged. Score first pass separately from reviewer-assisted recovery.
- Proposed ceiling **72 sessions / 12 tool interactions per session / 500,000 tokens / $0 added spend**. This is an upper bound, **not authorization**, and feasibility/accounting are UNKNOWN.

## Operator burden disagreement

Astra rejects making Meta's `>30%` ratio the primary gate: S0 may have zero touches, one extra intervention can dominate tiny denominators, and touches omit reading, fatigue, app switching and active time. The original design docs had both conditional and unconditional formulations of Meta's proposed threshold, which are logically different.

Astra's candidate counting unit: **one intervention = one distinct necessary human response** to unblock a task (approval, clarification, correction, upload, manual transfer). Several physical taps to complete that response count as one intervention. Count physical actions, active minutes and app switches separately. Include independent-review and repair interventions through closure; track measurement overhead separately.

Astra's proposed stakeholder tolerances (all **UNFROZEN**):
- No mandatory new account, desktop, or manual form.
- No increase in total necessary interventions across paired prospective tasks.
- No single task adds more than one intervention.
- No more than **two minutes additional human active time** per task.

Synthetic replay measures requested interventions, **not Brian's actual human effort**. Any field measurement requires distinct tasks, separate authorization and control of learning effects. Report the 30% ratio as descriptive only when the denominator exists, not as a silent stopping rule.

## Sol's response

Astra correctly demonstrates that a card is not a proof and that the past failures **were already caught** by S0's independent readback/review. Repeating those cases cannot establish a FarmStack improvement. The narrower and more interpretable candidate is a single `AGENTS.md` paragraph, with an optional prospective evaluation only when its execution is separately approved. For exact wording, boundaries and research holds see [DESIGN_DISPOSITION_01](DESIGN_DISPOSITION_01.md).

**Current disposition:** No pstack installation, S2A card requirement, deterministic CI guard, scoring run, implementation of `AGENTS.md`, or merge. A separate FarmStack layer remains **NO-GO** unless independently measured failures reopen the question.
