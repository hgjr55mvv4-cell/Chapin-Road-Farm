# FarmStack Design Round 01 — coordinated independent review briefs

**Status: ASSIGNMENTS PREPARED, NOT SENT.** Do not imply that an agent received or executed these briefs. Brian can relay an individual brief to the existing Muse, Astra and Grok conversations. No backend accounts, new model downloads, plugin installation, code implementation, merge or deployment is authorized. Additional spend: $0.

All reviewers should begin with public issue [#83](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/83), draft [PR #84](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/84), and the [minimum contract](FARMSTACK_MINIMUM_CONTRACT_01.md). The [Meta AI excerpt](META_AI_REVIEW_01_RELAYED.md) is *shared evidence*; each reviewer must disclose whether they read it before forming their verdict. Do not infer independent empirical replication from consensus.

## GROK — primary-source pstack compatibility and overhead skeptic

Investigate the actual upstream [pstack](https://github.com/cursor/plugins/tree/main/pstack) source at a **specified revision**, not just the latest README. Inventory the *smallest* skills that plausibly improve CRF's real failure modes: `correct`, investigation, bug fix, source/review interrogation, verification. Identify installed-only assumptions, Cursor vs Claude Code adapter behavior, reliance on Task/Agent or model slugs, hidden auto-merge/loop/automation prompts, generated harness copies, dependencies, credits, security and MIT attribution.

**Falsification assignment:** Find the cheapest pstack-compatible host-native setup that could beat S2A. If it cannot run on the actual accessible environment without unacceptable effort, report that honestly. Inspect Meta's linked time/verbosity anecdote only if verifiable; do **not** repeat a secondhand benchmark as measured. Output: source map, real compatibility matrix, minimal 2- or 3-skill selection, independent dissent, **GO/REVISE/NO-GO**. No installation.

## MUSE — engineer, source-level architecture skeptic

Independently challenge the [one-card contract](FARMSTACK_MINIMUM_CONTRACT_01.md) against current GitHub adapter behavior. Does it catch a branch accidentally based on main, a correct branch with wrong filenames, or a test reported as run but never executed? Could the entire thing fit in *one existing AGENTS.md subsection* without a new FarmStack directory? Compare S0, S2A and S2B; avoid implementation at this stage.

Provide two *minimal* competing sketches and a plain-language failure case for each. Specify how a fail-closed branch-base check could be verified against a benign wrong-base fixture with no unapproved repository mutation. Ensure it cannot block all valid branches and falsely earn a “safe” label. Report likely operator burden on an iPhone/iPad as estimate unless actually measured. Output: **one small architecture decision and a DO NOT BUILD option**, no code.

## ASTRA — independent protocol architect and falsifier

Do **not** inherit Meta's proposed 30% operator-touch cutoff as truth. Independently design the test of S0 vs S2A (S2B conditional), beginning with failure classes and prospective case selection. Freeze an objective primary benefit metric, false-block floor, exact touch counting rule, resource ceiling, case-family independence, assessor blinding, null controls, and explicit minimum evidence before claiming success. Propose an evaluation that could show S0 is sufficient, or that extra process reduces performance.

**Critical checks:** Design cannot use the two already-known wrong-base incidents as confirmation, cannot count correlated prompt variants as independent, cannot cite checksums as outcome proof, cannot treat unaudited AI self-reports as execution. Could a simpler rule in AGENTS.md win? If so, conclude NO-GO for S2B. Output: short falsifiable protocol, unfilled gates, hard stopping conditions, independent exposure disclosure. No scored agent execution authorized.

## SOL — reconciler and gatekeeper (role description only)

After individual responses arrive, compare primary-source evidence, resolve terminology, preserve dissent in the registry, and choose the **smallest** candidate deserving a separately authorized engineering preflight. Public improvements move via issue/draft PR with exact ancestry and readback; never declare a full plugin installed from a registered source entry.

## Common answer format — one screen first

1. **Verdict:** GO / REVISE / NO-GO, and the simplest solution that might work.
2. **What I verified:** exact source paths, version and commands actually run (or NOT RUN).
3. **One blocker and one counterexample:** what would change the verdict.
4. **Cost:** human touches, runtime/model tokens when actually measured, otherwise UNKNOWN/estimate.
5. **Next bounded action:** no future work assumed, no implicit merge/install authorization.

Append detailed methods or evidence only if necessary. Do not create a broad “FarmStack platform” implementation roadmap that presupposes a successful experiment. Reviewers may recommend abolishing the proposed new layer if its pieces belong in existing AGENTS.md and CI.
