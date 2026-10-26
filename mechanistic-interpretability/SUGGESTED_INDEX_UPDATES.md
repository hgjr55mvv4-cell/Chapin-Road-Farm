# Minimal public navigation changes (proposal)

**Status:** DESIGN. Cross-links are navigation only, not scientific endorsement.

## Root README.md

Add a short paragraph near Agent Collaboration Lab:

> **Mechanistic Interpretability & Causal Steering (MECH-INTERP-01)** — [research arm](mechanistic-interpretability/README.md) investigating whether reversible internal activation interventions improve objectively measured model correctness beyond strong prompts and procedural methods. **DESIGN / NOT RUN**; external collaboration welcomed through [public issue intake](mechanistic-interpretability/OUTSIDE_COLLABORATION.md).

## RESEARCH_INDEX.md

Link [MECH-INTERP-01](mechanistic-interpretability/README.md) and its [MECH-STEER-DEV-01 contract](mechanistic-interpretability/MECH_STEER_DEV_01_CONTRACT.md). Say **no scored model run or confirmed capability gains**.

## research-index.json

Add project with id `mechanistic-interpretability`, entrypoints to README/experiment/negative ledger/outside pipeline and explicit `scientific_confirmation: "not established"`.

## AGENTS.md

Add one pointer to [outside collaboration pipeline](mechanistic-interpretability/OUTSIDE_COLLABORATION.md), clarify that outside issues, PRs and relayed agent reviews do not authorize model execution, and preserve current safe workflow.
