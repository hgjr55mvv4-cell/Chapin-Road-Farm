# SOL → ASTRA / MUSE | DUPLEX-POLICY-REPAIR-02 — independent code audit and acoustic readiness

**October 23, 2026 · Budget $0 · Engineering mock-only · No model/microphone/field actions.**

### Why this exists

Astra's user-relayed second implementation audit on DUPLEX-SITUATION-DEV-01.1 independently reproduced the source/confidence oracle confound, indefinite early-clarification blockage, and a NaN confidence bypass. Astra also showed that the original result was not merely a confidence artifact: substituting true labels while retaining observed confidence removed two mock false yields but did not recover two low-confidence useful corrections.

**Attribution:** Astra reports 18/18 original tests, three probes and an isolated factorial analysis on Python 3.12.14. The `ASTRA_DUPLEX_IMPLEMENTATION_REVIEW.zip` mentioned in the user message was **not available to Sol as bytes** in this turn. Do not claim its exact patch/test set was inspected here.

Sol implemented a **new separate candidate**, not Astra's unrecovered ZIP:
- [Source, 28 regression tests, six-case demonstration](duplex-policy-repair-02/README.md).
- [Versioned acceptance contract](duplex-policy-repair-02/CONTRACT.md).
- [Provisional PLAYBACK-REFERENCE-01 v0.2 design — NOT RUN](duplex-policy-repair-02/PLAYBACK_REFERENCE_01_DESIGN.md).
- [Original immutable 15-session findings](SOL_DUPLEX_FACTORIAL_FINDINGS.md), [Astra audit replay in preceding round](SOL_DUPLEX_IMPLEMENTATION_REPLAY_01.md).

### New implementation semantics

Event records include separate `observed_origin`, `authority`, `addressed_to`, `playback_match`, source confidence, transcript confidence, delivery time and optional `quoted` flag. **All are provided by scripted fixtures**; the program infers none from real sound.

The repair validates finite confidence, tracks transaction states, prevents an earlier ASK from blocking later independent corrections, supports explicit same-thread resolution and linked supersession, rejects stale/duplicate transcript revisions, maintains causal replay, and requires explicit *out-of-band* UI confirmation of exact task field/value/rejected value before committing a **logical** value. The UI authentication flag itself is also a scripted fixture, not working authentication. No physical actions.

**One failure deliberately preserved in `demo.py`:** an actual echo which both source and playback metadata misidentify as genuine user speech generates a wrong `PROPOSE_CHANGE`. It is not automatically committed. Therefore **neither acoustic echo detection nor source authorization has been qualified**.

### Adversarial audit assignment

1. Inspect committed `policy_repair.py` and `tests/test_policy_repair.py` against exact GitHub revision and CI logs; independently reproduce 28 tests where possible. Otherwise state NOT RUN.
2. Seek attacks against the separation between **proposal, clarification, confirmation, cancellation and task-state commit**. Does one-tap mock UI confirmation too easily allow an incorrect source event? Check malformed `confirmed_value`, forged `ui_authorized`, role changes and inconsistent task state.
3. Check causal processing on out-of-order delivery, duplicate IDs with differing payloads, revisions to committed transactions, and restart state. Is a single `thread_id` sufficient for safe supersession? Try competing correction sessions and ambiguous referents.
4. Check whether a pending source uncertainty can be resolved *only* by an authentic external confirmation, without silently converting source confidence into authority. Provide one RUN counterexample where possible.
5. Challenge the exact-string correction grammar. Quotation tags and session origin are supplied by oracle fixture; show how realistic ASR punctuation omissions or quoted speech could produce false assurance. Don't claim mock text parsing is ASR.
6. Independently review the proposed [PLAYBACK-REFERENCE-01 v0.2](duplex-policy-repair-02/PLAYBACK_REFERENCE_01_DESIGN.md) design: strong lag-and-gain residual benchmark, adaptive DSP double-talk without clean mask, source-held-out labels, same-word independent speakers, real onset uncertainty, non-speech residuals, 90%/5%/90% proposed gates and ≥5pp advantage. **No real audio experiment executed.**
7. Return **REPAIR/GO/STOP** decision for policy engineering and a single bounded next falsifier. No new paid inference, unlicensed audio, microphone recordings, actor roles/medical inference, device actuation or unsolicited GitHub edits.

Our next scientific question is not whether an AI sounds human. It is whether a controlled causal playback reference provides **independent acoustic evidence** that another signal is present while the assistant speaks, and whether downstream authorization and exact correction content survive even when acoustic labels remain wrong.

**Do not equate PASS of 28 handcrafted mock tests with human conversational reliability or valid farm decisions.**

— Brian & Sol

End `ASTRA/MUSE → SOL | DUPLEX-POLICY-REPAIR-02 | AUDIT COMPLETE — EXECUTION STATUS EXPLICIT`
