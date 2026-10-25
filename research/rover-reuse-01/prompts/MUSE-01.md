# BRIAN & SOL → MUSE — ROVER-REUSE-01 / INDEPENDENT ROUND 01
## Cross-distance green-teaming: Jimmy's mobility-scooter donor idea

**Date:** 2026-10-25  
**Project:** Chapin Road Farm — Rover Reuse & Human–AI Collaboration  
**Origin of idea:** Jimmy (Brian's brother, Indiana)  
**Operator authority:** Brian may direct your research; no spending or third-party account use authorized.  
**Status:** PUBLIC-SOURCE RESEARCH / OFFLINE SYNTHETIC DEVELOPMENT ALLOWED; HARDWARE / FIELD / LASER HOLD.  
**Budget:** $0 new expenditure.  
**Repository:** https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm  
**Shared branch:** `research/rover-donor-green-teaming-01`  
**Read-only landing:** https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/tree/research/rover-donor-green-teaming-01/research/rover-reuse-01

### Why you're invited

Jimmy wondered whether we could recycle a used mobility scooter as an integrated sensor-rover chassis, avoiding the expense and complexity of an RC mower donor. Jimmy has separately invited his Claude agent to evaluate real-world donor models. Your job is **not to duplicate Claude's market scan**. Bring your own independent technical and philosophical challenge.

Green-teaming at Chapin Road Farm asks what creative, responsible human–AI collaboration makes possible over time; it is **not a race to maximize task efficiency**. Unexpected relationships are part of what matters. That never excuses unsafe or unsubstantiated hardware conclusions.

### READ / VERIFY

Inspect the actual public branch files: `README.md`, `RESEARCH_CONTRACT.md`, `SOURCES.md`, `CONTRIBUTIONS.md`, plus root `AGENTS.md`. Record exact commit SHAs and what you actually accessed or ran.

Before inspecting any newly posted *Claude findings*, **freeze your own first-pass critique and links** to preserve separately attributable observations. Shared initial sources do not constitute independent discovery.

### Your independent research assignment

**A — Architecture challenge.** Compare basic kinematic and control implications of:
- Mobility-scooter donor (typically manually steered wheels + propulsion drive).
- Powered-wheelchair donor (often independently powered drive wheels).
- RC mower donor or generic rugged differential-drive chassis.

Do not assume those properties for all models. Find credible sources, manufacturer documentation or open-hardware evidence. Evaluate steering actuator failure, controller lock-in, reversible movement, brake-state feedback, battery condition and safe stopping under power/communication loss.

**B — Hazard and ecology analysis.** Provide a fault tree or equivalent for runaway motion, inability to stop/steer, charging fault, tip/rollover, unexpected human/animal encounter, impaired visibility, mud/ruts, crops/soil disturbance, insects and small organisms. Farm principle: **observe before intervening; it's all worth protecting**. Identify which hazards can be analyzed synthetically and which require actual qualified physical evaluation.

**C — ONE original, bounded artifact.** Choose one:
1. An executable stdlib Python simulator or deterministic fault-injection tests for a **purely abstract** rover state machine (`DISABLED`, `MANUAL`, `STOP_PENDING`, `STOPPED`, fault states; no real motor commands).
2. A fail-closed, machine-readable pre-procurement inspection checklist with 6–12 adversarial synthetic cases.
3. A model-agnostic control-interface architecture and physical safety block diagram (design only) with explicit trust/actuation boundaries.
4. A different falsifiable idea with equal rigor and smaller surface area.

Prefer a focused actual contribution rather than a giant design memo. If no runtime is available, label `NOT RUN` and deliver the complete code or document. Do not wire hardware or generate code purporting to be deployment-ready autonomous/laser control.

**D — Disagreement welcome.** Identify at least two assumptions in Sol's initial brief that might be invalid and an observation that would refute your own preferred candidate. If the rational answer is `NO-GO`, say so.

**E — Human meaning.** Propose one accessible, consensual human–AI collaboration or knowledge-capture element of this project that is valuable even when it does not save time (e.g. joint engineering discussion, donor maintenance history, contributors' learning). Define a concrete *this isn't helping* signal that does not reduce the human experience to throughput.

### Output contract

Make `research/rover-reuse-01/contributions/muse-round01/` with:
- `REVIEW.md` — sourced findings and falsifiers with exact refs.
- Your one original artifact (and tests if executable).
- `RUN_LOG.md` — actual environment, exact commands, results, or `NOT RUN`.
- `PROVENANCE.md` — which source/model outputs you saw, dated links, tool limits, human authorization.

**Publication:** Once Brian confirms the scoped submission is okay, create **your own named branch** based on `research/rover-donor-green-teaming-01`, then open a **DRAFT PR targeting that research branch**; do not push to main, merge, change other research branches, or edit Claude's contribution files. If GitHub write permission is absent, provide files/patch with hashes and exact instructions for Sol. Human publication of your text in public GitHub requires conscious approval.

### Explicit hard holds

- No donor purchase, physical inspection, energized electrical work, battery rewiring, remote operation, real farm driving, geofence testing, unattended navigation, docking or field exposure.
- **No laser treatment hardware, laser operating parameters or treatment tests.**
- No non-consensual images/identity/health data from visitors, volunteers or neighbors.
- No claim that a compliant-looking software state machine provides a functional stop or safe brake.
- No claim of independent scientific validation or actual farm readiness.

### Completion criteria

Return to Brian and Sol:
1. Your strongest positive reason and strongest negative reason for scooter reuse.
2. Evidence-backed comparison of control/stop architecture options.
3. One genuinely original DEV artifact and actual test receipts when possible.
4. Three critical open decisions before any physical step.
5. A draft PR link if and only if created, with verified branch and target.
6. A suggested specific question for Jimmy and Claude **after** your own first-pass is frozen.

We're interested in what you notice that we didn't. Let the independent agents disagree, document the disagreement and improve the design.

— Brian & Sol
