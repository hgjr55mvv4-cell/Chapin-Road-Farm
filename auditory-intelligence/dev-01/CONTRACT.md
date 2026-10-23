# AUDITORY-DEV-01 — frozen synthetic timing preflight (engineering only)

**Status:** RUN locally, NOT speech recognition, human turn prediction, or situational understanding. All examples EXPOSED DEV. No inference, recordings, models, or paid API calls.

## Scope

Generate two *non-linguistic* pure-tone bursts in 8,000 Hz mono PCM16 WAV. Burst 1 ends at 0.620 s; burst 2 begins 0.120 s or 0.680 s later. The external transcript text is **identical** between both conditions: "I thought you knew." It is a symbolic label only; tones do not speak those words. The detector works at 10 ms fixed windows, computes RMS energy and returns a post hoc **inter-burst gap** after both bursts have occurred.

## Predeclared outputs / rules

- **Level 0:** Missing/unreadable/unsupported/clipped/unreliably background-dominated WAV must produce explicit non-OK status and no measured gap. Do not identify sound sources or speech content.
- **Level 1:** When valid two bursts are detected, return their intervals and the measured completed gap, with error <=20 ms versus known synthesizer boundaries on these cases.
- **Transcript-only A0:** Same text but no gap, so no justified SHORT/LONG distinction.
- **Transcript + gold timestamps A1:** Receives the *true* gap as a strong timing baseline.
- **Audio-derived B:** Receives gap computed from waveform and the same external transcript. It must not be declared better than A1 if it only recovers those timestamps.
- **Synthetic illustrative routing:** Gap <=0.30 s => WAIT; gap >=0.50 s => READY_NOT_OBLIGATED_TO_REPLY; middle => WAIT. These are **chosen fixture rules**, not labels of human conversational appropriateness and not a turn-end predictor.
- **Explicit lexical correction:** A supplied transcript containing "No, I meant" yields CONFIRM_EXPLICIT_CORRECTION regardless of waveform. This is a *text-sufficient control*, not acoustic gain.

## Negative controls

Missing/invalid WAV, clipped WAV, high-energy background, only one burst, identical words with manipulated timing, explicit correction that text already resolves. Sensor failure => ask for a clearer sample. No intervention on a real human and no observer-effect claim. The first 20 ms are inspected to flag energy already present at the boundary; this is a simplistic *engineering* signal validity check, not real-world microphone diagnostics.

## Advancement gates

Satisfying the synthesizer's expected gap demonstrates only timing measurement on authored tones. A future rights-cleared real-speech study requires independently specified boundaries, meaningful competing tasks, held-out speakers/accents/environments, calibration/latency, honest missingness, transcript+actual-timestamp baseline, consent, and external judgments of whether a system's wait/ask behavior helps humans. Until then all psychological and deployment claims remain HOLD.
