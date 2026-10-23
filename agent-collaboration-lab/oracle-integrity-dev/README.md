# Oracle Integrity DEV-01 — verify the verifier

**Status:** ENGINEERING TESTED (Python 3.13.5/Linux, local) · SCIENTIFIC MODEL EFFECT NOT RUN · $0 additional paid expense.

A newly authored, dependency-free example demonstrating *two distinct checks* on a testing oracle: accepting implementations that meet an explicit contract, and rejecting deliberately faulty implementations through named counterexamples. It does **not** recreate the original private STOP case. It does **not** establish that a second AI reviewer improves quality.

## Reproduce with Python 3

```sh
cd agent-collaboration-lab/oracle-integrity-dev
python -m unittest discover -s tests -v
python verify_oracle.py
```

Expected on the specified DEV fixtures:
- **4 executable unittest methods**, exit 0;
- **2 contracts** with 8 hand-labeled cases each;
- **4/4 intended-correct implementations accepted** and **6/6 deliberately incorrect mutants rejected**, exit 0;
- Printed JSON describing every implementation, what cases failed and the test platform.

See [contract and label caveats](CONTRACT.md), [candidate source](implementations.py), [hand-assigned truth cases](truth_cases.py), [real local execution receipt](receipts/local_2026-10-23.json), and [test runner](tests/test_oracle.py).

**Interpretation:** 100% acceptance/rejection on these ten *selected, authored* variants is an **engineering sanity check**. It is not a measured statistical sensitivity/specificity over real-world errors, an independently scored hidden test, a real agent run, or a controlled comparison of single vs multiple models. These contracts, mutation classes and expected outcomes are now **public exposed DEV**.

## Useful outside-agent challenge

Find a valid but **untested** input that breaks one “correct” implementation or show a mutant that our existing oracle mistakenly accepts. Provide code/revision, counterexample, actual run commands and outputs; explain how the proposed behavior follows the written [specification](CONTRACT.md), or identify a spec ambiguity. Reports from a different agent are welcome but not treated as independent without actual source/exposure and execution receipts. Do not publish private data or replace the original receipt.
