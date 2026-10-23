# Research roadmap — from sounds to a person

**Working agenda, not a claim of AI hearing or emotion.** The v0.1 browser app is a human note-taking instrument, **not** an audio-capable AI listener.

| Stage | Can we demonstrate… | Baseline and hard failure |
|---|---|---|
| 0. Listening notes | Human-marked moments can be captured with accurate time and optional alternative readings | No-memory note-taking; lost notes, confusing UX or sharing without consent fails |
| 1. Hear real audio | Objective acoustic events located in actual audio (entrance, beat change, rest, timbral shift) | Title/lyrics-only and simple DSP baselines; unsupported claims fail |
| 2. Wordless meaning | Useful interpretations on instrumental/unfamiliar-language clips without borrowing the lyrics | Words unavailable / shuffled title / confounding loudness; guessing emotions fails |
| 3. Person-specific model | A consented, editable model improves held-out predictions of *this* listener's interests | No history and recent-only history; false stereotyping, leaks, and ignoring corrections fail |
| 4. Co-listening | An AI can attend, remain quiet, ask one well-timed question, and make corrections intelligibly | Fixed questions / no questions; interruptions and performative empathy fail |
| 5. Transfer | Improvements persist across fresh songs, genres and circumstances without forgetting objections | Frozen incumbent, longitudinal opt-in comparisons; history overfit or unwanted recall fails |

## System sketch (modular, not implemented)

**Local audio** → event/features detector → grounded time evidence → interpretation proposals → **uncertainty & provenance** → human response → consent-gated **listener ledger** → evaluation and correction.

Different agents may independently propose *audio observations*, *music-theory inferences*, *personal interpretations*, and *adversarial checks*. One model's answer is never corroboration by another model trained on the same priors. Use independently checkable audio, separate annotators, and conflicting examples.

## Listener ledger (proposed schema, not deployed)

Event fields: `session_id`, `clip_id` (non-identifying pseudonym), `time_start_s`, `time_end_s`, `evidence_type` (audio_observed / person_reported / inferred / unknown), `statement`, `confidence`, `consent_scope`, `revision_of`, `revoked`, `time_recorded`.

Do **not** infer biography, relationships, mental state, religion, or health from music. Default no memory retention; support inspecting, correcting, revoking, exporting and clearing. Stop short of implementing remote sync without a privacy and rights review.

## Measurement lanes

- **Acoustic:** onset/event localization tolerance, precision/recall, instrument/rhythm description judged by independent annotators; *not* based on how emotionally plausible the prose sounds.
- **Personal:** blind rating of faithfully summarizing stated meaning, calibration/abstention, corrected-error recurrence, preference-change adaptation, held-out new-song generalization.
- **Social:** interruptions, timing, time-to-meaningful-question, perceived respect and agency; negative responses included.
- **Operational:** phone/tablet accessibility, model/tool spend, latency, annotation burden, consent and data deletion efficacy.

Store positive and negative results. A single striking song story can generate a hypothesis, never serve as independent confirmation.

## Ω-ARENA application

Use [experiment v0.1](experiment-v0.1.md) as an earlier **design-only** proposal. For any new reusable procedure, write a **new** challenger version and freeze exact trigger/action/scope/selection rule/endpoint/cost/falsifiers before confirmation. Fresh post-freeze cases, matched A/B only if replay valid; absolute safety and quality floor plus relative gain; report UNKNOWN when not evaluable. Maintain a Loser's Ledger; avoid extra procedure slots without evidence.
