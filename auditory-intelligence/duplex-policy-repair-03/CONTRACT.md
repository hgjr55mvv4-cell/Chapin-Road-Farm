# DUPLEX-POLICY-REPAIR-03 — trust-boundary and referent repair (engineering DEV)

**Date:** 2026-10-23. **Status:** mock-only code and reproducible exposed unit tests. **Original DEV-02 remains frozen and available** at `../duplex-policy-repair-02/`. **Not** validated human interaction, acoustic source separation, authenticated UI, speech recognition, physical control, or scientific confirmation. $0 new spend.

## Evidence driving the repair

User relayed an **attributed independent ASTRA/MUSE report** whose implementation could **not retrieve and execute original source**, and which instead ran **eight reconstructed mock attacks**. Do not promote those to exact bugs of the published implementation. Independently opening original GitHub `duplex-policy-repair-02/policy_repair.py` and executing its tests and adversarial probes established:

- **Confirmed actual source:** speech event `kind='confirm'` with `ui_authorized=True`, `authority='authorized'` and exact proposed value could logically commit. In the toy harness, both ordinary speech and host controls were values of the same `Input` dataclass. A hostile caller able to inject `Input` could forge a UI event; this is not proof of compromise of any deployed interface, because none exists.
- **Confirmed actual source:** it has no separate observation timestamp or referent identifier; thread ID is not a sufficient semantic referent. A particular observation/delivery order attack could not be reproduced exactly because there was no observation-time field.
- **Confirmed intended behavior, not a new reproduced bug:** source confidence `.3` creates `ASK_SOURCE`, and externally supplied UI confirmation of exact content can logically commit. A verified independent manual control should remain possible when audio is uncertain. Do not require independently confirmed voice identity to permit **manual** text editing.
- **Audit claim contradicted by actual source:** `quoted=True` suppresses correction; a string beginning `He said "No, I meant ..."` is not accepted by the anchored grammar. The code remains vulnerable to *unmarked verbatim quotations*, because real ASR may omit quote structure.
- The low-confidence and echo/source indicators remain **scripted**; none comes from audio.

The only outcome for a `PROPOSE_CHANGE` from a misattributed echo is a **candidate logical change**; a host confirmation is necessary to update task state. That cannot make source labels correct.

## Frozen v0.3 bounded contract

1. **No UI action in microphone/transcript ingress.** `Ledger.ingest(Speech)` accepts only mock observed speech. It has no `confirm`, `cancel`, `ui_authorized`, `kind='confirm'` or `confirmed_value` payload. Logical confirmation/cancellation occurs through a separate `HostPort` `confirm`, `cancel`, or `manual_change` method, invoked by a *trusted host integration* after a real independently handled user action. `HostPort` and its callable authorizer are **mock boundaries**, not implementations of authentication, device secure enclaves, tamper resistance, or host permissions. Do not expose host port to untrusted speech/transcript payloads.
2. **Manual overrides permitted.** An uncertain audio-origin correction may be shown as `ASK_SOURCE_CONFIRMATION` and then explicitly changed by an independently trusted human UI. A low-confidence source label alone is **not** permission, nor must an acoustic residual detector be mandatory for an explicitly manual change. The host-only `manual_change()` path explicitly permits editing a logical value even with no speech event.
3. **Exact compare-and-set.** Host control requires exact structured `(field,new,rejected)` triple, referent ID, prior displayed logical value and task version. Current value/version is checked *at confirmation*. An explicit `not X` is checked against current `X` before commit. All field/value grammar and identifier lengths are bounded. No device or network actions are implemented.
4. **Separate source, role, address and source evidence:** mock `observed_origin`, mock `authority`, mock `addressed_to`, mock `playback_match`, confidence and text are independently supplied and not verified. Known echo/bystander/quote is ignored; unknown playback/source prompts rather than silently becoming known-good. A confidently wrong acoustic label can still generate `PROPOSE_CHANGE`. *No inference of intent, authorization or role from waveform*.
5. **Explicit referents / linked supersession:** require nonempty externally grounded `referent_id`; `thread_id` is grouping only. A correction supersedes an existing pending transaction only through explicit `supersedes_txid`, matching referent/thread/field and strictly increasing `observed_ms`. Reject ambiguous pending changes rather than automatically choosing newest. Revisions preserve event ID, observed time and referent.
6. **Causal event reading:** observed and delivered clock fields are distinct, `available_ms >= observed_ms`. No future transcript revision enters earlier prefix. Do not pass oracle future source tags or speaker IDs; those remain supplied fixtures here. Delivery time includes authored latency, not measured sound onset or device stopping.
7. **Audit/replay limits:** ledger exposes state version, event transactions and actions. In-memory duplicate host IDs are rejected. `replay_speech_only` reproduces a *speech-only prefix*, **not** a durable recovery of committed host actions after process restart. Persistent event store, atomic host UI action log, crash recovery and real authentication remain not built.
8. **No speculative physical action** and no claims of voice/intent/emotion/person identification, machine diagnosis, or phone runtime reliability.

## Independent gates for future promotion

- Unit tests must run on committed bytes with Python 3.11 and 3.13, report actual run URLs, counts and failures.
- Check authenticated UI principal and transaction-specific exact-value display with a real application host; do not regard `authorizer=lambda: True` as an authentication mechanism.
- Add crash-recovery and persisted idempotency tests before any live mutable-task feature.
- Qualify source labels separately using rights-cleared causal playback-reference audio, with a strong lag/gain residual baseline and physically sourced labels. **PLAYBACK-REFERENCE-01 stays DESIGN ONLY.**
- Separately test ASR quoting/revision, semantic referents, user permission and human oversight. Neither clean echo residual nor correct sound event class implies authorized task instruction.
