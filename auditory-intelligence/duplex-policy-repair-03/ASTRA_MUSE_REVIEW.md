# SOL → ASTRA / MUSE | DUPLEX-POLICY-REPAIR-03 — independent implementation audit

**From:** Brian & Sol · **Date:** 2026-10-23 · **Status:** Independent code review and $0 mock-only adversarial testing authorized, physical-world/audio deployment HOLD. No direct GitHub modifications during this audit.

The prior ASTRA/MUSE audit was clearly labeled **reconstructed**, not an exact replay. Sol opened the original v0.2 code, reran **28/28** tests, tested a spoofed in-band `ui_authorized` confirmation (which committed), and confirmed that actual `quoted=True` was already suppressed; unflagged quotation remains a semantic risk. Reproducible new version: [source](policy.py), [tests](tests/test_policy.py), [contract](CONTRACT.md).

## We want you to break the new boundary

1. Can any `Speech` ingress payload or transcript revision cause a logical task commit without calling the separated, host-only confirmation API? Give executable counterexample with exact source revision and commands.
2. Challenge `HostPort`: a callable authorizer is **not** an authenticator. Identify how real host app must independently establish principal and intentional confirmation. Don't claim software-only authentication from this mock.
3. Challenge exact task-state compare-and-set: can a stale proposed value, wrong referent, mismatched rejected value or duplicate event override a newer accepted change?
4. Attack supersession across event ID, observed timestamp, delivery timestamp, thread and referent. Does any invalid supersession void another person's correct transaction? Does a pending vague correction cause avoidable blockage?
5. Add tests for persistent restart after host commit. The module explicitly does NOT implement durable replay of host actions; decide the minimal append-only log design to qualify in a future version.
6. Test unknown quotation and ambiguous speech. A `quoted` flag supplied by an annotator is not something an ASR model guarantees; a literal utterance might be a quotation even when its transcript is identical to a correction.
7. Challenge manual low-confidence override: explain how a trusted human can enter a precise change when acoustic evidence is unusable **without** a model deciding that speech was authorized. Do not demand acoustic source identification as a condition for manual editing.
8. Design-only PLAYBACK-REFERENCE-01 remains independent acoustic work; don't confuse residual activity with a particular authorized speaker or user intention.

**Required result:** exact commit, actual code/test receipts, one highest-severity counterexample and a GO/REPAIR/STOP for **engineering semantics only**. No real audio, paid inference, local microphones, machine actuation or field claims.

End: `ASTRA/MUSE → SOL | DUPLEX-POLICY-REPAIR-03 | INDEPENDENT CODE AUDIT COMPLETE — EXECUTION STATUS EXPLICIT`.

**Additional v0.3.1 regression:** Test a source-uncertain, unauthorized utterance which links to a valid pending proposal. It previously voided the target before confirming the new change. Now the old proposal must remain pending, and only a separate host confirmation of the new proposal may supersede it. Attempt to find a different path to retract an authorized pending correction using untrusted speech alone.
