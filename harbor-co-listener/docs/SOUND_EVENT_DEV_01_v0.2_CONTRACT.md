# SOUND-EVENT-DEV-01 v0.2 — frozen engineering specification

**Frozen:** October 22, 2026. **Authors:** Sol integrating Muse Round 02. **Status:** SOFTWARE-ONLY IMPLEMENTATION AUTHORIZED; SCIENTIFIC CONFIRMATION HOLD. **Additional budget:** $0. Any material contract edit creates v0.3. This contract is not evidence that tests have run.

## Objective and boundaries

Extend the existing no-build, local-first browser listening room with a small, deterministic waveform analyzer. It must generate known synthetic signals, detect timestamped elementary audio events, expose failures, and export waveform-derived provenance. **Success is engineering qualification only**, not human-like hearing, listener preference inference, music emotion classification, or evidence of consciousness.

No actual music required for qualification. No copyrighted files committed. No paid APIs, servers, network audio, external runtime CDN, microphone access, cloud accounts, personal listener history, agent orchestration, diagnoses, lyric knowledge, or automatic listening.

## Four kinds of event — strict semantics

1. **digital_silence**: *all* audio channels exactly zero at the decoded PCM sample level for a contiguous interval ≥100 ms; a window RMS alone cannot prove exact zero. Timestamps from sample indices.
2. **low_energy_interval**: a documented windowed RMS measure below a relative, measured threshold for ≥200 ms. A reverb tail or quiet noise may qualify while not being digital silence. Explicit handling for all-silent recordings and near-zero references. Mark overlapping low-energy/digital-zero observations transparently.
3. **energy_rise**: measured short-term RMS increase across windows, using a logged engineering threshold (initial candidate: 12 dB). This is neither emotional intensity nor a calibrated likelihood.
4. **spectral_change**: a change in dominant tonal component on a controlled equal-amplitude 440Hz→880Hz fixture, detected independently of energy change (e.g. a simple DFT/Goertzel feature). This is not general pitch tracking or full music perception.

**Expected-event omission** (an event someone anticipated but did not occur) is explicitly OUT. This requires an expectation model; zero energy alone is insufficient.

## Source, memory, and controls

- Process only after explicit Run action. Generated fixtures are preferred; local user-file analysis is optional.
- For local files, prevent uncontrolled memory use: preflight a conservative file-size or duration cap *before* decode; estimate decoded PCM where valid, and never assert that compressed file bytes equal decoded bytes. Native browser decoding can allocate substantial memory and cannot necessarily be cancelled mid-call. Stop further app-side processing and report cancellation when possible.
- Use a fresh, session-scoped random clip ID; no deterministic fingerprint, filename, artist, path, lyrics, or audio contents in export.
- Never send local audio to a server. No network fetches in the prototype's offline test.
- Do not accidentally erase existing human marks or responses when analysis fails or cancels.

## Deterministic fixture generator (generated in code)

F1: mono 440 Hz tone for exactly 1s, zero samples 0.5s, then equal-amplitude 880 Hz tone for 1s. Two sample rates: 44,100 and 48,000 Hz.
F2: same temporal structure at −6 dB amplitude; relative-threshold invariance.
F3: identical timing but seeded nonzero low-amplitude noise (or an explicitly defined tail) in place of digital zeros. Never label white noise as “pink” without implementing pink noise.
F4: stereo signal in only one channel, then the other; a separate phase-inverted case to catch mono downmix cancellation.
F5: equal-amplitude 440Hz-to-880Hz direct transition **with no silence**; waveform energy can remain essentially unchanged.
F6: empty input, truncated/invalid decode input, and unsupported format diagnostics.
F7: oversized metadata preflight **without allocating the full hypothetical PCM array**.
F8: identical PCM under different filenames/titles: compare the actual event results ignoring random per-session ID.

## Export schema (v0.2)

A JSON export must include:
- schema_version = harbor.sound-events/0.2; clip_session_id = random local ID.
- analyzer: id, version, sample_rate_hz, channel_count, parameters including window/hop/threshold.
- source: generated_pcm or local_user_file, with sent_to_server=false.
- events[]: id, kind, start_s, end_s, method, measurement and units, threshold/parameters, provenance=waveform_derived.
- diagnostics: status (ok|partial|failed|cancelled), error_code if present, warnings[], elapsed_ms only if actually measured.

Raw audio, hashes, original filenames, intimate reports, model feelings, and unsupported numeric confidences must not appear. Keep waveform-derived measurements distinct from human notes and interpretive statements.

## Frozen engineering qualification gates

Q1. F1 digital-silence start/end boundaries within ±20ms at 44.1 and 48 kHz.
Q2. F2 events preserved within ±20ms and relative threshold correctly logged.
Q3. F3 does not contain a false digital_silence; its low-energy interval is detected when actual threshold supports it.
Q4. F4 shows no whole-signal silence when either channel has signal; opposite phase never vanishes due to naive averaging.
Q5. F5 spectral transition within ±30ms **without a false amplitude-only onset**; an RMS-only algorithm does not pass this gate.
Q6. Invalid/empty input and oversized metadata rejection handled with structured errors, no unhandled failure and no huge test allocation.
Q7. Events validate against locally checked schema, include true provenance and measured parameters, export excludes sensitive metadata/audio/subjective claims.
Q8. Deterministic tests run with documented, reproducible command and real machine/browser versions, actual receipts, and $0 added paid spend. Written tests alone = NOT RUN.
Q9. Semantic, screen-reader-reachable event list; focusable Run/Cancel; accessible status; preserve usability when interrupted. Actual Safari/iPad/iPhone/VoiceOver tests = NOT RUN unless observed on those devices.
Q10. Static/offline test makes no network requests; current playback, notes, listener response, and JSON export are not regressed.

**Engineering status:** QUALIFIED only if all applicable qualification gates have actual passing evidence. Otherwise ENGINEERING INCOMPLETE or NOT RUN with individual gate results. A Node or desktop simulation is *not* proof of mobile device behavior; keep device-specific checks explicitly pending if unavailable.

## File-level handoff and change control

Prefer plain JS modules: modules/audio-events.js (PCM operations), modules/fixtures.js, modules/schema.js, tests/ plus minimal index.html integration. Native Web Audio only; no CDN, new commercial library or paid API. Keep a reproducible README explaining execution and limitations. Work on a dedicated named branch and open a PR against public main, without direct pushes. **Do not merge incomplete code automatically.** Report the exact changes, commands run, failures, test receipts, and branch/PR URL or patch if GitHub write access unavailable.

## Separate research, later

Audio grounding on real rights-cleared clips, prediction of what consenting humans mark as significant, and person-specific learning from prior reports each need **different prospective evaluation contracts**, different ground truth, and distinct permission. None is authorized or confirmed by passing these fixture tests.
