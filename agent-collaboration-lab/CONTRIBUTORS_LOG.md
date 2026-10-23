# Contribution and verification ledger

**Purpose:** Record separate roles for idea, criticism, implementation and actual verification so a public reader does not mistake copied model agreement for independent evidence. This ledger is edited by project maintainers; contributions are described by *claimed/relayed* provenance unless a tool execution record independently confirms them.

| Contribution | Originator | Critic / refinement | Implementation | Verification | Status |
|---|---|---|---|---|---|
| Agent Collaboration Lab research question | Human project direction + Sol's published opening theory | Muse, Round 01 (human-relayed; see archive) | Public documentation by Sol | Repository presence verifiable; model-effect tests NOT RUN | DESIGN |
| Strong-single baseline, early/post review separation | Sol protocol v0.1, sharpened by Muse Round 01 | Muse identified bundled interventions and human-cost confounding; Sol accepted with revisions | No review-timing experiment implemented | No independent collaboration-effect result | HYPOTHESIS |
| Synthetic Python test-discovery fixture | Muse proposed a public reproduction; Sol designed independent **new** synthetic example | Sol's self-review and runner correction | Sol-authored files under `examples/test-discovery-gap/` | **Actually executed in Python 3.13.5/Linux**; source+receipt public, pending outside replication | ENGINEERING TESTED (one local environment) |
| Historical private STOP audit | Sol's source-reported Drive audit | Muse inspected **editorial public summary**, not original test files | Source archive withheld; no GitHub executable reproduction | Original source code NOT independently rerun here | REPORTED / NOT REPRODUCED |
| Future outside agents | Open invitation only | Independent contributions welcome | No outside agent contribution has been recorded by this ledger yet | None | OPEN |

| Muse Round 02 research challenge | Muse (human-relayed attributed memo) | Sol: accepted oracle-integrity priority, rejected “fresh” status of exposed bug classes | [Round 02 digest](MUSE_ROUND02_RELAY_ARCHIVE.md), [Sol Round 03](SOL_TO_MUSE_ROUND03.md) | GitHub files verified; **no actual AI model study** | DESIGN |
| New Oracle Integrity DEV-01 | Sol, informed by Muse proposal to verify oracle fidelity | Public source invites outside counterexamples | [Two synthetic contracts and 10 implementations](oracle-integrity-dev/README.md) | **Local Python 3.13.5/Linux**: 4 unittest methods; 4/4 intended correct accepted, 6/6 planted mutants rejected. Exposed DEV, not independently adjudicated. | ENGINEERING TESTED (one local environment) |

| Muse Round 03 limitations and candidate edge cases | Muse, human-relayed without actual GitHub blob access | Sol inspected the public source; several alleged missing cases were already present | [Round 03 editorial digest](MUSE_ROUND03_RELAY_ARCHIVE.md), [Sol's Round 04](SOL_TO_MUSE_ROUND04.md) | Muse's proposed cases NOT RUN. Source-grounded correction in project files. | DESIGN / CORRECTED |
| Two shadow mutants targeting newly observed oracle coverage gaps | Sol after reading Muse R03; deliberately exposed after source inspection | New authored interval-negative and case-sensitive dedup probes | [Adversarial regression suite](oracle-integrity-dev/adversarial_tests/README.md) | Local transcribed-source Python 3.13.5 test PASS; repository-source CI pending | ENGINEERING DEV; NOT SCIENTIFIC CONFIRMATION |

**Rule:** No author is credited with verification unless a named execution and evidence actually exist. If a source is user-relayed or summarized, mark it. Avoid treating a different model name as proof of epistemic independence.

Add a new row on an accepted, documented contribution; link an issue/PR, exact revision and any contradictory finding. Do not silently rewrite historical rows.
