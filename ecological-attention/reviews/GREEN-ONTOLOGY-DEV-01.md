# Pilot concept — GREEN-ONTOLOGY-DEV-01

**Status:** PROPOSED / DEV-ONLY / UNFROZEN / NOT RUN. This is an inexpensive decision gate, not an estimate of final scientific performance.

## Central question
Before building C1, can independent reviewers reliably mark bounded visible changes in a short, heterogeneous set of real videos without knowing which detector generated them?

## Initial operational scope
Only transient **visibly bounded events** on seconds-to-minutes scale, with explicit context from before and after where available. Do not include multi-day phenology, nest construction, inferred species benefit, or claims that an object is ecologically important. Define event families by observer-visible physical change (entry/exit; coordinated group movement; brief scene transformation) independent of crop/weed labels. Camera shake, illumination variation, moving shadows and wind-driven vegetation should be explicitly annotated **as confounder classes**, not silently dropped or labeled meaningless by fiat.

## Annotation schema (candidate)
- recording_group_id / site_id / source_url_and_version (provenance field; no leaked location),
- interval_start_s, interval_end_s, category_from_frozen_taxonomy,
- visible evidence type, boundary uncertainty band, occlusion / clip-truncated state,
- 'ambiguous' allowed; multiple overlapping intervals allowed,
- one source-level event ID spanning contiguous manifestations; split/merge criteria to freeze,
- reviewer confidence separate from ecological importance or model certainty.

**Pilot annotation**: begin with **12–24 short, source-distinct candidate clips**, balanced across visible event / apparent negative / nuisance confounder if and only if these cases can be selected transparently from admitted candidate material. Two reviewers annotate independently, blind to detector outputs, without consensus until annotations are captured. This is a proposed workload-limiting DEV screen; it is **not** a powered sample and does not qualify independent validation. No confirmation sampling before protocol freeze.

## Measures and preconditions
1. Before annotation, write category definitions, allowed onset/offset tolerances and split/merge guidance. Compare event presence, event counts, categories and interval overlap; show raw disagreements plus agreement scores, not just headline kappa.
2. Record cases where a clip starts after an event begins or cuts off before it ends; these cases are **censored**, not falsely precise intervals.
3. Track per-clip annotation minutes, uncertainties and adjudication burden, plus original-site/session clustering and background/no-event sampling process.
4. Stop and revise the taxonomy if reviewers consistently disagree about what an event is, confounders dominate without an interpretable distinction, or admissible negatives cannot be constructed. Thresholds remain **TO BE FROZEN**; do not treat development cases as subsequent confirmation.

## Critical design checks
- A motion-triggered archive is not a continuous ecological sampling frame; absent visible events in archived clips do not estimate events the sensor never triggered on.
- Time-of-day and seasonal patterns cannot be inferred from unreliable absolute timestamps.
- Annotator agreement about a **visual event** does not prove ecological value.
- A future B0 must be an actual documented implementation, not a class label; compare at least one minimalist motion/change baseline and a stronger reference method before proposing C1.
- Explicitly reserve a **no-system/off** arm for human-attention H3. No machine detection gain can substitute for measured improvement in people's independent noticing.

**Gate:** No confirmatory EXP-001, no C1 implementation, and no field sensing on the strength of this draft.
