# TLR-R2-MUSE-01 — Sol's independent reconciliation (DEV)
**Date:** 2026-10-25  
**Status:** Exploration accepted; v0.1 contribution schema NOT promoted; real participant intake HOLD.

> **Source attribution correction:** The work reviewed here was produced by **Meta AI (historically called "Muse")**, not the newly available separate Muse app. This title is retained as an original project ID. See [model attribution correction](MODEL-ATTRIBUTION-CORRECTION-2026-10-25.md).

## Reliable starting points
- Lamont & Loveday (2020) distinguish memory *for* music, memories *associated with* music, preference and significance (https://doi.org/10.1177/2059204320948315).
- Chaganty et al., SIGIR 2023, CPCD: 917 public conversations show set-level conversational preferences are worth measuring, not that autobiographical meaning improves recommendations (https://github.com/google-research-datasets/cpcd).
- Cheng, Joachims & Turnbull, ISMIR 2020: 117-person study reports acoustic similarity associated with playlist choice/recommendation but not necessarily liking; limited study population (https://archives.ismir.net/ismir2020/paper/000246.pdf).
- Hirschprung & Leshman (2021) and Tel Aviv University summary: reidentification via music selections shown in a limited participant-group setting. Treat playlists as potentially identifying; do not generalize 80–100% rates to the population (https://doi.org/10.1016/j.tele.2021.101564).
- Greasley & Lamont (2011) document ESM methods and listening context, including the methodological risk of heightened awareness (https://doi.org/10.1177/1029864910393417).

Muse supplied no complete citation-by-claim bibliography. Several numeric, legal, and causal claims remain **NOT SOURCE-QUALIFIED**. Neither Muse's report nor this reconciliation is evidence of a completed experiment.

## Provisional decisions
**KEEP:** distinction between HUMAN REPORT / TRACK METADATA / AUDIO OBSERVATION / SYSTEM HYPOTHESIS; user-chosen grouping at a specific occasion; optional no-explanation; corrections; separate research/public/training permissions; no public GitHub intake.

**REVISE:**
1. Distinguish 'liked', 'meaningful', 'right now', 'favorites' and 'unlabeled grouping' without forcing one definition; prompt responses must be optional and the prompt's effect measurable.
2. Playlist identity and 'tonight' context are not lifelong preferences; make time, revision and consent scope explicit.
3. Baseline A cannot be restricted to like/dislike. Compare a *strong conversational preference system* with same ordinary attributes/context, allowed questions, catalog and explanation exposure.
4. Distinguish withholding information from changing its representation. B beating an under-informed A1 cannot establish a unique meaning representation.
5. Don't assert that 'no explanation' means 'interface success'; ask about satisfaction separately, unobtrusively and optionally.
6. A skip alone is not dislike and the link-out prototype cannot observe skip/playback.
7. Publication of an individually identifying playlist requires specific publication choice; never assume name removal makes it anonymous.
8. A GitHub issue posted publicly may remain in notification mirrors, forks, archives or Git history even if closed/edited. **Auto-closing does not erase it.** Establish a responsible incident process and prevention.

**SCHEMA OBSERVATIONS (v0.1-dev, not defects proven in running software):**
- Schema is synthetic-only (synthetic=true, research_use=false, public_release=false, model_training=false); do not simply relax these constants for real intake.
- It does not validate the relation between playlist.song_ids and songs[].song_id; does not guarantee unique song IDs.
- The human_report.text field can be null, but it does not distinguish refusal from no entry or unknowability; consider minimal statuses only if they improve listener experience.
- Recording identity is title/artist only, optionally source URL; alternate releases/mixes and source verification remain unresolved.
- It has no correction/revision linkage, as expected for an early draft.
- The proposed '3–7 songs' is a human-interface invitation, not a scientific invariant or schema hard limit (current schema permits 1–30).
- URL fields need validation and safe browser use in later implementation.

**BLOCK:** actual GitHub submissions of personal musical autobiographies; uncontrolled audio uploads; claiming physiological or acoustic patterns from metadata or human self-report; automated model training on submitted comments; merging changes into app before the interrupted Sprint 01 build is recovered.

## Next gate
Grok should deliver adversarial evidence and an improved research design, including blind negative controls, privacy threat model, culturally respectful refusal cases, and a fair strong preference comparator. No promotion, schema replacement or real collection until that review is reconciled.

## Sources and limits
URLs above identify inspected primary publications, abstracts or publisher/institutional summaries. The music-selection privacy effect is setting-specific. The existing public branch is documentation/synthetic examples, not a released Listening Room product.