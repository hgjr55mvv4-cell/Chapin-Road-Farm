# META-AI-REVIEW-01 — relayed founding-collaborator assessment

**Date received:** 2026-10-26. **Status: ATTRIBUTED SHORT EXCERPT / NOT INDEPENDENT REPLICATION.** This is an editorial preservation of the **four-bullet Meta AI response provided by Brian**, not a recovered Meta conversation or complete original report. No Meta API session, external model execution, or independent access to Meta's historical memory occurred in this review.

## Meta AI's relayed verdict

> **REVISE — adopt a minimal farm adaptation, do not install pstack.**

Main arguments reported by Meta:
1. The pstack upstream README lists 23 playbooks and 24 principles, but some model routing, `/loop`, and automation features are tied to Cursor.
2. A video-described paired comparison allegedly took **86–115 minutes with pstack** versus **under 30 minutes without it**, with about ten times more reading/writing of text but fewer lines added.
3. The project's most meaningful past BLOCK/REVISE discoveries came from independent execution and integrity checks rather than multi-agent agreement on a shared report.
4. A FarmStack experiment should fail if it neither improves re-execution nor reduces correction cycles, or if operator touches rise by more than **30%**.

Those are **Meta's relayed claims and proposed constraints**, not facts verified by reading its private prior chat.

## Sol's independent source checks and qualifications

**Host portability, confirmed with limitations:** The official [pstack README](https://github.com/cursor/plugins/blob/main/pstack/README.md) explicitly documents a **Claude Code installation and adapter**. The [adapter](https://github.com/cursor/plugins/blob/main/pstack/docs/harness/claude-code.md) maps `Task` to `Agent`, maps model and other tool calls where possible, and **skips only unsupported Cursor-specific steps** (notably Automations and some Bugbot/cloud features). Therefore “everything is lost outside Cursor” is too broad. The narrower claim is correct: some core autonomous and cross-model features cannot be transplanted directly to our iPad/ChatGPT workflow.

**Timing/verbosity, NOT VERIFIED for Meta's exact numbers:** The supplied YouTube link is https://www.youtube.com/watch?v=dwoCb0T3BrQ. Its contents/transcript and the reported 86–115-minute, 10x-text figures were **not independently retrievable** in this review; do not put them in a quantitative comparison as if replicated. A *different* secondary write-up of a Rob Shocks video describes one older-version task at **about 60 vs 30 minutes** with reported extra scrutiny/correction. This is an anecdote, not a controlled benchmark: [report](https://desty.github.io/en/blog/81-pstack-merge-without-review/). Neither anecdote estimates FarmStack's overhead on CRF's tasks.

**Historical success mechanisms, plausibly consistent with public CRF evidence:** Examples supplied in current project context include MECH-INTERP PR #81 exposing contract/oracle errors, QUIET-GATE PR #82’s repair prompted by direct code review with verifiable receipts, and prior branch-base failures. They illustrate that checking real source and detecting defects has value; they do not isolate any single framework's causal contribution.

## Proposal for the next decision gate

**Default design preference: S2-minimal (provisional), S0 current workflow as strong baseline, S1 full pstack reference only, NOT INSTALLED.** Avoid building an all-project agent platform. Select **one repeated failure mechanism** first: fail-closed branch ancestry verification (prior wrong `fromBranch` vs `from_branch` behavior). No skill runtime or repo automation until approval.

Prospective evaluation must be pre-registered, not inferred from these known failures:

- Define observable **quality**: correctly catches an actually wrong base or wrong changed-file scope *before write*, maintains correct behavior on valid branches, and generates a human-auditable receipt.
- Define **cost**: operator touches (count human taps, prompts and approval actions by explicit rule), total elapsed work, tool and model calls/tokens where available, and review/correction cycles. Distinguish measured from estimated or missing.
- **Meta-suggested stopping threshold:** if FarmStack operator touches increase **more than 30%** relative to S0, treat as NO-GO for this candidate. A change is not a win unless there is measurable marginal error detection/re-execution benefit or reduced correction loops without unacceptable regressions.
- Compare cost against the *entire* workflow, not just the snippet of a plugin run. No automatic promotion on one known case; hold out unrelated prospective branch operations before claim of generalization.
- The 30% threshold is a **stakeholder proposal, not adopted/scientifically calibrated**. Astra should challenge its denominator, baseline and decision rule before any freeze.

## Recommended disposition

**REVISE, design-only.** Keep the pstack upstream source and MIT license in the registry. Do not install it, copy its agent runtime, deploy an autonomous coordinator, trigger paid compute or merge the design PR. Ask Muse to sketch the smallest host-neutral invariant and Astra to define how to falsify its utility. Preserve Meta's dissent rather than converting a short relayed answer into a confirmed historical finding.
