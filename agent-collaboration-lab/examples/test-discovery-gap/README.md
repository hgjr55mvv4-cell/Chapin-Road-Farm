# Synthetic test-discovery gap — independently generated example

**Status:** ENGINEERING DEV fixture, not a recreation of the private HARNESS-MECHANISM-DEV-01 code or a self-improvement experiment.

A historical Sol-authored STOP report described how direct invocation of test functions yielded passing results while an advertised `python -m` path discovered zero tests. We **do not** have public runnable original source or rights-clear receipts for that audit. This new, dependency-free teaching example merely illustrates that **the executed test count, not a developer's assertion that “tests pass,” must be verified**.

## Reproduce with Python 3 (no third-party dependencies)

From the directory containing this README:

```sh
python -m unittest discover -s tests -v
python verify_fixture.py
python -O verify_fixture.py
PYTHONOPTIMIZE=1 python verify_fixture.py
```

The verification runner executes three separate commands, requires their expected test-count markers, and records each exit code. Explicit checks remain active under optimized Python (`python -O`):

1. Direct-run `bad/test_checks.py`: two checks passed because the `__main__` path calls two ordinary functions.
2. `python -m unittest discover -s bad -p 'test_*.py' -v`: **zero tests discovered**, despite test-like function names. `unittest` discovery requires supported test structures, such as `unittest.TestCase` methods.
3. `python -m unittest discover -s good -p 'test_*.py' -v`: two `unittest.TestCase` methods found and executed.

The two assertions used in each path are innocuous synthetics about a boolean-vs-integer type check and a **pre-execution** budget decision. This fixture does not reproduce the STOP audit's original defects in either implementation or scoring.

### Actual local execution receipt

[Local Python 3.13.5/Linux run, Oct 23, 2026](receipts/local_test_2026-10-23.txt) observed:
- direct 2/2, exit 0;
- broken discovery **0 tests, exit 5**;
- repaired discovery 2/2, exit 0;
- verification script completed successfully.

**Important environment correction:** Some older tools/tests may exit 0 after running zero tests; our specific Python 3.13.5 `unittest` discovery exited **5**. Do not generalize the historical claim of silently successful zero tests across versions. Record actual command, count, exit status, Python version and stdout/stderr for every qualification path.

### Fail-closed verifier regression (Oct 28, 2026)

The original runner used Python `assert` for its exit-code and marker checks. A copied fixture with a deliberately failing repaired suite was rejected under ordinary Python but exited 0 and printed `VERIFICATION_PASS` under `python -O`, because optimization removed those checks. The runner now uses explicit validation and clears inherited `PYTHONOPTIMIZE` for child fixture processes so their own direct assertions remain active. New regression tests execute the valid fixture and three corrupted copies under ordinary Python, `python -O`, and `PYTHONOPTIMIZE=1`; the original fixtures and historical receipt are unchanged. See the [new local execution receipt](receipts/local_verifier_2026-10-28.txt). This is exposed engineering DEV, not a new scientific result; local execution is not a claim that GitHub Actions has passed.

## Outside contributor invitation

Run the script on another Python version/platform and report the observable test count, exit code, version, and any discrepancy. A different environment may behave differently. Open a public issue/PR without private datasets, names or credentials. If any output is changed, preserve the original and add a versioned correction rather than declaring an unrelated historical audit independently confirmed.
