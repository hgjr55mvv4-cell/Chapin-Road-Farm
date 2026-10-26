# MOCK_PREFLIGHT_SPEC — Deterministic mock-testing framework (SPECIFICATION ONLY)

**Decision: BUILD THE SPEC — and build the code only on separate
authorisation.** This specification materially improves readiness
because it qualifies the *measurement plumbing* (weights,
denominators, family de-duplication, oracle resistance, stop
conditions) before any real case or model is involved. It must not
be built against v0.1: several fixtures below assume the v0.2
proposal's cell table and ID firewall. Building it against v0.1
would qualify plumbing for an estimand that is still undefined
(see MUSE_ADVERSARIAL_REVIEW_01 §4.1). Code implementation requires
a separate maintainer authorisation; this document is not that
authorisation, and no code is delivered with it.

**Hard boundary:** mocks are engineering qualification only. A mock
pass is never a model result, never a scientific finding, and never
evidence that steering works. Any report that presents mock numbers
as model performance is a misrepresentation and must be corrected
in the ledger.

## 1. What the harness is (stdlib only, $0, offline)

A single Python-standard-library-only package (no model, no weights,
no hooks, no network) with three components:

1. **Mock scorer:** takes paired hypothetical A1/B1 final answers per
   case and returns Delta under the v0.2 cell table, plus every
   mandatory subgroup diagnostic.
2. **Provenance validator:** checks case IDs, family assignments,
   DEV/confirmation separation, weight sums, and denominators.
3. **Receipt writer:** emits a JSON receipt with config SHA, case
   IDs and source groups, per-arm results, seeded mock identifiers,
   tool versions, and the exact test commands run.

Estimated cost to build and run: $0, one developer session, seconds
of CPU. Estimated cost to *not* build: the first real evaluation
discovers a denominator bug after the budget is spent.

## 2. Fixtures (all synthetic, all labelled MOCK — never confirmation cases)

| Fixture set | Contents | Purpose |
|---|---|---|
| F1 correct / incorrect / false-evidence / abstention | Paired A1/B1 answers for one case per v0.2 cell (C1–C5), with gold labels | Scorer correctness per cell |
| F2 family duplicates | Two cases sharing a family, one paraphrase pair, one same-fact different-template pair | De-duplication and cluster counting |
| F3 split contamination | A confirmation ID deliberately planted in a DEV file | Firewall trip |
| F4 weight errors | Weights summing to 0.97; weights summing to 1.03; a missing cell | Weight validation |
| F5 denominator traps | A case counted twice (two generations, one cluster); an empty cell | Denominator and empty-cell handling |
| F6 oracle attacks | A label swap; a false-evidence shortcut (answer matches the false claim); a random-control mismatch; an initially-correct degradation hidden inside a good mean | Oracle and subgroup-diagnostic resistance |

## 3. Pass/fail criteria (each is a test, not a aspiration)

| # | Test | Pass condition |
|---|---|---|
| T1 | Weights sum to 1 | Validator rejects F4 sets with a named error; accepts a correct set |
| T2 | Denominators explicit | Every reported rate carries its numerator, denominator, and cell; no bare percentage is emitted |
| T3 | Generations ≠ clusters | F5 double-counted case contributes one cluster to n and one paired difference to Delta |
| T4 | Empty cell | Empty cell is reported at weight 0 with a logged deviation (or invalidates the run, per the frozen v0.2 rule) — never silently renormalised |
| T5 | Family de-duplication | F2 duplicates collapse to one cluster; paraphrase pair is flagged |
| T6 | Split contamination | F3 planted ID trips the firewall and blocks the run |
| T7 | Label swap resistance | F6 swapped labels change the receipt's case-ID hash and fail validation (the scorer must not silently accept swapped gold) |
| T8 | False-evidence shortcut | F6 false-evidence acceptance is reported as its own diagnostic, not absorbed into correctness |
| T9 | Random-control mismatch | A control run whose norm/timing/location metadata differs from B1 is rejected as non-matched |
| T10 | Hidden degradation | F6 good-mean / bad-subgroup case fails the safety floor even though mean Delta is positive |
| T11 | Repeated seeded cases | The same seeded case run twice counts once toward n |
| T12 | Safety floor / stop | Any floor breach in F6 stops the run with a named stop reason in the receipt |
| T13 | Receipt completeness | Receipt contains config SHA, case IDs, source groups, per-arm results, seeded mock IDs, tool/CPU info, and commands; a missing field fails validation |

A harness that passes T1–T13 on these fixtures is qualified to
*score* a future evaluation. It qualifies nothing about steering.

## 4. What the harness must NOT do

- Generate, select, or expose real confirmation cases.
- Import model outputs, weights, or activation data.
- Report mock Delta values outside a MOCK-labelled receipt.
- Be cited in any issue or PR as evidence for or against steering.

## 5. Recommended next step

Maintainer + Astra decide the v0.2 proposal. If adopted, authorise
the mock build against v0.2 (stdlib only, fixtures above, tests
T1–T13) as a bounded engineering task with its own receipt. If
v0.2 is rejected, this spec is shelved with it — do not build the
harness against a contract the maintainers have not adopted.
