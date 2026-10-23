# AUDITORY-REAL-01 — CC0 source clips in controlled mixtures

**Status: ENGINEERING DEVELOPMENT / exposure known / field diagnosis HOLD.** This benchmark tests if extremely simple acoustic features can recognize an **experimenter-inserted pair of clip-level source categories** in a controlled sound mixture, using actual recorded environmental WAV samples rather than oscillator tones.

- [Frozen pre-execution design](CONTRACT.md) (implementation was drafted first, so not scientific preregistration)
- [Exact pinned ESC-10 source manifest](sources.json)
- [Executable decoder, two baselines and mixture evaluator](real_audio.py)
- [Fail-closed downloader that verifies dataset CC-BY subset and original CC0 licenses](fetch_clips.py)

The official [ESC-50 dataset](https://github.com/karolpiczak/ESC-50) states ESC-10 is CC BY 3.0, while each selected Freesound original is individually marked CC0. The benchmark retains original authors, source Freesound IDs, dataset commit, exact WAV hashes, train/eval folds and generated case-level decisions. **No dataset audio is committed or redistributed**. CI downloads the ten selected source WAVs transiently.

Run on a networked machine with Python 3.11+:

```sh
python -m unittest discover -s tests -v
python fetch_clips.py
python real_audio.py --audio-dir clip_cache --manifest sources.json --out results.json
```

The task uses fold-1 source identities for category reference and fold-2/3 sources for evaluation. There are two evaluation source sets reused for eight insertion schedules and three gains: 48 test rows, **6 positive/42 negative**, but **only two source sets**. Evaluation is not an independent random population sample. The comparison is energy-only two-active-region alert versus cheap ZCR class heuristic versus richer 9-bin fixed spectrum prototypes.

**Very important:** ESC-50 supplies *clip-level* labels (dog, chainsaw, rain), not naturally timed event or physical-object/source identity. The experiment creates 0.8-second windows and insertion times itself, and gives both baselines those **oracle slot boundaries**. This can test neither free-form onset localization nor which physical dog/machine produced the recording. Also not machine anomaly detection or field-ready VFM diagnosis.

## Actual reproducible outcome — CI verified

Python 3.11 and 3.13 GitHub Actions [run 40003763414](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions/runs/40003763414) each passed **8/8 offline tests**, retrieved **10 real WAV recordings** with verified pinned attribution/metadata, and completed 48 mixture queries. Their structured JSON payloads were **byte-identical** (SHA-256 `4ccc41912a9a0ba05790828a989b3efffe8874e873124b479fbc0e5da5c35d0c`).

[Evidence-based findings and source limits](RESULTS_REVIEW.md): raw energy detected 5/6 positives but made 16/42 false two-active-region alerts (not class identity); ZCR identified **3/6 positives**, all from one source group, with 0/42 false ordered-class alerts; the supposedly richer nine-frequency spectral model identified **0/6 positives**, 0/42 false positives and **22/48 abstaining queries**. Keep these failures; do not retune this same two-source evaluation population and claim confirmation. [All 48 cases](receipts/real_case_decisions.csv) and [exact source hashes](receipts/source_sha256.json) are permanently in the repository.

**STOP spectral promotion:** The richer method did not earn complexity on this bounded sample. Real-onset localization, unscripted soundscapes, real-world physical object identity and VFM diagnostics are untested. [Astra's independent red-team assignment](../ASTRA_REAL_AUDIO_01_REVIEW.md) is ready.

If a future run cannot retrieve source files, verify licenses, or decode them, the real-audio evaluation is **NOT RUN**—do not fall back to generated signals or claim a result.

Next: a separately designed, strongly time-labeled public benchmark and physical source-association controls. DataSED/DESED may support event labels; DCASE Task 2 pertains to normal/abnormal machine condition, not identification of an individual sounding fault component.
