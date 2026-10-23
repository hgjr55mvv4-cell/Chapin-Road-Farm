# D1-FEASIBILITY-01 v0.1 — frozen ENGINEERING intake contract

**Decision:** GO for **software-only intake and scoring preflight** at $0 additional expenditure. **HOLD** on genuine model-comparison execution, participant work, inference claims and scientific confirmation. Freeze applies to this engineering interface and failure rules, not to an unseen prospective task bank. See [executable harness](d1-feasibility/README.md).

**Review origin:** Sol / Muse Round 01–05 correspondence, with [Muse Round 05 relayed digest](MUSE_ROUND05_RELAY_ARCHIVE.md). The design is not independent empirical validation of multiple AI models.

## The primary proposed question, not yet tested

At an equal **total opportunity budget**, does blind parallel oracle authorship with a predetermined aggregator produce more **useful, independently adjudicated decisions** than a strong single-model process with self-critique and access to the same frozen specification?

### Treatment and arms (for future, not authorized here)

- **S:** One strong model, entire per-task resource cap B; can use self-critique and deterministic spec-derived verification.
- **P1/P2:** Two separately initialized agent processes, each given the same frozen spec, allowed examples and tool permissions, but not one another's draft/output or any hidden adjudication. **Joint** cap B.
- Freeze before outcomes: individual S/P1/P2 outputs, aggregation rule, all allowed sources, model/role versions, and scoring rules.
- Prespecified P aggregator: **REJECT if either rejects, otherwise ABSTAIN if either abstains, otherwise ACCEPT**. This is a baseline, not an optimality claim.
- A cross-provider result confounds model family with workflow; two isolated provider names **do not** guarantee independent errors. Role swaps or same-model controls are later study design, not part of a two-task feasibility demonstration.

## Engineering intake gate — must be true before any real inference request

1. A versioned, rights-cleared contract and adjudication plan exist; expose no private Drive conversation, sensitive information, secret prompts, or unreleased confirmation cases.
2. A selected case pool is logged **after this protocol's freeze**, with explicit prior-exposure/overlap notes. **After-freeze selection does not guarantee novelty.** A publicly disclosed pilot is **DEV**, not unseen scientific confirmation.
3. Model roles S, P1 and P2 have distinct execution receipts from actual calls, not merely distinct string IDs. Hashes identify artifacts only after bytes are independently checked. **Identical outputs may still result from legitimate repeated model calls**.
4. All roles are restricted to the same allowable spec/examples and cutoff. Isolation is **audited**, not guaranteed by public manifest declarations.
5. Every accepted truth label has a verifiable adjudication reference; unresolved contract disagreement is `unknown` with a dispute reference. A human and another LLM agreeing are not infallible truth.
6. Budget opportunity cap B is the same for S and **combined** P1+P2; record **actual** usage separately. Spending below B in S must not reduce P's opportunity cap. Missing token or operator accounting means cost parity is UNKNOWN, not proved.
7. Score ACCEPT/REJECT/ABSTAIN for each candidate. Report valid acceptance, faulty acceptance, valid rejection, faulty rejection, class-specific abstention and truth-UNKNOWN count. The denominator for coverage is **adjudicated known-truth candidates**. Separately report inclusion of unknown-truth cases when useful; do not conflate them.
8. Report observed model tokens/calls if available, end-to-end time, human handoffs and optional voluntary operator effort. No automatic personal telemetry. Cost per useful decision cannot be computed if costs or truth are unknown.
9. Stop on privacy leaks, unauthorized charges, invented executions, missing critical receipts, budget overruns or a critical false assurance. A self-reported receipt passing schema validation does **not** establish that its corresponding tool call occurred.

## Intentionally small pilot

After the **engineering preflight passes and separately approved execution resources become available**, select at most two *newly authored rights-free* contracts with clear and independently adjudicated truth conditions. A two-contract run tests whether workflow actors can stay separated, produce analyzable results, record cost, and handle disputes. It cannot estimate population error rates or establish that dual-agent verification is scientifically superior. Do **not** preregister 5%, 10%, 2% or 80% outcome thresholds from two tasks; report exact numerator/denominator and outcomes.

**Authoritative software preflight:** `d1-feasibility/audit.py` and `tests/` validate manifest shape, declared isolation/source references, explicit unknown truth, token cap opportunity, conservative aggregation, and scoring. The bundled example is **SYNTHETIC_DEV** with mocked agent fields—no real calls occurred. Parser acceptance cannot authenticate an API/provider log or certify blindness; a human or independent execution system must check actual receipts.

## Disposition and completion gate

- **Engineering preflight GO:** Source, tests and synthetic example successfully execute on named environments. This demonstrates **software readiness only**.
- **Real two-agent pilot HOLD:** Until explicit approval of model access/resource cap and an independently reviewed task/adjudication packet; do not silently run, spend, or declare success.
- **Scientific confirmation HOLD:** Requires a later version, sufficient prospective tasks, unbiased sampling, repeatability, stronger controls and independently adjudicated results, with operator effort counted.

**Next move:** stop conceptual rounds and invite Muse or outside contributors to find a concrete implementation/metric flaw in the public preflight source. A reproducible counterexample or corrected code PR is more useful than a sixth abstract proposal.
