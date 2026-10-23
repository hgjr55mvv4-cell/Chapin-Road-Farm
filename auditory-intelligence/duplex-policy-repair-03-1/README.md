# DUPLEX-POLICY-REPAIR-03.1 — defer supersession until trusted confirmation

**Status:** EXPOSED MOCK ENGINEERING REPAIR; no audio, real authentication, production UI, persistent journal or physical actions. **Original v03 source and test cases remain unchanged.**

## Independently reproduced new incumbent defect

A v03 speech observation with `supersedes_txid` can retract an earlier pending proposal **before source confidence, authorization, or the host confirmation is checked**. In a run against the published v03 ZIP, a high-confidence correction for `north_gate/gate` first produced `AWAIT_CONFIRM`; a later unknown-source, `authority='unauthorized'`, confidence=0.1 transcript referring to it returned `RETRACT_PENDING` then `ASK_SOURCE_CONFIRMATION` and marked the valid earlier proposal `VOID`.

This is a practical **availability / lost-correction state** flaw, not a physical action or an audio classification error.

## Change

- Speech-originated supersession becomes **tentative only**: a new linked proposal does **not** retract its predecessor. The new pending transaction records `supersedes_txid`, original observation time and exact referent/field.
- Only separate host-port confirmation, after the same exact state-version/content and referent checks, can atomically mark the old pending proposal `VOID` while committing the new value. If the target was committed or otherwise closed, the link is rejected as stale; the old commit is not overwritten.
- The original host-only/ingest-only boundary, manually entered accessible values, finite-confidence checks, exact-value compare-and-set, prefix causality and known false proposal when echo metadata is wrong remain unchanged.

### Reproduce

```sh
cd auditory-intelligence/duplex-policy-repair-03-1
python -m unittest discover -s tests -v
```

57 authored unit tests in this version, adding: (55) uncertain/unauthorized linked speech **does not void** an existing proposal, (56) successful separately host-confirmed supersession voids the predecessor, and (57) a new linked correction cannot commit after the target was already committed. See `receipts/` for the local test output and source digests. CI verifies committed bytes on Python 3.11 and 3.13 separately.

**WARNING:** Host-port callbacks in this module are injected test doubles, not an identity provider or proof of an actual UI gesture. Same-process arbitrary code can bypass Python object boundaries. It has no durable transaction journal and no independent source/role/address evidence, so **production authorization and field deployment HOLD**. PLAYBACK-REFERENCE-01 remains **DESIGN ONLY**, with no real microphone/echo suppression executed.
