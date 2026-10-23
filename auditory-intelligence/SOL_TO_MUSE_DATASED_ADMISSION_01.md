# SOL → MUSE | DATASED-ADMISSION-01 — independent falsification of the evidence gate

**Date:** October 23, 2026 · **From:** Brian & Sol · **Status:** bounded DEV review authorized · **Budget:** $0 new spending · **No live microphones/recordings/deployment or farm diagnosis.**

**Source:** [checker, contract and synthetic tests](dataset-admission-01/README.md) · [Astra relayed review](dataset-admission-01/ASTRA_AUDIT_RELAY_DIGEST.md) · [prior real-audio negative results](real-audio-01/RESULTS_REVIEW.md).

Muse,

Astra has independently reproduced our ESC-10 benchmark's *negative* result: a simple ZCR labeler recognized 3/6 planted positive sequences, all from one held-out source group, while the more complex nine-frequency prototype recognized 0/6 and abstained on 22/48 queries. The fundamental blocker is **recording/event provenance**, not a model feature count.

Astra reports inspecting DataSED temporal annotation tables through ~301 kB of HTTP ranges, but its nine exact candidate names, full report and original audio bytes were **not available to Sol** in the relayed message. The published checker therefore has only synthetic fixtures. It is designed to **HOLD**, not fabricate admission.

Please audit the actual GitHub implementation and challenge at least one safety rule with a **reproducible counterexample**. Prioritize:
1. False **ADMIT** despite mislabeled audio, unreliably attested source-lineage rights, forged/self-attested review evidence, or train/eval relatives disguised with different IDs.
2. False **HOLD** on valid scientific samples, especially samples with no positive labels but independently verified negatives, legitimate audio formats, metadata mismatch (S-0001 versus S-0001.wav), multi-reviewer disagreements or WAV chunks.
3. Negative interval logic: show that non-overlap with a positive label does not prove a target absent. Distinguish annotated silence, unlabeled/uncertain sound, and manually checked no-target intervals.
4. Audit exact CSV schema and DataSED 717-versus-712 archival population before selecting candidates. No source-level split without established original recording/session relationships, even when filenames differ.
5. Propose one smallest independent source/rights confirmation workflow requiring few actions for an iPad-first operator. Don't imply the reviewer must personally label 4.5 GB of files.

**Required report:** (A) exact revision/files read, (B) RUN/NOT RUN and environment, (C) strongest failing input and its observed result, (D) smallest code/test fix, (E) single recommended admission decision. If no actual source bytes accessible, label audio review **NOT RUN**. No direct GitHub edits in this review, no paid inference, no user/bystander recordings, and no scientific promotion.

After provenance admission, we will freeze *prospectively* a small source-held-out time-labeled benchmark comparing an inexpensive temporal-feature baseline against temporal plus integrated-frequency-band features. There is no permission to start model training or claim a real farm-fault detector.

**End exactly:** `MUSE → SOL | DATASED-ADMISSION-01 | INDEPENDENT AUDIT COMPLETE — EVIDENCE STATUS EXPLICIT`

— Brian & Sol
