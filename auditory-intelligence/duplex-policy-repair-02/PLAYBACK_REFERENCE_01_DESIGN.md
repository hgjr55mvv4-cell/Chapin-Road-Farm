# PLAYBACK-REFERENCE-01 v0.2 — Astra-proposed acoustic experiment (DESIGN ONLY / NOT RUN)

**Provenance:** User-relayed Astra independently executed the mock code review and proposed the below acoustic research direction; the full Astra ZIP was **not attached** here. These are *provisional engineering gates*, not deployed safety thresholds. Costs/hardware $0, ≤25 MB selected source audio and ≤10 CPU-minutes proposed. **No audio has been downloaded or evaluated in this branch.**

## Bounded question
Can a **causal** playback-reference method distinguish extra independent acoustic activity while the assistant's known output plays, without confusing playback echo with external speech? This does **not** identify a person, their authorization, or their intention.

## Three comparator arms — all receive identical evidence

E: No playback reference, simple audio-energy/activity detection.

L: **Strong simple comparator**. Causal delay/lag and gain fit to the assistant playback reference followed by residual-activity detection. Mere correlation isn't an adequate baseline, because independent speech may coexist with playback echo.

A: Bounded causal adaptive echo canceller with documented update freeze/double-talk protection. **No clean evaluation stems or oracle double-talk masks** to any detector. Record CPU/latency.

## Asset admission before executing

Potential legal leads are LibriSpeech (original recorded read speech, CC BY 4.0) and Full-Duplex-Bench v1.5 (synthetic-overlap data documentation with MIT), but **exact audio file permissions are not verified here**. Admission requires license, speaker, chapter, source-recording ID and original attribution, audio hash, complete actual WAV frames, segment onset labels with uncertainty, and a disjoint speaker/chapter split across playback and independent-source roles. Keep all transformations of the same source grouped. *File insertion time is not independent speech onset.* Never invent onset from nominal placement or call unlabeled silence a negative. No microphone or human recruitment.

## Four matched source conditions

1. Assistant playback echo only (no independent component).
2. Independent recorded speech only.
3. Playback echo + independent speech (true double talk).
4. Independent speech repeats the same words as playback (correlation trap).

Vary echo delays, gains, bounded room filters, clipping, path changes, near-end noise and deliberately mismatched playback references. Include **non-speech residual noises**, otherwise activity cannot be claimed as speech. Clean stems and source origin are held for scoring, never detector features.

Freeze before source-held-out evaluation: selection IDs, simulation seeds, decoder checks, calibration groups, lag windows, thresholds, sampling, allowed causal buffers, decision cutoffs, online update state and CPU limits. Identical observed prefixes must yield identical actions and internal states. Output not just frame accuracy but per-source-group detection, false echo interruptions, non-speech false alerts, double-talk miss, coverage/abstention, delay from independently annotated audible onset and processing time. An abstention on a positive is a miss; on echo-only negatives it must be separately counted from successful rejection.

## Provisional falsifiers — not qualified thresholds

- ≥90% independent speech presence detection within 300 ms of annotated onset, ≤5% false detection on echo-only, ≥90% nonabstaining coverage by main condition.
- Rich A should improve double-talk detection by **≥5 absolute percentage points** over L without worsening echo-only errors or violating predeclared compute budget. If not, STOP A and prefer L when it meets gates.
- A run with only a handful of speaker/chapter groups must remain *pilot/inconclusive* regardless of attractive query-level rates. No field/source/authorization claims.

**Execution status: DESIGN ONLY / NOT RUN. Scientific confirmation & VFM action HOLD.**
