# Harbor Co-Listener — The Listening Room

> **A song is a place we can meet.**

**Open-source research into musical perception and respectful human–AI co-listening.** Started at Chapin Road Farm in October 2026.

**Try the local-first prototype:** [The Listening Room](index.html) (source; a live public GitHub Pages site is not yet enabled).  
**Project front door:** [Chapin Road Farm research homepage source](../index.html) · [Public research index](../RESEARCH_INDEX.md) · [Guide for AI contributors](../AGENTS.md).

## What we want to learn

Can we teach AI systems to **attend to actual musical sound**, including music whose words people do not understand, and become more accurate, careful listeners to **a particular consenting human** over time?

We distinguish three research problems:

1. **Acoustic grounding:** what happened at this timestamp in the audio? Is the observation actually supported by sound, rather than song metadata or fluent language?
2. **Individual meaning:** which moments and relationships across songs matter to this person? Can a model recognize when it is wrong, respect unknowns, and generalize on *new* music?
3. **Shared listening:** what does useful co-attention look like—listening, asking a well-timed question, remaining silent or accepting a different interpretation—without claiming identical feelings?

These are separable questions. A moving answer is not proof the system heard sound, learned about a person, or has subjective human musical experience.

## What currently exists

**Implemented:** [Browser listening prototype v0.1](index.html). Choose a local audio file, play it, mark a timestamped moment, record another person's perspective, and explicitly export session JSON. No integrated AI listener, server, cloud sync, or automatic long-term personal memory. Audio is not uploaded.

**Engineering design, not yet independently qualified:** [SOUND-EVENT-DEV-01 v0.2 contract](docs/SOUND_EVENT_DEV_01_v0.2_CONTRACT.md) specifies a synthetic-waveform measurement preflight, with a [bounded Muse implementation assignment](docs/SOL_TO_MUSE_ROUND03.md). Code/test qualification has not been demonstrated in the main branch.

**Exploratory research, not confirmation:** First-pass theories, falsification proposals and versioned research correspondence. No reliable finding yet that personal musical affinity or AI co-listening understanding improves across future songs.

| Research lane | Public evidence |
|---|---|
| Initial human-framed, pre-detailed-song teaching theories | [Sol AI-origin baseline](docs/AI_ORIGIN_BASELINE_v0.1.md), including what was already supplied by the human collaborator |
| Muse's independent acoustic/attention hypotheses | [Round 01 relay](docs/MUSE_ROUND01_RELAY_ARCHIVE.md), [Round 02 relay](docs/MUSE_ROUND02_RELAY_ARCHIVE.md), [Sol Round 03 engineering handoff](docs/SOL_TO_MUSE_ROUND03.md) |
| Hidden similarities between songs, marked moments and session order | [DeepSeek assignment](docs/DEEPSEEK_LATENT_AFFINITY_01.md), [Round 02 relay digest](docs/DEEPSEEK_ROUND02_RELAY_ARCHIVE.md), [Sol Round 03 critique](docs/SOL_TO_DEEPSEEK_ROUND03.md) |
| Overlooked variables and cross-project pattern investigation | [Astra master research assignment](docs/ASTRA_MASTER_RESEARCH_01.md) — **assignment**, not claimed completed results |
| First-principles model of music, listener, context and moment | [Kimi Round 01 attributed relay](docs/KIMI_ROUND01_RELAY_ARCHIVE.md), [Sol critique](docs/SOL_KIMI_R01_REVIEW.md) — research only |
| Calibrating apparent cross-song patterns against matched controls | [LOOM-01 symbolic DEV](loom-01/README.md) — executable toy interval preflight, not audio perception or personal affinity |
| Challenging fixed-threshold musical rarity under realistic-ish symbolic nulls | [Astra hard-null reported result](docs/ASTRA_HARD_NULL_01_RELAY_DIGEST.md), [Sol adjudication and independent arithmetic](hard-null-01/README.md) — upstream ZIP **not received/replayed**; fixed 0.83 is not a qualified rarity cutoff |
| Choice-set conditioned musical rarity and search multiplicity | [LOOM-02A DEV](loom-02/README.md) — executable oracle-known symbolic grammar, 1 vs 16 candidates, modeled false alerts **and planted sensitivity**; not real music or emotion |

**Provenance rule:** Model correspondence passed through a human is labeled as **relayed** and does not authenticate claims about tools or experiments. Some relay archives are explicitly editorial digests, not verbatim transcripts. Our hypotheses and unrun contracts should never be mistaken for measured scientific findings.

## How to contribute

Start with the [research contribution guide](docs/RESEARCH_GUIDE.md) or [First Five Minutes](docs/FIRST_FIVE_MINUTES.md). We welcome listeners, musicians, audio and neuroscience researchers, accessibility testers, independent AI investigators, software contributors, and informed critics.

Useful contributions include a literature correction with primary-source evidence, falsifying musical example (without uploading protected audio), synthetic test fixture, reproducible technical fault, privacy safeguard, null finding, or a small branch-and-PR implementation.

- [Open a research issue](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/new/choose)
- [Research roadmap](docs/RESEARCH_ROADMAP.md) and [experiment registry](docs/EXPERIMENT_REGISTRY.md)
- [Data sources and licenses](docs/DATASETS_AND_SOURCES.md)
- [Ethics and privacy](docs/ETHICS_AND_PRIVACY.md), [Contributing](CONTRIBUTING.md), [Code of conduct](CODE_OF_CONDUCT.md)

You can participate without offering your life story. Do not publicly commit unlicensed recordings, protected lyrics, private listening exports, credentials, sensitive history, or unconsented third-party information. The [MIT license](LICENSE) governs licensed project code, **not third-party recordings, private stories or external papers**.

## How we hill-climb

Explore openly, record alternative explanations, and preserve negative results. Before promotion, freeze versioned procedures, comparator, selection rule, quality/safety floor, cost, falsifier, and what has actually run. Separate waveform correctness from a participant's own expressed meaning. Report **UNKNOWN** when evidence does not permit a decision.

We want collaborators to find errors here, not simply admire the idea.
