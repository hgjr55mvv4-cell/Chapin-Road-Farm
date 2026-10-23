# Shadow-mutant counterexamples — newly authored DEV challenge

**Status: Engineering DEV, public/exposed. Does not update original truth cases, test receipt, or any model-learning claim.**

This follow-up arose from an adversarial reading of Muse's human-relayed Round 03 memo. Muse could not fetch actual files and hypothesized the original test suite omitted touching endpoints, empty intervals, or first-payload preservation. Reading the **actual repo** showed those cases are already present. His input-domain questions are still relevant, but `CONTRACT.md` already states that interval input satisfies `start <= end`, empty intervals are allowed and non-overlapping, and deduplication keys are **strings** with first payload preserved. Therefore reversed intervals, None, unhashable keys and cross-type equality lie **outside** the current defined input domain and do not constitute valid counterexamples.

Instead, we found **two newly authored faulty implementations** that satisfy all eight original cases for their respective contract but violate a legitimate input in the published domain:

1. **Negative time intervals.** A plausible faulty overlap routine clamps time to zero. Its current eight positive-coordinate examples all pass, but `[-8,-4)` overlaps `[-6,-2)`, and the flawed routine returns false.
2. **Case-sensitive key identity.** A plausible faulty dedup implementation case-folds strings. Existing examples use only lowercase letters, so all eight pass, but keys `"A"` and `"a"` are different strings and both must be preserved.

The two original intended-correct routines in each family accept these cases as specified. **No mislabel of an original “correct” implementation was demonstrated.** This proves only that a test suite with 100% success on selected planted mutants can miss additional different mutants.

## Reproduce using the actual repository source

```sh
cd agent-collaboration-lab/oracle-integrity-dev
python -m unittest discover -s tests -v
python -m unittest discover -s adversarial_tests -v
python verify_oracle.py
```

`adversarial_tests/test_shadow_mutants.py` **imports the real existing modules** `implementations.py` and `truth_cases.py`. Its four new tests demonstrate: both shadow mutants pass the original cases; both fail their newly supplied valid input; the two existing intended-correct implementations for each contract pass the new input. Check actual stdout/stderr, exit codes and test counts. CI runs on Python 3.11 and 3.13.

**Local test provenance:** Before publishing this repo-importing version, Sol executed a separate faithful transcription of the public Python functions and labels on Python 3.13.5/Linux; its [JSON receipt](receipts/transcribed_source_2026-10-23.json) explicitly says it is a *transcription*, not execution of a repository checkout. CI is the subsequent execution of imports from the real committed source.

### Scientific limits

- These two faulty variants were created *because* the original cases did not contain these values; all feature selection is retrospectively targeted. They are exposed DEV, **not surprising prospective held-out discovery**, and must not be scored as a new independent confirmation sample.
- A contract's logical semantics require prior adjudication. Current source and test author is the same collaboration system; we cannot claim independent ground truth.
- The new result strengthens future oracle engineering and reveals test-coverage gaps. It cannot estimate general fault-detection rates or the usefulness of two AI models.
