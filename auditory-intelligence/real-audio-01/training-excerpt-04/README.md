# AUDITORY-TRAIN-EXCERPT-DEV-04 — frozen training-only sensitivity

**EXPOSED ENGINEERING DEV. No scientific confirmation, human listening claim, or farm deployment.**

DeepSeek's 2026-10-24 independent static review proposed a cheap new falsifier: perhaps the original highest-RMS **training** excerpts created narrow spectrum templates. This experiment isolates that factor without changing the [PR #69](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/pull/69) evaluation recordings, labels, source triples, rain beds, normalizations, 0.50 gain, oracle slots, or the original [`real_audio.py`](../real_audio.py) algorithms.

## Frozen version and selection

The [exact contract](frozen_contract.json) is frozen at SHA-256 `54b3717be2004da81d65074f5b5b2d394995212f191c7d60408278fcbeb8a4ff`; any material edit requires a new candidate version and new evidence. Baseline algorithm SHA-256 `3dc01418d91546e373b21520b25f22b4ae4909070df2903a70d54da479c3e014`; PR #69 source-selection SHA-256 `bb6d17f2fb8f81db7b74f45ea0120716433263bf8edf088bdb0b83524de38b11`; prior public CI group receipt SHA-256 `b11e089a5a039d37043b5d2e2735ff0fdbb97c24849d1ed1f11820662b3a5f9e`.

Four fixed training WAVs, original Freesound source IDs `100032`, `30226`, `116765`, `47250`; dog has two and chainsaw two. Before hearing new outcomes, `random.Random(20261024 + int(source_id)).sample(range(17),3)` selected three distinct `0.8s` window starts per source from the 0.25s grid (0–4 seconds). The **explicit offsets in the contract** are the authoritative selected cases. Never reroll or replace quiet windows based on results.

Arms:

- **T0 original:** Each training example uses the original highest-RMS 0.8s excerpt, peak-normalized.
- **T1/T2/T3:** For all four training recordings, use respectively the first/second/third preselected offset and apply exactly the same peak normalization. Recompute the original two-class prototypes using unchanged `train()`. No hyperparameter or feature tuning.

All arms classify the **identical 500 PR #69 evaluation mixtures** formed from 15 previously unused evaluation source IDs in 125 reused triples and four fixed active-slot schedules. Arm T0 must reproduce *all* PR #69 source hashes, method totals and five per-dog source result distributions before alternative arms score. A further row-by-row check verifies T0 predictions from reconstructed mixtures equal the frozen baseline. Training windows with peak below the original `.002` validity threshold cause a controlled failure—no resampling.

## Reproduction

From `auditory-intelligence/real-audio-01` on a networked Python 3.11 host:

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s novel-sources-02/tests -v
python3 -m unittest discover -s training-excerpt-04/tests -v
python3 fetch_clips.py
python3 novel-sources-02/fetch_novel.py
python3 training-excerpt-04/training_excerpt_dev.py --out training_excerpt_results.json
```

All WAVs are retrieved through the existing pinned public CC0 license checks, locally only; no audio is republished. A separate [read-only GitHub Actions workflow](../../../.github/workflows/auditory-training-excerpt-dev04.yml) runs the test for ≤12 minutes, cost $0, and retains a temporary machine-readable artifact. **Execution status at freeze: NOT RUN**.

The output reports all arm-specific method counts, per-dog-source detections, training window RMS/peak and peak-offset coincidences, exact source SHA-256s, and paired changes in category decisions/abstention. Totals over 500 repeated mixtures remain *descriptive*; per-source effects are not estimates based on 500 independent recordings.

## Success, falsifiers, interpretation

Success means valid source/case identity, exact T0 reproduction, and a reproducible measurement of performance sensitivity when *training excerpts alone* change. Improving a score is not the objective.

Fail if any baseline source/receipt/hash changes, training source overlaps evaluation IDs, selection offsets change, a frozen window is invalid, constructed mixtures drift, T0 outputs differ, or claims incorrectly treat the 125 reused triples as independent.

A large T0→T1/T2/T3 score change demonstrates sensitivity of the four training prototypes to excerpt selection. **It does not establish that the original template was false or that any selected 0.8s interval actually contains an audible dog or chainsaw.** The ESC-10 labels describe whole recordings, not those windows. No result here can establish natural onset localization, physical emitter identity or farm diagnostic readiness.

DeepSeek's separate proposal to vary *evaluation* excerpts remains an **unbuilt** challenger. The training ablation cannot make that question scientifically unnecessary: both effects can coexist.

Only exposed DEV cases are used; source IDs and results from PR #69 were already public. No scientific promotion is permitted from this run.
