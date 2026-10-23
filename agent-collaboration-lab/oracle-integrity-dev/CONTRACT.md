# Oracle Integrity DEV-01 — public specifications

**Engineering DEV; exposed cases, NOT an independently blinded validation.**

**T1 — Half-open interval intersection:** Each input is a pair of integer tuples `(start,end)` satisfying `start <= end`. Return true exactly when intervals `[start,end)` intersect with **strictly positive length**. Touching endpoints and zero-length intervals do not overlap. Symmetry is required.

**T2 — First occurrence by key:** Given a list of `(string_key,integer_payload)` pairs, return the first tuple for each distinct key in **original encounter order**. Preserve the first payload. Empty input gives empty output.

Eight hand-selected truth cases per task are in `truth_cases.py`, separately from `implementations.py`. The implementations include two intended-correct variants and three deliberately faulty mutants per contract. We designed **both** the truth cases and mutants; they are not externally adjudicated or a population sample. New outside counterexamples and corrections are welcome; none of these cases can become future untouched confirmation.

This package does not run AI inference, measure reviewer independence or reproduce the original private STOP audit.
