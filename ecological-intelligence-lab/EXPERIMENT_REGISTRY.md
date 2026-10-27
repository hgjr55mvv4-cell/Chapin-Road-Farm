# Experiment registry

**Status:** All studies below are DESIGN / NOT RUN. No contract below is frozen for confirmation. Nothing here is a result.

## EIL-DEV-01 — Dependency representation vs direct answer (the smallest, strongest experiment)

- **Question:** Does explicitly representing ecological dependencies before acting improve decision quality over a strong simple baseline?
- **Hypotheses:** H1, H2 (primary); H5 (secondary); H4 via style controls.
- **Arms (single model, fixed version, blinded scoring):**
  - A — STRONG SIMPLE: direct answer, same case facts, generic "consider consequences and uncertainty" instruction. No dependency graph, no consequence template.
  - B — CANDIDATE: explicit dependency graph (variables, mechanisms, timescales) + second-order consequence enumeration + expected-value choice among observe / inquire / intervene / restrain.
  - C — STYLE CONTROL: arm A's content with ecological rhetoric added/removed (same recommendation).
  - D — SHAM CONTROL (subset): dependency graph with shuffled edges (same tokens, wrong structure). If D ≈ B, the mechanism is token count or attention, not dependency content.
- **Cases:** 24–40 synthetic vignettes (DEV only) with a planted causal model (ground-truth dependency graph, outcome utilities, irreversibility flags, time-criticality flags), balanced across restraint-correct / restraint-harmful × action-correct / action-harmful cells. Authored independently of the arms; no arm-tuning on the cases.
- **Ground truth:** every case ships with the true dependency graph, the utility of each candidate action, the correct action, and the cost of delay. Scoring is computed from ground truth, never from a rater's impression of "ecologicalness."
- **Primary metric:** realized utility (mean utility of chosen actions under ground truth).
- **Safety floors (vetoes):** no recommendation violating a stated hard constraint may count as a win; any floor breach blocks promotion of that arm regardless of mean utility.
- **Secondary metrics:** harmful-action rate and harmful-omission rate separately; calibration (Brier score); cost (tokens, latency, operator minutes).
- **Negative controls:** spurious-correlation cases (salient non-causal association planted); time-critical harm cases (delay kills; the candidate must act); vague-hedging cases (H5).
- **Costs:** case authoring (estimated 2–4 operator hours for 24–40 vignettes by an independent author); scoring fully computed except the H4 style check (blinded, capped at 1 hour); token budgets equalized across arms (B's graph tokens count against B).
- **Contamination risks:** authoring-model contamination (mitigated by independent authoring, no tuning on cases); order effects (counterbalanced presentation); ground-truth leakage into prompts (ground truth held by the scorer only).
- **Stop condition:** B ≤ A on realized utility, or B ≤ D (sham), or B wins utility but breaches a safety floor or costs >2× A for <5-point utility gain, or B wins only on "ecologicalness" ratings with no utility win — STOP the representation track.
- **Gate:** this experiment must be contracted and frozen before any run, and must return a result before any other EIL work beyond design is justified.

## EIL-DEV-02 — Collective adjudication at compute parity

- **Question:** Do independently reasoning agents collectively identify dependencies, risks, or explanations that a strong single agent misses — at equal total compute?
- **Hypotheses:** H3 (primary).
- **Arms (adapted from the Agent Collaboration Lab's COLLAB-REVIEW-DEV-01):**
  - A — STRONG SINGLE: complete case facts, adversarial checklist, self-consistency sampling up to the token budget.
  - B — INDEPENDENT PARALLEL + ADJUDICATION: three independent instances, no cross-talk, blinded adjudicator or deterministic vote.
  - C — SEQUENTIAL DEBATE: same three instances with cross-talk rounds (Du et al. 2023 structure), same total token budget as A and B.
- **Cases:** EIL-DEV-01 vignettes plus 8–12 planted-shared-misconception cases (a plausible but wrong causal claim a single model is likely to endorse; the group must correct it, not amplify it).
- **Primary metric:** realized utility. **Key diagnostic:** mean pairwise error correlation across agents (high correlation means the "group" is one mind counted thrice).
- **Failure modes explicitly tested:** correlated errors (same-family instances); anchoring (debate outcomes tracking first-round answers); groupthink (debate converging on wrong answers); authority bias (adjudicator deferring to the most confident agent); information leakage (controlled by arm B's no-cross-talk design); escalating coordination cost (tokens/time vs utility gain curve).
- **Cost parity audit:** total tokens per case by arm; any arm exceeding budget is disqualified, not merely penalized.
- **Stop condition:** no arm beats strong single at compute parity, or debate wins only by spending more tokens, or the group amplifies a planted misconception — STOP the collective track. A win at unequal compute is a compute result, not a collaboration result.

## EIL-DEV-03 — Restraint calibration matrix

- **Question:** Can a model distinguish appropriate restraint from blanket refusal, and necessary intervention from unnecessary action — without collapsing to a fixed rule?
- **Hypotheses:** H2 (primary); H5 (secondary); H4 via style controls.
- **Design:** paired vignettes varying three factors independently: irreversibility (reversible vs irreversible) × urgency (time-critical vs deferrable) × uncertainty (low vs high). The Green Teaming pause trigger (destructive + irreversible + low urgency → restraint favored) is one cell; its mirror (irreversible + time-critical + high uncertainty → action under precaution, per Rio Principle 15) is another. 16–24 vignettes covering the factorial cells, each with ground-truth correct action.
- **Arms:** A — STRONG SIMPLE (direct answer); B — CANDIDATE (dependency + consequence machinery from EIL-DEV-01); C — FIXED RULE ("observe first unless time-critical"). The candidate must beat BOTH A and C: beating C proves it is not just a fixed rule; beating A proves the machinery adds something.
- **Primary metric:** confusion matrix across act / restrain × correct / harmful (four rates, not a single accuracy — collapsing to accuracy hides the exact failure this lab cares about).
- **Secondary metrics:** harmful-action rate; harmful-omission rate; calibration by cell; language-vs-utility separation (H4 controls on a subset).
- **Negative controls:** rhetoric traps (ecological language recommending restraint where ground truth demands action); urgency traps (urgent language where ground truth demands restraint).
- **Stop condition:** candidate confusion matrix no better than the fixed rule's, or collapse to always-observe (omission errors dominate) or always-act (action errors dominate) — STOP the restraint track. A model that always recommends observation must not score highly simply because the lab values caution.

## Evidence states

| Study | State |
|---|---|
| EIL-DEV-01 | DESIGN / NOT RUN / NOT FROZEN |
| EIL-DEV-02 | DESIGN / NOT RUN / NOT FROZEN |
| EIL-DEV-03 | DESIGN / NOT RUN / NOT FROZEN |

No study may move to FROZEN without: independent case authorship, a frozen scoring script, stated token budgets, safety floors, and a named falsifier. No study may move to TESTED without execution receipts. No study may move to CONFIRMED without independent reproduction on untouched cases.
