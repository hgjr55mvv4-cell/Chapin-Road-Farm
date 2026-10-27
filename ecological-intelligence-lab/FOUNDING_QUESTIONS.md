# Founding questions

**Status:** DESIGN ONLY. No claim below is a finding.

## Founding question (as posed, issue #88)

Can ecological intelligence be defined and tested as context-sensitive recognition of ecological relationships, causal consequences, uncertainty, and appropriate observation / inquiry / intervention / restraint? Does independent human–AI collaboration add anything beyond a strong single-agent baseline?

## The five senses — separated before they are studied

" Ecological intelligence" bundles five different things under one attractive name. Each already has a science; the lab must say which one it studies, or it cannot design a falsifiable test.

1. **Environmental knowledge** — facts about ecosystems. This is environmental science and education. Reciting facts demonstrates retrieval, not a distinct intelligence.
2. **Context-sensitive decision competence** — judging well under uncertainty in a specific environment: which heuristic fits this environment's structure, when to gather information, when to act. The most defensible sense — and the most thoroughly pre-empted (see "Strongest redundancy" below).
3. **Ecologically inspired architectures** — design metaphors borrowed from ecology (diversity, niches, resilience, feedback). A metaphor is only scientifically interesting when it makes a differential prediction: beating a non-ecological architecture on the same task at the same cost.
4. **Collective intelligence within networks of agents** — independent agents jointly identifying dependencies, risks, or explanations that individuals miss. This is distributed cognition and collective-intelligence research, and in this repository it is already the Agent Collaboration Lab's question.
5. **Intelligence that produces beneficial ecological outcomes** — a system counts as ecologically intelligent when its actions help ecosystems. **Rejected as a scientific construct:** beneficiality is a property of an objective function, not of intelligence. A system can reason superbly about an ecosystem and use that reasoning to extract from it maximally (precision overfishing is ecologically knowledgeable, context-sensitive, and ecologically catastrophic). Building benefit into the definition makes every test circular: good outcomes prove intelligence, and intelligence is defined as producing good outcomes.

## The strongest redundancy: the framework that could make EIL unnecessary

**Gigerenzer's ecological rationality, combined with decision theory and Ostrom's social-ecological systems (SES) framework:**

- Ecological rationality (Gigerenzer, Todd & ABC Research Group 1999; Gigerenzer & Gaissmaier 2011, *Annual Review of Psychology* 62:451–482) already defines the core question — when does a decision procedure fit its environment? — with a prescriptive program (adaptive toolbox + environment structure + match conditions) and a falsification discipline (specify where a heuristic fails, not only where it succeeds).
- Decision theory already supplies action-selection machinery (expected value, value of information, irreversibility, option value) for the observe / inquire / intervene / restrain choice.
- Ostrom's SES framework (Ostrom 1990, *Governing the Commons*; Ostrom 2009, *Science* 325:419–422) already supplies the description language for real socio-ecological cases (resource systems, resource units, governance, actors, interactions, outcomes).
- Hutchins' distributed cognition (1995, *Cognition in the Wild*) and Woolley et al.'s collective-intelligence factor (2010, *Science* 330:686–688; contested — see the founding review) already supply the collective question and its failure modes.
- Holling's resilience theory (1973, *Annual Review of Ecology and Systematics* 4:1–23) already supplies the validity language for real systems (absorbing disturbance without regime shift vs merely returning to equilibrium).
- Gibson's affordances (1979, *The Ecological Approach to Visual Perception*) remind us that the original "ecological" in psychology concerns perception–action coupling, not environmental virtue; the shared word is not a shared theory.
- Goleman's *Ecological Intelligence* (2009) is a popular book about consumer information and "radical transparency," not a scientific construct with a measurement model. EIL must distinguish itself from that usage explicitly.

What remains genuinely unanswered after all of that is narrow and empirical: **does explicitly representing ecological dependencies and simulating consequences before acting improve decision quality over a strong simple baseline, on cases where the ground truth is known, at equal cost?** That is the question worth one experiment. It does not need a new kind of intelligence to ask it.

## Strongest null hypothesis (H0)

**H0:** The proposed ecological intelligence construct provides no predictive or explanatory advantage beyond existing measures of causal reasoning, environmental knowledge, calibrated uncertainty, decision theory, and collective problem-solving.

**Test that could support H0:** EIL-DEV-01 (see `EXPERIMENT_REGISTRY.md`). If explicit dependency representation shows no utility advantage over the strong-simple baseline at equal compute, or if every ESDC win is fully explained by generic reasoning scores, H0 stands and the construct is retired. H0 is the default; the burden of proof is on the construct, not on the null.

## Working operationalization: ecologically situated decision competence (ESDC)

**Recommendation (founding review, Round 01): reject the unitary construct; adopt ESDC as the working object.**

On a specified scenario with a human-stated objective and explicit constraints, ESDC is the agent's ability to:

1. **Identify** the causally relevant dependencies (which variables affect which, through what mechanisms, over what timescales) — scored against a planted ground-truth causal model, not a rater's impression.
2. **Estimate** the consequences and uncertainty of each candidate action, including restraint — scored by calibration (stated confidence vs actual correctness) and by whether second-order and delayed consequences are named.
3. **Select** the action maximizing expected objective value net of costs (tokens, time, operator burden, irreversibility risk) — scored by realized utility under the ground-truth model, with safety-floor violations vetoing any win.

ESDC is NOT a trait, a general factor, a form of moral concern, or a claim about subjective experience. The objective is human-specified and stated in the scenario; the lab measures competence against it and never infers the right objective from the model's behavior. "Ecological" modifies the *domain* (socio-ecological scenarios), not the *virtue* of the outcome.

**Retirement condition:** if EIL-DEV-01 shows no utility advantage for dependency representation, or if no scenario bank can be built in which ecological competence separates from generic causal reasoning + decision theory, ESDC adds nothing and the program stops. Renaming the same result "ecological" after generic measures explain it is not a finding.

## Competing theories and what would favor each

| Theory | Core claim | What would favor it over ESDC |
|---|---|---|
| Ecological rationality (Gigerenzer) | Rationality = heuristic–environment match | ESDC wins are fully explained by heuristic–environment match conditions, with no additional structure needed |
| Decision theory / expected utility | Optimal choice = maximize expected value under uncertainty | A full expected-value computation beats dependency representation on the same cases |
| Distributed cognition (Hutchins) | Cognition lives in systems of people + artifacts | System-level measures (artifact use, coordination) predict outcomes better than individual-agent scores |
| Collective intelligence factor (Woolley et al.) | Groups have a general factor *c* | Group performance generalizes across vignette types beyond what individual scores predict |
| Active inference (Friston) | Perception/action = free-energy minimization | A generative-model agent beats the dependency-graph candidate at equal compute on the same cases |
| Precautionary governance (Rio Principle 15) | Act under uncertainty when serious/irreversible harm threatens | Restraint rules derived from irreversibility × urgency outperform utility-maximizing selection on harm metrics |

## EIL-04: PARKED, with gates

Real-world ecological validity is parked, not active. It unparks only when all of the following exist: (1) a field protocol approved by a human decision-maker; (2) a consent framework (no visitor, volunteer, or listener becomes a participant automatically); (3) a human decision-maker for every consequential step; (4) a farm-procedure authority that explicitly authorizes any procedure touch. Until then, EIL-04 contributes no track, no cases, and no claims.

## Open questions for later rounds

- Can a scenario bank be built in which ecological competence separates from generic reasoning? (EIL-DEV-01 decides this.)
- Does the dependency-graph machinery generalize across scenario families, or only within the family it was tuned on?
- What is the minimum human oversight that keeps a restraint/intervention recommendation safe without making the human a rubber stamp?
- Later-round reviewers (DeepSeek, Grok, Meta AI) are invited to challenge the ESDC reframing directly; their disagreement belongs in `REVIEWS/`.
