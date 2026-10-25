# The Listening Room — Open Research Staging Area

> **Research attribution correction (2026-10-25):** Earlier work credited to "Muse" was actually produced via **Meta AI** under that informal name; a separate Muse app is now newly available. The source record and independence limitations are documented in [Model attribution correction](docs/MODEL-ATTRIBUTION-CORRECTION-2026-10-25.md). Original filenames remain unchanged for continuity.

**Status: Round 2 design exploration, October 25, 2026. NOT a released listening application or an open human-subject study.**

The Listening Room is an experimental human–AI co-listening project: people explore music with a personal assistant that can learn explicitly shared preferences, explain supported recommendations, accept corrections, and remain silent when listening is the point.

## Current tracks

- **Sprint 01 app:** Claude's metadata-only prototype is under construction and not included in this branch. No playback/audio perception or AI understanding is claimed here.
- **Round 02 research:** Explore how volunteers might privately annotate songs and cross-genre playlists with *their own* descriptions of what connects them. Research, consent architecture and test design first; public data collection remains closed.
- **Audio-grounding research:** Distinguish verified audible features from song metadata and listener-reported reactions. No audio claims here.

## Planned contributions (not open for intake)

A future listener might select a song from their own music service, note a passage they appreciate, explain why it matters **if they wish**, and group songs into a present-moment playlist. Private notes stay private unless a separate, explicit sharing decision is made. No copyrighted audio uploads or full song lyrics.

**Please do not post personal listening histories, autobiographical accounts, sensitive details, or identifiable participant records in public GitHub issues or pull requests.** Public GitHub is for code, schemas, documentation and **synthetic examples**, not a confidential intake channel.

## Research questions

1. What do listeners themselves say connects otherwise dissimilar songs?
2. Which proposed musical commonalities can actually be verified from authorized audio?
3. Does a listener's AI improve with permitted feedback over repeated sessions?
4. Does a richer meaning-aware model improve useful recommendations beyond equally capable ordinary preference and context learning?
5. Can listeners refuse questions, memory and publication without losing a useful product?

## Navigation

- [Research contribution contract](docs/CONTRIBUTION-CONTRACT-v0.1.md)
- [Research roadmap](docs/ROUND-02-PLAN.md)
- [Example schema](schemas/listening-contribution.schema.json)
- [Synthetic example](examples/synthetic-contribution.json)
- [Contribution guidance](CONTRIBUTING.md)
- [Muse's first Round 2 assignment](prompts/MUSE-ROUND-02.md)

This branch is a staging area within the Chapin Road Farm public repository. A separate Listening Room repository is intended after project layout, licensing and publication review. No app code from Claude's incomplete run has been committed.