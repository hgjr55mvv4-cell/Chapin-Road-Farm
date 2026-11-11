# Grok independent review — attributed editorial digest

**Relayed to Sol by the user on October 25, 2026.** This document summarizes and preserves the *substance* of the supplied review; it is **not** an authenticated tool execution, full verbatim archive, independent reproduction, or copy of Grok's reported separate local package. Grok reported `/home/workdir/artifacts/mechanistic-interpretability/` and eight files, but those bytes were not accessible in this workspace.

## Executive verdict (Grok, relayed)

- **Established externally:** superposition/polysemanticity and the fact that neuron/vector/SAE interventions can cause large behavioral effects; some circuit methods yield useful causal hypotheses.
- **Promising but task-specific:** interventions such as CounterSteer may suppress a bounded failure mode with utility tests.
- **Not established:** strong, repeatable net gains on factual correction, reasoning or calibration over an appropriate prompting/procedural baseline.
- **Adverse evidence:** MIB found SAE features not superior to native neurons for its causal variables; SAEBench challenges proxy metrics; Basu et al.'s 2026 clinical-triage study documented a large representation-to-action gap.
- **Disposition:** REVISE, then limited GO for research *design only*, with no inference/training or promotion.

These are Grok's research assessments, not extra independent experimental observations.

## Ranked opportunities (Grok)

1. Capability head-to-head, with strong A1, matched perturbation controls and net accuracy over correct and incorrect cases.
2. Representation–action gap: what probes encode versus what interventions actually change.
3. Failure ledger and transfer tests across prompts/checkpoints/directions.

Grok prefers exploring residual-stream directions over relying on highly polysemantic native neurons, while keeping SAE directions for causal description and targeted comparisons. This is a proposal, not an observed superiority on our task.

## Adversarial dissent (Grok, summarized)

Models may internally encode useful signals that cannot be converted into stable output corrections by simple local edits. Prompting, retrieval, and verification may provide better value at much lower cost. A research program focused on pleasing pictures or famous “green neuron” effects risks misallocating scarce attention while still neglecting sound oracles and strong baselines.

## Corrections and added cautions from Sol

- Grok's raw three-rate “net correction” subtracts subgroup proportions with incomparable denominators; v0.1 replaces it with a population-weighted final-correctness estimand plus mandatory subgroup floors.
- The primary controlled comparison should be **A1 versus B1 with *identical* prompts**, not A0 versus B1.
- Probe discrimination is not a direct actuator and a task-specific negative result is not a universal impossibility.
- “Grok created files” is a relayed author claim; the exact source files were not recovered, diffed, or verified. This package is an **editorial reconstruction**, not Grok's original package.
- SAEBench's arXiv metadata states acceptance to **ICML 2025**.

## Status

Paper-level source spot checks conducted; experiment **DESIGN / UNFROZEN / NOT RUN**. No validation of claimed local Grok execution was possible. Independent Muse and Astra challenges are next.
