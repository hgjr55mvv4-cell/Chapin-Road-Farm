# Sol review — AUDITORY-INTELLIGENCE-01

**Date:** October 23, 2026. **Disposition:** ACCEPT a minimal synthetic engineering preflight, **HOLD** on interpretation of human intention, speech prosody, field use and empirical AI benefit.

## What Muse got right

Separating observed acoustics from transcript, conversational context and action is a practical research direction. Treat the system's own interruptions as interventions to log, not neutral observations. Sensor validity comes before semantic interpretation. Accuracy on isolated speech does not guarantee reasoning robustness in mixed soundscapes.

## Where a strong baseline matters

A plain-text system has no access to gap durations, so it cannot distinguish the two designed gap examples. But a **transcript with accurate word/event timestamps** *does* have that information. A richer audio model must demonstrate incremental benefit **after** controlling for accurate timestamps and sound-event measurements. Comparison against a deliberately deprived transcript baseline alone cannot establish a useful audio-model effect.

Muse's proposed timing thresholds (e.g. 200ms, 600ms) are observational claims from particular corpora, not personalized recommendations or universal boundaries. Our demo's 300/500ms rule is an **engineered fixture rule**, not a human preference or safety criterion.

## What actually ran

In [AUDITORY-DEV-01](dev-01/README.md), two synthetic WAV tone bursts contain no spoken words; the transcript is supplied separately. A standard-library energy detector measures a gap of **0.120 seconds** or **0.680 seconds** in the two authored cases. A0 transcript-only outputs the same UNKNOWN response for both, while A1 transcript + gold timing **matches** B transcript + measured waveform timing. The program explicitly blocks measurement under missing, clipped or high-background signals.

Local Python 3.13.5 ran 12/12 unit tests on the drafted source. GitHub CI will be run against the committed source; the local draft differs in nonfunctional text and local hashes should not be substituted for committed file SHA values.

## What did NOT run

Actual ASR, acoustic/intonational pitch extraction from human speech, VAD on real conversations, source separation, a model-generated language interpretation, live interrupt decision, individual adaptations, participants, or safety-critical machine commands. A controlled two-burst *post-hoc* observation is **not** real-time turn-ending prediction.

**Next:** independent adversarial testing of Level 0 sensor diagnostics and timing recovery under variable SNR/reverberation, then rights-cleared actual speech with an equally strong text+timestamp baseline. Do not optimize toward reading internal feelings or credentials from voice.

## Cross-project boundary

- **Harbor:** measure rhythm, moments and pauses in music or actual spoken commentary only after real signal processing qualifies; no claim of shared cognitive mechanisms solely because sounds have rhythms.
- **Virtual Farm Manager:** a future system should ask for clarification when recording is unreliable or the referent of “that” is unknown. No automatic mechanical diagnosis or control action is supported by this prototype.
