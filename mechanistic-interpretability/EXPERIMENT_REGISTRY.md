# Experiment registry

Evidence stages: IDEA / DESIGN / IMPLEMENTED / TESTED (mock engineering only) / EXECUTED (actual model) / CONFIRMED. Use FAILED for valid negative evidence, UNKNOWN for unevaluable claims, and HOLD for blocked activity. A row may track scientific status separately from engineering status.

| ID | Candidate | Engineering | Scientific | Status date | Actual runs | Decision / next gate |
| --- | --- | --- | --- | --- | --- | --- |
| MECH-STEER-DEV-01 | Counterevidence correction; residual stream preferred | NOT IMPLEMENTED | DESIGN / NOT RUN | 2026-10-25 | 0 model calls; 0 confirmed cases | Muse adversarial design critique, then Astra independent review; **HOLD** model execution |

## Before any new row or promotion

Record frozen candidate version + hash, intervention mechanism, exact model revision, endpoint, independent case-selection, accidental exposure, quality and safety floor, resource ceiling, human labor, evaluator/version, and explicit falsifier. Negative evidence and UNKNOWN stay visible. Mock pass != inference or scientific validation.
