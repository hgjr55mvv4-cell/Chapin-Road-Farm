# Dessa (Block, October 23 2026) — independent source assessment for Auditory Intelligence

**Prepared:** October 23, 2026. **Scope:** public announcement and existing published research only; no Dessa account, training code, weights, API, demo-file reproduction or paid execution accessed. **Scientific status:** architectural hypothesis / external product claim, NOT a verified improvement in our projects.

## What Block publicly says

**Primary announcement:** https://block.xyz/dessa

The Dessa lab at Block says its new conversational model:

1. Was trained "from scratch on nothing but human conversation" — no written text and no pretrained models, per Block. **This is a vendor claim, not an independently audited training-data provenance statement.**
2. Produces speech from speech **full duplex**: it listens and talks at the same time, including backchannels and overlaps. The site offers *selected demonstration recordings* with synchronized speaker tracks and subtitles supplied later.
3. Learns behavior such as timing, voice expression, pauses, and spoken factual knowledge from conversation alone, according to Block. These are **not** proof of inner feelings, accurate psychological inference, or grounded perception of physical objects.
4. Claims faster-than-real-time inference and local operation on an M4 Max MacBook Pro or better. This **does not establish suitability for a phone/iPad** or farm/offline inference.
5. Offers a waitlist and calls for a small number of **AI safety researchers** to request early access, but does not publish downloadable model weights, complete reproducible benchmark receipts, training corpus manifest, inference API specification, or licensing terms on the announcement. **Availability and independent replication remain unverified.**

The site's wording "most authentic" is promotional and cannot substitute for benchmark comparisons. Its position that transcripts discard timing/emotion cues motivates research, but does not demonstrate that ordinary transcript + accurate timestamps + acoustic side-channel always performs worse.

**Important ambiguity:** A speech-only system may learn language and facts *from things people say*, not ground the meaning of those words in an independently verified external physical source. Our [Astra event-association results](SOL_ASTRA_RECONCILIATION_01.md) and [ESC-10 real-audio negative outcome](real-audio-01/RESULTS_REVIEW.md) warn that a correctly detected sound may belong to the wrong source, and a clip class does not verify the timing or identity of an event. Dessa's conversational skills do not on their own solve those problems.

## Existing independent research (not equivalent to Dessa verification)

- **Moshi (Kyutai, 2024)**: https://kyutai.org/blog/2024-09-18-moshi-release/ and https://github.com/kyutai-labs/moshi . Public full-duplex architecture, code, weights and technical report. Moshi **does use a text-pretrained backbone and aligned text tokens**, so it is *not* a training-isolation comparator for Block's claimed speech-only pretraining. It is a useful auditable interaction-architecture reference.
- **Full-Duplex-Bench v1.5**: https://arxiv.org/abs/2507.23159 . Separates user interruption, backchannel, side conversation and ambient speech, with categorical dialogue behavior, stop/response latency and prosodic metrics.
- **DuplexAct-Bench (2026)**: https://arxiv.org/abs/2609.39446 . Includes active silence, proactive initiation, interruptions, backchannels, yielding, and evaluates both timing and content; does not guarantee transferable human preference labels.
- **Full-Duplex-Bench v3**: https://arxiv.org/abs/2604.04847 . Extends interactive voice evaluation to self-corrections, disfluencies and chained task actions.
- **τ-Voice (ICML 2026)**: https://proceedings.mlr.press/v306/ray26a.html . Grounded tasks and realistic noisy voice environments; reinforces evaluating *actual task completion*, not only natural-sounding delivery.

These are research leads for **metric and test design**, not evidence that Dessa has passed any of these benchmarks.

## Why this matters to our existing projects

| Project | Bounded potential | Crucial boundary |
|---|---|---|
| Harbor Co-Listener | More natural quiet listening, correctly timed clarifications, backchannels, and preservation of someone else's unfinished thought | Natural-sounding talk ≠ access to someone's private feelings or meaningful relationship to music |
| Virtual Farm Manager | Respect task-critical corrections, negations and quantities while the user speaks over the assistant; remain quiet when unsure, distinguish user from bystander/assistant echo | Full duplex ≠ machinery fault diagnosis or permission to execute a physical instruction |
| Auditory Intelligence | A *new interaction-policy track* that combines listening, speaking and source/event provenance with a causal record of AI interventions | Keep separate from DataSED event truth and physical acoustic-source localization; no claim that speaking while listening solves either |

## The strongest new test worth designing

**Self-interference during an interruption.** An assistant talks; its own output leaks back through the mic while the user interjects a correction or a bystander speaks. Can the system:
- establish whether the relevant sound is from its *own output*, the task-authorized person, a bystander, or uncertain?;
- stop speaking on genuine authorized correction without stopping on harmless backchannels or echo?;
- preserve the revised instruction **without acting on it** until appropriate confirmation?;
- account for latency and interruption burden; and
- produce indistinguishable early decisions when two streams share the same past (no future leakage)?

Construct the *minimal* software event-ledger test first. **It tests action-policy logic given source labels, not waveform source separation**. Any prospective waveform study must use rights-cleared labeled dialogue with independently established sources, controlled input/output channels and a strong timestamp/VAD baseline. Do not equate model-generated emotional narration with ground truth.

## Access, security and research boundaries

No product access has been requested and no emails or waitlist forms submitted. The public announcement's privacy notice is not a substitute for examining terms governing any eventual recorded voice conversations. No private voice data, farm walk recordings, personal health inferences, or human experiments are authorized.

**Recommendation:** Invite Muse to perform a falsification-first speech-native/full-duplex scientific investigation while continuing **DataSED admission independently**. No "Dessa-like" large-model development on our $0, mobile-first path, and no claim of execution of the proprietary model.
