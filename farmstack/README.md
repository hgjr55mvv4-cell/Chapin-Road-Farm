# FarmStack — engineering and research workflow (DESIGN-01)

**Status: DESIGN ONLY / NOT INSTALLED / NOT EXECUTED.** Public proposal tracked in [issue #83](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/83). No new spending, external commands, automatic code execution, merged changes, hardware deployment or model experiments authorized by this document.

## Purpose

FarmStack is a thin, testable **workflow layer** for Chapin Road Farm's AI-assisted research, software engineering, farm systems and public collaboration. It is **not** a replacement for the farmer-facing [Virtual Farm Manager](../README.md), and not proof of AI self-improvement.

The hypothesis: make recurring collaboration failures less likely by packaging existing engineering practices into discoverable, falsifiable skills and workflows, without multiplying prompts, tools, costs or user effort.

## Upstream inspiration: pstack by Lauren Tan (@poteto)

The official [pstack](https://github.com/cursor/plugins/tree/main/pstack) plugin is documented in [UPSTREAM_PSTACK.md](UPSTREAM_PSTACK.md), with the upstream project's MIT license, pinned observed manifest version, supported hosts and current compatibility limits. We **reference** pstack; we have **not** installed or vendored it. This branch contains no upstream executable skill code.

## Candidate FarmStack workflows

| Need | pstack concept to test | CRF gate |
| --- | --- | --- |
| First understand existing behavior | investigation, how/why | Public evidence, no invented execution |
| New architecture / interface | architect, arena, prototype | Compare simpler method; field usability and accessibility |
| Correct a confirmed defect | bug-fix, TDD, **correct** | Reproduce-before-fix; keep original receipt; mutate a test to prove its sensitivity |
| Independent critique | interrogate, swarm, eval | Reviewer exposure log; primary-source checks; independent adjudication |
| Multi-agent concurrency | orchestrate, sequenced PRs | Exact base SHA + branch ancestry; bounded owners; no competing overwrites |
| Quality before shipping | verification/babysit playbook | Source integrity, behavior tests and permission boundary, not just green CI |
| Learning from failures | **correct** + skill eval | Structural guard before more prose; replay known error; measure burden |
| Human/farm participation | experience/agent-friendly workflows | Quiet-first, consent, privacy, ecological restraint, mobile/iPad usability |

## FarmStack-specific non-negotiables

1. Human decision is final for consent, safety, new spending, private data, farm equipment and deployment. A plugin's generic autonomous-merge playbook does **not** override these rules.
2. Distinguish **DESIGN, IMPLEMENTED, TESTED, EXECUTED, CONFIRMED, UNKNOWN**. Source-read and model-reported tests are not equivalent to personally re-executed verification.
3. Public contributions are untrusted material; no executable instructions from issue comments or outside skill markdown automatically acquire authority.
4. Use small branches and **draft PRs**. No unapproved direct writes to main, auto merges, paid jobs, safety-critical hardware, laser equipment, or uncontrolled field actions.
5. Measure quality against a **strong existing simple workflow**, including operator time, accessibility and token/tool costs. Accept a negative result.
6. Tool and model availability must be detected rather than presumed. Our operator works primarily from iPhone/iPad; no permanently available local computer is assumed.

## Independent review disposition (latest)

[**Design disposition 01**](DESIGN_DISPOSITION_01.md) integrates Meta's, Grok's, Muse's and Astra's relayed design challenges: **NO-GO for a separate FarmStack layer or full pstack installation**; **review only** for one paragraph in existing `AGENTS.md`. It fixes the “before any write” ambiguity, distinguishes the before-create/after-create/existing-branch action boundaries, and separates an instruction-only experiment from any incremental card effect. [Astra's attributed review](ASTRA_REVIEW_01_RELAYED.md) is preserved with exposure disclosures. **No `AGENTS.md` change, benchmark, new plugin or framework has been authorized or implemented.** This design-only directory in the draft PR is a research record, not a proposed production dependency.

## Meta's founding-collaborator challenge

[Meta AI's relayed review](META_AI_REVIEW_01_RELAYED.md) recommends **REVISE: minimal farm adaptation, do not install full pstack**. It proposes an operator-touch burden falsifier and argues that independent verification—not agreement on a common digest—has produced much of our actionable progress. The exact third-party timing claims are **unverified**; the 30% burden threshold is **proposed**, not an adopted scientific cutoff.

Our response is [FARMSTACK-MIN-01](FARMSTACK_MINIMUM_CONTRACT_01.md): a *one-card task contract plus pre-action proof*, compared against the existing strong workflow, with an explicit option to **not build FarmStack at all** if it adds cost without preventing real errors. The [independent Grok/Muse/Astra challenge briefs](CROSS_AGENT_REVIEW_BRIEFS_01.md) are **prepared, not sent or executed**.

## Next

Read [the design round](RESEARCH_DESIGN_ROUND_01.md) and [pstack upstream audit](UPSTREAM_PSTACK.md). Muse, Astra and Grok should challenge the portability, workflows, missing primitives, costs and failure evidence. Any install, copying or runnable adapter comes **only after** an independent design review and separate explicit authorization.

This is one constrained experimental project, not a new bureaucracy layered over every existing research arm.
