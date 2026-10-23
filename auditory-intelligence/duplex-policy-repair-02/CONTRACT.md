# DUPLEX-POLICY-REPAIR-02 — versioned engineering acceptance contract

**Date:** 2026-10-23 · **Scope:** synthetic event-ledger logic ONLY. **Evidence:** public exposed engineering checks, not independent preregistration or scientific evaluation. No actual sound, ASR, AEC, speaker diarization, model, hardware, user study or machine actuation; $0 incremental spending. Original [DUPLEX-SITUATION-DEV-01.1](../duplex-situation-dev-01/CONTRACT.md) remains unchanged.

## Independent review context

Astra user-relayed implementation review (Python 3.12.14) said the original 18 tests and three probes reproduced. On a controlled factorial, replacing **source labels** alone removed 2/6 false yields, but replacing **confidence too** was needed to recover 8/9 rather than 6/9 actionable corrections. An unhandled early clarification blocked later corrections. `NaN` confidence bypassed `< .8` comparisons. Original Astra ZIP bytes were not available in this conversation, so its original extra probes cannot be claimed independently run here.

## Implementation requirements (bounded toy)

Each causally delivered message has a unique event ID, revision, delivery time, explicit session thread, transcript and independently *supplied* information: observed acoustic origin, source confidence, independently supplied task authority, addressee, playback-match state, transcript confidence and optional quotation tag. There is **no acoustic classifier producing any of those labels**.

1. Reject NaN, infinity and out-of-range confidence; reject invalid event revisions/categories.
2. Separate **acoustic origin**, **speaking to the assistant** and **task permission** as *different fields*. None is inferred from another. A confident speaker tag is never permission alone.
3. Known echo/playback match may suppress correction proposals; when playback origin remains unknown, ASK rather than implicitly assume non-echo. This does **not** establish correct practical echo detection. If an actual echo is *both* mis-tagged user and falsely marked playback-nonmatch, a false proposal can still occur.
4. Use distinct states ASK_TEXT, ASK_SOURCE, ASK_SUPERSESSION, AWAIT_CONFIRM, VOID and COMMITTED; maintain multiple pending corrections without an early ASK blocking newer independently admissible work. An explicitly linked correction or completed same-thread clarification may resolve an older uncertain one; conflicting completed corrections require explicit supersession.
5. Event delivery is idempotent by ID/revision; later transcript revisions retract unconfirmed proposals but **do not rewrite historical actions or confirmed changes**; stale/revised messages cannot retroactively affect earlier prefix decisions.
6. **No unconfirmed changes committed.** The only way to update a logical task ledger is an externally authorized UI control that explicitly confirms the *exact* structured field/new value/rejected value. The UI control is supplied by the test oracle; this mock does NOT authenticate any real user. No device action, tool command, route change, maintenance diagnosis or physical control exists.
7. Unrelated speech cannot cancel or block a pending correction; two independently authorized changes can be separately committed. Duration pending and unresolved outcomes remain visible, not silently scored as success.
8. Prefix causality: at cutoff T no event with delivery time >T can affect state; a restarted replay of the identical prefix must produce identical state; future transcript revisions cannot alter previous states. Delivery time is authored, not measured acoustic onset.
9. Passing all unit tests does not establish that the toy grammar handles paraphrases, quotations lacking quote flags, ASR edits without trusted versions, malicious speech, or consent/authorization.

## Acceptance gates

- Run deterministic regression tests on Python 3.11 and 3.13 on **committed code**, show executed count and source commit.
- Preserve an explicitly failing scenario by interpretation: a confidently misattributed echo *without* trustworthy playback evidence can generate a proposal, but cannot commit without external UI confirmation.
- Require cases for NaN confidence; incomplete→complete; source uncertainty→explicit confirmation; two valid successive changes; unrelated speech; duplicates; revisions; cancellations; same-prefix replay; no spontaneous task commits.
- STOP model/field promotion. A real audio playback-reference experiment is an independently designed future work package, **not run** in this codebase.
