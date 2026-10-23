# Case study — a self-improvement harness that independent review stopped

**Technical source:** `SOL — HARNESS-MECHANISM-DEV-01 v0.1.1 Independent Falsification Audit — 2026-10-22 — STOP`, accessed from the user's authorized Google Drive. This is a **public editorial case study of source-reported results**. The audit code and private archive have not been reproduced or published here. No model-effect result is confirmed by this migration.

## What the audit reported

The prior implementation described engineering qualification through scripted positive and negative test cases. The independent audit reported that the directly invoked test functions passed **13/13 positive and 8/8 negative** cases, yet the documented `python -m` commands executed **zero tests**. Other defects included:

1. A hard budget ceiling was not enforced *before* execution: 150 tokens were reserved, but a run consumed 216 before a settlement step raised an error.
2. A purported observation map allowed a valid JSON response to be marked `JSON_PARSE_ERROR` and a malformed one to be treated as error-free.
3. A faithfulness grader labeled a changed existing email field successful.
4. A schema validator incorrectly accepted `age=true` as an integer, consistent with Python's `bool` being an `int` subclass.
5. A recovery path reported no observable error despite a failed requirement.
6. Two supposedly distinct retry paths produced deterministic duplicate outputs, not genuinely independent inference.
7. The reported DEV-only outcomes on 10 constructed cases did not establish actual model-learning gains. One described preserved ZIP was reportedly a 22-byte empty archive.

These are **claims from the authored Drive audit**; this GitHub edition did not execute code, compare ZIP hashes or independently verify the underlying environment. Sensitive identifiers and private archive references are withheld.

## What the audit concluded

The author assigned **STOP** to scoring the v0.1.1 harness. Passing hand-invoked fixtures did not qualify the published execution path or independently validate the observation/grading boundary. Repeated deterministic mock calls did not show a real model received an additional useful opportunity. **Model-effect improvement: UNKNOWN.**

## Why this belongs in an agent-collaboration project

This gives us a concrete research question: can independent *pre-implementation* criticism avert serious implementation defects more efficiently than a strong single-agent self-check, or a post-build audit?

It does **not** prove that multiple agents outperform one. A single expert reviewer or rigorous independent test oracle might have discovered the same defects at lower cost.

## Proposed next test — NOT RUN

Compare strong-single review, second-model review *before* implementation, and second-model review *after* implementation on prospectively selected tasks. Keep evidence, task difficulty, validation oracle, human operator burden and budgets comparable. Score actual defect avoidance, accepted functionality, time, calls and cost. Preserve this published STOP case as exposed inspiration **outside confirmation**.

**The valuable outcome is not a success claim. It is an error boundary that prevented a stronger unsupported claim.**
