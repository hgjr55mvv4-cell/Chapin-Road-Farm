# AUDITORY-EVENT-INCREMENT-02 — frozen DEV contract v0.1

**Scope:** rights-free mono 8-kHz PCM16 symbolic-tone WAV only; no humans, speech, acoustic fault diagnosis, or real sensor. **Exposed DEV**: fixture and implementation will be openly co-developed; results are not prospective science.

## Target and observable truth
A *positive* capture contains a deliberately scheduled **440 Hz A tone followed by a 620 Hz B tone**. A *negative* contains A with no B, A followed by 760 Hz C instead of B, or B before A. Independent generator event schedules, not detected activity regions, define intended events and onset/offset. Background and distractors are independent components; their energetic intervals do not acquire target identity just because they happen to be selected by a detector.

Compare candidate arms on identical WAV bytes and allowed metadata: (T) externally supplied generic text with no event labels (text-only null), (G) event-blind aggregate activity intervals with gold timing (non-deployable information diagnostic), (E) existing low-cost RMS two-region detector (practical), and (F) a **simple frequency-specific A/B detector**. Richer representations are deferred unless F has a measured failure they can address. T and G cannot infer frequency identity from word/time labels; no fabricated content labels.

## Fixed generator/evaluation plan
Independently seeded **400 paired scenarios**: each pair contains one positive and one matched negative sharing background, gain, echo, distractor, latency pattern. Positive A/B scheduled before B; negative B omitted, replaced with 760 Hz, or reversed. Perturbations vary noise amplitude, dropout, soft onset, mild echo, target attenuation and 310 Hz interference. Seed for published DEV evaluation: **20261023**, all pairs public; no assertion of blinded holdout. Gold includes intended onset and offset. Transport-invalid cases (truncated/invalid WAV and saturation) are evaluated separately. 8-kHz PCM16 audio under the v0.1 ≤256 KiB/15s transport limits.

## Predicates and metrics
- Positive detection: algorithm returns MATCH_A_THEN_B and the intended A/B times it reports are within 100 ms of source schedule. If it returns MATCH_A_THEN_B but references wrong event times, count as **wrong association**, not a correctly identified positive.
- Negative: any confident MATCH_A_THEN_B is false assurance, even if the region gap is a valid measurement.
- Abstention: explicit uncertainty is distinct from NO_MATCH. Report both total coverage and rates conditional on decided cases. **Always-abstain does not count as success.**
- Report TP/(400 positives), wrong-time association count/(400 positives), false assurance/(400 negatives), abstentions by class, sensor-invalid confident decisions/(invalid cases), and per-case runtime. Group pairs, not individual tones, for uncertainty.
- Do not claim a single threshold generalizes to speech, equipment, other acoustic settings or future human decisions. Failure to distinguish event classes, confident wrong-time associations or invalid input yielding MATCH block promotion.
- Incremental benefit of any richer detector must be shown against F, not text-only T.

## No future leakage
Post-hoc event association here is *retrospective*. For a future streaming rule at cutoff t, the policy must see **only samples up to t**; two recordings with identical prefix must have indistinguishable decisions until divergence. Streaming turn prediction is NOT part of v0.1.

## Safety/evidence
Sensor transport OK ≠ source event association verified ≠ real-world machine fault or human intention. An acoustic class 440/620 is an artificial source label only. No actual farm machine, mic, speech, music, physical-world control, paid API, private recordings or consent-sensitive material permitted.