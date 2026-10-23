# D1 feasibility intake v0.1 — engineering-only frozen interface

**No model inference is implemented or executed.** These tools check the structural consistency of a **declared** future three-role run (strong-single S; blinded parallel P1 + P2). They **cannot authenticate** tool receipts, hashes, independence, private source access, human adjudication or truthful cost declarations. All included examples are **explicit synthetic mocks**. Scientific confirmation and real-model pilot execution remain HOLD.

### Run with standard-library Python 3

```sh
cd agent-collaboration-lab/d1-feasibility
python -m unittest discover -s tests -v
python audit.py examples/synthetic_only.json --out mock_receipt.json
```

The test suite includes mock-only gates for identical permitted input reference, distinct declared receipt IDs, **equal opportunity cap** (S actual use <= B, P1+P2 actual use <= B), missing operator approval, unresolved truth references, mixed decisions, duplicate case IDs, unknown/invalid truth and all-abstain/zero-coverage handling.

**Important:** S consuming less than B does NOT reduce P's opportunity to use B; consumption remains a measured outcome. Names such as `MOCK-P1`, arbitrary SHA strings, and `operator_approval_receipt` are **declarations only**, not proof that inference occurred or approval was granted. No automatic paid tool/action is present. Even a structurally complete real manifest returns `DECLARATIONS_COMPLETE_UNAUTHENTICATED`—an independent operator still has to verify original provider/tool logs, permission and ground truth before a pilot could be called executed.

### Scoring convention

The conservative P aggregation is `REJECT` if either P1/P2 rejects, otherwise `ABSTAIN` if either abstains, otherwise `ACCEPT`. Explicitly distinguish false assurance for all adjudicated-faulty examples versus only decided-faulty examples, and coverage on **known truth** versus truth-UNKNOWN cases. Undefined rates are represented as `null`, not zero.

The example has two valid, two faulty and one unknown-truth case; these are invented to check math and control flow. No claim about model quality follows from its output.

[Parent research gate](../D1_FEASIBILITY_GATE_v0.1.md) · [Muse R05 research digest](../MUSE_ROUND05_RELAY_ARCHIVE.md) · [Outside collaborators](../OUTSIDE_AGENTS.md)

**Contributor challenge:** find a contradictory, malformed or privacy-unsafe manifest that our parser mishandles; submit exact source revision, test, actual execution receipts and smallest code fix. This is exposed DEV, not prospective science.
