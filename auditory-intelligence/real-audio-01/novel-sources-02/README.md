# AUDITORY-NOVEL-SOURCES-DEV-02 — new-source-ID diagnostic

**Frozen source-selection and method contract, exposed engineering DEV only.**
Scientific confirmation, human-listening interpretation and farm deployment: **HOLD**.

The previous [eight-way source crossing](../source-crossing-01/README.md) reused six held-out recordings and uncovered source-configuration sensitivity. This experiment uses **15 different ESC-10 original Freesound source IDs**—five dog, five chainsaw, five rain, with no source ID overlapping any of the original ten training/evaluation recordings. The original four training examples and **unchanged** [real_audio.py](../real_audio.py) algorithms remain fixed.

## Pre-committed selection

Dataset: [ESC-50](https://github.com/karolpiczak/ESC-50) at immutable commit `33c8ce9eb2cf0b1c2f8bcf322eb349b6be34dbb6`; ESC-10 entries only. Accept a WAV only when the pinned metadata confirms its class, source ID and fold; the pinned original LICENSE explicitly marks its Freesound original **CC0**; and its source ID is absent from all ten original experiment recordings. Within a source ID, use the lexicographically first WAV filename. Before examining any new outcomes:

- **Chainsaw:** all five remaining CC0 unique IDs (three from fold 4, two from fold 5). No additional eligible distinct IDs remain in folds 2–3 once the original study’s IDs are excluded.
- **Dog and rain:** lowest numeric source ID in each of folds 2, 3, 4 and 5, then lowest numeric eligible ID not already selected.
- The exact [source list](selected_sources.json) was frozen at SHA-256 `bb6d17f2fb8f81db7b74f45ea0120716433263bf8edf088bdb0b83524de38b11`. A source-list edit invalidates this test version.
- The algorithm bytes are pinned to SHA-256 `3dc01418d91546e373b21520b25f22b4ae4909070df2903a70d54da479c3e014`. Any source change fails rather than silently retunes the method.

This is a deterministic convenience sample, **not** a random draw from a general acoustic population. The unequal availability of individually CC0-licensed source identities prevents pretending the classes are fold-balanced.

## Experimental unit and construction

Full Cartesian crossing: **5 × 5 × 5 = 125 mixed-source triples** from **15 distinct original Freesound source IDs**. Each triple receives exactly one `0.50` gain and four active-slot schedules:

1. `dog → chainsaw` (one planted positive)
2. `chainsaw → dog`
3. `dog → dog`
4. `chainsaw → chainsaw` (three planted negatives)

Total **500 constructed rows**, 125 positives / 375 negatives. The *methods* (energy, ZCR, nine-band), training prototypes, frame/feature math, normalization, 0.8-second highest-RMS excerpt, noise bed, and oracle insertion slots at 0.4/1.6 seconds stay unchanged.

**Important:** The 125 triples are not 125 independent source recordings. Each of the 15 source IDs occurs in 25 triples, and all share a fixed training set and authored mixing rules. Report per-source and per-triple descriptive outcomes. No row-level confidence intervals, population error bars, source-object identity, natural event-onset, speech or human perception claims.

The energy method measures two active slots only; it is *not* a dog-vs-chainsaw classifier. ZCR and nine-band are compared on the same cases as cheap matched baselines.

## Execute from `auditory-intelligence/real-audio-01`

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s novel-sources-02/tests -v
python3 fetch_clips.py
python3 novel-sources-02/fetch_novel.py
python3 novel-sources-02/novel_source_dev.py --out novel_source_results.json
```

The existing downloader validates the ten historical files. The new downloader checks pinned ESC-10 metadata, attribution and CC0 license for all 15 new WAVs and saves them locally only; **WAV files are not committed or rehosted**. The analysis checks the original four training WAV SHA-256s against the historical receipt, computes SHA-256s for every new WAV, checks source isolation, abstention and mixture clipping, and writes all 500 row-level decisions plus grouped summaries.

[Isolated CI workflow](../../../.github/workflows/auditory-novel-sources-dev02.yml) runs in Python 3.11 with a 12-minute time ceiling, no paid API, repository read-only permissions, and a temporary JSON artifact. At freeze, new WAV execution is **NOT RUN**; only a passing CI job can establish engineering execution.

## Falsifiers and next action

- Missing/unlicensed/misidentified or LFS-pointer WAV; hash mismatch; duplicate ID; source fold/role drift; selected manifest edit; changed algorithm bytes; missing result; clipped waveform; incomplete test schedule => **BLOCK**.
- Matching or not matching previous six-source outcomes does not by itself prove generalization. Treat unusual source-specific combinations as candidates for source-controlled follow-up.
- The five new examples per class are **consumed development cases after execution**, not independent future confirmation. A next version must state material novelty, preselect genuinely unseen source IDs when possible, and count operator/network burden as well as score changes.

Budget ceiling: **$0, ≤12 min per CI run**, stdlib only. Evidence floor: license+identity checks, preserved historical code, deterministic case selection, no synthetic fallback, no private data, and explicit uncertainty.
