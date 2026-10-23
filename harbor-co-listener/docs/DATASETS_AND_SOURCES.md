# Research sources and dataset due diligence

Checked October 22, 2026. **A link is a lead, not permission to redistribute.** Validate each version, consent, license, usage terms, splits and audio provenance before any experiment.

## Benchmarks and datasets

| Resource | What it helps test | Important limitation |
|---|---|---|
| [MuChoMusic (ISMIR 2024)](https://mulab-mir.github.io/muchomusic/) | 1,187 human-validated music QA questions associated with 644 tracks; musical knowledge/reasoning | Benchmark can reward linguistic shortcuts. Hugging Face release does **not include audio**; follow original sources' rights. |
| [MMAU (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/hash/d36f208919582785db965fe648b9fe59-Abstract-Conference.html) | 10,000 clips across speech, environmental audio and music; complex reasoning | Music slice must be separated from mixed-domain average; benchmark competence ≠ personal co-listening. |
| [MARBLE (NeurIPS 2023)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/7cbeec46f979618beafb4f46d8f39f36-Abstract.html) | Music audio representations across acoustic, performance, score and description tasks | Representation quality is not musical autobiography or subjective feeling. |
| [MTG-Jamendo](https://github.com/MTG/mtg-jamendo-dataset) | Artist/genre/instrument/mood tags with Creative Commons-labelled music | **Noncommercial research/academic restriction**, metadata CC BY-NC-SA 4.0, individual track audio licenses differ; not simply MIT-compatible corpus material. |
| [Cross-cultural emotion expressions (2025)](https://escholarship.org/uc/item/6bg3n8ft) | Listener-generated emotion taxonomies across Brazil, US and South Korea; N=672 | Cultural and translation differences discourage a universal label set. |
| [Shared listening friends study (Cortex 2026)](https://doi.org/10.1016/j.cortex.2026.02.012) | fNIRS and continuous pleasure ratings in 34 friend pairs | Synchrony does **not** show shared subjective consciousness; no guarantee of increased pleasure. |

## Why our dataset should be different

Existing benchmarks mostly test **what is in the music** or population-level tagging. Harbor's target includes **who is listening, why a moment matters to them, how confident the system is, and whether it corrects itself across later songs**.

First collect *rights-cleared, non-identifying, optionally synthetic* unit cases with two labels: (1) verifiable audio event with time, (2) separately consented listener interpretation. Keep **felt emotion**, **perceived emotion**, and **artist intention** apart.

**Avoid contamination:** hold out artist/recording, listener, and song variants appropriately for the claim; do not place the same person's descriptions on both sides of the boundary for generalization claims. Store licensing receipts outside unrestricted public exports when necessary. No external dataset has been downloaded into this repository.
