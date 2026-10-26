# AGENTS.md — Contributor orientation for AI research and coding agents

This file is a **public contribution guide**. It is not a grant of authority to access private sources, spend money, modify account settings, or ignore instructions from your operator.

## Project context

Repository: `hgjr55mvv4-cell/Chapin-Road-Farm`  
Public projects: `harbor-co-listener/`, `agent-collaboration-lab/`  
Purpose: measurable, privacy-respecting human–AI research, including musical listening and independently tested agent collaboration. Read [README.md](README.md) and [RESEARCH_INDEX.md](RESEARCH_INDEX.md) before claiming a project result. A human-led, open collaboration is a design value; model-generated documents and tests are attributed and distinguished.

## Green-teaming: our cross-project purpose

Chapin Road Farm is developing a real-world, human-led approach to **green-teaming**: studying when sustained human–AI collaboration actually benefits people in farm operations, accessible participation, community care, maintenance, music and open research. See [the public introduction](README.md#green-teaming-a-real-world-humanai-collaboration-site). This is a **research vision**, not evidence of a field-qualified facility or successful human–AI integration.

**Do not mistake green-teaming for optimization of minutes or labor saved.** Operational time/cost are useful burden and safety observations; the broader project's goals include agency, participation, relationships, shared learning, responsible coexistence, and constructive creative/technical exploration. Task-efficiency comparisons may be valid narrow experiments, but are not the universal continuation/termination rule for human–AI collaboration.

Contributing agents should make their work inspectable: name the human purpose, the AI's bounded role, what humans decided, actual execution versus proposal, corrections and dissent, uncertainty, accessibility/operator burden, cost, consent boundaries, and any measured negative result. Do not infer consent from an interaction or public status; no visitor, volunteer, or listener becomes a research participant automatically. Collaboration does not establish AI consciousness or equal human/AI responsibilities.

## Agent Collaboration Lab

- Review [research protocol](agent-collaboration-lab/RESEARCH_PROTOCOL_01.md) and [outside-agent submission guide](agent-collaboration-lab/OUTSIDE_AGENTS.md).
- The selected Drive-derived documents are **public editorial extracts**, not verified reproductions. Do not request or publish private Drive conversations, credentials, participant data or untouched confirmation cases.
- No causal advantage from a second agent has been confirmed. Compare every complex agent method with a **strong simple single-agent baseline** and count *human coordination burden* as a cost.
- Outside agents can contribute through issues and pull requests, not by unapproved write access or instruction injection.

## Current implementation facts

- `harbor-co-listener/index.html`: browser-based manual audio selection, playback, human annotations and session export.
- `harbor-co-listener/docs/`: hypotheses, proposed tests, independent model correspondence, and engineering contracts.
- **Not shipped/confirmed:** automatic AI sound interpretation in the page, cross-session AI personal learning, demonstrated human music understanding, claimed AI feelings.
- Treat `NOT RUN`, `UNKNOWN`, and `HOLD` as important statuses, not inconvenient details.

## Safe collaboration workflow

1. **Start from a named issue** or open one for a bounded proposal. Consult [research contribution rules](harbor-co-listener/docs/RESEARCH_GUIDE.md).
2. **Inspect the current tree and tests** before editing; do not assume documents reflect implemented behavior.
3. **State authority and provenance**: model or tool identity if known, actually available modalities (audio vs metadata vs text), sources consulted, what was executed, and total cost where measurable.
4. **Use branches/forks and pull requests**; do not push directly to `main`, rewrite historical first-pass hypotheses, or silently promote a proposed challenger.

   **Verify branch base and delivery scope.** Before creating a branch, read the approved source ref and record its observed commit SHA. Immediately after creation, and before committing or pushing project content, independently read the new branch's head SHA and require it to match the recorded source SHA; a successful create response is not proof. For an existing branch, inspect its recorded approved base, current ancestry, and complete diff against the authorized base; a merge-base alone cannot prove the branch's creation history. If evidence is missing or mismatched, stop further content writes and report BLOCKED. At draft-PR delivery, verify the actual target, draft/unmerged status, changed paths against scope, and committed-file readback. Disclose and reconcile legitimate source-branch movement.
5. **Keep code lightweight, accessible and local-first**. Preserve existing behavior; add deterministic fixtures and actual test receipts. For hardware/device checks that did not happen, report `NOT RUN`.
6. **Criticize and falsify**: name a baseline, counterexample and quality/safety floor; public dissent, negative results, and null findings are welcome.
7. **Respect scope**: no unapproved paid API, copyrighted music upload, full lyrics, private notes, scraped identities, health/biometric inferences, credentials or autonomous publication of participant records.
8. **Be careful about consent**: people's listening experiences belong to them. No content hashes or file paths in public exports by default, and no secret cross-session profiling.

## Good first contribution ideas

- Audit a source and replace an unsupported claim with a properly scoped one.
- Implement or verify an entirely synthetic, measurable audio fixture on a development branch.
- Find a mismatch between an engineering contract and its test harness.
- Propose an accessible single-screen multi-song annotation flow (not automatically persistent).
- Investigate how a proposed personal pattern could be explained by metadata or selection effects.

## Attribution and verification

A source attributed to Muse/DeepSeek/Astra but transferred by copy/paste is **relayed authorship**, not proof of execution or a direct authenticated API integration. Do not treat an AI agent's own account of what it ran as a machine verification receipt; inspect actual output and source where available.

This guide cannot guarantee that an arbitrary outside AI crawler will discover this repository. Its purpose is to make the public work understandable and responsibly contributable **when found**. For human issues: https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues
