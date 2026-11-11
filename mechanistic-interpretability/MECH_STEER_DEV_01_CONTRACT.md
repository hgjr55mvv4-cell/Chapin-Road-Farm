# MECH-STEER-DEV-01 v0.1-DESIGN — Counterevidence Correction

**Status: DESIGN / UNFROZEN / NOT RUN.** This is not a scientific protocol ready for confirmation; all bracketed decisions below must be frozen independently **before** confirmation cases are chosen. Original proposal: Grok (user-relayed, Oct 25 2026). Editorial corrections: Sol. Additional spend: $0. Model downloads, GPU, real inference, scored model execution, training and deployment **HOLD**.

## Question and potential value

Can a **bounded residual-stream intervention** improve final objective correctness when a fixed-weight model revises a previously provided answer after new evidence, *beyond* the identical model receiving the identical strong correction prompt/evidence without steering?

**Alternative hypotheses:** steering merely increases willingness to change answers; damages correct answers; absorbs false evidence; worsens fluency or confidence; matches random perturbation; strong prompts saturate the task.

## Unit, population and paired design

**Independent case cluster:** a unique factual claim/problem and source-family, with an externally checkable gold answer, one held-fixed initial answer, and one evidence packet of known reliability. Paraphrases/seeds/generations of a single claim or source family remain **within that cluster**, not independent n. For every case, generate/provide the same baseline initial answer, evidence packet, message history, output format, max length, decoding config and scorer to **each** arm. Evidence reliability is determined independently; do not use model agreement as oracle.

Prospectively stratify case clusters by (i) initial-answer correctness and (ii) supporting vs truthful contradictory vs false/unsupported contradictory evidence, as sensible for that case. Include at minimum:

- **Recoverable error:** initially incorrect, trustworthy contradiction supports correction.
- **Preservation:** initially correct, trustworthy corroborating/non-corrective information.
- **Adversarial false correction:** initially correct, purported contradiction is false/unsupported.
- **Ambiguous/cannot adjudicate:** separate optional stratum with abstention; never quietly count as right.

If an initial answer is needed, generate it *once* in a predeclared, intervention-free way (or draw from a fixed admissible record) before arms. Its creation is a common pre-treatment input, not an extra uncounted model call; log it. No choosing only a candidate-friendly subset after seeing intervention outputs.

## Experimental arms and fair comparator

| Arm | Final answer setup | Purpose |
| --- | --- | --- |
| A0 | Original prompt, new evidence; no explicit correction instruction, no intervention | Descriptive ordinary workflow |
| **A1 — incumbent** | Same strong prompt, evidence and explicit instruction to revise *only if justified*; no intervention | **Primary comparator** |
| **B1 — challenger** | Exactly A1 + one frozen, bounded internal intervention; no extra information, changed output budget or new prompts | **Primary contrast B1 minus A1** |
| B2 | Exactly A1 + norm-, timing- and location-matched randomly oriented intervention | Negative control |
| B3 | Exactly A1 + direction learned on deliberately unrelated/shuffled discovery labels, if technically justified | Selection/label control |

A2 (strong procedural memory/retrieval), probe-only, SAE and neuron-based alternates are **optional separate designs**, not automatically part of the confirmation arms. Do not let expensive arm proliferation compromise sample quality. Never compare B1 using better prompting or privileged evidence against an intentionally weak A0.

## Primary endpoint — correction to Grok's draft

Grok proposed adding three conditional percentages (true correction minus degradation minus false correction), which has **incompatible subgroup denominators**, implicit arbitrary weights and potential double-counting. That is **not** a valid default net-estimand without an explicit target population and weights.

**Primary candidate estimand:** for a *pre-registered target mixture* of independent case clusters, the difference in **gold-judged final answer correctness** between B1 and A1: 
`Delta = sum_s w_s * [mean(Y_B1,s) - mean(Y_A1,s)]` where strata s are fixed before confirmation, `Y` is binary objectively correct final answer (an incorrect refusal is incorrect unless the rubric legitimately expects abstention), and `sum_s w_s = 1`. Use paired per-case differences and cluster-aware intervals. Clearly label whether weights reflect balanced stress testing or real deployment prevalence; do not claim real-world prevalence from artificial balance.

**Mandatory subgroup diagnostics:** proportion of initially incorrect answers corrected; proportion of initially correct answers degraded; false-evidence acceptance/incorrect flips; warranted abstentions; and case-family heterogeneity. Do not collapse a damaging subgroup into a good average. Multiple generations per cluster are sensitivity runs, not more independent samples.

**Quality/safety floor:** maximum tolerated degradation in initially correct cases, false-evidence acceptance, incoherence/format violations, unsafe/injected instruction following, plus a minimum usable completion fraction must all be preregistered. **Exact numeric floors NOT YET SET: scientific execution BLOCKED.**

## Candidate discovery and OOD falsification

Explore development cases only. Prefer a single hypothesis-driven contrastive direction in residual space over unconstrained neuron hunting. Disclose full search history/number of tested layers, candidate directions, magnitudes and prompts. Match natural activation scale; log `layer`, `position`, `norm`, `alpha`, `hook`, whether residual state is before/after normalization, thinking-mode config and numeric dtype.

Set discrete magnitudes and strength-selection rule *before exploration*; no “largest safe” without evaluating quality and control failures. Select a frozen intervention on discovery only. Set a bounded search budget, with multiple-comparison approach or exploratory-only designation. Use fresh withheld confirmation case clusters after freeze; family-level blocking avoids shared templates/sources/near duplicates. Audit contamination and pretrained knowledge of the facts. Include paraphrase, false-evidence and unrelated-task OOD stress cases.

## Analysis, uncertainty, and costs

- Declare primary test and CI family; pair models by identical case and seed where operationally sensible. Use a cluster-respecting bootstrap/randomization method; if few clusters or unstable outcome, say **UNKNOWN**.
- Score answers by a deterministic gold rubric where possible; blind adjudicate genuine ambiguous outputs. Preserve raw outputs and abstention classes. Calibration/Brier requires reported probabilities or a defined elicitation protocol, not imaginary confidence.
- Report token use, runtime/GPU type, activation capture overhead, number of search probes, additional development work, human relay and review time, output length distribution and persistent configuration complexity.
- **Unfrozen ceilings:** total GPU minutes [TBD]; inference calls/tokens [TBD]; operator minutes [TBD]; maximum number of discovery trials [TBD]. The current authorized expenditure is $0; actual model execution remains HOLD.
- Block continuation if A1 saturates discovery performance (predeclared threshold), B1 matches random-direction controls, the target metric becomes unscoreable or any critical floor is breached.

## Immutable freeze fields still required

Exact source/checkpoint/revision and license; inference backend/versions; intervention tensor and insertion point; frozen SHA of direction/procedure; trigger/strength; case population and weights; split and time boundary; primary estimand/CI and adverse floors; evaluation oracle; thresholds/alpha; sample size/power rationale; search budget; human/compute ceiling; termination/retest rule; operator signoff. Material edits after freeze produce a *new challenger version*.

## Next authorized activities

1. Muse: independently challenge this contract and provide an audit delta; do not self-certify.
2. Astra: adversarial independent review of repaired design.
3. A bounded deterministic **mock-only** scorer/provenance checker may be proposed after review; no real models, weights or activation hooks.
4. Any later model execution requires a separate explicit authorization; no retroactive confirmation.
