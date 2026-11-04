# Evidence rules (EIL-specific only)

Everything not listed here is governed by existing repository rules, linked — not duplicated — per founding issue #88:

- Repository `AGENTS.md` — contribution workflow, branch-base verification, strong-simple baseline rule, consent boundaries, scope limits.
- [Agent Collaboration Lab protocol](../agent-collaboration-lab/RESEARCH_PROTOCOL_01.md) — collective-method arms, pre-execution controls, safety floor, simpler-incumbent promotion rule.
- Ω-ARENA discipline (see the shared research channel and the Agent Collaboration Lab) — version and freeze a procedure's contract before confirmation, keep exploration separate from confirmation, do not promote without valid comparative evidence.
- Repository `README.md` — evidence-state vocabulary (`IDEA`, `DESIGN`, `IMPLEMENTED`, `TESTED`, `CONFIRMED`, `UNKNOWN`).

## EIL-specific rules

1. **Normative-objective separation.** Every scenario states its objective and constraints explicitly, set by a human. Competence is measured against that stated objective. The lab never infers the right objective from a model's behavior, and never counts a beneficial outcome as evidence of understanding without a competence score to match. Violating this rule invalidates the study, not just the claim.
2. **Scenario-bank provenance.** Every vignette records: author (human or model, named), authoring date, ground-truth causal model, utility table, irreversibility and time-criticality flags, and any model that saw the vignette before scoring. A vignette seen by a tested model before scoring is contaminated and is removed from confirmation sets (it may remain in DEV sets, labeled as exposed).
3. **Ground-truth custody.** Ground truth is held by the scorer only and never appears in prompts, examples, or few-shot context for the tested arms. Any leak discovered after scoring voids that run.
4. **Style controls are mandatory for language claims.** Any claim involving ecological language, rhetoric, or framing must include a style-only control (same recommendation, rhetoric added or removed). "Ecologicalness" ratings are diagnostics, never outcomes.
5. **Error decomposition is mandatory for restraint claims.** Restraint results are reported as a confusion matrix (act / restrain × correct / harmful), never as a single accuracy or a restraint rate. A high restraint rate is not a good result.
6. **Compute parity is audited, not asserted.** Every comparative run reports total tokens, latency, and operator minutes per arm per case. An arm that exceeds its token budget is disqualified. A win at unequal compute is reported as a compute result.
7. **Dissent is preserved.** Independent reviews live in `REVIEWS/` as attributed documents. Founding documents are not edited to remove or soften recorded disagreement; if a review changes the lab's position, the change is recorded as a new version with the review cited, and the prior position remains readable.
8. **The founding insect observation is UNKNOWN.** It has no provenance record in this scaffold and is not evidence for any hypothesis. It may enter the evidence record only with observer, date, conditions, observed-vs-inferred separation, and an independent check.
9. **No real-world generalization from synthetic results.** A DEV win on synthetic vignettes is a DEV win. It licenses a better-designed DEV experiment, not a field claim, a farm-procedure change, or a public statement about ecological outcomes.
10. **Retirement is a success condition.** If EIL-DEV-01 falsifies H1, or if ESDC cannot be separated from generic reasoning, the program stops and the stop is recorded here with the falsifying evidence. A lab that cannot be retired cannot be trusted when it claims a win.
