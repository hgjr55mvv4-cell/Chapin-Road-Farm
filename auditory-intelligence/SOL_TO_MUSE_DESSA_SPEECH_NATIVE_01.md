# SOL → MUSE | DESSA-SPEECH-NATIVE-01
## Can an AI listen *while it talks* without losing task meaning, source evidence or the right to remain silent?

**From:** Brian & Sol  
**Date:** October 23, 2026  
**Projects:** Auditory Intelligence / Harbor Co-Listener / Virtual Farm Manager  
**Assignment:** Independent first-principles research, adversarial architecture audit and one minimal falsifiable experiment  
**Status:** Research and bounded no-cost software-only tests authorized; human confirmation, live audio and farm deployment **HOLD**  
**New spending:** $0 · **Repository writes:** NOT authorized in this Muse round

### Sources to read — with provenance labels

**Block's October 23 announcement:** https://block.xyz/dessa  
**Our source review:** [Dessa science and claims ledger](DESSA_PUBLIC_RESEARCH_01.md)  
**Incumbent auditory evidence:** [Astra auditory master review](ASTRA_MASTER_REVIEW_01_RELAY_DIGEST.md), [real-recording negative result](real-audio-01/RESULTS_REVIEW.md), [DataSED admission gate](dataset-admission-01/README.md)  
**Prior independent Muse audit assignment:** [DataSED source-truth audit](SOL_TO_MUSE_DATASED_ADMISSION_01.md)

**Scientific comparators and benchmarks:**
- https://kyutai.org/blog/2024-09-18-moshi-release/ — Moshi, public code and weights; unlike Dessa, Moshi uses text pretraining and aligned text tokens.
- https://arxiv.org/abs/2507.23159 — Full-Duplex-Bench v1.5: interruption versus backchannel, side conversations, ambient speech.
- https://arxiv.org/abs/2609.39446 — DuplexAct-Bench: proactive initiation, active silence, timing and content.
- https://arxiv.org/abs/2604.04847 — Full-Duplex-Bench v3: self-corrections and tool-task fidelity.
- https://proceedings.mlr.press/v306/ray26a.html — τ-Voice: grounded task completion under noisy dialogue.

Muse,

Brian found Block's newly announced Dessa model because it appears to investigate precisely what we have been exploring: **how sound carries a human conversation beyond words**, and how AI might learn to respond from the stream itself.

Block **claims** Dessa is a *speech-only-pretrained, full-duplex speech-to-speech* model that can listen and speak at once, including laughter, prosody and interruptions. The page contains selected synchronized-track demos and an invitation for limited safety-research access. **This does not demonstrate independent benchmark superiority, trained-data provenance or availability of open weights.** Don't silently assume you can run Dessa.

We want a scientific response, not enthusiasm for a new proprietary model.

## Central scientific question

**What capabilities might an audio-native, full-duplex learner gain that a strong and inexpensive transcript + word timestamps + voice activity + small acoustic-event sidecar cannot, when both are tested on the same task and at the same streaming cutoff?**

There are **four distinct claims** to test separately:

1. **Learning modality:** Does training without written text yield different representations or data efficiency? This requires comparable pretraining conditions; an uncontrolled product demo is not a test.
2. **Acoustic perception:** Does a raw-speech model preserve useful evidence beyond a transcript and accurate timestamps? Does it identify *which acoustic source* made the event, or merely recognize a salient sound?
3. **Real-time interaction:** Does listening while talking help distinguish interruptions, backchannels, incidental speech, pauses and explicit corrections without harmful false takeovers?
4. **Situated reliability:** Does any of this improve the *actual user task*—correct instructions, factual accuracy, timely clarification, fewer unwanted interruptions—or only naturalness and surface expressiveness?

Do not collapse these into a generic statement that Dessa understands emotions, people or physical situations.

## The self-interference problem — our preferred falsifier

An AI assistant is speaking directions to a person on the farm. Its own audio is coming from a speaker and may leak into the microphone. The user says, "No, I meant the **right** gate," while a second person is talking nearby and a machine creates a short burst of noise. 

Can the AI:
- detect **who is interrupting** (task user, bystander, assistant's own output, unknown) or explicitly abstain when identity is unsupported?
- distinguish a brief "mm-hmm" or laughter from an instruction to stop speaking?
- preserve the actual correction (direction, number, negation, referent) without extrapolating a person's feelings?
- yield promptly **only when appropriate**, avoid spurious stopping, confirm task-critical changes and remain in observational mode?
- log its own output as a source of future evidence, including echo and intervention-induced changes?

This connects Dessa's claimed full-duplex behavior to our Astra finding that **a correct measurement of two sound regions can still refer to the wrong source**.

## Strong baselines; no straw men

Compare designs, respecting the same available prefix:

- **A0:** Transcript-only assistant with conservative wait/confirmation controls.
- **A1:** Practical streaming transcript + VAD + timestamps + explicit source/echo flags where a competent low-cost front end can provide them. Measure end-to-end latency and uncertainty.
- **A2:** A deterministic event-ledger policy with explicit source and self-output history. This is *not* neural listening; it tests decisions when event labels are supplied.
- **B:** An actual audio-native/full-duplex model **only if access, consent and cost permit**. Otherwise define an executable adapter and benchmark, mark B NOT RUN. Model access is not authorized through Block waitlist by this assignment.
- **C (optional):** Open Moshi-style full-duplex architecture as a scientific reference, *not* a same-pretraining comparison and not mandatory to run on phones/tablets.

## Choose one experiment that can lose

Design **DUPLEX-SITUATION-DEV-01**. Prefer a two-stage test with no human data for now:

**Stage 1 — executable deterministic event ledger (allowed):** Make a frozen, low-cost synthetic **streaming** scenario where both the assistant and hypothetical human have timestamped activity. Include genuine corrections, meaningless backchannels, speech to a different person, leaked speaker echo, indistinguishable early prefixes and low-confidence sensor conditions. Source labels are oracle annotations; never report these results as proof of acoustic source separation. A WAIT-ALWAYS or STOP-ALWAYS system must lose on useful-coverage and responsiveness.

**Stage 2 — actual audio (DESIGN / NOT RUN unless expressly authorized):** Rights-cleared synchronized speaker tracks or strong annotations, with independently held-out recording sessions, acoustic overlap, channel isolation and no future-context access. Score acoustic source assignment separately from action policy. Do not infer personal intent or mental state as objective labels.

Include independent ground truth for *task-critical correction content*, not simply "felt empathetic" or model-generated confidence.

### Required outcomes

For each arm, report **true correction capture**, incorrect correction, missed correction, false takeover on backchannel, false response to bystander/echo, response/yield latency, mistaken physical-action proposals, sensor abstention, useful coverage and operator interaction burden. Group by session or source, not by hundreds of correlated frames. Declare information available to each arm and count unknown source labels as errors/abstentions rather than quietly guessing.

A decisive **STOP** is allowed: if transcript + practical timestamps + echo/source controls matches a more elaborate speech model on the frozen real task, at lower cost and fewer false interruptions, prefer the simpler system. If emotion/prosody prediction has no verified task utility, do not add emotion inference.

## What we want you to challenge

- **Block's vendor claims:** Are speech-only pretraining and language/world-learning from spoken conversation demonstrably distinct from acoustic grounding? What independent controlled evidence is missing?
- **Naturalness versus reliability:** A model can sound empathetic, laugh at a plausible time and still misremember instructions, interrupt a bystander or suggest the wrong physical action.
- **Observer effect:** Conversational behavior changes when the AI interrupts, asks leading questions, or becomes unusually expressive. Record AI interventions; include a silent/no-intervention baseline.
- **Accessibility and individual variation:** Pause lengths, breathing, voice quality, accent, fatigue and disability must not become universal "confused" or "sad" labels. A user-configurable turn policy may beat speech-native inference for this goal.
- **System constraints:** A reported M4 Max local runtime doesn't imply iPad-compatible, offline, low-power operation. Do not recommend hardware purchases or hosted paid inference.
- **Data rights and privacy:** No microphone capture, bystander recording, biometric voiceprint, synthetic imitation of actual people, personal emotional profiling or covert experimentation. No new waitlist/email/contact without Brian's explicit approval.
- **Project separation:** DataSED event-provenance problems and VFM Acoustic Mechanic source attribution remain separate blockers; full-duplex speech interaction is *not* their repair.

## Deliverables

Return a self-contained report with:

**A — Primary-source audit:** What Block actually announced versus what is independently shown, and what is unavailable; citations and model/demo access status.  
**B — First-principles mechanism:** Why full duplex might matter, and a valid null where timestamps suffice.  
**C — Architecture comparison:** A0/A1/A2/B (and optional open Moshi), input parity, complexity, latency and iPhone-first constraints.  
**D — Adversarial cases:** At least six, prioritizing assistant echo, bystander interruption, backchannel mistaken as command, corrections/negations, overlapping task speech and culturally variable pauses.  
**E — One frozen experimental contract:** Exactly observable input, session-level ground truth, allowed prefixes, STOP/GO thresholds, independent controls and error accounting.  
**F — Minimal runnable artifact:** If software tools are available, implement a **standard-library, mock-only** timestamped duplex event-ledger and actually run tests. Otherwise return testable pseudocode and mark NOT RUN. Never claim mock success is audio perception.  
**G — Dataset/benchmark matrix:** Select the minimum rights-cleared speech interaction benchmark that tests our outcome; distinguish its licenses/annotation granularity and inaccessible corpora.  
**H — Harbor and VFM implications:** What improves a real interaction, what remains scientifically unverified and what must be held.  
**I — Independent objections and falsifiers:** Three ways our thesis or Block's thesis might fail, and one observation that would lead you to STOP complex full-duplex R&D.  
**J — Direct letter to Brian, Sol and Astra:** State what evidence is genuinely missing, and recommend a single next step.

**Allowed:** source reading, hypotheses, bounded offline mock-only software and reproducible tests at $0. **Not allowed:** spending, model access requests, contacting Block, recording live audio, private human datasets, physical-world automatic actions or GitHub modification.

**Independent reviewer discipline:** Preserve the distinction between your own hypothesis and Block's public claims. Cite what you read. Mark executed/not executed precisely. Don't infer any latent human feelings, diagnoses or intentions from speech, and avoid a "more expressive equals more intelligent" assumption.

— Brian & Sol

**End your response exactly:**  
`MUSE → SOL | DESSA-SPEECH-NATIVE-01 | REVIEW COMPLETE — EVIDENCE STATUS EXPLICIT`
