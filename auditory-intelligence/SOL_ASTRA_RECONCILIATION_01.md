# Sol reconciliation — Astra master auditory audit and VFM implications

**Date:** 2026-10-23. **Disposition:** **REPAIR DEV-01 FIRST**, transport-subset code **ENGINEERING DEV**, event association and actual machine/speech diagnosis **UNQUALIFIED**.

## Independent checks executed

The prior conversation's own `AUDITORY_DEV_01_2026-10-23.zip` contained a local original-source snapshot, with the same relevant parser/event logic as current public DEV-01. Running that snapshot locally on Python 3.13.5 reproduced all **12 original tests** and the truncated-header case: `render(.12)[:-3200]` returned `sensor_status='OK', gap_s=.12`. An inflated RIFF header, inflated `data` length and extraneous tail likewise returned `OK` in the original snapshot. **This is Sol's local reproduction; not a replay of Astra's full inaccessible patch or its 19-case suite.**

Sol independently authored [transport-v01](dev-01-transport-v01/README.md): strict RIFF total-length check, expected PCM-frame completeness, bounded 256 KiB input and 15-second declared frame count, explicit `event_association_status='UNVERIFIED'`. Locally, its candidate ran **20/20 tests**: 12 inherited and 8 new (six bounded transport/meaning guards and two deliberately preserved event-association counterexamples). GitHub CI should be read for results **against committed bytes**; a local draft is not the CI run.

## The decisive unresolved event-association problem

1. A single real tone burst with an 80 ms artificial dropout produced *two measured activity intervals*, `gap_s=.08`, and status `OK`. Only **one** source event was intended.
2. An intended second burst 680 ms after the first was attenuated below the energy threshold while a stronger extra event was placed 180 ms after the first. The code returned `gap_s=.18`, status `OK`.

These are *valid recordings whose region-level measurements are numerically consistent with the wrong sources*. Header checks cannot solve them. The new `event_association_status='UNVERIFIED'` prevents treating region detection as verified source matching, but **is not event-association inference**.

## Other known limitations

- `decide` checks audio status before explicit lexical correction despite the old contract saying a confirmed text correction is independent of waveform reliability. A quoted occurrence can spuriously match the substring `no, i meant`. Preserve this as a separately versioned semantic-rule dispute; do not fold unreviewed natural-language understanding into a WAV parser fix.
- The fixed WAV restrictions are **synthetic DEV compatibility gates**, not support for arbitrary device formats, quiet microphone failure detection or live streaming. Real captures may use different encodings, chunk metadata, loudness or durations.
- Comparing text-only versus waveform-derived timing alone is uninformative when an accurate timestamp/event baseline is available.
- A two-tone **post-hoc** gap is not a prediction of conversational completion, an emotion label or a mechanical fault diagnosis.

## Next step: independently qualified AUDITORY-EVENT-INCREMENT-02

Freeze a task with labeled intended events **independent of detector output**, non-leaking prefixes, source mixtures, gain/distractor/dropout/echo cases, strong practical timing control and a **simple frequency-specific detector** before sophisticated learned features. A rich model needs incremental improvement under equal information/cost and explicit false-action/abstention metrics.

**Virtual Farm Manager:** This separation is crucial for [Field Mechanic](../README.md): detecting a whine or knock is not locating its component; a clean recording is not necessarily an adequate diagnostic sample. VFM diagnosis/operation **HOLD**, equipment-specific baseline memory and human-inspection support remain research goals.

## Original scientific state

No real speech, field audio, speech prosody, human turn-taking, live mic, automatic machine control, or mechanic-confirmed faults have been tested in this repair.

**If Astra's original ZIP/patch arrives**, preserve the bytes, independently review the strict-format acceptance scope, run its exact test commands, and compare with this separate repair candidate. Never claim the two patches are identical solely because they both address truncated headers.
