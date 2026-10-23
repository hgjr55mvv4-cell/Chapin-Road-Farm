# DUPLEX-POLICY-REPAIR-03 — separated speech ingress / host confirmation

**Status: EXECUTED ENGINEERING MOCK / No production authentication, voice inference, field operation or acoustic qualification.** This is a new, stand-alone version. [Prior v0.2](../duplex-policy-repair-02/README.md) is unchanged.

The current release repairs the confirmed mock `ui_authorized`-in-ingress trust-boundary problem by separating `Ledger.ingest(Speech)` from `HostPort.confirm()`, `HostPort.cancel()`, and `HostPort.manual_change()`. It introduces distinct authored `observed_ms` and `available_ms` fields, explicit `referent_id`, linked supersession with observation-time order, bounded value/grammar rules and version-checked task-state commits. The separately host-issued `manual_change()` allows accessible text-only editing when no usable speech is present.

**The security-sensitive limit is crucial:** `HostPort` takes an external authorization callback, but this library does **not** authenticate a person, verify an actual UI action, persist signed action logs or isolate its in-memory code from untrusted callers. In the unit tests it uses a scripted callback, **not a real secure host**. Never expose this host object to a model, mic/transcript input or network clients. A low-confidence transcript can be corrected through an **independent** human UI path, and no speech is needed at all for a manual edit; acoustic certainty is not a prerequisite for manual correction.

### Reproduce

```bash
cd auditory-intelligence/duplex-policy-repair-03
python -m unittest discover -s tests -v
```

The engineering tests include forged `Input`-style confirmation, duplicate host actions across separate host ports, a stale field/version compare-and-set, unknown source with manual override, confirmed echo misclassification, quotes, explicit supersession and source/referent/field mismatch, out-of-order observation time, invalid numerical confidence, transcript revisions and future-prefix invariance.

What remains **unresolved**: how to authenticate a host principal, prove UI display and explicit confirmation, persist/recover a transaction log after restart, discover true physical acoustic sources, infer a user's addressee/authorization, detect quotations from raw speech, or map vague correction referents. The possibility of **false proposals** from wrong source/playback metadata remains explicitly tested. No speech, acoustics, Dessa inference or actual farm equipment interaction was used.

Scientific confirmation, farm actions and live speech remain **HOLD**. [Exact contract](CONTRACT.md). [PLAYBACK-REFERENCE-01 design](../duplex-policy-repair-02/PLAYBACK_REFERENCE_01_DESIGN.md) is separate and NOT RUN.
