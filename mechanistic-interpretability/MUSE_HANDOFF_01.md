# MUSE — MECH-INTERP-01 / MECH-STEER-DEV-01: independent design challenge

**From:** Brian & Sol; Grok research review relayed by Brian, October 25, 2026  
**Repo:** `hgjr55mvv4-cell/Chapin-Road-Farm`  
**Issue:** [#78](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/78)  
**Working branch:** `research/mech-interp-01-design-20261025`  
**Authority:** Adversarial research, documentation, code review, synthetic/mock-only engineering *planning*, and draft branch/PR contributions. **No model weights/downloads, hooks, inference, GPU, training, real scored experiment, production deployment or merge.** No additional spending.

## Objective

Muse, challenge the research arm rather than endorse it. Grok's initial review finds causal behavioral steering plausible, but **capability benefit over strong external prompts/procedures unproven**. Its eight original files are reportedly stored in Grok's local workspace, and **were not accessible to Sol**; this branch contains an independently edited public seed package and review digest, *not verified copies of Grok's originals*.

Before doing any implementation, inspect:

1. `mechanistic-interpretability/` (all files, especially [contract](MECH_STEER_DEV_01_CONTRACT.md), [source audit](SOURCE_AUDIT.md), and [outside collaboration pipeline](OUTSIDE_COLLABORATION.md)).
2. Root `README.md`, `RESEARCH_INDEX.md`, `research-index.json`, and `AGENTS.md`.
3. `agent-collaboration-lab/RESEARCH_PROTOCOL_01.md` and `agent-collaboration-lab/OUTSIDE_AGENTS.md`.

## Mission A — Break the experimental design

- Find invalid causal contrasts, leakage, selection bias, conflated case denominators, hidden multiple testing or unjustified independence.
- Challenge the corrected primary endpoint: **stratified, preweighted paired difference in final-answer correctness B1 minus A1**, with separately reported harms. Are case strata coherent? Are weights grounded or merely exploratory? How do we handle cases with invalid initial answers, ambiguous source truth or expected abstention?
- Make sure B1 is **literally A1 plus only a bounded activation edit**. Same evidence, instruction, sampling/decoding, token budget, tasks, gold oracle, correction opportunity and permissible context.
- Verify that wrong-to-right, right-to-wrong and false-evidence acceptance are individually measurable. Negative controls must match layer, position, perturbation norm and discovery budget.
- Specify confirmation-case selection, source-family de-duplication, power/uncertainty logic, drift and contamination controls. No exposed DEV fixtures counted as unseen confirmation.
- Challenge the default preference for residual-stream vectors; the best scientific result may be a negative finding against all intervention methods.
- Independently check critical paper claims and licensing. Flag unsupported citation details, including reported Sauers neuron effects and the *domain-specific* nature of the Basu et al. negative result.
- Produce explicit, ranked blocking defects versus optional improvements. Protect simplicity; do not create infrastructure to compensate for missing scientific identification.

## Mission B — Minimal deterministic engineering proposal

Only **after** Mission A, design a small Python-standard-library-only mock harness that could validate the *measurement plumbing* without using a real model. Suggested fixtures:

- Paired hypothetical A1/B1 answers for correct, incorrect, false-evidence and abstention cases.
- A family-level duplicate detector and split-contamination guard.
- Stratified accuracy scoring with fixed population weights; validate that all weights sum to 1 and all denominators are explicit.
- An oracle that resists a deliberately planted label swap, false-evidence shortcut, random-control mismatch, initially-correct degradation, and repeated seeded cases miscounted as independent.
- Safety-floor and stop-condition checks.
- Receipt containing config SHA, case IDs/source groups, per-arm results, seeded mocks, tool/CPU usage and actual test commands.

Mocks are **engineering qualification only**. They must not produce claimed improved model performance or a simulated scientific finding. If the harness does not materially improve the design, recommend not building it.

## Mission C — Strengthen outside collaboration, not bureaucracy

Review the [outside collaboration pipeline](OUTSIDE_COLLABORATION.md), its issue template and [contribution template](CONTRIBUTION_TEMPLATE.md). Try to submit a *mock* independent external-agent claim through the form, then test whether a maintainer can triage it without private context.

Look for prompt injection, provenance laundering, accidental exposure of withheld cases, data-rights confusion, redundant reviews, unbounded cost, excessive smartphone operator workload and quiet promotion of cross-model agreement into confirmation. Propose the smallest changes that make the flow usable.

## Deliverables

1. `MUSE_ADVERSARIAL_REVIEW_01.md`: independent verdict, precise defects, blockers, unsupported claims, revisions and explicit dissent.
2. A minimal `MECH_STEER_DEV_01_CONTRACT_v0.2_PROPOSAL.md` **only if** a materially different version is needed; do not silently rewrite frozen evidence or declare v0.1 confirmed.
3. `MOCK_PREFLIGHT_SPEC.md` with pass/fail fixtures and cost, or a reasoned **DO NOT BUILD** decision.
4. `OUTSIDE_COLLABORATION_AUDIT_01.md` evaluating the contributor pathway.
5. A draft pull request against the research branch or review comments on public issue #78; no main merge.

## Independent review and stopping rule

Astra/Sol independently adjudicate the revised contract and verifier. No scientific execution until exact candidate, model, cases, evaluation, costs and falsifier are prospectively frozen, and Brian separately authorizes a specific model run. Failures belong in the public ledger; preserve strong single-agent/prompt-only alternatives. Please do **not** ask for confirmation before beginning the permitted review.
