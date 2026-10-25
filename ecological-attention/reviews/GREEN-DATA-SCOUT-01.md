# Dataset scouting and qualification — GREEN-DATA-SCOUT-01

**Date:** 2026-10-25. **Status:** DESK RESEARCH / NOT ADMITTED / NO BYTES DOWNLOADED / NO ANNOTATION OR EXPERIMENT EXECUTED.

## Scope and scientific boundary
This review checks published primary dataset descriptions and licensing claims, **not** original file hashes, constituent-video rights, annotation accuracy or operational usability. Existing animal labels are not automatically temporal ground truth for **non-task events**. No candidate is admitted for EXP-001 confirmation. The original farm insect clip remains outside the public dataset.

| Candidate | Primary-source evidence | Strength | Blocking uncertainty / cost | Preliminary disposition |
| --- | --- | --- | --- | --- |
| Seattle(ish) Camera Traps | https://lila.science/datasets/seattleish-camera-traps/ | ~4,500 intact videos from an ordinary consumer camera; labeled 'empty' instances; LILA lists CDLA Permissive | **Single backyard/site**, unreliable absolute capture date/time; mostly animal/empty labels rather than onset/offset; same-creator human present in portions of data; inspect selective sample and licensing before use | **CONDITIONAL — development pilot only** |
| MammAlps (v3) | https://zenodo.org/records/15588220 ; https://openaccess.thecvf.com/content/CVPR2025/html/Gabeff_MammAlps_A_Multi-view_Video_Behavior_Monitoring_Dataset_of_Wild_Mammals_CVPR_2025_paper.html | Nine cameras, three sites; ~14 hours of video; 8.5 hours dense behavior tracks; 397 multi-view longer events **including false triggers**, making it a serious alternative | CC BY-NC 4.0, **87.9 GB** archive; same event captured by multiple cameras (must group by event/site); event definitions differ from EXP-001; test availability of limited lawful clips | **CONDITIONAL — strong ontology reference; not admitted** |
| SA-FARI | https://www.conservationxlabs.com/sa-fari ; https://huggingface.co/datasets/facebook/SA-FARI | 11,609 wildlife videos, 99 species, 741 sampling locations; dense tracklets/segmentation | Dataset card says **CC BY-NC 4.0** and access through Hugging Face requests contact-information sharing; study says **every video contains at least one animal**, so no ordinary empty-trigger negative class; video species-negatives are not event-negative videos; data rights and access workflow need checking | **CONDITIONAL — benchmark/positive reference; not admitted** |
| Lindenthal Camera Traps | https://lila.science/datasets/lindenthal-camera-traps/ | 775 15–45-second RGB/IR/depth video sequences; groupable video source; LILA lists CDLA Permissive | Video package **213 GB** in RealSense rosbag format; annotations from sparse sampled frames and only a subset; specialized depth sensor; no ready temporal-event ontology; impractical as first $0 small pilot without partial access | **CONDITIONAL — lower priority; not admitted** |

## Cross-dataset warning
Camera traps are often **motion-triggered**, selecting observations precisely because motion occurred. That can bias estimates of true missed-event rates and false alerts during continuous observation. SA-FARI states all videos contain animals; “negative video–species pairs” must not be mistaken for empty scenes. Seattle(ish) 'empty' image counts do not prove corresponding continuously captured event-negative video intervals. MammAlps multiple views of one event are **not** independent events. Privacy/retention constraints persist even when data is ostensibly public.

## What evidence is still missing for admission
1. Verify specific candidate files, version, licensing scope, download access and allowable annotations/derivatives.
2. Establish actual recording/video IDs, site/session groups, timestamp integrity and sequences/false-trigger metadata for selected files.
3. Examine a small original sample to establish observable event categories and negatives.
4. Decide and freeze whether an event is an **observable state transition in time** or a more general ecological occurrence, independent of model categories.
5. Verify whether the dataset permits valid within-source development and truly independent site-level confirmation; if not, mark **UNKNOWN** and retain it as DEV only.

## Recommended direction
Begin with a **metadata/source audit** of Seattle(ish) and MammAlps before fetching footage. Favor a tiny two-annotator *ontology development* pilot, with a genuinely negative case set, if rights and appropriate files can be qualified. **Do not construct C1** or claim a research-performance result from the present evidence.

## Research-source audit
All descriptions above are from official dataset pages, repository cards and the CVPR paper, not independently examined video bytes or verified full chain of original constituent rights. Verify before re-use. No human participants recruited, no video downloaded, no experiment conducted.
