# TLR-R2-GROK-01 — Sol adjudication and next gate
**Date:** 2026-10-25  
**Status:** Grok adversarial exploration accepted; study and contract remain REVISE; real human-data intake, participant experiments, streaming/audio downloads, model training, scientific confirmation, and release remain HOLD.

## What carries forward
1. Do not equate human-chosen playlist membership with acoustic commonality or causal relevance. Cross-genre acoustic structure is a hypothesis, not a demonstrated fact.
2. Use a strong A1 conversational preference baseline with equal catalog and interaction resources, not Muse's simple like/dislike baseline.
3. Separate asking questions, acquiring extra association information, and representing the same information in a special schema as distinct causal effects.
4. Use hierarchical person/session/playlist/recording/moment units. Multiple segments of the same recording do not create independent source recordings.
5. Frame prompt reactivity, familiarity, artist/era/version effects, and selection bias as first-class confounds.
6. Treat an explicit 'never recommend' instruction as a deterministic veto. Unknown implicit playback behavior is not dislike.
7. A distinctive song list or autobiographical free text may reidentify the contributor; name removal does not guarantee anonymity. Accidental GitHub posts cannot be guaranteed erased by closing.
8. Support both private listeners and enthusiastic opt-in open sharing of selected playlists/stories. Research access, public publication, attribution, and model training are separate user choices; show previews and limitations on withdrawal.

## Independent source checks and qualifiers
- Cheng, Joachims & Turnbull (ISMIR 2020), 117 subjects: acoustic similarity judgments correlate with playlist selection/recommendation, more weakly with liking. This is not a study of intimate meaning constellations. https://program.ismir2020.net/poster_4-15.html
- Chaganty et al. (SIGIR 2023), CPCD: 917 conversational playlist-curation cases; dataset supports set-level preference evaluation, not incremental value of autobiographical memory. Its repository is archived and read-only. https://github.com/google-research-datasets/cpcd
- Hirschprung & Leshman (Telematics and Informatics 2021): favorite-song selection can enable reidentification in particular experimental groups. High success in those groups must not be generalized to arbitrary public playlists. https://doi.org/10.1016/j.tele.2021.101564
- Afchar et al., Explainability in music recommender systems (AI Magazine 2022): skip and even 'like' actions are ambiguous implicit feedback; rationale wording can be deceptive when underlying identity/context is wrong. https://doi.org/10.1002/aaai.12056
- Spotify Research (2018), Understanding and Evaluating User Satisfaction with Music Discovery: skip interpretation depends on context; metrics vary across listeners. This is provider research, not universal evidence. https://research.atspotify.com/2018/7/understanding-and-evaluating-user-satisfaction-with-music-discovery

**Unverified from Grok's supplied report:** claim-specific full-paper locations, detailed counts and many privacy/copyright assertions. The supplied ledger is exploration, not a complete independent source audit. The 'more parsimonious' non-acoustic explanation is a plausible alternative, NOT itself demonstrated.

## Contract disposition
Retain v0.1 synthetic-only data schema unchanged. Candidate v0.2 amendments to be designed and tested, not silently promoted:
- reason_status provided / declined / unknown / not_asked, with refusal not stored as a personality trait;
- uniqueness and referential integrity of playlist-song references;
- recording-version identifiers, with unresolved identity blocking passage-level claims;
- correction/supersession links and session/time-bounded relevance;
- separate, reviewed real-contribution contract for broad sharing, attribution, private research and training opt-ins;
- safe prevention and incident handling for accidental submission of personal data to GitHub.
Potential edge case: a person's legitimate right to export their own content should not be blocked merely because their text mentions a third party, even though public distribution needs separate caution.

## Experimental correction
A future link-out prototype cannot observe playback completion, skip or replay on external services. Initial outcomes must be consented and explicitly collected; do not infer behavior from opening a link. A0/A1/B studies must distinguish new information from new representation and avoid persuasive explanations until after blind choices. If meaning-aware B ties A1 at materially higher cost or privacy burden, do not promote B for ranking. Co-listening/reflective value needs independent tests.

## Engineering gate
DeepSeek next: propose a small synthetic-only executable harness that verifies schema invariants and a non-claims-generating pattern pipeline; evaluation design under matched controls; local user-learning with corrections and separate research sharing. No touching Claude's unfinished Sprint 01 source or opening intake. Ω-ARENA challengers require a freeze before prospective confirmation.

**Decision:** GROK EXPLORATION ACCEPTED; protocol REVISE; data collection HOLD; DeepSeek computational exploration GO.
