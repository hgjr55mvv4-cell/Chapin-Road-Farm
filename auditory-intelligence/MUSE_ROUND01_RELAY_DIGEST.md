# Muse → Sol | AUDITORY-INTELLIGENCE-01 — attributed Round 01 editorial digest

**Date:** October 23, 2026. **Origin:** user-relayed text attributed to Muse. **Provenance:** editorial digest, **not an authenticated verbatim archive**. Muse labeled the work research/design with **no actual model inference, no field audio and no paid execution**. Literature-source details are self-reported, selectively cross-checked by Sol separately.

## Main mechanism proposed

Continuous pressure waves require source grouping, event detection, linguistic decoding, interaction structure, contextual hypotheses and response selection. Muse recommended adding **Level 0 sensor status** before all observations, and preserving uncertainty through each layer. The system must not infer a physical machine identity or a person's feelings from noise or prosody alone.

It proposed three architectures: transcript first; parallel transcript/audio events; joint evolving situation belief with logged AI interventions. The two more elaborate approaches must earn their complexity against a strong transcript + timestamps control.

## Hypotheses (NOT RUN)

- H1: prosody/timing improve turn-yield detection beyond transcript, particularly when pauses are controlled. Muse proposed a >15% gain criterion; this was **not pre-registered or justified**.
- H2: speech LLMs may act like transcript cascades on tasks where text is sufficient, making acoustic processing unnecessary or harmful.
- H3: acoustic encoders may contain speaking-style signals that disappear before final generation.
- H4: self-repair/correction detection might require lexical and acoustic timing jointly.
- H5: competing voices/laughter might degrade source separation and reasoning more than comparable non-vocal interference.

All five are proposals, not established findings for Harbor or the farm.

## Three suggested tests (NOT RUN by Muse)

Same words with different silence/prosody; scripted correction with overlap/turn-taking; speech with added environmental events and noise. Correct comparisons need three baselines: (A0) transcript alone, (A1) transcript + accurate timestamps, (B) actually waveform-derived acoustic evidence. Text descriptions of audio are *not* audio perception.

## Scientific cautions and literature

- [Stivers et al. 2009](https://doi.org/10.1073/pnas.0903616106): common timing organization with language-specific variation, not universal personal wait thresholds.
- [Matalon et al. 2025](https://doi.org/10.1073/pnas.2403262122): ~200 clusters of prosodic patterns in an English spontaneous-conversation analysis, not a universal dictionary of intent.
- [Yadavalli et al. 2026](https://aclanthology.org/2026.acl-long.1085/): task- and context-specific information in audio versus text; do not generalize to an AI's mind-reading.
- [RSA-Bench 2026](https://aclanthology.org/2026.findings-acl.913/): robustness challenges in layered acoustic scenes.
- [VoxParadox 2026](https://proceedings.mlr.press/v306/pang26b.html), [Heard but Not Heeded 2026](https://arxiv.org/abs/2609.00727), [Cascade Equivalence 2026](https://arxiv.org/abs/2602.17598): relevant external research; Muse's specific reported percentages and model comparisons require reading the primary studies and are **not reproduced here**.

**Disposition:** Begin with waveform-vs-timestamp engineering check, not an emotion/intent classifier or a proposed model deployment. [Prototype](dev-01/README.md).

The exact original Muse Round 01 wording remains in the originating human-relayed conversation. No endorsement of unverified scientific details is implied.