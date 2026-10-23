# COLLAB-REVIEW-DEV-01 v0.1 — proposed experimental protocol

**Status:** DESIGN / NOT RUN / NOT FROZEN FOR SCIENTIFIC CONFIRMATION. **Budget:** $0 additional paid inference. Human copy/paste actions, time, tool use, and context cost count even when dollar charges are zero.

## Research question

Does independent second-model review **before implementation** produce fewer serious, independently adjudicated defects and greater usable completion than a **strong single-agent** process or **post-implementation** review at comparable evidence access and total cost?

The earlier [STOP audit](case-studies/HARNESS_STOP_AUDIT.md) motivates the question but is **exposed DEV evidence**, not an independent test case.

## Three challengers

| Arm | Method | Essential fair comparison |
|---|---|---|
| A: STRONG SINGLE | One capable model with complete requirements, readback, strong adversarial checklist, coding and a real test oracle | Not an intentionally weakened no-review baseline; equivalent budget and access |
| B: SPLIT PRE | Designer freezes requirements; separately briefed reviewer challenges before coding; implementation follows | Independence disclosure, capped rework and shared runtime budget |
| C: SPLIT POST | Designer implements first; second reviewer audits, then bounded repair | Same tasks, total budget, stopping rule and adjudicator |

## Pre-execution controls

1. Sample *future* tasks from a fixed eligibility population and stratify by difficulty. Do not reuse famous failures as pristine confirmation.
2. Freeze primary endpoint, evaluation oracle, model versions, task source, contamination/exposure map, prompt access, time and token constraints **before outcomes**.
3. Assign arms independently; audit role/model-family confounding. A better model could win without collaboration adding any value.
4. Score technical validity externally, not by author claims or agreement among reviewers.
5. Include prospective nulls and adversarial cases where shared context produces correlated false answers.
6. Record model/tool calls, elapsed time, rework, human relay actions, accessibility friction, extra storage and whether each actor actually read/run the source.

## Outcomes

**Primary candidate:** rate of independently verified critical defects among completed artifacts, jointly reported with usable completion. Avoid treating abandoned hard tasks as quality successes.

**Safety floor:** no data leak, invented execution, breached hard budgets, privately exposed confirmation cases or unreviewed destructive actions; any critical breach blocks promotion regardless of mean gain.

**Secondary:** correctness by defect class, cost/resource parity, elapsed time, burden of human coordination, regression on earlier capability and ability to use corrections on genuinely held-out tasks.

**Uncertainty:** if tasks are few or contaminated, report NOT EVALUABLE or UNKNOWN. Do not manufacture confidence from repeated seeded mocks, correlated cases or pairwise judgments.

## Failure and promotion rule

If split-pre review does not beat strong-single review at acceptable total cost, **prefer the simpler incumbent**. If split-pre catches more faults but no longer improves final deliverables, record a process-only finding, not a learner improvement. If pre-review or post-review causes delay, contamination or overgeneralized correction, report the regression.

No numeric promotion threshold, sample size, independent evaluator or test bank is yet approved. Muse must challenge this proposal before any future v0.2 freeze.

## Reproducibility boundary

All currently migrated Drive sources are **editorial excerpts**. A valid later public experiment needs original permitted source code or new synthetic fixtures, full commands, exact revisions, oracle results and execution receipts. Unreleased/hidden confirmation content must not be imported merely for convenience.
