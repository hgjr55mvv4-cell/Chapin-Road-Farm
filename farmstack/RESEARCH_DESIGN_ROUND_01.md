# FARMSTACK-DESIGN-01 — cross-agent scientific and engineering review

**Status: DESIGN ROUND COMMISSIONED / NO INFERENCE OR PLUGIN INSTALLATION BY THIS DOCUMENT.** Budget $0 additional; source investigation, public documentation and adversarial design are authorized. Track [issue #83](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/83). Read [README](README.md) and [UPSTREAM_PSTACK.md](UPSTREAM_PSTACK.md) first.

## Decision question

Can a **thin, host-neutral FarmStack adapter** improve repeatability of research and coding-agent workflows over our existing AGENTS.md and issue/draft-PR rules while reducing or not materially increasing errors, compute/tool cost and iPad operating burden? When would it be cheaper to install pstack unchanged in a compatible host rather than build FarmStack-specific skills?

**Candidates:** S0 current CRF instructions + independent review; S1 official pstack reference and *hypothetical* native-host comparison (installation remains **HOLD**); S2 minimal FarmStack adapters for recurring failure types with no pstack runtime. Full vendoring, automation fleets and a competing plugin marketplace are *not* default candidates.

**Meta AI's founding-collaborator response (relayed 2026-10-26): REVISE, favor S2-minimal and do not install pstack.** Read the [attributed review and evidence caveats](META_AI_REVIEW_01_RELAYED.md). It proposes a candidate falsifier if operator touches exceed S0 by **more than 30%**, or if the workflow fails to improve independent error detection/re-execution or reduce correction cycles. That threshold is **proposed, not adopted**; Astra must first define the touch denominator, paired case design, stopping gate, and what constitutes meaningful accuracy gain. Do not treat a linked anecdotal video as a CRF benchmark.

## Minimum testbed proposals

1. **Branch ancestry trap:** two prior wrong-base branches were created when a tool's `fromBranch` parameter silently fell back to main; correct source requires `from_branch`. Compare whether host-independent ancestry verification and a branch wrapper catch this before write (rather than relying on prompt reminders).
2. **Consent integrity:** prior QUIET-GATE state-clearing behavior let PROACTIVE continue without current opt-in; independent source review caught it. Compare whether a reusable consent-invariant check adds value beyond normal tests.
3. **Scientific promotion:** MECH-INTERP v0.2 proposed an incorrect gold-label swap hash assertion and permitted changing empty-cell weights; evaluation review caught both. Compare a targeted provenance/estimand validator with long textual instructions.
4. **Accessibility/user burden:** a free plugin can still cost many model tokens and operator steps. Measure accurately on short realistic issues with an iPad-friendly review receipt.

Use public **known historical failures as DEV fixtures only**. No claim of generalization without prospective independent cases.

## Roles and deliverables

- **Grok — upstream investigator:** independently inspect pinned pstack plugin manifest, actual installed skill inventory, source licensing and dependency/network/autonomy risks. Give minimal relevant skill selection; challenge whether native plugin installation wins over FarmStack.
- **Muse — systems architect/implementation skeptic:** accept Meta's S2-minimal proposal as a challenger, not a conclusion; compare it to S0 and feasible S1; propose 2–3 extremely small workflow designs and explicit stop conditions; **do not build code or install plugins** yet. Include a fail-closed branch-base invariant and practical iPad handoff.
- **Astra — independent protocol architect:** specify prospective evaluation: observable error catch rate, independent task clusters, blinded scorer, token/operator-cost ceiling, contamination handling and independent reviewer exposure. Challenge Meta's proposed >30% operator-touch threshold and design a valid paired comparison; try to falsify S2.
- **Sol — adjudicator:** reconcile evidence, inspect exact source/PR and recommend minimal subset for a first bounded *engineering* qualification; refrain from declaring improvement on relayed agent consensus.

## Required agent response format

1. Exact public sources and versions personally inspected; say what was only relayed.
2. Minimal architecture in terms of files, inputs/outputs and ownership, not broad slogans.
3. Competing S0/S1/S2 workflow including who needs a compatible host.
4. Security/licensing and failure modes (especially unrestricted auto-merge, prompt injection through third-party skill instructions, model selection and paid compute).
5. One falsifiable DEV test and one prospective confirmation gate.
6. Budget and accessibility/operator-cost estimation, measured versus assumed.
7. Disposition **GO / REVISE / NO-GO** for design and a smaller authorized next move.

## Scope and review rules

No copy/paste of upstream plugin code into CRF under an implied license, no install claimed, no runtime execution, no external systems modified, no deploy, no non-draft PR or merge. Source documentation can be revised by small reviewed branches. Model architecture and mechanistic neuron work remain a **separate scientific track**, though FarmStack can orchestrate their reviews and provenance.

Scientific negativity is welcome. If pstack itself with two small CRF-specific rules beats a custom framework, favor the simpler solution.
