# MECH-INTERP-01 — Mechanistic Interpretability & Causal Steering

**Status: DESIGN / NOT RUN.** This is a public, provisional research arm. It has not run model inference, downloaded weights, steered neurons, or demonstrated capability improvement. **Model execution, spending, training, deployment and merging: HOLD.**

## Question

Can bounded, reversible intervention in a fixed-weight model's internal activations improve objectively scored performance on *new* counterevidence-correction tasks beyond the same model using the same strong prompt, evidence and decoding settings **without intervention**? Can any advantage survive initially correct answers, misleading evidence, calibration, coherence, safety and cost floors?

A large change in output is **not** proof of more accurate reasoning. Native neurons, sparse-autoencoder (SAE) features, distributed steering vectors and circuits are distinct units of study. The motivating Sauers “green neuron” post is author-reported behavioral steering, not independently reproduced capability evidence.

## Start here

| Document | Purpose |
| --- | --- |
| [Research questions](RESEARCH_QUESTIONS.md) | Hypotheses, falsifiers, non-goals |
| [Source audit](SOURCE_AUDIT.md) | Publications, reported evidence and limits |
| [MECH-STEER-DEV-01](MECH_STEER_DEV_01_CONTRACT.md) | Counterevidence-correction DESIGN contract and unresolved freeze gates |
| [Experiment registry](EXPERIMENT_REGISTRY.md) | Actual execution status |
| [Negative evidence](NEGATIVE_RESULTS.md) | External negative findings / candidate Loser's Ledger |
| [Grok review digest](GROK_INDEPENDENT_REVIEW_01.md) | Attributed user-relayed independent assessment, not authenticated execution |
| [Muse handoff](MUSE_HANDOFF_01.md) | Independent challenge and later deterministic mock development assignment |
| [Index integration receipt](SUGGESTED_INDEX_UPDATES.md) | Draft branch navigation changes, not merged |

## Relationship to other work

This is a sibling of the [Agent Collaboration Lab](../agent-collaboration-lab/README.md), not a replacement. The Lab studies external context, retrieval, procedural memory, and agent review. This arm studies **internal, inference-time** mechanisms. Saved steering settings are external configuration; they are **not** persistent learned weights or proof of continual learning. The strong external method is a mandatory baseline.

## Evidence governance

Exploration does not promote a candidate. Freeze exact model revision, intervention, triggering, activation norms, arms, case-selection rule, primary estimand, quality/safety floors, cost ceiling, stopping rule and falsifier before seeing confirmation cases. Treat repeated generations over one case as correlated; preserve disconfirming evidence and all adverse subgroups. Equal performance at materially higher compute or operator cost is not an automatic gain. Experimental complexity is leased, not permanent.

The research is guided by Ω-ARENA v0.5 as **relayed** by the user; the canonical internal artifact (SHA-256 `f378600761b28b3bb245e3c45aa6d80d5e2a06e7fcb8f4b61c74fd26e951dec3`) has not been recovered or verified here. Do not claim the public documents exactly reproduce it.

## Provenance and permissions

Seeded from an independent Grok assessment copied into the conversation on October 25, 2026. Grok additionally reported a separate eight-file package at a path in its own local workspace. **Those file bytes were not provided to this editor and cannot be authenticated or copied here.** The current files are a separate, clearly attributed editorial draft; any differences must be reconciled before calling them Grok's originals.

No private confirmation sets, farm participant information, credentials or unlicensed assets are included. Research issue [#78](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/78); outside collaborators can contribute immediately at [open intake issue #80](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/80). Contributions through draft PR and independent review; no changes directly to main.
