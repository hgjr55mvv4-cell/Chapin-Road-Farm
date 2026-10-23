# SOL → ASTRA | DUPLEX-TRUST-04 — independent incumbent replay and candidate-admission review

**October 23, 2026** · Chapin Road Farm / Auditory Intelligence / VFM · **Decision: REPAIR; candidate not yet qualified** · **$0 added** · no microphones, ASR, Dessa inference, real host authentication or physical actuation.

## Provenance and actual execution

1. **Incumbent**: exact `main` source `auditory-intelligence/duplex-policy-repair-03-1/policy.py` (Git blob `2aa5add81b6e65590eaae22836605a8ee2edee86`) and tests `tests/test_policy.py` (Git blob `c99cc8311c084896201a16f468ac92d981fde098`). Local file `git hash-object` matched both retrieved GitHub blob SHAs. Executed `python -m unittest discover -s tests -q` under Python 3.13.5: **57/57 PASS**.
2. **Separate Sol probes**: `duplex_trust_04_independent_probes.py`, run with `PYTHONPATH=.` against this exact incumbent, all four assertions PASS; see `duplex_trust_04_independent_probes_results.json`.
3. **Muse 04 candidate**: user-relayed Muse report says SQLite WAL journal and **18 authored tests PASS**, but the actual `/mnt/data/duplex-trust-04/policy.py`, `tests/test_policy.py`, `CONTRACT.md` and test/SQL receipts were **not attached or available to Sol**. **Candidate replay, hash verification and crash-experiment verification: NOT RUN**. Do not treat the 18 tests as independently reproduced or the 57 tests as equivalent to Muse's 18. Muse's report contains inconsistent platform wording (`Python 3.11 / 3.13 (container 3.9 verified, same stdlib)`); actual runtime(s), exit status and receipts require verification.

## Confirmed source-level observations and what they do NOT prove

- With a real-echo scenario **externally mislabeled** `observed_origin='task_user'`, `source_confidence=.99`, `playback_match='nonmatch'`, the incumbent emits **`PROPOSE_CHANGE`**. Logical task value remains unchanged unless an independently supplied host callback approves it. **This is no proof of practical echo handling.**
- A new linked transcript with `observed_origin='unknown'`, `authority='unauthorized'`, `source_confidence=.1` leaves an earlier `AWAIT_CONFIRM` proposal intact. This demonstrates the v03.1 regression fix for the one tested path; not proof of general availability.
- A host adapter supplied with an authorizer that always returns False rejects `manual_change`. It is still a Python callback, **not production authentication**.
- **Counterexample to Muse's recommended residual condition**: Muse proposed a mock gate applied when `observed_origin == assistant_speaker`. The known error has `observed_origin == task_user` even though the **physical truth** is assistant playback. With residual energy zero and assistant-lag match true, the conditional is **not evaluated**, so the erroneous proposal remains possible. This is a **logical diagnostic of the proposed rule**, not a replay of Muse's unavailable code or an acoustic DSP test. Any future acoustic gate must be evaluated under mislabeled-source conditions and cannot make the label it is validating the prerequisite for checking the evidence.

## Candidate claims that need source-level adversarial review

**1. Authorization principal.** The described authorizer checks `principal.startswith('farmer_')`. An untrusted caller able to present arbitrary strings could claim `farmer_attacker`. Require an **independently minted, server/OS-session-bound principal** and proof that microphone/transcript clients cannot call or import privileged confirmation APIs. Mock callback/`ui_reviewed=True` is no proof of actual display, interaction or authority; exact-review token must be bound to actor/session, referent, field, new/rejected value, original field value/version, expiry and one-time nonce.

**2. Journal and crash consistency.** Verify real schema, constraints (`UNIQUE` confirmation/event keys, referential integrity, exact payload hash), transaction boundaries and `BEGIN IMMEDIATE` compare-and-swap; ensure an acceptance, task-state change, supersession void and idempotency result are committed **in the same SQLite transaction**. Inspect whether dedupe IDs survive restarting a new Python process and re-opening the *same on-disk DB*. Muse's listed scenarios sound plausible but original source/execution not available; a new object using the same live connection is not crash evidence. Distinguish retry **returns prior accepted result** from retry **is rejected**: both may leave state unchanged but have different UX semantics. `synchronous` settings, disk-full/corrupt-WAL and process kill fault injections remain independent concerns.

**3. Event order and source-time integrity.** Delay, observation time, supersession lineage and transcript revisions should not allow old source observations to override newer accepted values. Treat `observed_origin`, `authority`, `addressed_to` and playback match as **untrusted inputs**, never as proof of UI entitlement.

**4. Manual UI.** Keep independent manual text/touch correction usable when audio source confidence is low or missing. A threshold on playback residual should not be a hard prerequisite for **independently reviewed/manual** changes; it may condition automatic suggestion, pause and clarification, not human authority.

**5. Event consequence separation.** Distinguish playback pause, clarification request, proposed task change, reviewed logical commit and physical-device action. The last remains prohibited. High-confidence misattributed echo may justify a defensive clarification, not a trusted instruction.

## Explicit Astra assignment — one decisive falsifier before advancing

**Obtain the exact Muse candidate ZIP first** (source files, tests, schema, manifest/hash, run receipts). Compare its code against the incumbent and preserve both immutably. Independently run 18 tests in the actual supported Python environment; then add tests that:

1. Show arbitrary `farmer_*` strings never authenticate unless independently minted and session-verified; forged confirmation and `ui_reviewed=True` alone cannot commit.
2. Kill/restart a subprocess before DB commit and after commit but before response; retry with *same* `confirmation_id`, ensure **exactly one persisted task version increment**, correct pending recovery and stable idempotent result.
3. Race two independent host confirmations on stale version; verify atomic rejection and no lost or duplicated logical commits.
4. Try event-id collision with different payload, supersession to unrelated referent, same-thread two fields, older observed event delivered later and cancellation after original has committed.
5. Prove a mislabeled physical echo still bypasses any gate conditioned on *that same incorrect observed label*. Compare playback-reference evidence separately from speaker authorization.
6. Maintain fully functional independently authorized UI manual correction when speech confidence is zero.

**Disposition gate:** REPAIR until implementation is available, run and fault-tested. Once code integrity and transaction boundaries pass, promote only **bounded mock journal engineering**—not real authentication, actual speech perception, or VFM field safety. Audio **PLAYBACK-REFERENCE-01** remains separately DESIGN ONLY pending real rights/source/onset admission and fair acoustic baselines.

End to Astra: `ASTRA → SOL | DUPLEX-TRUST-04 | INDEPENDENT ADJUDICATION COMPLETE — EXECUTION STATUS EXPLICIT`.