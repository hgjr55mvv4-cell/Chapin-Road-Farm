# Oracle DEV-01 — bounded property checks

**EXPOSED ENGINEERING DEV, NOT FORMAL PROOF OR MODEL EFFECT.**

Uses standard-library Python only: exhaustive **bounded** cases and seeded metamorphic tests, not the third-party Hypothesis library.

Run from `agent-collaboration-lab/oracle-integrity-dev`:

```sh
python -m unittest discover -s property_tests -v
python property_tests/test_properties.py
```

The suite checks **2,025 pairs** of half-open integer intervals whose endpoints range from -4 to +4; 1,000 seeded translations (seed 20261023); and **4,369** deduplication lists of length 0–3 over eight string keys and two integer payload values. It uses an integer-point-set reference for bounded interval overlap and a linear search reference for deduplication. It includes explicit new witnesses for mistakenly stripping whitespace and normalizing Unicode before deduplicating. Both originally labeled correct functions passed in a local Python 3.13.5 execution against a faithful manual mirror of the public module; GitHub CI runs the submitted test file against actual repository modules.

**Important:** Cases and reference functions were designed by this same research process, not independently adjudicated. Finite examples and randomized properties can **falsify** a proposed implementation but do not mathematically prove correctness across all inputs. Standard Python string equality is used for the deduplication reference; the current contract does not explicitly state a Unicode normalization policy. A **future contract version** should make that rule explicit after review, rather than silently rewriting the original document.

These examples and errors are permanently **EXPOSED DEV**. They are not “held-out” model-evaluation data, and no second agent's model performance has been tested.
