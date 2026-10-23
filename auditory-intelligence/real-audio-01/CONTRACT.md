# AUDITORY-REAL-01 v0.1 — controlled mixtures from real ESC-10 audio

**Frozen public engineering design, October 23, 2026.** This research is $0, noncommercial, no microphones, no private user audio, no paid inference. The real-audio benchmark has **NOT RUN** at contract freeze. Its implementation was drafted beforehand, so the frozen design is a pre-execution DEV commitment **not** an independent, blinded scientific preregistration.

## Task and ground truth

- Use only the ESC-10 subset of ESC-50 (dataset CC BY 3.0). The **10 chosen original Freesound source recordings are individually marked CC0** in `LICENSE` of `karolpiczak/ESC-50`, pinned revision `33c8ce9eb2cf0b1c2f8bcf322eb349b6be34dbb6`. Cross-check `meta/esc50.csv`, clip class, fold, source ID and license at runtime. Source audio remains ephemeral in CI and **must not be committed to the public repo**.
- The audio contains **real environmental recordings** of dogs barking, chainsaws and rain. The dataset supplies only **clip-level** classes—not actual event-onset or individual emitter labels. Our experiment selects energetic 0.8-second excerpts and inserts them into a rain-bed WAV-like numerical mixture at two known slot starts (0.4 s and 1.6 s). **Experimenter-controlled insertion/class is the truth**, not human annotation of an original event.
- Question: did an event sourced from an ESC-10 `dog` clip occur in slot 1 **and** an event sourced from a `chainsaw` clip occur in slot 2? The metric is *association of class labels with predefined slots*, **not open-set localization, individual physical-source attribution, speech recognition or machine-fault diagnosis**.
- Train with **2 distinct fold-1 Freesound source IDs per category**. Evaluate with **2 separate fold-2/3 sources each** for dog/chainsaw plus two independent rain backgrounds. The held-out sources are never used to calculate prototypes or select thresholds.
- For each eval source set and three fixed gains (.25/.50/.85), run eight schedules: dog→chainsaw (positive); chainsaw→dog; dog→dog; chainsaw→chainsaw; dog→none; none→chainsaw; none→none; chainsaw→none (negatives). This produces **48 query rows: 6 positive + 42 negative**, but only **two independent eval-source configurations**; rows are highly dependent. Do not report binomial confidence intervals or population generalization.
- The reference processing uses a fixed energetic 0.8s excerpt selection per source (highest RMS segment on a 0.25s grid), simple 44.1kHz→8kHz box averaging, peak normalization, deterministic rain-bed gain and two fixed insertion slots. This processing changes audio. The beginning of the 0.8s excerpt is NOT an annotated natural onset.

## Frozen baselines and endpoint

1. **Energy-only (E)**: classify each already-known slot as active if RMS ≥ 0.034; declare `two_active` if both slots active. This is explicitly **not** an A→B class-identification baseline; any interpretation of its output as dog→chainsaw is false assurance.
2. **Cheap practical category baseline (Z)**: train a per-class mean **zero-crossing rate** on fold-1 source excerpts, then classify active slots by nearest univariate training prototype. This is the fair *cheap waveform* baseline.
3. **Fixed spectral prototype (M)**: nine Goertzel frequency energies (150,250,400,620,900,1250,1750,2500,3250 Hz), aggregated on 0.1s frames; cosine nearest class prototype using fold-1 only. If class cosine-score difference less than **0.07**, abstain. Classify low-RMS slot as `none`. No external model or learned embeddings.

For Z/M report: **correct positive associations / 6**, **false positive associations / 42**, **missed positives**, **correctly rejected negatives**, **query-level abstention count** and exact source-group outcomes. Compare M vs Z—not merely against identity-blind E. If M gains no reliable value or Z dominates, **STOP extra spectral complexity** for this task.

### Sensor and evidence integrity

Any missing source, metadata mismatch, license mismatch, unsupported audio encoding, incomplete WAV frames, clip-source reuse across train/eval, or clipped constructed waveform **aborts**. NEVER replace failed audio downloads with synthetic tones, invented output or a different file. Record actual clip SHA-256 hashes, Python version, CI logs, source-fold identities and limitations. Never infer physical object origin, mechanic diagnosis or human mental state from clip labels.

**Scientific HOLD:** This is an extremely small exploratory real-recording benchmark with constructed mixtures and oracle slots. Even a perfect score would NOT demonstrate soundscape source localization, general acoustic understanding, or useful farm equipment fault diagnosis.

## STOP/GO

GO only for execution feasibility if license/source verification, WAV reads, exact group split and all tests succeed. A result with all abstentions must not be called success; an identity-blind energy alert must not be scored as class attribution. Stop any interpretation that fails to preserve the class/event/physical-source distinction.
