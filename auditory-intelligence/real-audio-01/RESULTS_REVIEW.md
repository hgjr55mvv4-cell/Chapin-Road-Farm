# AUDITORY-REAL-01 — exact GitHub execution receipt

**Status:** EXPOSED REAL-RECORDING CONTROLLED MIXTURE DEV; no real-world auditory understanding or physical-source attribution. **Source commit evaluated:** `4c66d143dd3355a789f1ca08b847fbc87491906b`, on branch `research/auditory-real-esc10-controlled-mixtures-v01`.

[GitHub Actions run #40003763414](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions/runs/40003763414) executed real-data evaluation twice (Python 3.11 job `120586330713`, Python 3.13 job `120586330249`). Both jobs: **8/8 offline tests passed**, ten actual upstream WAV downloads (each 441,044 bytes), pinned `meta/esc50.csv` and `LICENSE` checks passed, and 48 real-clip mixture rows produced.

**Outcome (48 constructed rows; 6 planted positives, 42 planted negatives, only 2 independent sets of evaluation clips):**

| Method | Positive associations | False-positive associations | Abstaining queries |
|---|---:|---:|---:|
| RMS two-active-regions (NOT class identity) | 5/6 raw two-activity alerts | 16/42 raw two-activity alerts | 0 |
| ZCR class-label heuristic | 3/6 | 0/42 | 0 |
| 9-frequency class prototype | **0/6** | 0/42 | **22/48** |

**The ZCR success is all in one held-out source group:** on source group 0 it scored **0/3**, on source group 1 **3/3**. Gains are repeated treatments, not independent samples. The spectral prototype missed all positives; zero false positives arose alongside low useful coverage. **This is a negative engineering result for the richer representation under this frozen implementation**.

**Exact case outcomes:** [all 48 case rows](case_decisions.csv), with slot-source labels, gain, every arm's decisions. A classifier receives the **oracle** slot boundaries and source audio already peak normalized and resampled. It does not identify original spontaneous sound onset, overlapping original source identities, an actual dog or a particular chainsaw.

**Input SHA-256 at pinned ESC-50 revision:** [verified hashes](source_sha256.json). The sources are individually marked CC0 in the upstream `LICENSE`, drawn from CC BY 3.0 ESC-10. **No original audio is in this repository.**

**Structured artifact:** [Python 3.11 GitHub archived JSON](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/actions/runs/40003763414) and Python 3.13 artifacts (30-day retention) contained an identical `results.json`; original uncompressed file **SHA-256 `4ccc41912a9a0ba05790828a989b3efffe8874e873124b479fbc0e5da5c35d0c`** in both. ZIP artifact digest differs by metadata but JSON payload hashes match. Persistent compact case CSV sha256 **`c5f14b064d8f2d05ea71520c182cdf0fe8e14b4f1d836ec20b0de6b4345b27ad`**.

### Independent status and decision

**What ran:** actual 10 downloaded environmental WAVs, checked class/fold/source and license; controlled mixture scoring on Python 3.11 and 3.13, source SHA hash matching, all rows preserved. **What did NOT run:** DataSED/DESED strongly labeled event timestamp benchmark, real-time audio sensor, source localization, generalization to more than two source groups, trained LLMs or mechanical fault diagnosis.

**GO:** This code establishes a rights-safe first actual-waveform pipeline with honest recorded results.

**STOP / REVISE:** Do **not** promote the richer 9-bin spectral prototype. Do not claim calibrated low false alerts from 42 dependent negatives, or general effectiveness of ZCR based on a single successful held-out recording group. Next step: independent adversarial review by Astra, with Muse invited to challenge source selection and event-boundary leakage. Build a truly time-labeled, independently sourced test only after verifying annotations and permissions.

**Scientific confirmation:** HOLD. No audio-derived farm diagnosis or inference about individual speakers or physical equipment.
