# FARMSTACK-MIN-01 — smallest testable workflow, not a plugin

**HISTORICAL SUPERSEDED DESIGN CANDIDATE.** The current [design disposition](DESIGN_DISPOSITION_01.md) supersedes its ambiguous “before any write” wording, the two-arm S0/S2A comparison and the conflicting 30% burden rule. Retained unmodified below for research provenance; do not adopt this candidate as operational practice.\n\n**Status: DESIGN / UNADOPTED / NOT EXECUTED.** Draft discussion seeded by Meta AI's user-relayed REVISE verdict, October 26, 2026. No code, no plugin installation, no main merge, no software or model execution, no paid resources, no deployment, no new automated permissions.

## Hypothesis in one sentence

A **small pre-action proof and post-action receipt**, fitted to the existing CRF GitHub process, can prevent a recurring, independently observable error without creating more human work than it saves.

A longer prompt is **not** by itself FarmStack. A passing self-report is **not** verification. The simplest acceptable winner could be **S0 (do nothing)**.

## Architectural choices (candidates, not yet a decision)

| Candidate | What is added | Strength | Risk / why it could lose |
| --- | --- | --- | --- |
| **S0 — incumbent** | Existing AGENTS.md, issue → draft PR, independent verification | Already works; near-zero new overhead | Repeated wrong-base branches escaped before direct checks |
| **S1 — upstream reference** | pstack where actually supported; no vendor/fork; installation separately authorized | Mature task playbooks and correction approach | Host dependence, latency, many procedural steps, cost, unattended auto-actions |
| **S2A — paper-thin FarmStack** | One compact task card and one checkable receipt, existing GitHub primitives | Portable to iPad, GitHub connector, multiple agents | Human-dependent; may merely duplicate good practice |
| **S2B — tiny guard candidate** | S2A + **one** deterministic fail-closed base/scope check | Prevents a repeat failure before any write, in principle | Requires a trusted runtime, maintenance and implementation permission; may catch no new cases |

**Default for design challenge: S2A.** S2B is an *escalation only if* S2A cannot robustly catch a known failure and an accessible, low-cost execution host exists. Do not call it “installed FarmStack.”

## The one-card contract — shared by any agent, maintained in the task thread

No required new account, dashboard, form, task database or plugin. A single short block is enough:

```text
FARMSTACK-01 | task <id> | DESIGN/IMPLEMENTED/TESTED/UNKNOWN
GOAL: <one externally checkable outcome>
BASE: <repo + exact target branch/ref; exact expected base SHA when relevant>
SCOPE: <allowed paths and actions; explicit HOLDs>
PROOF: <what would falsify completion; direct readback/re-execution or honest NOT RUN>
COST: <human touches, model/tool calls if measurable, time; record UNKNOWN otherwise>
END: PASS / REVISE / BLOCKED with evidence, outstanding debt, next owner
```

The contract is **not** a gate for sharing a small observation, reporting a typo, or pausing safely. No extra operator interaction is required to fill it: the agent writes it from already-available instructions.

## A single critical invariant before repository writes

A branch write or PR is **not** “delivered” until the agent checks and records:

1. The exact target branch and its SHA **as observed, not assumed**.
2. The branch's actual common ancestor / merge base, and any intervening changes.
3. The candidate's changed path list compared to the authorized scope.
4. Readback of relevant committed bytes/links, and whether tests are **actually run**.
5. `draft = true`, `merged = false`, and explicit HOLDs not silently lifted.

**Fail closed** on wrong base, unknown ancestry, missing/refused read, changed scope, failed checksum, or unfrozen scientific metric. The check must occur **before** any risky downstream PR/push or promotion when possible. If a plugin/connector's argument name is silently ignored (the observed `fromBranch` vs `from_branch` failure), trust an inspected branch ancestry rather than a successful creation response. No generic GitHub command in these docs authorizes a write.

## Scientific claims are a separate gate

A model says “I ran 28/28 tests” → **author-reported execution** until a reviewer inspects a receipt, and **independently re-executed** only when the reviewer actually reruns the command. Checksums establish *integrity*, not scientific validity. Shared-source reviewer agreement is not independent empirical replication. An experiment's conclusion needs its own frozen estimand, oracle, cases, controls, cost, falsifier, and independent adjudication.

Avoid making one “PASS” badge erase these distinctions. Engineering PASS, accessibility PASS, model-confirmation PASS and production approval are different things.

## First experiment proposed (not authorized to execute)

**FARMSTACK-GATE-DEV-01 — branch ancestry/scope.** Motivation: twice a collaborator reported a new branch started from `main` because the branch-creation tool ignored a misnamed `fromBranch` parameter. Existing independent review caught this. The experiment must ask whether a *simpler* preflight would catch it earlier with fewer operator interventions.

**DEV fixtures:** sanitized, replayable synthetic scenarios modeled on the two known failures: (a) wrong base that the tool call returns “success” for, (b) correct ancestry, (c) intended base advanced concurrently, (d) changed files exceed scope, (e) missing read permission, (f) no change or abandoned empty branch. Historical real PRs are **known training cases**, not confirmation data.

**Compare with a strong incumbent:** S0 agents receive the actual existing AGENTS.md instructions and ordinary independent review; S2A agents receive the **same evidence** plus this one-card contract. S2B is a separate later arm only if a real guard runtime is approved. Do not give a challenger unique access to correct branch metadata.

**Provisional measures:** per case, (1) detection of wrong base *before any write*; (2) valid-branch false blocks; (3) number of independent correction loops; (4) operator touches; (5) total model/tool calls and elapsed time; (6) actual direct evidence vs relay. For real errors, include wrong-base escape as a critical failure regardless of speed.

**Case independence:** group by root failure mechanism, not by how many seeded prompts repeat it. Hold out independent variation in base movement, branch state and scope, with an unknown-case rule. Do not use the already-public two failures as blind confirmation.

**Meta's proposed cost falsifier:** reject if operator touches rise **>30%** against S0 with no commensurate error-detection/correction benefit. This is **not frozen**. “Touch” must be defined first (proposed: one distinct, necessary human prompt/approval/upload/device action to keep the task moving; automated reads are not touches). Report integer counts, paired differences, zero-baseline cases and task variability. Do not infer ratios from a few tasks or cherry-pick durations.

**Scientific decision rule: UNFROZEN.** Astra must define sample size, error/harm floors, time/cost ceiling, independent scoring and stopping *before* prospective tasks are drawn. Missing evidence → UNKNOWN, not victory.

## What FarmStack deliberately should not become

- A 23-playbook clone, multi-model subscription requirement, mandatory user form, agent swarm by default, scheduled “keep running” process, new persistent farm-person data store, automated merge pipeline, or system that can silently relax human HOLDs.
- A farm operations product built in parallel to VFM, or a rule that every field observation must become a measurable intervention.
- A justification to replace primary scientific evidence with consensus, fancy receipts or screenshots.

**If one deterministic rule prevents repeated branch-base mistakes, that may be enough.** If even that adds more burden than it saves, retire FarmStack as a separate layer and keep the good rule directly in AGENTS.md or a test.
