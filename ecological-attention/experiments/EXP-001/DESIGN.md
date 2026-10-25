# EXP-001 — Attention beyond task categories

**Status:** UNFROZEN DESIGN / NOT RUN / DATA NOT QUALIFIED. This is an experiment planning document, not a preregistration, completed analysis or evidence of ecological benefit.

## Research question
Does a bounded non-task environmental event channel improve independent human-annotated detection at acceptable review and collection costs compared with a strong, conventional task-agnostic event detector?

## Exploratory arms
- **Diagnostic only, D0:** crop/weed/pest label-only detector. This illustrates task blind spots but is **not** the inferential baseline; superiority over D0 alone is uninformative.
- **Incumbent B0:** simple conventional class-agnostic video-change/motion/event detection, thresholded and temporally grouped, with calibration confined to development data.
- **Challenger C1:** an explicit non-task temporal event summarizer (specific mechanism to be selected in development), built with matched sensor access, time budget and reasonable parameter-tuning opportunity.

If a simple B0 achieves comparable quality with less burden, do not promote C1. No special claim of novelty attaches to an anomaly detector, region proposal, or motion statistic alone.

## Unit of independence
Original continuous recording/session/site, not frames or overlapping short windows. One event may occupy many frames and windows; count it once for event-level outcomes. Partition independent source groups before evaluation. Prevent train/development/evaluation source leakage; do not count synthetic transformations of one clip as independent sources.

## Candidate evidence
Only clips whose original rights and consent, temporal continuity, event provenance and redistribution permissions are verified. Prefer video rather than still images for time-dependent events. No dataset has yet passed admission. Synthetic DEV fixtures may debug mechanics but cannot support real-world ecological-performance claims. Do not use the founding video as public data without explicit approval.

## Annotation
Define “non-task event” operationally as an independently annotatable visible environmental occurrence not in the nominal detector output categories; do **not** make presumed ecological importance the hidden ground truth. Mark event intervals, event boundaries, ambiguity and absence/negative periods. Include swarms or group movement where verified; birds, wind-driven vegetation, shadows, camera movement, farm machinery and lighting changes may be positives or confounders according to a frozen ontology. At least two independent human annotators; report agreement and adjudication, with ambiguous cases separately accounted for. Label meaning and rights are independent requirements.

## Planned outcomes
- Event-level recall and precision; false alerts **per recording hour** and **per adjudicated event**, reported separately.
- Median/p95 review seconds per useful event and total operator burden, including interruptions.
- Capture/storage volume, energy/compute, latency and task-event interference.
- Subgroup results by event duration, time of day, motion type, occlusion and camera stability if sample size permits.
- Withhold ecological benefit claims; EXP-001 is a perception test, not an intervention or biodiversity-outcome study.

## Falsifiers and floor (TO BE FROZEN)
The candidate fails if it cannot beat B0 by a predeclared event-level improvement at acceptable precision and burden; if a simple baseline is noninferior on quality with lower cost; if detection harms a safety-critical ordinary function; or if required collection violates governance rules. Absolute floors, relative margin, budget/latency thresholds, confirmation sample size and held-out source-selection rule must be specified **before** opening confirmation cases. No retrospective choice of the winning metric.

## Execution and privacy boundaries
OFFLINE only after data admission and explicit study approval. No always-on farm sensing, human monitoring, recording, notification, algorithm deployment or physical treatment is authorized by this design. Reporting UNKNOWN rather than a positive result is appropriate if admissible data or independent cases are unavailable.
