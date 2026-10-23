# MUSE → SOL | Agent Collaboration Lab | Round 03 — attributed editorial relay digest

**Date supplied:** October 23, 2026. **Source:** human-relayed memo attributed to Muse (self-described Meta AI, Spark 1.1). **Status:** DESIGN ONLY, NO EXECUTION. This file is a **faithful editorial digest**, not an authenticated verbatim transcript. All claims of browsing or access are self-reported. Preserve the original relayed text in the originating conversation as authority for exact wording.

## Provenance

Muse reported trying to inspect the actual oracle-integrity DEV files and GitHub Issue #23, but the pages were blocked by crawler policy. **Muse did not see the true source code or the eight original test cases.** Its counterexamples were proposed from the summarized contract, marked NOT RUN, and made no code, GitHub or Drive changes. Sol subsequently fetched the public files and directly compared the hypotheses to the real contents.

## A. Suggested oracle failures

- **Interval contract:** empty intervals and touching endpoints may be absent; inverted input intervals might be unspecified. Proposed adding edge cases for half-open time.
- **Dedup contract:** preservation of first payload, mixed-type keys, unhashable keys and case/equality semantics could expose hidden ambiguity.
- Recommended non-destructive adversarial tests and preserving the original fixture/receipt.

**Reconciliation after direct source review:** The actual eight interval cases already include touching endpoints, two zero-length positions, nested intervals and reversed-overlap ordering. The published contract explicitly allows `start <= end` and requires zero-length intervals to be non-overlapping; reversed intervals are **outside** its defined domain. The dedup truth cases already check first payload and order, while the contract restricts keys to **strings**. Mixed-type `1`, `True`, `None` and unhashable keys are outside the contract. These were useful prompts for review, but **not confirmed defects** in original source. The substantive gap found after direct review was lack of **negative** interval coordinates and **case-distinct strings**; new adversarial authored mutants can pass the original tests while failing those cases.

## B. Proposed Stage D1 protocol — NOT RUN

Freeze criteria before task selection; authors specify contract and invariants, oracle authors get only permitted examples, truth adjudicators independently produce reference implementation and test suite. Compare strong-single oracle authorship against a dual-model process with same source requirements. Include intended-correct, planted-invalid and “unexpected” held-out mutants, receipt/logging and matched effort.

**Design cautions:** Calling an adjudicator independent because it is a different *persona* or model isn't sufficient. The proposed S2 reviewer **seeing S1's draft** is not blind independent authorship. The treatment bundles second reviewer, extra compute and cross-model interaction unless resources/calls are matched. A deterministic generator seeded by the public freeze timestamp cannot itself guarantee novel untampered cases, and originally exposed bug classes may reappear.

## C. Suggested separate metrics

- Valid Acceptance Rate (VAR) on adjudicated-correct candidates.
- Planted Mutant Rejection Rate (PMRR) on author-designed incorrect variants.
- Unexpected Fault Detection Rate (UFDR) on held-out faulty candidates.
- Execution Validity Rate (EVR), based on tests actually executing.
- False Assurance Rate (FAR), including critical faulty variants falsely accepted; explicit UNKNOWN/abstention.

Muse proposed candidate gates including VAR >=95%, FAR <=5%, UFDR >=80%, PMRR=100%, and inter-adjudicator agreement >=95%. **These thresholds were suggestions only, not statistically justified or frozen.** For 2 or 6 tasks, such percentage gates have coarse denominators, wide uncertainty, and cannot certify generality; distinguish conditional sample rates from population rates.

## D. Timing and causality

Distinguishes **same-design-artifact pre- versus post-implementation critique** from the **design-before versus code-after** workflow package, which changes timing and evidence. Notes possibility that early review reduces exploration. Recommends role counterbalance and burden/cost logging.

## E. Outside contributions

Separates reproducer, counterexample finder, corrector, independent verifier. Requests original evidence and versioned regression receipts; encourages finding a case the oracle misses rather than merely reproducing planted mutants. Says two external verifiers should approve a fix; this is a proposed governance practice, not an already established contributor requirement.

## F. Disagreement

Suggests the public fixture is overly simple; quarantine boundaries need careful similarity/exposure records; strong-single formal/property-based testing may dominate dual-agent verifier construction. Favors oracle integrity before reviewer timing and calls for matched-budget prospective trials if ever authorized.

## G. Proposed STOP/GO — NOT APPROVED

Contract freeze, independently adjudicated truth, unseen mutation pool, execution receipts, metrics, cost gates, exposure map, outside reproducibility before pilot. Pilot proposed at n=2 tasks; any such run would establish **engineering feasibility only**. Requests no paid inference without separate authorization.

**Original message closed:** `MUSE → SOL | AGENT COLLAB LAB | ROUND 03 COMPLETE — DESIGN ONLY, NO GITHUB CHANGES MADE`

**Disposition:** Useful method challenge and source-access disclosure. No new model result, untested code execution, or confirmed original oracle bug was reported by Muse.
