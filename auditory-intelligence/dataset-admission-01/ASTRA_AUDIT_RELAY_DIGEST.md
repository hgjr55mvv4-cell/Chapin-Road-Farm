# Astra → Sol | AUDITORY-REAL-01 independent review — attributed digest

**Date:** 2026-10-23. **Source:** user-relayed message attributed to Astra, not authenticated original full A–J report. The named `AUDITORY_REAL_01_INDEPENDENT_REVIEW.md` and ZIP files were referenced but their bytes were **not accessible in this conversation**. Do not attribute this gate's source code to Astra.

## Astra's reported original execution

- Python 3.12.14, fetched ten pinned public ESC-10 recordings, verified source checks/hashes, reproduced original eight unit tests and all 48 predictions. Regenerated `results.json` matched published SHA-256. Read both original CI logs.
- Class-agnostic energy: 5/6 two-active-region alerts, 16/42 false two-active-region alerts (not valid class attribution).
- Zero crossing rate (ZCR): **3/6 positive ordered categories**, **0/42 false ordered-category alerts** on heavily dependent source sets. Every successful positive belonged to one evaluation-source group. Its four training excerpts already overlap: nearest-mean misclassified two of its own references.
- Nine-frequency prototype: **0/6 positives**, **0/42 false ordered-category alerts**, **22/48 queries with abstention**. Removing the abstention margin only recovered **2/6 positives** in exposed cases, showing both margin and wrong-rank issues. Nine isolated frequency bins do not preserve temporal envelopes/order.
- Strong dependence: 48 rows encode **44 distinct mixtures and 28 distinct slot waveforms**, appearing 96 times. No independent population uncertainty interval is justified.
- Background confounding: changing only rain caused one fixed dog/chainsaw pair to change ZCR predictions; mixed source recombinations showed spectral information still can be informative, without constituting independent improvement.
- **Crucial label problem:** an energetic crop from a clip with class tag `dog` or `chainsaw` may not contain the event. Astra did not independently listen to those excerpts; natural-event label validity remains UNKNOWN.

## Dataset access findings *reported*, not independently rerun here

Astra says it read DataSED's ZIP metadata using seven HTTP byte-range requests totaling 300,891 bytes, recovering archive directory and both annotation tables without downloading ~4.5 GB of audio. The release includes human temporal labels, edited clips and incomplete annotation coverage. No per-file original-source/attribution lineage was found. An attempted candidate selection was unbalanced: four dog, four other, only one vehicle-idling recording. **The nine exact candidate filenames were not present in the relayed text.**

## Astra's recommendation

**REPAIR BENCHMARK / LABEL PROVENANCE FIRST. STOP nine-frequency promotion.** Before another classifier: confirm the original source/session identity and rights, independently audit a small admissible audio excerpt against the time label, identify genuinely verified negatives, exclude uncertain spans, and stop if source independence or usable labels are absent. Proposed six-feature temporal baseline vs temporal+frequency-bands contender is **DESIGN / NOT RUN**.

## Sol implementation status

A standalone [dataset admission checker](README.md) is authored **by Sol**, not part of Astra's unavailable source package. Its synthetic unit tests check fail-closed evidence rules. **It cannot invent the missing original source lineage, listening receipts, or real audio.** Until an independently reviewed small DataSED sample is supplied, scientific real-event admission remains HOLD.

