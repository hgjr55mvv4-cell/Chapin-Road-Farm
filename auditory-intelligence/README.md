# Auditory Intelligence — sound, language and situated interaction

**Status: OPEN RESEARCH + SYNTHETIC AND CONTROLLED REAL-RECORDING ENGINEERING DEV. No deployed listening system.**

Research shared across Harbor Co-Listener and Virtual Farm Manager: can an AI distinguish what was **actually recorded**, what a transcript says, what an acoustic event suggests, what context remains unknown and what action is warranted?

Start with [AUDITORY-DEV-01 synthetic waveform preflight](dev-01/README.md), [Muse Round 01 attributed research digest](MUSE_ROUND01_RELAY_DIGEST.md), [Sol review](SOL_REVIEW_01.md) and [next bounded Muse review prompt](SOL_TO_MUSE_ROUND02.md).

**Astra independent master review received:** [attributed Round 01 audit digest](ASTRA_MASTER_REVIEW_01_RELAY_DIGEST.md) and [Sol's evidence reconciliation](SOL_ASTRA_RECONCILIATION_01.md). Astra reports 12 original tests, 19 adversarial probes and a separate 16-test isolated repair; the original full report and patch **bytes have not been received**. **Disposition: REPAIR DEV-01 FIRST; scientific confirmation HOLD.**

**New bounded repair:** [DEV-01-TRANSPORT-v0.1](dev-01-transport-v01/README.md) is a separate Sol-authored source/test branch derived from the historical parser, with **20 local tests**; the original DEV-01 is preserved. Importantly, **a valid WAV and a correctly measured gap do not prove the detected sound regions are the intended source events.** [Earlier recovery handoff](SOL_TO_MUSE_RECOVERY_01.md) is now historical, superseded by Astra's relayed review.

**Current DEV-02 advancement:** [AUDITORY-EVENT-INCREMENT-02](event-increment-02/README.md) now compares a matched 440→620 Hz tone-class detector with an energy-only baseline on **400 constructed positive and 400 negative WAV recordings**. The [case-level ledger](event-increment-02/receipts/cases.csv), [dataset candidate register](event-increment-02/DATASETS.md), and [independent Muse handoff](SOL_TO_MUSE_EVENT_02_AUDIT.md) are public. This is **synthetic tone-class identification only**, not physical source identity or real-audio understanding.

## Astra review: ground truth before model complexity

[Astra's independently reproduced AUDITORY-REAL-01 negative result](dataset-admission-01/ASTRA_AUDIT_RELAY_DIGEST.md) exposes clip-class and event-label uncertainty. The **[DATASED-ADMISSION-01 fail-closed checker](dataset-admission-01/README.md)** now tests provenance declarations, source overlap, audio hashes/WAV completeness, event-time validity, manual listening receipts and explicit verified negatives (**14 synthetic local tests; real DataSED candidates NOT RUN / HOLD**). The candidate filenames and original ZIP were not supplied to Sol. [Muse's bounded independent red-team assignment](SOL_TO_MUSE_DATASED_ADMISSION_01.md) is ready. The nine-frequency real-audio model remains STOP, and VFM mechanical diagnosis remains HOLD.


## Dessa and speech-native full-duplex research (Oct 23, 2026)

[Block announced Dessa](https://block.xyz/dessa), a **vendor-described** speech-only-pretrained, full-duplex conversation model. [Source/evidence assessment](DESSA_PUBLIC_RESEARCH_01.md) distinguishes public product claims from independently verified scientific behavior, and [Sol → Muse research handoff](SOL_TO_MUSE_DESSA_SPEECH_NATIVE_01.md) sets a falsifiable **streaming interruption / echo / bystander / correction** study with strong timestamp baselines. **No Dessa weights, access, public evaluation or inference execution obtained; no field deployment, phone capability or psychological interpretation established.** Keep this interaction-policy lane separate from the [DataSED ground-truth admission gate](dataset-admission-01/README.md) and [VFM machine diagnostics](real-audio-01/RESULTS_REVIEW.md).

## Duplex implementation replay and playback-reference proposal

[Sol's actual-byte ZIP replay and independent diagnostic probes](SOL_DUPLEX_IMPLEMENTATION_REPLAY_01.md) confirmed 18/18 original tests and found three actionable mock issues: **the oracle changes both source and confidence**, a confidently misclassified echo causes a false correction yield, and an unresolved older clarification blocks a later valid correction. [Astra/Muse review and PLAYBACK-REFERENCE-01 handoff](SOL_TO_ASTRA_PLAYBACK_REFERENCE_01.md) distinguishes implementation fixes from a **design-only** echo-versus-independent-speech acoustic experiment. **Neither source authorization nor actual audio listening is qualified.**

## Duplex correction transaction repair (Oct 23, 2026)

Astra's latest user-relayed audit challenged the original [duplex 15-session mock](SOL_DUPLEX_FACTORIAL_FINDINGS.md): the oracle changed source labels **and** confidence, earlier ASK events blocked later complete corrections, and non-finite confidence could bypass checks. [DUPLEX-POLICY-REPAIR-02](duplex-policy-repair-02/README.md) is a new **mock-only transactional implementation** with 28 local regression tests, explicit UI-only logical commits and a retained failure for confidently misattributed echo. Source, authority, addressee, playback status and quote tags remain **externally supplied fixture metadata**, not measured capabilities. [Sol → Astra/Muse independent audit](SOL_TO_ASTRA_MUSE_POLICY_REPAIR_02.md) and [PLAYBACK-REFERENCE-01 v0.2 acoustic design](duplex-policy-repair-02/PLAYBACK_REFERENCE_01_DESIGN.md) are ready. **No actual playback audio experiment has run; scientific and farm deployment HOLD.**

## Evidence ladder

**Level 0:** sensor validity (missing, clipping, interference, sample format).  
**Level 1:** waveform-grounded intervals, activity and acoustic measurements.  
**Level 2:** uncertain classifications of acoustic events (not physical source identity).  
**Level 3:** words/turns/corrections, conditional on actually available speech data.  
**Level 4:** contextual hypotheses about referents or the conversational situation.  
**Level 5:** cautious wait, ask, abstain or verify actions; never automatic physical action on speculative inference.

**Update (Oct 23):** [AUDITORY-EVENT-02](event-increment-02/README.md) handles constructed tone classes; [AUDITORY-REAL-01](real-audio-01/README.md) now uses actual rights-verified **ESC-10 environmental sound WAVs in operator-constructed mixtures**. Its [negative result](real-audio-01/RESULTS_REVIEW.md) found a simple ZCR method detected 3/6 planted sequences (all from one source group), while a 9-bin spectral prototype detected **0/6** with 22/48 abstaining queries. Both used *oracle insertion windows* and only two held-out source groups, so neither establishes spontaneous event localization or real-world classification. [Astra independent full audit assignment](ASTRA_REAL_AUDIO_01_REVIEW.md) published. Actual speech, physical emitter identity and fault diagnosis remain HOLD. A supplied transcript is an external symbolic label, not speech decoded from WAV.

No microphone, bystander surveillance, speaker identification, emotion diagnosis, field operation, copyrighted audio, human labels or paid API inference. Every source/test case is public **EXPOSED DEV**, not scientific confirmation. 