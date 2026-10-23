# Real-audio dataset reconnaissance — 2026-10-23

**Research only; no external corpus downloaded or executed in DEV-02 v0.1.** This file is a candidate registry, not a list of validated training inputs. Preserve dataset-source URLs, DOI, version, category, sensor type, event-label granularity, rights, split and potential contamination. Challenge-imposed rules are separate from Creative Commons license rights.

## Lane A — event identity, overlap and temporal association

| Source | Labels / potential test | Limit or action |
|---|---|---|
| [DataSED — environmental sound event detection](https://zenodo.org/records/15346092) (DOI 10.5281/zenodo.15346092) | Real recordings, expert-labeled event onsets/offsets with mono and polyphonic labeling; outdoor/rural categories such as machinery, vehicle idling/pass-by and workshop | **Most immediately relevant** to wrong-event association. Official Zenodo record says **717 WAVs / 17.02 h**, but the October 2025 paper states **712 recordings**; version/revision difference must be resolved and the **exact file-level licenses** verified before use. ~4.5 GB full archive, no download now. |
| [DCASE 2025 Task 3, stereo SELD](https://dcase.community/challenge2025/task-stereo-sound-event-localization-and-detection-in-regular-video-content) | 13 strongly time-labeled classes including speech, footstep, door, knock, plus spatial sound direction; up to several simultaneous events | Strong for distinguishing *which source*, not for our tone frequencies. Development+evaluation roughly **27.6 GB**; specialized stereo/spatial sensor and dataset permissions. Use dev/test splits as provided, no training on evaluation. |
| [DESED / DCASE 2023 Task 4](https://dcase.community/challenge2023/task-sound-event-detection-with-weak-labels-and-synthetic-soundscapes) | Strong onset/offset labels in validation/evaluation and synthetic mixtures with explicit event schedules | Good near-term test of sound-event detection; home-domain sounds not farm. License varies by sourced audio; validate individual provenance. |
| [FUSS sound separation](https://zenodo.org/records/3710392) | Synthetic mixtures with source-separated reference stems; source mixture test | Very useful for checking *source assignment* under overlap; not necessarily labeled intended mechanical events. Large 24+ GB archive and rights by components; defer. |
| [FSD50K](https://fsannotator.upf.edu/fsd/release/FSD50K/) | 51,197 human-tagged Freesound clips across 200 classes, mixed licenses | **Weak clip-level labels** rather than guaranteed time-localized event identities. Useful to select isolated event sources or stress generalization, not direct ground truth for ordered event association. Check individual Creative Commons terms. |

## Lane B — machine-specific abnormal sounds (later VFM Acoustic Mechanic)

| Source | What is recorded | Limits / rights |
|---|---|---|
| [DCASE 2025 Task 2](https://dcase.community/challenge2025/task-first-shot-unsupervised-anomalous-sound-detection-for-machine-condition-monitoring) | 7 development machine types **including gearboxes and bearings** (also fans, slide rails, toy car/train, valves), normal/anomalous mono clips with operating domain shifts | Strongest initial real-machine benchmark. Development ~**2.93 GB**; labels are condition-level, not verified location of a click or wheel-bearing cause. Respect challenge train/test and linked source license conditions. |
| [MIMII](https://zenodo.org/records/3384388) | Pumps, valves, fans, slide rails, real industrial machine sound with background noise | **CC BY-SA 4.0**, large ~**100 GB** full record. Normal/anomalous labels, not farm diagnosis; dataset source/version and redistribution obligations matter. |
| [IDMT-ISA-ELECTRIC-ENGINE](https://www.idmt.fraunhofer.de/en/publications/datasets/isa-electric-engine.html) | 2,378 short recordings from three small electric motors under good/heavy-load/broken conditions | **CC BY-NC-ND 4.0** evaluation use; useful for distinguishing load vs fault, but license restricts commercial/derivative redistribution. Not a tractor engine or wheel bearing. |

## Dataset decision and next gates

1. **Current DEV-02 v0.1:** remain all-synthetic, because event source truth can be independently generated and full correctness can be inspected without licensing or sensor-format ambiguity. Do not retrain/tune on reported cases and call them independent confirmation.
2. **Next real event benchmark candidate:** DataSED (prefer time-labeled polyphonic subset) or DESED strongly labeled validation, only after exact archive revision and file-level license audit; use original sampling rate/features, not pretending 8kHz tone templates recognize arbitrary noises.
3. **VFM machinery candidate:** DCASE Task 2 **bearing/gearbox** subsets, compare under recorded RPM/load/domain attributes. Condition labels alone never identify physical fault source; mechanic diagnosis and safety clearance remain HOLD.
4. **Source separation:** FUSS or DCASE Task 3 when the study needs multiple concurrent sources, only after computational feasibility and provenance audit.
5. **Human factors:** No available dataset here labels a person's personally meaningful music or their correct response in a farm conversation. Don't substitute machine labels or prosody tags for that ground truth.

**Recorded:** Research links checked from original dataset/steward pages or papers. Dataset archives were **not downloaded**, their individual license files **not inspected**, and no audio from these sources was evaluated in this run.