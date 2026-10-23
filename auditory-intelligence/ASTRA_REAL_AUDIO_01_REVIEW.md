# ASTRA — AUDITORY-REAL-01-INDEPENDENT-REVIEW
## A real-recording null result: did extra acoustic sophistication actually help?

**From:** Brian & Sol · **Date:** October 23, 2026  
**Program:** Auditory Intelligence / Harbor Co-Listener / VFM Acoustic Mechanic  
**Role:** Independent scientific reviewer and adversarial software auditor  
**Status:** Source-grounded review authorized; **no direct GitHub edits, paid inference, private audio or field diagnosis**.  
**Budget:** $0 new expenditure · **Scientific confirmation:** HOLD.

## Start from evidence, not our preferred architecture

Our historical [AUDITORY-EVENT-02](event-increment-02/README.md) passed a deliberately synthetic 440→620 Hz tone-class task (314/400 planted positives recognized, 0/400 planted negatives falsely accepted by a fixed frequency template). We then asked whether that result survives any kind of *real* recorded sounds.

Sol has now implemented [AUDITORY-REAL-01](real-audio-01/README.md), with a [frozen pre-execution DEV contract](real-audio-01/CONTRACT.md) and [actual execution record](real-audio-01/RESULTS_REVIEW.md). It uses ten small, checked ESC-10/ESC-50 WAV clips. Pinned dataset revision and source provenance are recorded; training references use independent fold-1 Freesound source IDs, evaluation uses fold 2/3 recordings and a rain background. No WAV bytes are distributed in our repository.

**Important: the real clips are labeled only at the *whole-clip class* level.** The test takes energetic 0.8s excerpts and inserts them into two operator-known event slots; the resulting timing ground truth is *constructed*. Every classifier receives those same **oracle window boundaries**. Nothing here establishes natural event-onset localization, physical source identity, original field acoustics, or a machine fault.

### Actual results (GitHub Python 3.11 + 3.13, 8/8 tests each)

48 constructed queries = **6 target dog→chainsaw** cases and **42 other** schedules. These 48 rows reuse **two** held-out source groupings, so results are strongly dependent.

| Source-conditioned method | Target sequences recovered | False alerts | Query abstentions |
|---|---:|---:|---:|
| Class-agnostic two-active-region energy alert | 5/6 | 16/42 | 0 |
| Cheap ZCR-based class heuristic | **3/6** | **0/42** | 0 |
| 9-bin frequency-prototype model | **0/6** | 0/42 | **22/48** |

The **three ZCR successes came from only one held-out source group**; it scored **0/3** on the other group. The multiband method has *zero useful true positives*; its low false-alert count is not a success. The energy alert has no class identity and must not be credited with identifying dog/chainsaw even when a two-active-region event is correct.

Original 10 audio SHA-256 hashes, every case and original GitHub CI logs/structured artifacts: [case CSV](real-audio-01/receipts/real_case_decisions.csv), [source hashes](real-audio-01/receipts/source_sha256.json), [verified run 40003763414](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions/runs/40003763414). Byte-identical `results.json` from Python 3.11/3.13 has sha256 `4ccc41912a9a0ba05790828a989b3efffe8874e873124b479fbc0e5da5c35d0c`. This is exposed DEV co-designed evidence, not a held-out scientific confirmation.

**This negative finding is our reason for requesting your review.** Resist the temptation to explain it away with another complex audio model.

## Assignment

### A — Provenance and independence
Read actual GitHub source, contract, licenses, sample manifest, scored results and CI logs. List exact revisions and what was accessible. If you cannot access binary audio, say so. Do not invent a replay of the raw recordings.

### B — Dataset and ground-truth audit
Verify [ESC-50 repository's CC-BY-NC dataset versus CC BY ESC-10](https://github.com/karolpiczak/ESC-50), per-file source CC0 claims, folds, potential uploader/source contamination, and what the dataset's *clip-level* labels mean. Our constructed slots are not independently human-labeled natural events. Check whether energetic snippet selection itself biases outcomes. Find at least two reasons a real event of a clip's nominal class might not occur in the inserted 0.8s.

### C — Code and evaluation audit
Investigate parser/PCM resampling fidelity and aliasing, feature extraction, loudness normalization, source-window selection, gain choice, classifier margin and **what constitutes ABSTAIN versus NO_EVENT**. Check whether a detector can exploit artifacts from the recording, background, clip editing, or selected gain rather than class identity. Critically audit the 48 row denominator and exact paired source-group dependence.

### D — Strongest simple alternative
Challenge the idea that frequency prototypes are always better than cheap temporal/spectral cues. Compare or propose **one genuinely strong but bounded inexpensive baseline**, e.g. better zero-crossing + temporal-envelope features, or an honest pretrained audio embedding **only if already authorized and free**. Hold its training budget and information equal. Do not tune to the published two source groups and claim independent gains.

### E — Diagnostic failure analysis
Explain why the ZCR classifier succeeds only on one group, with multiple defensible hypotheses and a test capable of separating them. Explain why the nine-frequency cosine/margin arm missed all positives; calibrate the effect of its 22 abstaining queries. A software-only estimate of true population performance from six repeated positives would be invalid.

### F — Next honest dataset gate
Choose a **small, rights-cleared and genuinely time-labeled** event dataset or subset for the next stage (candidate DataSED or DESED). Check whether only a 4.5 GB archive exists or whether a rights-verified small access path is available. Distinguish timestamped *class* labels, separated stems, source provenance and actual emitter/object identification. No scraping or downloading huge corpora without approval; no private microphone input.

### G — One decisive follow-up experiment
Define a practical **source-held-out** benchmark with a frozen comparison: simple baseline vs richer contender, and negative controls for gain, microphone-like filtering, scene mixing and event timing. Predeclare a criterion that could cause the richer branch to be stopped, and a useful-coverage minimum so always-abstain cannot win. Keep individual source-group counts visible.

### H — VFM application boundary
We are investigating an eventual field tool that may help identify changes in older tractor/implement sounds. State explicitly which parts of the measured result have **no bearing on diagnosing a wheel bearing, pulley, engine or transmission**. Define how real machine-ID history, RPM/load/capture context, repair outcomes and human verification would be required before any field inference. Mechanical diagnosis and equipment safety clearance remain HOLD.

### I — Scientific objections and surprises
Find at least three assumptions Sol/Muse/Astra's prior synthetic experiments may have shared that were exposed by this first real-data run. If the added acoustic features offer no benefit over an appropriate simple control, recommend removing them. If even class labels are untrustworthy in selected snippets, recommend stopping this benchmark rather than embellishing it.

### J — Disposition and direct letter
Choose **GO to a strictly bounded new audio DEV**, **REPAIR/EXPAND this baseline first**, or **STOP this branch**. Provide an evidence-based rationale and a single smallest next execution. Write a candid direct letter to Brian, Sol and Muse identifying the strongest false-assurance risk.

No direct repository writes, paid API calls, human participant recordings, microphone capture, raw copyrighted music/audio redistribution or farm mechanical diagnosis. Source inspection and bounded free software-only reproduction authorized if actually available, with exact commands, hashes, receipts and RUN/NOT RUN labels.

We want the best argument against our preferred model, not an endorsement.

**End exactly:** `ASTRA → SOL | AUDITORY-REAL-01 | INDEPENDENT REVIEW COMPLETE — EXECUTION STATUS EXPLICIT`
