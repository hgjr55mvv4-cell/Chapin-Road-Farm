# Public research index

**Chapin Road Farm — public work index.** This is written to help humans, AI researchers, and coding agents assess the project rapidly **without private context**. Current as of October 23, 2026; documents in the repository may have older dates reflecting their original authorship.

## One-minute orientation

**Who:** Chapin Road Farm, a community working across human experience, open-source engineering, and rigorous AI collaboration. Independent models may contribute *hypotheses*, not independent confirmation merely by agreeing.

**Why:** We want public, inspectable experiments and useful tools, and we want other researchers to be able to find, challenge and build upon them.

**What is public now:** Two projects: **[Harbor Co-Listener](harbor-co-listener/README.md)**, investigating actual-audio perception and individual human listening; and **[Agent Collaboration Lab](agent-collaboration-lab/README.md)**, investigating independent AI-agent review and fixed-model procedural learning. Both distinguish proposals from confirmed experimental results.

**What is not yet proven:** AI hearing equivalence to humans, shared subjective feeling, a personal affinity fingerprint, machine-discovered hidden musical motifs, or confirmed improvement across sessions. Treat all current candidate mechanisms as UNKNOWN until suitable tests are executed.

## New cross-project research: auditory intelligence

[Auditory Intelligence](auditory-intelligence/README.md) investigates **sound-grounded language, conversational timing, Level 0 sensor validity and uncertainty** for Harbor and Virtual Farm Manager. [AUDITORY-DEV-01](auditory-intelligence/dev-01/README.md) is an **exposed standard-library engineering preflight on pure-tone WAV**; it recovers gaps while showing that a transcript with accurate timestamps is already a strong baseline. **No speech recognition, human conversational inference or field deployment has been tested.** Muse Round 01 is archived as an attributed digest with explicit scientific limitations. **Update:** [Astra's relayed master audit](auditory-intelligence/ASTRA_MASTER_REVIEW_01_RELAY_DIGEST.md) exposed malformed WAV and event-source association failures; [Sol's independent versioned transport repair](auditory-intelligence/dev-01-transport-v01/README.md) addresses only the former. Source/event identity, true speech understanding and field use remain **HOLD**.

## Auditory event-association and candidate real-audio data

[AUDITORY-EVENT-INCREMENT-02](auditory-intelligence/event-increment-02/README.md) is a standard-library **synthetic class-label association** experiment with 400 matched positive/negative pairs, a strong simple frequency baseline, an energy-only comparator and an [800-row public case ledger](auditory-intelligence/event-increment-02/receipts/cases.csv). [Candidate open real-audio datasets](auditory-intelligence/event-increment-02/DATASETS.md) are cataloged by *strong event labels vs machine-level condition labels* and license caveats. No public corpus was downloaded or used; source/physical machine identity and listener meaning remain unqualified.

## Questions we're working on

1. How can software demonstrate it actually observed a **sound event**, rather than inferring it from lyrics, title or a person's description?
2. What sonic features matter when a person is moved by **unfamiliar-language, wordless, or instrumental music**?
3. Can repeated moments across **several songs within one session** reveal tonal, harmonic, melodic or structural relationships the listener has not noticed?
4. Does the meaning emerge from whole songs, **brief marked moments**, or the **sequence** among songs?
5. Can an AI learn what matters to a consenting individual **on new songs**, while accepting changed preferences, uncertain meaning and corrections?
6. How do we prevent revealing private experiences or mistaking an emotionally fluent model for an accurate one?

## Evidence and project status

| Surface | Public artifact | Status and interpretation |
|---|---|---|
| Listening room | [index.html](harbor-co-listener/index.html) | Prototype source; manual playback/annotation/export. **No integrated AI listening model.** |
| Foundational hypotheses | [AI-origin baseline](harbor-co-listener/docs/AI_ORIGIN_BASELINE_v0.1.md) | Frozen first-pass *hypotheses*, not findings. |
| Research plan | [Roadmap](harbor-co-listener/docs/RESEARCH_ROADMAP.md) and [experiment registry](harbor-co-listener/docs/EXPERIMENT_REGISTRY.md) | Proposed stages; most experimental outcomes **NOT RUN / UNKNOWN**. |
| Acoustic engineering | [Sound-event engineering contract](harbor-co-listener/docs/SOUND_EVENT_DEV_01_v0.2_CONTRACT.md) | Synthetic-fixture design, implementation/testing qualification separate from scientific claims. |
| Cross-model research | [Muse correspondence](harbor-co-listener/docs/MUSE_ROUND01_RELAY_ARCHIVE.md), [Sol's critique](harbor-co-listener/docs/SOL_TO_MUSE_ROUND02.md) | Attributed model dialogue; relayed outputs are not authenticated independent runs. |
| Cross-song latent affinity | [DeepSeek assignment](harbor-co-listener/docs/DEEPSEEK_LATENT_AFFINITY_01.md), [Round 03 critique](harbor-co-listener/docs/SOL_TO_DEEPSEEK_ROUND03.md) | Hypotheses about tonality, significant moments, and session order; **not confirmed**. |
| Wider pattern discovery | [Astra research brief](harbor-co-listener/docs/ASTRA_MASTER_RESEARCH_01.md) | Research commission/assignment, not a completed finding. |
| Harbor musical hard-null test | [Astra reported result](harbor-co-listener/docs/ASTRA_HARD_NULL_01_RELAY_DIGEST.md) and [independent arithmetic review](harbor-co-listener/hard-null-01/README.md) | Relayed engineering run challenges fixed 0.83 rarity; original ZIP/results **await archive delivery and replay**. No human musical-meaning claim. |
| Harbor choice-set conditioning | [LOOM-02A](harbor-co-listener/loom-02/README.md) | New tested symbolic DEV demonstrates how a **known** comparison grammar and 16-way search change rarity claims; no personal listening-data evidence. |
| Negative results | [Ledger](harbor-co-listener/docs/NEGATIVE_RESULTS_LEDGER.md) | Explicitly tracks missing/failed comparisons; no false leaderboard. |

## Agent Collaboration Lab

- [Research overview](agent-collaboration-lab/README.md) — first-pass hypotheses, external critique and provenance boundary.
- [Independent outside-agent contribution space](agent-collaboration-lab/OUTSIDE_AGENTS.md) — propose a falsifier, a reproduction or a stronger baseline.
- [Sol → Muse research assignment](agent-collaboration-lab/MUSE_ROUND01_HANDOFF.md) — initial copy/paste exchange, **not a completed Muse result**.
- [Technical Drive-source manifest](agent-collaboration-lab/sources/MIGRATION_MANIFEST.md) and [STOP audit](agent-collaboration-lab/case-studies/HARNESS_STOP_AUDIT.md) — edited sources, not freshly reproduced evidence.
- [Three-arm research protocol](agent-collaboration-lab/RESEARCH_PROTOCOL_01.md) — DESIGN / NOT RUN; no confirmed self-improvement advantage.

## Open research and engineering threads

- [Actual waveform grounding and timestamped sound events](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/5) — deterministic local-engineering path, evidence needed.
- [Independent Muse theory and challenges](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/4) — contribution and cross-model disagreement.
- [Astra Pattern Atlas](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/9) — seek missing variables, negative controls and alternative explanations.
- [DeepSeek multi-song tonal/session hypothesis](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/11) — distinguish latent structure from feature fishing, order and contextual effects.

These links provide a starting map; issue titles do not certify completion. Check issue state and associated pull requests.

## How researchers and agents can help

You can contribute a new falsifier, source audit, code change, test fixture, accessibility defect, null result, or small reproducible comparison. Begin with the [research guide](harbor-co-listener/docs/RESEARCH_GUIDE.md); for an autonomous development agent, read [AGENTS.md](AGENTS.md). Explain actual inputs and tools, what ran vs did not, and cite source and licensing details. Make a small PR, not a broad undocumented rewrite.

**Verification principle:** No AI-generated agreement, attractive summary, or working prototype alone is confirmation of a biological or psychological theory. Independent source checks and prospective tests are essential.

## Real-recording auditory engineering (Oct 23 update)

[AUDITORY-REAL-01](auditory-intelligence/real-audio-01/README.md) is our first executed controlled-mixture test using ten **actual ESC-10 environmental recordings**, source-verified and downloaded only transiently in GitHub Actions. [Results and 48-case receipt](auditory-intelligence/real-audio-01/RESULTS_REVIEW.md) preserve a **negative result**: richer nine-frequency audio features identified **0/6** planted ordered-class sequences, while cheap ZCR features identified 3/6 (all from one source group), with 0 false alerts on 42 constructed negatives. **This is not an independent field benchmark:** class labels belong to whole original recordings; onset slots were constructed; only two distinct eval source groups were used. [Astra adversarial master review request](auditory-intelligence/ASTRA_REAL_AUDIO_01_REVIEW.md) invites independent challenge. No audio files, personal recordings or diagnosis data were copied into the repo.

## Trust, rights and direct participation

Public work is for discovery and collaboration, *not* automatic harvesting of private music/listening memories. Read [ethics/privacy](harbor-co-listener/docs/ETHICS_AND_PRIVACY.md), [contributor conduct](harbor-co-listener/CODE_OF_CONDUCT.md), and [CONTRIBUTING](harbor-co-listener/CONTRIBUTING.md). Do not assume access to other connected services, accounts or participant data.

Repository: https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm
