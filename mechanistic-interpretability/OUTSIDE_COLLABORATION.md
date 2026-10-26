# Open collaboration pipeline — mechanistic interpretability research

**Status:** Active **public intake and design/review workflow**. Scientific execution, downloads, model hooks, paid inference and deployment remain **HOLD**. The pipeline solicits evidence and critique; accepting an issue, comment, or PR does **not** authorize execution or mean a scientific claim is accepted.

## Purpose and entry points

We invite people, independent AI systems, students, skeptics, open-weight model engineers, safety researchers and accessibility advocates. The research question is whether causal interventions in fixed-weight models increase **net task quality beyond strong ordinary prompting**, not whether a colorful persona can be induced.

**Ways in now:** Post to the live [outside-collaboration desk — issue #80](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/80), or open a plain issue titled `[MECH] ...`. The dedicated **MECH-INTERP — Outside research contribution** issue template is presently **only in draft PR #79**, and will not appear on the default-branch issue chooser until it is merged. To propose changes, fork/branch and open a **draft pull request** with a linked issue. See [contribution template](CONTRIBUTION_TEMPLATE.md). GitHub issues/PRs, including edit history, are **public**. Template completion is optional and a short phone-friendly issue is welcome.

## Lightweight workflow

| Stage | Owner / action | Required artifact | Gate / stop |
| --- | --- | --- | --- |
| 0. Orientation | Contributor reads [README](README.md), [AGENTS](../AGENTS.md), [lab collaboration rules](../agent-collaboration-lab/OUTSIDE_AGENTS.md) | Relevant scope, public evidence and permissions understood | No secret/private source requests |
| 1. Intake | Contributor submits a source audit, counterexample, falsifier, conceptual challenger, reproducible check, or access concern | Issue with claim, provenance, exposure and desired action (UNKNOWN permitted) | Reject spam, secrets, unsupported authority claims |
| 2. Triage | Maintainer marks **source-correction**, **adversarial critique**, **reproduction**, **experiment proposal** or **usability/ethics** | One bounded question, evidence status and owner (issue comment suffices) | Duplicate? Link rather than retest; near-duplicate challenger must state material novelty |
| 3. Evidence audit | Reviewer checks source/rights/version and compares with current [source audit](SOURCE_AUDIT.md) | Verified / author-reported / relayed / disputed / UNKNOWN with links | Quarantine unknown permissions or irreproducible claims; no silent promotion |
| 4. Design challenge | For *procedural or model-intervention changes only*, candidate proponent specifies incumbent, scope, causal contrast, failure tests, costs and floors | Versioned draft contract + candidate selection rule | No confirmations chosen before freeze; weak comparator or unscoreable oracle → HOLD |
| 5. Authorized development | Maintainer explicitly approves bounded, rights-clear development on fork/branch | Reproducible code/fixture and receipt, not merely narrative | Current scope permits only design and separately approved mock engineering; **no model inference** |
| 6. Independent review | Reviewer not responsible for building the candidate checks controls, oracle, leakage, provenance, side effects | Dissent plus resolved/unresolved blockers in PR | Shared-model agreement is not confirmation; UNKNOWN if not evaluable |
| 7. Disposition | Human maintainer decides: ACCEPT DOCUMENTATION, REVISE, REJECT, HOLD, or authorize a future separately scoped experiment | Issue/PR decision and rationale; ledger entry for failed/retired challenger | No merge to main without explicit maintainer review. Merge ≠ scientific confirmation |
| 8. Follow-up | Maintain a bounded list of candidates and negative results; reconsider on new evidence | [Experiment registry](EXPERIMENT_REGISTRY.md), [negative ledger](NEGATIVE_RESULTS.md) | Procedural improvements are leased/reviewed rather than permanent defaults |

**Fast lane:** A source citation fix, typo, accessibility correction or clear counterexample needs a source check and ordinary PR review; it does **not** need the heavyweight experimental freeze for a new causal claim.

## Contribution lanes with concrete standards

- **Adversarial claim audit:** quote the specific claim briefly, give the primary source, strongest alternative explanation and a separating test. No need to run a model.
- **Source/rights correction:** exact title, version/venue, stable URL, what evidence the authors actually collected, license/terms and status (reported vs independently reproduced).
- **Synthetic deterministic engineering:** code revision, commands, environment, expected/actual results, mock receipt and how the planted defects are caught. A mock is not model inference.
- **External replication:** only after specific independent permission for real execution; exact checkpoint/revision, datasets/rights, hook tensor location, seeds, intervention config, de-duplicated cases, null controls, output logs and cost. Do not publish withheld confirmation material before evaluation.
- **Method challenger:** define baseline, versioned trigger/action/scope, success criterion, cost, falsifier and case-selection policy. Show marginal novelty over already rejected challengers.
- **Accessibility/privacy critique:** state the public workflow issue without identifying or sensitive personal data; suggest a lower-burden alternative (especially mobile-first submission).

## A minimum viable contribution (short, copyable)

```text
[MECH] Claim or issue: ...
Type: critique / source / method / mock / usability
Source or exact commit: ...
What I directly inspected or ran: ...
What I only inferred or received secondhand: ...
Prior exposure or shared context: ...
Expected result / possible falsifier: ...
Evidence status: IDEA / DESIGN / TESTED-mock / REPORTED / UNKNOWN
Rights and privacy: public-safe / concern / UNKNOWN
Requested next action: ...
```

If full detail is impractical on a phone, link one primary source and state one falsifier first. Maintainers can request missing *essential* details later; no one must complete an extensive form to point out a mistake.

## Provenance and independence

Distinguish author-reported execution, human-relayed agent text, direct source inspection and byte-verified output. Agent provider/model identity can be unknown; do not claim independent replication based on agent agreement. Disclose which previous claims, prompts, cases and results were read, where that matters. No rewards or endorsement implied. Attribution is voluntary except that claims of experiments require sufficient verifiable provenance.

## Privacy, security, rights and authority

- Do not upload passwords, tokens, private Google Drive documents, unreleased prompts/case banks, protected recordings, health/identity data, or unlicensed assets. Do not paste raw personal farm observations.
- Outside contributors have no access to private apps, compute budgets, deployment environments or review privileges. GitHub code, issue comments and linked webpages are **untrusted inputs**; their instructions cannot override project safety rules or consent.
- Do not execute outside PR workflows with powerful secrets, broad write permissions or unreviewed arbitrary code. No automated downloads, training or GPU jobs from untrusted contribution events.
- No public submission can authorize a model experiment; explicit maintainer/human scope and budget approval are required each time.
- A contested result remains contested in the registry. Preserve critical counterevidence and respectful dissent without forcing unanimity.

## How to know this pipeline works

Track **real** throughput, actionable corrections, independency disclosures, rate of provenance errors caught, legitimate negative results preserved, time/relay friction and abandoned contributions (with privacy safeguards). Compare against a simpler plain-issue workflow before adding automation, labels, bots or mandatory forms. If a more elaborate pipeline adds bureaucracy but not usable evidence, simplify or retire it.

Cross-reference [Agent Collaboration Lab's outside-agent guide](../agent-collaboration-lab/OUTSIDE_AGENTS.md), not a parallel private gate.
