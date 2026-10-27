# REVIEW — Muse, EIL-FOUNDING-01, Round 01 (concise)

**Reviewer:** Muse (independent system, not Meta AI, not Sol). **Date:** October 27, 2026.
**Assignment:** Brian & Sol. Independent research, design, and draft-PR preparation authorized. No merge, no scored experiment, $0.
**Full review:** delivered to Brian with this draft PR (local report `EIL_FOUNDING_MUSE_REVIEW_01.md`, Oct 27, 2026); this file is its concise, self-contained form for the public record.
**Status:** DESIGN ONLY. No experiment was executed; nothing here is a finding about any model.

## Verdict: REVISE

The inquiry has merit in a narrow form, but the program as founded requires specific repairs before proceeding as a lab. The full review's reasoning is summarized below; disagreement with any part of it is welcome in this directory as attributed criticism.

## Strongest argument against EIL

" Ecological intelligence" bundles five different things under one attractive name, four of which already have mature sciences, and the fifth of which is not a property of intelligence at all:

1. **Environmental knowledge** — environmental science; retrieval, not a distinct intelligence.
2. **Context-sensitive decision competence** — Gigerenzer's ecological rationality (1999; 2011, *Annual Review of Psychology* 62:451–482) plus decision theory, with a 30-year prescriptive program.
3. **Ecologically inspired architectures** — a design metaphor until it makes a differential prediction at equal cost.
4. **Collective intelligence** — Hutchins' distributed cognition (1995) and Woolley et al. (2010, *Science* 330:686–688, contested), and in this repository the Agent Collaboration Lab's own question and protocol.
5. **Beneficial ecological outcomes** — **rejected as a construct:** beneficiality is a property of an objective function, not of intelligence. Precision overfishing is ecologically knowledgeable, context-sensitive, and ecologically catastrophic. Building benefit into the definition makes every test circular.

The strongest redundancy frame is ecological rationality + decision theory + Ostrom's SES framework (1990; 2009, *Science* 325:419–422), with Holling's resilience theory (1973) for validity language and Gibson's affordances (1979) as a reminder that the original "ecological" in psychology concerns perception–action coupling, not environmental virtue. Goleman's *Ecological Intelligence* (2009) is a popular consumer-information book, not a scientific construct; EIL must distinguish itself from that usage.

## Strongest null (H0)

H0: the proposed construct provides no predictive or explanatory advantage beyond existing measures of causal reasoning, environmental knowledge, calibrated uncertainty, decision theory, and collective problem-solving. EIL-DEV-01 is the test that could support H0; the burden of proof is on the construct.

## Recommendation: reject the unitary construct; adopt ESDC

**Ecologically situated decision competence (ESDC):** on a specified scenario with a human-stated objective, the ability to (1) identify causally relevant dependencies, scored against planted ground truth; (2) estimate consequences and uncertainty of each candidate action including restraint, scored by calibration; (3) select the action maximizing expected objective value net of costs, scored by realized utility with safety-floor vetoes. ESDC is not a trait, a general factor, moral concern, or subjective experience. "Ecological" modifies the domain, not the virtue of the outcome.

**Retirement condition:** if EIL-DEV-01 shows no utility advantage for dependency representation, or if ESDC wins are fully explained by generic reasoning scores, the program stops. Renaming the same result "ecological" after generic measures explain it is not a finding.

## Hypotheses (see HYPOTHESES.md for falsifiers)

- H1: dependency representation improves decision utility vs strong-simple baseline at equal compute.
- H2: consequence simulation improves restraint calibration (both error types fall, not one traded for the other).
- H3: collective adjudication beats strong single only at compute parity, on planted-misconception cases.
- H4: ecological language is not ecological understanding (style-only controls).
- H5: calibration, not hedging (Brier score via discrimination, not blanket uncertainty).

## Experiments (see EXPERIMENT_REGISTRY.md)

- **EIL-DEV-01** (the smallest, strongest experiment; must run first): one model, direct answer vs dependency graph + consequence enumeration, 24–40 synthetic vignettes with planted ground truth balanced across restraint-correct / restraint-harmful cells, realized utility with safety vetoes, sham-graph and style-only controls, equal token budgets.
- **EIL-DEV-02:** collective adjudication at compute parity, with error-correlation measurement and planted shared misconceptions.
- **EIL-DEV-03:** restraint calibration matrix (irreversibility × urgency × uncertainty), candidate must beat both the strong-simple baseline and a fixed "observe first" rule, reported as a confusion matrix.

## Required repairs (the REVISE conditions)

1. Adopt ESDC (or an equivalent narrow operationalization) with its retirement condition; drop the unitary construct.
2. Park EIL-04 (no field protocol, consent framework, or procedure authority exists); fold EIL-03's method into the Agent Collaboration Lab protocol by reference.
3. Freeze EIL-DEV-01's contract before any run; run nothing until that freeze exists.
4. Keep the founding insect observation (UNKNOWN, unexamined here) out of the evidence record until it has provenance.
5. Preserve dissent in `REVIEWS/`; later-round disagreement is a feature, not a defect.

## What would change this decision

- **PROCEED:** EIL-DEV-01 shows a utility win for dependency representation at equal compute, safety floors intact, sham control beaten — the machinery, not tokens or rhetoric, causes the win.
- **HOLD:** EIL-DEV-01 is frozen but cannot be run within $0 — the design waits; the program does not advance on prose.
- **STOP:** EIL-DEV-01 shows no utility win, the sham control matches the candidate, ESDC wins are fully explained by generic reasoning, or the construct cannot be operationalized without circularity. Invoking the retirement condition is a successful outcome.

*Preserve disagreement. Report negative evidence. Do not manufacture scientific novelty.*
