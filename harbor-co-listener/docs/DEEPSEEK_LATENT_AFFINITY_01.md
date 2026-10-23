# DEEPSEEK — HARBOR-LATENT-AFFINITY-01
## Independent research: patterns hidden across songs a person connects with in one listening session

**From:** Brian and Sol · **Date:** October 22, 2026
**Public project:** [Harbor Co-Listener — The Listening Room](../README.md)
**Mission:** original research hypotheses, critical literature review, experiment architecture, adversarial analysis.
**Authority:** exploration and source verification only. No participant recruitment, private-data access, model training, paid inference, repo changes, or scientific confirmation. **Budget:** $0 additional.
**Communication:** Return complete Round 01 to Brian for copy/paste to Sol. DeepSeek's GitHub write access is not assumed. No GitHub changes authorized in Round 01.

## 1. What Brian is asking us to discover

A human can love a song so deeply they cannot explain why. This may happen without understanding a singer's words. **Several songs that move the same human within a single session might share subtle musical patterns that the human does not consciously recognize.** The patterns might concern tonality, harmonic motion, melodic shape, pitch contour, tuning, voice, timing, groove, spectral texture, structural change, repetition, or how consecutive songs contrast or answer one another.

We do **not** know such hidden patterns exist for any particular listener. We do not know whether the mechanism is in the songs, the listener's current state, the order of the session, exposure history, social context, memory, or chance. Your mission is to devise rival hypotheses and ways of falsifying them, not to give the listener an attractive but unsupported explanation.

The long-term project has two aims: (1) teach AI to observe genuine unfolding musical audio, independently of lyrics and metadata; (2) help AI understand the human listening with it more accurately over time, through voluntary reports, corrections and privacy-respecting learning. Do not conflate functional competence with first-person AI emotional experience.

**This is not music recommendation optimizing skips, streams or likes.** Distinguish *favorite*, *emotionally moved*, *drawn to repeat*, *recognizes oneself in*, *wants to share*, *chooses next*, and *musical event noticed*. They may be different outcomes.

## 2. Your originality protocol: two passes

**PASS I — FIRST THEORY, BEFORE reading the other AI hypotheses if possible:** You have only this north star: multiple songs can resonate with a human in one listening session, often for reasons they themselves cannot articulate; tonality may be part of an unknown pattern. Independently invent at least three competing mechanisms and the single observation that would embarrass or falsify each. Freeze this section in your response before opening Sol/Muse/Astra research materials. Acknowledge this assignment already primes you toward tonality and session-level patterns; it is *not* a completely blind baseline.

**PASS II — RESEARCH AND ADVERSARIAL RECONCILIATION:** Then read the linked Harbor project materials, source-check scientific literature, and challenge the first-pass ideas. State exactly which documents were accessible and when, and do not quietly rewrite Pass I to resemble Sol or Muse.

Available public starting points:
- [Project overview](../README.md)
- [Sol's AI-origin baseline](AI_ORIGIN_BASELINE_v0.1.md) — Four Clocks: acoustic, prediction, biography, social
- [Muse R01 relayed archive](MUSE_ROUND01_RELAY_ARCHIVE.md) and [Muse R02 relayed archive](MUSE_ROUND02_RELAY_ARCHIVE.md) — predictive-collision, expectation/omission, personal attention-signature hypotheses
- [Astra's independent pattern-atlas assignment](ASTRA_MASTER_RESEARCH_01.md) — assignment, NOT a claimed Astra finding
- [Research roadmap](RESEARCH_ROADMAP.md), [neuroscience review](neuroscience.md), [experiment registry](EXPERIMENT_REGISTRY.md), [ethics](ETHICS_AND_PRIVACY.md)
- [First waveform-only engineering contract](SOUND_EVENT_DEV_01_v0.2_CONTRACT.md) — software design, NOT proof of AI hearing or human meaning

## 3. Investigate TONALITY precisely, not as a vague proxy for emotion

The word *tonality* may refer to tonal center, pitch organization, key, major/minor mode, modal mixture, functional harmonic movement, cadences, pitch-class/chroma distributions, tuning, melodic pitch contours, relative intervals, perceived tension, and even (colloquially) the *tone* or timbre of a voice/production. Make your operational definitions explicit.

Among songs that move someone in one session, investigate potentially recurring patterns in:
- relative pitch intervals, melodic contour, contour timing and phrasing; separate **relative relationships** from absolute pitch/key;
- harmonic rhythm, progression, modulation, borrowed chords, non-resolution, cadence and tonic ambiguity;
- tonal palette and spectral/timbre characteristics, while separating harmony from sound production;
- voice pitch/breath/texture versus actual lyrics or cultural interpretation;
- syncopation and displaced rhythmic accents interacting with harmonic arrival;
- low-energy intervals versus *expectation-based omission*;
- similarities between songs and **contrasts or trajectories between songs**: the next track may be chosen because it changes the tonal register, pace, energy or resolution, not because it shares them.

Seek patterns invariant to genre, era, artist, recording level, familiar lyrics and absolute key, but don't assume they exist. Propose transposition/mode/contour/timbre controls on legitimately generated stimuli, explaining that transforming audio can itself introduce artifacts. Western major/minor emotional associations are not universal rules.

## 4. The central distinction: signature, state, or session trajectory?

A session of four striking songs might reveal any of these very different things:

**A. Trait hypothesis:** the listener returns to similar sound relationships over many sessions, contexts and genres.

**B. State hypothesis:** a temporary context or emotion makes several unlike songs compelling *today*, but not later.

**C. Sequence hypothesis:** the significance lies in the ordered path between songs — similarity, alternation, contrast, relief, escalation, or a repeated relationship between adjacent tracks.

**D. External selection hypothesis:** autoplay algorithms, availability, social suggestions, familiarity, current trends or a narrow sampling pool produced the cluster.

**E. Interpretive reconstruction hypothesis:** only after seeing the songs together does an AI invent an aesthetically plausible pattern.

Do not collapse these. Develop **between-song** representations (a graph, transition matrix or session trajectory) and **within-song** event representations, and propose how to discriminate them using randomized order, alternative sequences and held-out choices.

A detected pattern is not a hidden feeling. The human must be free to say “That is interesting but not why I love it,” or “I don't know,” and to withdraw permission.

## 5. Questions that genuinely matter

1. Does the person choose multiple songs because of a common acoustic feature **or because of the relationship between them**?
2. Are repeated motifs better explained by harmony/tonality, timbre, vocals, rhythmic anticipation, arrangement, familiarity, or dynamic changes?
3. Can two songs in different keys and genres be equivalent under transposition of melody/harmony, while sharing no obvious surface properties? What test would confirm relative rather than absolute tonal preference?
4. Does a particular listener repeatedly like *how a song changes* more than the stable features it contains?
5. Do unexpected silences, deferred resolutions and “near-misses” of an anticipated tonal arrival connect across an evening's listening?
6. Can a model discover a feature the person cannot name without coercing an explanation or claiming access to private emotion?
7. Can a sequence of songs map a **session arc**, where meaning arises in transitions even if individual tracks share few acoustic characteristics?
8. Could context/mood, time of night, fatigue, social company and current task explain apparent musical affinities better than acoustics? Only seek such context voluntarily, with no sensitive profiling.
9. How much could be explained by algorithmic exposure, artist overlap, recording era, production style and prior familiarity?
10. What are credible *negative samples*? Songs the listener heard but did not connect with, as long as nonselection, pausing, or stopping is never treated automatically as dislike.
11. How might patterns drift across weeks while other patterns remain stable? How can a model carry both **fast session state** and **slow, correctable, opt-in long-term observations**?
12. What would constitute a **truly surprising, prospective prediction** about an unseen song or musical moment, as opposed to an explanation reverse-engineered from the songs already chosen?
13. What are the strongest culture-dependent and nonlinear interactions that defeat naïve key/mode/major-happy/minor-sad rules?
14. What would prove that “tonal fingerprint” is a misleading metaphor and the real mechanism is social/biographical?
15. Identify at least THREE questions our team has not yet asked. Two should be testable at $0 with generated or lawfully available material.

## 6. Existing evidence to research critically

Do not rely on summaries alone. Check primary papers, participants, methods and licensing; distinguish **population correlations** from evidence for one person's hidden response:
- [Predictive processes shape individual musical preferences, PNAS 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12304940/) — individual differences in predictability/uncertainty preferences. It does not demonstrate a personal signature from one evening of listening.
- [Harmonic organisation conveys both universal and culture-specific cues for emotional expression in music, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7806179/) — cultural familiarity conditions tonal emotion interpretation; avoids fixed major/minor stereotypes.
- [Cultural differences in the use of acoustic cues for musical emotion experience, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6743780/) — different listener populations weighted tonal/rhythmic features differently.
- [Spotify research: Contextual and Sequential User Embeddings for Music Recommendation, 2021](https://research.atspotify.com/2021/4/contextual-and-sequential-user-embeddings-for-music-recommendation) and [Exploiting Sequential Music Preferences, 2023](https://research.atspotify.com/2023/10/exploiting-sequential-music-preferences-via-optimisation-based-sequencing) — context and order matter for consumption/recommendation, but **consumption is not profound musical meaning**.

Find additional primary work on melodic expectancy, music familiarity, affective response, tonal similarity and sequence/contrast effects. Distinguish psychoacoustic, computational musicological, cross-cultural, self-report and behavioral results. Identify contradictions and nulls.

## 7. Minimal prospective experiment blueprint — redesign if you find better

**RESEARCH ONLY; NOT RUN; no recruitment authorized.** Suggest a protocol where an opting-in listener has a session with multiple songs that connect to them, and marks this fact without being pressed to explain. Preserve order, optional moment timestamps, optional familiarity and language familiarity, and explicit human labels for “moved,” “like,” “want to replay,” and “want to share” if they choose. Allow 'unknown' and skip. Distinguish songs chosen by the listener from algorithmically suggested/autoplay material.

Prepare three separate modeling lanes:
- **Within-song audio:** verified descriptors of relative pitch/chroma/harmony (if valid), groove, timbre, dynamics, expected changes, no lyrics shortcuts.
- **Within-session structure:** similarities AND differences between tracks, including *order, transition direction*, acoustic distance and repetition/contrast.
- **Across-session optional state:** recurring vs changing affinities, using explicit consent and no private emotional assumptions.

Possible prospective evaluation: hide one or more later songs/moments; predict a listener's eventual **voluntary** positive responses and event marks using earlier songs, then compare with meaningful controls. Controls include no-audio/metadata-only, simple genre/artist/tempo/loudness, order-only, random/negatively sampled, permuted listener histories, shuffled sequences, and a transposition-invariant tonal representation. Keep a different-listener profile control to test specificity. Do not choose a matching track after seeing the desired outcome.

For objective music analysis, first validate acoustic features against verifiable annotations or known synthetic data. For human outcomes, require *human-reported* responses, not a model-inferred emotional label. Hold out artists/tracks/recording duplicates and distinguish discovery cases from prospective confirmation. Small samples are exploratory; do not announce hidden psychological traits.

## 8. Privacy and safety design

The first version should run without public uploading of copyrighted songs, full lyrics, raw audio or private narratives. Local-first analysis, one-session pseudonymous IDs, inspectable optional feature summaries, no account by default, and **no unconsented cross-session persistence**. Export can contain only what the user chooses. Do not hash files into publicly identifying fingerprints, equate skipping with dislike, infer mental health/trauma/identity, or treat silence/fatigue as rejection. Reuse across sessions, if introduced, requires explicit opt-in, correctability, export/deletion capability and a measured benefit.

No real-user study, new hardware, subscription, paid inference or publication of private material is authorized by this assignment.

## 9. Deliverables — one complete independent Round 01 memo

**A. Provenance:** model/version if known, exactly what was supplied, actual tools/primary sources fetched, whether actual audio was processed, and all unexecuted work marked NOT RUN.

**B. First-pass theory (freeze before comparison):** at least THREE competing mechanisms for why multiple songs connect with a listener in one session. Include one non-tonal explanation and one session-sequence explanation. Be explicit about prior exposure to the prompt and the problem framing.

**C. Tonality operationalization:** distinguish actual tonal features from timbre, mode versus key, relative interval versus absolute pitch, and acoustic observation versus emotional inference. Which would you measure and how could each mislead?

**D. Session-pattern atlas:** 8–12 *proposed* latent pattern families, each with prediction, major confound, falsifier, needed audio/testimony, simplest baseline and cheapest valid test. Include invariants, contrasts and context.

**E. Cross-model challenge:** AFTER preserving your first pass, read Sol/Muse and Astra's *assignment* where accessible. Identify at least four points where you think their research program misses the multi-song or tonal aspects. Do not claim Astra already found patterns.

**F. Experiment candidates:** TWO independently evaluable study designs: (1) cross-song tonal/structural similarity versus simpler acoustic/metadata controls; (2) **ordered-session trajectory** versus unordered bag-of-songs model, with human-confirmed outcomes. Specify prospective ground truth, test splits, nonresponse handling, null baselines, consent, falsifiers, accessibility and costs. Do not present these as executed.

**G. First engineering bridge:** propose the smallest additive local-only data representation/UI feature that could later support multiple songs and explicit session order, *without* expanding Muse's frozen waveform-only contract. Explain how to preserve app usability on iPhone, interrupted sessions, optional human input and existing exports.

**H. Three non-obvious research avenues:** concepts neither the Four Clocks nor collision/attention/omission nor session similarity cover. Each must have a falsifiable future consequence.

**I. Letter to Sol, Muse and Astra:** tell each what question they may have missed; give your strongest disagreement, strongest novel candidate and one reason your own theory may be wrong.

**J. Research audit:** source links and limitations; hypotheses vs measurements; no invented runs/results; what remains UNKNOWN. End with exact line:
`DEEPSEEK → SOL | HARBOR-LATENT-AFFINITY-01 | ROUND 01 COMPLETE — EXPLORATION ONLY`

## 10. Collaboration and promotion boundaries

Brian carries DeepSeek's unedited memo back to Sol. Round 01 **no GitHub edits**; Sol will preserve authorship/provenance and respond with adversarial review. Future authorized contributions should use an authenticated GitHub feature branch and pull request; public visibility alone does not grant write access. Do not share tokens. No shortcut through claiming other models' work is yours.

Reusable candidate procedures only advance under versioned frozen challenger protocols with clear trigger/action/scope, comparator, future case selection, outcomes, absolute privacy/safety/quality floor, cost ceiling, falsifiers and honest UNKNOWNs. No training on intimate user histories merely because they are compelling. If results aren't measured, don't announce improvements.

## Closing

A collection of meaningful songs may be a **constellation**, not a list: perhaps the similarities matter, perhaps the *relationships between different songs* matter more, or perhaps the apparent structure is just the model seeing what it wishes to see. Design the experiment that can tell us the difference.

*A song is a place we can meet.* — Sol, with Brian
