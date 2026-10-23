# AUDITORY-DEV-01 — Does acoustic timing add information beyond text?

**Cross-project research:** Harbor Co-Listener / Virtual Farm Manager / Agent Collaboration Lab. The source here is a **bounded executable engineering example**, not a listening AI or production voice assistant.

Muse's Round 01 proposed that spoken language understanding requires sensor validity, timing, acoustic event grouping, transcript evidence, and cautious context-sensitive decisions. This exercise implements **only Level 0 and post hoc Level 1 timing** on generated pure tones. No microphone access, personal audio, recognizer, acoustic scene labeling, neural model, or subjective inference.

## Run with Python 3, standard library only

```sh
cd auditory-intelligence/dev-01
python -m unittest discover -s tests -v
python run.py
```

Local Python **3.13.5**: **12/12 tests passed**. The two examples use identical external transcript strings but different *synthesized tone-burst gaps*:

| Engineered case | True gap | WAV-derived gap | A0 transcript-only | A1 transcript + true timestamps | B transcript + measured WAV timing |
|---|---:|---:|---|---|---|
| Short gap | 0.120 s | 0.120 s | UNKNOWN_WAIT | WAIT | WAIT |
| Long gap | 0.680 s | 0.680 s | UNKNOWN_WAIT | READY_NOT_OBLIGATED_TO_REPLY | READY_NOT_OBLIGATED_TO_REPLY |

**Interpretation:** A0 cannot distinguish these cases with identical words. B can recover the gap on this simple generator but **does not beat A1**; extra waveform complexity has not earned a claim of improved reasoning. The action labels are artificial rules, not observed human turn-taking preferences. This is **offline** measurement after both tones, not prediction of when an unfinished human turn will end.

Tests also check missing WAV, corrupted WAV, clipping, continuous loud energy, only one event, a transcript-explicit correction that requires no audio, determinism, and refusal to infer hidden speech/mental state.

## Scientific context and limitations

- [Stivers et al. (2009)](https://doi.org/10.1073/pnas.0903616106): timing coordination studied across ten languages, with variation. Does not establish a universal wait threshold for a personal assistant.
- [Matalon et al. (2025)](https://doi.org/10.1073/pnas.2403262122): clustered prosodic patterns in English conversations; not a universal emotional dictionary.
- [Yadavalli et al. (2026)](https://aclanthology.org/2026.acl-long.1085/): information-theoretic differences in what prosody/text convey in specified datasets and tasks; not a causal claim about person-level intent.
- [RSA-Bench (2026)](https://aclanthology.org/2026.findings-acl.913/): acoustic ecology challenges audio-language models; motivates stronger stress tests beyond synthetic tones.
- [VoxParadox (2026)](https://proceedings.mlr.press/v306/pang26b.html) and [Heard but Not Heeded (2026)](https://arxiv.org/abs/2609.00727): examples of an encoder-to-output gap and limitations of audio-based pragmatic claims; not run here.

Next possible stages: voiced synthetic/rights-cleared actual speech and external reference timestamps; no extra feature extraction unless it beats a transcript+accurate-timing baseline; actual consented interruption trials only after separate approval and ground-truth planning. For real farm use, safety-critical physical actions must be verified independently.

**Provenance:** New Sol-authored demonstration responding to Muse's human-relayed Round 01. All expected examples are designed by the same implementer, and all are **EXPOSED DEV**; neither independence nor generalization is established. See [frozen contract](CONTRACT.md) and [local results](receipts/local_eval.json).
