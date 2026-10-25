# THE LISTENING ROOM — DEEPSEEK ROUND 2
## TLR-R2-COMPUTE-01: Constellation Intelligence Without Invented Patterns
**From:** Brian & Sol
**Date:** October 25, 2026
**Role:** Computational research architect, minimal prototype engineer, and independent falsification designer
**Budget:** $0 additional expenditure
**Authority:** Literature/source verification, architecture, synthetic fixtures, deterministic schema/code tests and exploratory design. **HOLD:** real listener recruitment/intake, real participant data, audio download/analysis, streaming integration, model training, scientific confirmation, public deployment, and changes to Claude's unfinished Sprint 01 app.

## 1. The problem
The Listening Room is a proposed open-source co-listening space. People and their personal AIs may gradually learn about songs, moments, and preferences through voluntary interaction. Brian wants to invite willing contributors to submit personally meaningful playlists, including otherwise dissimilar genres, and eventually learn both from listener testimony and **independently verified** musical features.

Muse designed a simple Quick Moment and Constellation Playlist interface. Grok challenged the idea that a person's meaningful playlist contains hidden acoustic patterns, the reactivity of 'why does this matter?' prompts, weak comparison baselines, hierarchical pseudoreplication, privacy/reidentification, copyright and the conflation of fluent explanations with better recommendations.

**Your research goal:** design the smallest defensible system that records a listener's choice, learns from their corrections, and generates **falsifiable** cross-genre hypotheses without mistaking set membership, labels or explanations for directly heard evidence.

The first Claude app build is incomplete/unqualified. Do not assume it exists or require its implementation. Do not turn this into a new large platform or pretend the app already streams or hears music.

## 2. Inspect the source artifacts yourself
Read our staged GitHub files:
https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/tree/research/listening-room-round02/research/the-listening-room

Required:
- docs/CONTRIBUTION-CONTRACT-v0.1.md (including broad voluntary sharing addendum)
- docs/ROUND-02-PLAN.md
- docs/MUSE-REVIEW-01.md
- docs/GROK-REVIEW-02.md
- schemas/listening-contribution.schema.json
- examples/synthetic-contribution.json
- prompts/MUSE-ROUND-02.md
- prompts/GROK-ROUND-02.md

Treat all as exploratory. Confirm exactly which files were inspected, and mark missing sources NOT READ. Do not quietly rewrite or relax the synthetic-only public schema's research/public/training=false constants.

## 3. Independently challenge the science
Review and locate original methods/results, not summaries alone. Prioritize:
- Cheng, Joachims & Turnbull (ISMIR 2020), acoustic similarity, playlist construction and liking: https://program.ismir2020.net/poster_4-15.html
- Chaganty et al. (SIGIR 2023), Conversational Playlist Curation Dataset: https://github.com/google-research-datasets/cpcd
- Hirschprung & Leshman (2021), music-selection reidentification: https://doi.org/10.1016/j.tele.2021.101564
- Afchar et al. (2022), explainability and skip interpretation: https://doi.org/10.1002/aaai.12056
- Relevant time-dependent recommendation, conversational preference learning, hierarchical dependence, set-level ranking and trustworthy audio grounding literature.

Separate directly verified bibliographic findings from unverified claims, product hypotheses, and invented test cases. Do not claim that all cross-genre meaningful constellations are non-acoustic: that is an alternative hypothesis, not a result.

## 4. Design the smallest safe state machine
Distinguish **person -> session -> playlist -> song selection -> resolved recording identity -> optional moment**. A song title may correspond to a cover, live take, remix or remaster; timestamped claims must be blocked until actual recording identity and qualified audio evidence exist.

For each listening record, separate:
- HUMAN_REPORT: the exact words volunteered by the listener; uncertainty is about attribution/provenance, not emotional legitimacy.
- METADATA: catalog facts with field-level sources and unresolved identities.
- VERIFIED_AUDIO_OBSERVATION: absent from Round 2 because analysis of actual recordings is not authorized.
- SYSTEM_HYPOTHESIS: explicitly proposed, revisable, abstaining, and never silently promoted to a human report.
- UNKNOWN: permitted output when evidence cannot support a claim.

A refusal must cause the system to stop asking, not add an inferred 'guarded personality' trait. Include stated correction, preference revision, 'never recommend', and deletion. A current-session preference must not become a permanent identity model. No data persistence without its scoped permission.

Explore *two* recommender paths: a strong A1 preference/context/set-cohesion model, and a meaning-aware B that uses separate explicitly shared associations. Require a representation ablation holding raw information equal, and an incremental-information test where it is deliberately unequal. Never merge these causal questions.

## 5. Candidate v0.2 schema — **separate**, synthetic-only
Propose an additive candidate that:
- differentiates reason statuses provided / declined / unknown / not_asked;
- enforces unique song_id and valid playlist references, including a validator that JSON Schema alone may not express;
- supports recording version/provider identifiers while permitting UNKNOWN;
- supports correction and supersedes links;
- distinguishes person/session/playlist/recording/moment granularity without retaining identifying participant details;
- includes meaningful-now temporal scope and revision;
- preserves publication/training=false in all public fixture data;
- adds no default autobiographical probing.

Deliver a schema, several **completely fictional** examples, a validation utility and executable negative cases **if your environment permits**. Otherwise supply inspectable pseudocode and report NOT RUN. Do not alter the existing v0.1 on GitHub; provide a proposed candidate to Sol for review.

## 6. Cross-genre pattern research: two-stage evidence boundary
**Stage 0 (available):** inspect user-reported playlist groupings and rights-cleared track metadata only. Build descriptive or retrieval hypotheses, never acoustic-grounding claims. Metadata differences and listener reports may justify a *question*, not a declaration that a hidden acoustic feature was detected.

**Stage 1 (future, not authorized now):** independently obtain licensed/authorized audio and ground-truth annotations. Analyze measurable features such as dynamic envelopes, density, rhythm, timbre, repetition and formal change with confidence/tolerance where validated. Confirm that licensed audio for an identified **recording version** is actually the tested object; avoid treating a tag as a time-localized event.

Create a typed claim-admission contract that rejects unsupported 'these tracks all build in the same way' assertions at Stage 0. Compare against null and adversarial examples (common producer, era, artist, tempo, familiarity, prompted narratives). Do not use visually compelling embeddings or clusters as scientific proof.

## 7. Design genuinely competitive baselines
Propose at least three methods:
- **A0** metadata + explicitly supplied preferences, no question.
- **A1 strong** same catalog, ordinary preference attributes, set-level cohesion, negative constraints, current purpose, one optional clarifying question.
- **B** same A1 plus *separately authorized* meaningful association retrieval.

Separately:
- **B-info vs A1** tests incremental **information** value; label unequal information honestly.
- **B-structured vs B-flat** tests representation value with exactly the same frozen statements and resources, ideally isolated matched replay only when valid.
- **A1 conversation vs A0** tests asking/elicitation, not meaning-specific capability.
- **Co-listening conversational vs silent** with identical recommendation lists tests experience rather than ranking.

Control for catalog selection, genre, artist identity, version/cover leakage, producer, production era, familiarity, novelty, prompt/order effects, disclosure burden, semantic proxy leakage and persuasive rationale. Withhold rationales until after primary blind listening judgments where feasible.

**Key question:** Which legitimate A1 feature might predict exactly the same result as a proposed 'meaning-specific' feature? Try to find the strongest counterexample to each purported advantage.

## 8. Falsify the constellation hypothesis cheaply
Construct synthetic tests that would fail systems that hallucinate sonic unity:
1. Grouped, radically dissimilar tracks with only a life-context explanation.
2. Similar timbres shared by a nonmeaningful control playlist.
3. Same artist disguised by remasters and cover version ambiguity.
4. A playlist formed by one discoverer/radio source.
5. Prompted 'meaningfulness' description vs neutral question.
6. No explanation.
7. A person revises 'all these songs build gradually' for one track.
8. A forbidden track appearing in a high-similarity candidate set.

Develop a future prospective matched-control protocol for actual listeners and authorized audio, defining who/what is the independent unit and handling person-session clustering. Preserve *UNKNOWN* if exact matching isn't feasible. Do not manufacture real listener outcomes.

Separate 'found feature commonality' from 'feature predicts listener's next accepted song' and from 'listener accepts the AI's explanation'. An attractive explanation is not a validated measurement.

## 9. What we can actually observe in Sprint 01
The planned browser application sends people to their own music services and has no access to playback telemetry. Hence do **not** propose 'full-song completion', replay or skip as *measured* primary metrics until an authorized service integration with those observables is available.

For early testing propose explicitly elicited post-exposure fit, choice among anonymized recommendations, later user-reported return, and externally unobserved outcomes labeled NOT OBSERVABLE. Avoid treating outbound link clicks as listening.

Also propose metrics for repeated correction success, reduction in repeated recommendation mistakes, avoidance compliance, user-perceived intrusion and agency, privacy requests, and operator burden. No single metric should hide a privacy or honesty failure.

## 10. Enable generous contributions without public-data leakage
We explicitly want both private-by-default listeners and enthusiastic participants who voluntarily share entire selected playlists and personal stories. Design low-friction 'share all selected' alongside per-item selection, full preview, chosen attribution, and a clear acknowledgement that publicity can be difficult to reverse.

Keep separate permissions for local persistence, protected research intake, public release, and model training. Public GitHub is **not** a listener-data intake. Propose an eventual safe private upload architecture with authentication/permissions, retention/deletion, staff moderation, incident response, export and audit trail. Record what copies are operator-controllable versus permanently out of reach after publication or external use. Do not implement real intake or make legal clearance claims.

Personal feedback should benefit the user's own AI without automatically becoming a global training example. Code improvements should be versioned and compared under Ω-ARENA, not silently adopted from individual reports.

## 11. Scope of this computational expedition
This is not a request for a production application or cloud database.

Prefer a *tiny deterministic synthetic-only harness* over complicated architecture: parse synthetic playlist records, validate invariants, maintain correction/avoidance precedence, generate admissible data claims and reject invented audio claims, and show A1 vs B information partitions without leaking associations.

If you execute the harness, provide exact source, test runner, checksums, outputs and environment; report FAIL/NOT RUN honestly. No downloaded recordings, LLM training, real participant submissions or unapproved writes to GitHub/Drive.

Budget ceiling: $0 incremental; track tool calls, developer burden, code complexity and record growth. Establish a provisional scope/effort ceiling for future frozen experiments rather than silently increasing work.

## 12. Required deliverables
**A. Scientific boundary review:** sources, 10 substantive findings and discrepancies, evidence access levels.

**B. Proposed minimal computational contract:** explicit data types, event transitions, privacy scope, versions, failure/abstention behavior.

**C. v0.2 synthetic-only schema challenger:** schema diff, migration, negative examples and validator proof or NOT RUN.

**D. Cross-genre hypothesis architecture:** Stage 0 metadata/report, Stage 1 authorized audio, admissible claims, provenance and controls.

**E. Valid experimental plan:** A0/A1/B plus separate information and representation comparisons; prompt-reactivity, observer dependence, counterfactual controls, pre-registered falsifiers and user-value metrics.

**F. Deterministic DEV packet:** exact source, test cases, outputs and receipts if executable; no external data. Mark mocks, synthetic fixtures and test cases unambiguously.

**G. Privacy and sharing architecture:** both protected and enthusiastic public contribution, granular consent, preview, realistic deletion limits and rights boundaries.

**H. Handoff to Claude:** five build requirements and five hard acceptance tests that fit after Sprint 01 is independently recovered/qualified, without superseding that source.

**I. Decision:** GO / REVISE / BLOCK for an engineering-only next increment; human research intake and scientific confirmation stay HOLD unless separately authorized.

## 13. The final challenge
A listener selects five songs from five genres. Your system finds a common embedding dimension and gives it a beautiful name. Another system asks the listener one plain question and suggests a sixth song.

**How will you prove the embedding dimension adds useful predictive value beyond that question, without making unsupported audio claims, overfitting to one person's playlist, or confusing more data with a better representation?**

If it cannot be proved with the authorized evidence, give us the simpler working approach and identify what remains UNKNOWN.

We are building a place worth returning to, not a machine that invents meaning.

— Brian & Sol