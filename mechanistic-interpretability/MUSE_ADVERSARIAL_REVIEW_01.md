# MUSE_ADVERSARIAL_REVIEW_01 — Independent adversarial review of MECH-INTERP-01

**Reviewer:** Muse (independent of Grok and of Sol's editorial reconstruction).
**Reviewed:** draft PR #79, branch `research/mech-interp-01-design-20261025`
(head `bc47dbfa…` at review time), `mechanistic-interpretability/` in full,
`agent-collaboration-lab/RESEARCH_PROTOCOL_01.md`,
`agent-collaboration-lab/OUTSIDE_AGENTS.md`, issues #78 and #80.
**Status:** REVIEW ONLY. No model execution, downloads, inference,
training, confirmation, deployment, or merge. $0.
**Verdict: REVISE — do not freeze, do not confirm, do not merge as a
scientific protocol.** The package is honest about its own limits and
already corrects Grok's worst estimand error. That is not enough to
freeze: eight blocking defects below (B1–B8) each break identification,
measurement, or confirmation on their own. Fixing them is a contract
revision (see `MECH_STEER_DEV_01_CONTRACT_v0.2_PROPOSAL.md`), not a
polish pass. A negative result against all intervention methods
remains a live, respectable outcome and must stay the default
expectation until a frozen test says otherwise.

## 0. What I agree with (so the disagreements are legible)

- Grok's three-rate "net correction" was invalid: it subtracted
  proportions with incompatible denominators. The v0.1 replacement —
  a population-weighted paired difference in final correctness —
  is the right estimand family.
- A1 (strong prompt-only) is the correct primary comparator, not A0.
  Comparing B1 against a weak baseline would prove nothing.
- The residual-stream preference is a hypothesis, not a finding, and
  the package says so. Probe accuracy is not actuation (Basu et al.
  is the right caution, used correctly as domain-specific evidence).
- "Exploration does not promote a candidate" and "merge ≠ scientific
  confirmation" are the right gates, and the registry keeps negative
  evidence visible instead of deleting it.

## 1. Blocking defects (each blocks a freeze on its own)

### B1. The weights are still ungrounded, and the strata are not a partition
`Delta = sum_s w_s * [mean(Y_B1,s) - mean(Y_A1,s)]` is stated, but
no rule chooses `w_s`, and the strata as described are not mutually
exclusive: "supporting vs truthful contradictory vs false/unsupported
contradictory" evidence crosses with "initially correct vs incorrect",
and "ambiguous/cannot adjudicate" is "optional". If a stratum is
optional, dropping it renormalises every other weight and changes the
estimand after the fact. If a confirmation stratum comes back empty,
the estimand is undefined unless a fallback is pre-registered.
**Required:** a fixed Cartesian cell table (initial × evidence type),
one weight per cell summing to 1, a stated grounding (balanced stress
test vs deployment prevalence — and if balanced, no prevalence claim),
an empty-cell rule, and an explicit statement of whether the
ambiguous cell is in or out, with its weight fixed either way.
Weights must be chosen before confirmation cases are seen, not fitted
to where the effect looks best.

### B2. "Initially correct" is itself an unblinded measurement
Stratification happens on initial-answer correctness, but the
contract never says who judges initial correctness, whether that
judgment is blinded to arm outcomes, or what happens to borderline
initial answers. An initial answer that is half-right, hedged, or
format-invalid can be sorted into whichever stratum flatters the
result after arms are run. **Required:** initial correctness is
adjudicated once, before arms run, by the frozen gold rubric, blind
to B1 outputs; borderline cases go to a pre-registered rule (counted
incorrect, counted ambiguous-cell, or excluded by a rule written
before adjudication — not chosen after); and Delta is reported under
at least one alternative initial-labelling sensitivity analysis.

### B3. Invalid initial answers and expected abstention are undefined
The contract says an incorrect refusal is incorrect "unless the
rubric legitimately expects abstention" — but the rubric does not
yet exist, and no case is pre-listed as abstention-expected. The
same hole covers malformed initial answers (no parseable answer) and
initial answers that refuse. **Required:** a pre-registered
abstention-expected case list (or a rule that generates it before
arms run); a malformed-initial rule (e.g. malformed initial counts
as incorrect-initial and its final answer is still judged, never
silently dropped); and a format-violation class reported separately
from correctness, so steering cannot win by changing answer format
into something the scorer happens to parse more generously.

### B4. Confirmation selection, de-duplication, and contamination are aspirational
"Family-level blocking" and "audit contamination" are named but not
operationalised. What makes two cases the same family — same source
document, same fact, same template, same entity? Paraphrases of one
claim are within-cluster by the contract's own rule, but nothing
detects a paraphrase that slips into the confirmation set, nothing
forbids reusing a DEV case ID, and nothing sets a time boundary
(cases created after the direction was frozen vs before). Worse,
pretrained knowledge is unaddressed: if the model already knows the
fact, "correction" may be retrieval, not steering. **Required:**
a written family definition; a duplicate/near-duplicate check with a
named method and threshold (even a conservative human check counts
if it is pre-registered and logged); a DEV/confirmation ID firewall
(confirmation IDs must not appear in any DEV file, mock fixture, or
issue); a case-bank hash commitment published at freeze; and either
a novel-facts stratum or a knowledge-probe pretest, so a memorisation
explanation has a place to lose.

### B5. The negative controls are not budget-matched, and one control is missing
B2 (random direction) matches norm, timing, and location — but not
*discovery budget*. B1's direction is the winner of a search over
layers, magnitudes, and candidates; a single random direction is not
the same procedure. A budget-matched control draws K random
directions, applies the same DEV selection rule, and confirms the
winner — or B2 must be labelled a weak control and the claim
downgraded accordingly. B3 (shuffled-label direction) is conditional
("if technically justified"), so the selection control may vanish
entirely. And there is no inert-hook control at all: installing a
hook can change numerics (dtype, padding, kernel path) even at
alpha = 0. **Required:** add arm A1-H (A1 with the hook installed
and alpha = 0) to separate hook artefacts from steering; make B2
budget-matched or label it weak; and state what happens to the
design if B3 cannot be built (the design must not silently lose its
selection control).

### B6. "A1 plus only a bounded activation edit" is underdetermined
The contract says to log layer, position, norm, alpha, and
pre/post-normalisation — but logging is not freezing. It never
fixes: at which token positions the edit applies (all positions?
last token only? evidence tokens?); for how many generated tokens
it persists; whether it decays; whether it applies during
prefilling only, generation only, or both; or what happens under
thinking/reasoning mode (a steering effect that works by changing
the reasoning trace is a different claim from one that changes the
final answer, and the two must not be pooled). **Required:** a
frozen intervention schedule (positions, duration, decay, mode
config) as a freeze field, with any deviation producing a new
challenger version.

### B7. The oracle and the uncertainty claim are incomplete
"Deterministic gold rubric where possible; blind adjudicate genuine
ambiguous outputs" leaves open: who adjudicates, what agreement
threshold is required, what happens on disagreement, and whether the
scorer is sensitive to output length or fluency changes caused by
steering (a steering method that makes answers shorter and cleaner
can inflate a parser-based scorer without improving correctness).
The CI family is named ("cluster-respecting bootstrap/randomization")
but no statistic, alpha, or multiplicity rule is given, while five
mandatory subgroup diagnostics invite exactly the multiple-testing
problem the contract warns about. **Required:** adjudicator rule
and disagreement procedure; a length/format sensitivity analysis;
a named primary statistic with alpha; and subgroup diagnostics
labelled exploratory unless a family-control rule is frozen with
them. If clusters are few, the honest output is UNKNOWN, and the
contract should say the minimum cluster count below which no
confirmatory claim is made at all.

### B8. Floors, ceilings, and power are TBD — the contract blocks itself, correctly
The contract already states execution is BLOCKED until numeric
floors are set. I agree, and extend it: ceilings (GPU minutes, calls,
operator minutes, discovery trials) and a power/sample-size rationale
are equally blocking. Without floors, a positive mean Delta with a
damaged subgroup can be spun as a win. Without power, a null result
is uninterpretable rather than negative evidence. Without ceilings,
control arms (which multiply cost ~3–4×) can quietly eat the budget
and force a cut to the controls — which is how B2/B3 get dropped.
**Required:** floors, ceilings, and a power rationale frozen together,
with control-arm costs inside the ceiling, before any confirmation
case is chosen. The v0.2 proposal suggests starting values for
maintainer decision; it does not adopt them.

## 2. Non-blocking improvements (do these in the same revision)

1. **Method preference is a prior, not a result.** "Prefer a single
   hypothesis-driven contrastive direction" pre-excludes SAE and
   neuron baselines from the DEV comparison. Pre-register a
   method-agnostic DEV comparison under an identical search budget
   instead; the residual-stream direction must earn its place.
2. **Evidence packets can smuggle instructions.** A counterevidence
   packet containing an embedded instruction ("ignore your previous
   answer") confounds correction with instruction-following.
   Sanitize packets for instructions and log the screen, or the
   B1–A1 contrast measures obedience, not correction.
3. **Multiple generations per cluster need an aggregation rule.**
   Majority vote, first generation, and mean correctness give
   different answers; pre-register one as primary.
4. **Checkpoint transfer is a separate claim.** A direction learned
   on one checkpoint does not transfer by default; RQ4 transfer
   tests must re-derive or explicitly test transfer, not assume it.
5. **Cost accounting must include controls and relay.** The
   contract counts token/compute costs; add human relay and review
   time for every arm, since that is where this project's real
   budget goes (cf. COLLAB-REVIEW-DEV-01's cost rule).
6. **Strata labels must not leak into the estimand's story.**
   "Recoverable error" and "preservation" are fine as names, but the
   reported result must be the cell table, not a renamed average.

## 3. Source independence and citation checks (my own, not relayed)

| Claim | My check | Status |
|---|---|---|
| Qwen3-0.6B 28 layers; Qwen3-8B 36 layers | Qwen3 technical report, Table 1 (dense models) | **Confirmed** (numbers match). Layer *indexing* (0- vs 1-based) and hook location still unverified — the audit already says this. |
| MIB, ICML 2025, PMLR 267; DAS best; SAEs not better than neurons | PMLR 267:45069–45108 abstract and project page | **Confirmed, with a precision correction:** the project page notes an SAE exception (RAVEL continent, Gemma-2). "Not better than neurons" should carry that exception as a footnote, not as an absolute. |
| SAEBench accepted to ICML 2025 | Not re-verified by me | **Unverified by this review** — audit's claim stands as author/audit-reported only. |
| Basu et al. 2026: 98.2% probe AUROC, steering often fails, some correct answers damaged | Not re-verified by me | **Author-reported, preprint.** Correctly used as domain-specific evidence only; must not be cited as a general steering impossibility result. |
| CounterSteer 2026 (Russinovich) | Not re-verified by me | **Author-reported, preprint.** Task is prompt-injection suppression, not factual correction; transfer to this task is an assumption, not evidence. |
| Sauers "green neuron" demonstration | No primary post, weights revision, hook, sign, seeds, or selection scope recovered | **UNKNOWN.** Must not be cited as evidence for anything beyond "a social-media report exists". The audit correctly quarantines it; keep it quarantined. |
| Grok's eight-file original package | Not accessible to Sol, not accessible to me | **Unverified.** Everything attributed to Grok in this package is relayed editorial reconstruction. No statement in the package should be upgraded to "Grok found" without source recovery and diff. |
| Ω-ARENA v0.5 guidance (SHA cited in README) | Canonical artifact not recovered here | **Unverified here**, as the README itself states. Do not cite as authority beyond "relayed". |

**Independence warning (applies to this review too):** Muse, Astra,
and Sol have all now read the same relayed Grok digest. Agreement
among us is shared-evidence agreement, not independent replication.
For Astra's adjudication to add independence, Astra should review
the contract against the primary sources and the freeze checklist
alone, without re-reading the Grok digest as evidence — or its
review should be labelled shared-evidence as well.

## 4. Explicit dissent

1. **Against the package's implied ordering:** the package treats
   the mock harness as the next step after this review. I disagree
   in part: the mock is useful only *after* the v0.2 contract fixes
   (see MOCK_PREFLIGHT_SPEC.md). Building it against v0.1 would
   qualify plumbing for an estimand that is still undefined.
2. **Against "residual-stream preferred" as a design default:**
   preference before a budget-matched DEV comparison is a bias,
   not a hypothesis. The default should be method-agnostic until
   DEV evidence exists.
3. **Against treating reviewer agreement as progress:** three
   reviewers reading one relayed digest do not make a finding more
   true. The registry should record reviewer exposure (who read the
   digest) alongside each review, so future readers can discount
   shared-evidence agreement appropriately.

## 5. What would change my verdict

A v0.2 contract that fixes B1–B8 in text (not in intent), a frozen
floor/ceiling/power block, and a mock spec that passes its planted
defects would move this review from REVISE to READY-FOR-ASTRA.
Nothing in this review requires new spending, model access, or data
collection — only writing, done before any case is chosen.
