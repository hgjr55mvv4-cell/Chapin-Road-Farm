# AUDITORY-SOURCE-CROSSING-DEV-01 — Exposed source-factor diagnostic

**Engineering DEV / not run when frozen / scientific and field deployment HOLD.**

The original [AUDITORY-REAL-01](../README.md) evaluates two coupled source triples: each selects one held-out dog, chainsaw and rain recording together. An independent audit of AUDITORY-REAL-01 raised a source-identity confounding hypothesis. This pilot crosses the *same six* fold-2/3 held-out recordings into all 2 × 2 × 2 = **8 configurations** while preserving the fixed frozen decoder, training prototypes, energy/ZCR/nine-frequency methods, normalization, 0.8s excerpt choice, source labels, slot boundaries, and thresholds.

Each configuration repeats the existing eight schedules and three gains, yielding **192 constructed rows**. There are **only six distinct evaluation recordings**. Neither eight configurations nor 192 rows are independent samples of new sounds. The two original diagonal pairings must reproduce every one of the [48 prior decisions](../receipts/real_case_decisions.csv) or the script fails.

## Public reproduction

From `auditory-intelligence/real-audio-01` on a networked Python 3.11+ host:

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s source-crossing-01/tests -v
python3 fetch_clips.py
python3 source-crossing-01/source_crossing_dev.py --out crossed_results.json
```

The downloader enforces the pinned ESC-10 metadata and individual CC0 source licenses. The diagnostic separately checks all ten SHA-256 values against the unchanged [source receipt](../receipts/source_sha256.json). No source WAV is republished. Missing files, changed hashes, mismatched source IDs, clipped mixes and diagonal-control disagreements fail closed.

The output includes all 192 rows plus per-configuration correct-positive, false-alert and abstention counts for each method. A new [GitHub Actions workflow](../../../.github/workflows/auditory-source-crossing-dev01.yml) executes this isolated diagnostic and retains a temporary JSON artifact. Its CI results, if any, must be checked separately; publication of this script is not an execution receipt.

## Frozen contract

- **Incumbent:** AUDITORY-REAL-01, 2 coupled triples, 48 exposed rows; unchanged.
- **Trigger:** the group-0 versus group-1 outcome cannot separate individual dog, chainsaw and rain effects.
- **DEV action:** preselected full Cartesian crossing of existing six held-out sources, with 24 repeated treatments per triple; no retuning or cherry-picking.
- **Success:** source license/pinned-byte chain remains valid; two original diagonal groups exactly reproduce; eight groups and 192 rows score without clipping; source-specific patterns are exposed.
- **Safety/quality floor:** no network except authenticated public dataset retrieval via the existing downloader; no private recordings; no production decisions; no original code/receipts modified; $0, ten-minute CI job ceiling.
- **Falsifiers:** any original diagonal mismatch, hash mismatch, invalid source split, changed counts, or false claim of independent statistical power.
- **Selection:** all source triple indices are frozen before CI: (0/1 dog) × (0/1 chainsaw) × (0/1 rain). Same underlying recordings were already exposed: DEV only, not prospective scientific confirmation.

### How to read a result

A source-specific dependence in these eight combinations would strengthen the need for *new independent source IDs*, but would not identify a causal recording feature. No effect would not prove generalization. All summaries must be grouped by source identity; **do not treat repeated gains or crossed reuse as independent n**. We do not evaluate natural onset localization, physical emitters or farm machinery.

Next stage, only if useful: independently reserve new eligible ESC-10 clips after validating pinned metadata and original CC0 licenses. The official pinned ESC-10 metadata has 40 recordings per class (eight in each fold), but the individually CC0-eligible number of unique Freesound source IDs differs substantially by class. Source IDs, not WAV takes or their Cartesian products, constrain independent evidence.
