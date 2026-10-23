# DEV-01-TRANSPORT-v0.1 — independently authored bounded repair

**Engineering DEV only. No real listening, source identification, or speech semantics.** Original [DEV-01](../dev-01/README.md) is frozen/preserved. This standalone version is an independently authored **Sol candidate** informed by an attributed Astra audit. The original Astra `TRANSPORT_REPAIR_v0.1.patch` bytes were not supplied and are **not** represented here.

## Exact accepted subset

Input is immutable byte-string RIFF/WAVE PCM16, mono 8kHz, uncompressed, ≤ **256 KiB** in this *synthetic* contract and ≤ **15 seconds** of declared frames. Actual RIFF byte count must equal declared RIFF size, and actual PCM data read must fulfill the declared sample-frame count. Any missing, declared-too-long or inconsistent capture yields a non-`OK` status and null gap.

**Important:** these limits are arbitrary engineering caps intended for the original generator; other legitimate WAV features (metadata chunks, streaming layouts, multichannel/device codecs) may not be supported or may require a later, separately validated decoder. Strict container checks do not establish real microphone health, non-corruption of signal samples, or event/source identity.

## Reproduce

```sh
cd auditory-intelligence/dev-01-transport-v01
python -m unittest discover -s tests -v
```

Sol ran the **local drafted candidate** with Python 3.13.5 and obtained **20/20** test passes:
- 12 inherited DEV-01 tests;
- six added malformed/header/size/semantic-boundary tests;
- two **known event-association limitation** tests that demonstrate one source can fragment or a distractor replace an intended target **while energy-region status remains OK**.

The latter two tests intentionally **do not pass by fixing the defect**: they document failure patterns with `event_association_status='UNVERIFIED'`. Never interpret `sensor_status='OK'` as a claim that two intended events were found.

The old source accepted a header-declared but truncated WAV with `OK`; this candidate marks it non-OK. Source and tests are publicly exposed and co-designed, so this is not independently blinded qualification or proof of actual auditory intelligence.

GitHub Actions validates the **committed** module on Python 3.11 and 3.13. No paid services, human/recorded music/speech or other private datasets were involved.

## Open problems / STOP

Event-association errors, echoes and ramped boundaries, quiet microphone/signal corruption, lexical correction policy disagreement, quoted text and streaming-prefix leakage are **not repaired**.

Next contract should test intended **tone identity and event order** with an independent synthetic ground truth and a strong simple frequency-based comparator, preserving uncertainty. No speech recognition, mechanical fault classification, source identity, farm operation or personal emotion inference authorized.
