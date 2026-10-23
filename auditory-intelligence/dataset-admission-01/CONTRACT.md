# AUDITORY-DATASET-ADMISSION-01 v0.1 — frozen before real DataSED candidate intake

Date: October 23, 2026. Scope: scientific dataset admission, **not event detection or machine diagnosis**. All currently executed input cases are synthetic unit fixtures; no DataSED WAV files or the nine Astra-selected candidate IDs were supplied to this run. Research evaluation **HOLD**.

## Unit of analysis and expected evidence

One candidate WAV recording with an explicit original-source lineage and label table, plus a separate independently reviewed interval. Event spans and negative spans are separate units; the absence of an annotation is **UNKNOWN, not NEGATIVE**. All downstream metrics must group dependent transformations by original recording/source/session rather than use augmented windows as independent observations.

At minimum, require: dataset and exact revision; file-specific original recording ID and provenance evidence; processing/edit history; rights evidence; original WAV bytes and SHA-256; time-label CSV with filename, class, start/end seconds; manual reviewer identity and linked receipt for every prospective positive interval and any verified-negative span; verified disjoint recording lineage between train/eval.

**Hard gate:** any missing original recording, incompatible WAV/declared frames, unsupported size (>64 MiB), audio checksum disagreement, malformed timestamps, time spans outside duration, unknown lineage or license, annotation without independent audio check, unverified negative, or train/eval reuse of original lineage => HOLD. CLI exits 2 and writes the reasons. Successful synthetic fixture tests establish only that the gate *can enforce these rules*, not that any DataSED source qualifies.

**Admit does not certify an individual physical emitter.** Provenance and listening receipt fields are not cryptographically authenticated, and external auditors must verify documentary truth. Metadata can be internally consistent and yet refer to misleading audio. Rights and lineage are separate checks.

Dataset acceptance is not permissible from publisher claims alone where the original per-file source manifest is missing. The full Zenodo archive is ~4.5 GB; this project does not download or copy it into GitHub. No trained audio detector is evaluated here.

## Scientific stop/advance rule

- **HOLD** until eligible source-original recording and human time-label evidence is present and inspected.
- **REPAIR** if first real candidate fails or produces contradictory labels / unverifiable lineage; retain exact blockers.
- **GO to a separately frozen, prospective classifier benchmark** only if a small source-disjoint positive/negative sample is admitted and independent review can hear the intended event in the annotated span. No positive by empty negative intervals, no source identity inferred from filename, no threshold tuning against the later evaluation fold.

