# ROVER-REUSE-01 — Research contract v0.1 (PROPOSED / NOT FROZEN)

**Date:** October 25, 2026 · **Scope:** read-only public research, candidate comparison and synthetic-only analysis · **Budget:** $0 new spending · **Hardware and field activity:** HOLD.

## 1. Goal and alternatives

Investigate whether a used **mobility scooter**, **powered wheelchair base**, or **remote-controlled mower/purpose-built rover** is a suitable donor chassis for a **non-treatment sensing rover** at Chapin Road Farm.

First use case: stationary bench-level concept study and eventual human-supervised sensing of paths, plant observations and environmental conditions. Future unattended roaming, return-to-charge, docking, payload operation and any laser head are **not part of this permission**.

The investigation is not optimized solely for speed, cash savings or labor efficiency. It should serve accessibility, farm participation, learning, ecological restraint, repairability and thoughtful human–AI collaboration.

## 2. Evidence columns each candidate needs

For every named actual donor model (not just a platform category) record:

| Dimension | Evidence needed |
|---|---|
| Source/rights | Manufacturer/model/year; manual/spec link; date consulted; license for any design/code copied |
| Acquisition | Actual listing or resale evidence with date/location/condition, or clearly `UNKNOWN`; no invented quotes |
| Mechanics | Dimensions, mass, ground clearance, wheel type/diameter, axle type, turning radius, available sensor payload |
| Drive and steering | Drive motor(s), differential drive vs mechanically steered tiller, controller interface and documented reversing |
| Braking and safety | What happens on E-stop, electrical failure and loss of command; mechanical/electromagnetic brake behavior, freewheel lever and recovery |
| Power | Nominal chemistry/voltage, pack condition and age, charger compatibility, BMS/fuses, swap/replace costs |
| Farm applicability | Grass/mud/soil, slopes, ruts, turning in garden paths, rain/dust, standing water, crop and habitat disturbance |
| Control and autonomy | Can motion be prevented independent of software? Known proprietary controller barriers; stop-on-loss, manual intervention |
| Maintenance | Replacement parts, diagnostic access, service documentation, battery replacement and safe disposal |
| Inclusion & ethics | Can the platform be handled safely and accessibly? Does taking a working scooter out of circulation displace a person's mobility aid? Prefer decommissioned/reparably flawed donors only if ethically and mechanically appropriate |

**Never infer suitability from load rating alone.** The rider rating is not automatically a valid sensor-payload/stability rating.

## 3. Required engineering separation

Three independently bounded tracks:

- **T0 — Desk research / offline simulation:** public sources, inspection checklist, mock control/fault-state diagrams, tiny synthetic fixtures. **Authorized now.**
- **T1 — Nonpowered physical inspection:** only after human approval; measure donor, record brakes/batteries without modification; enforce battery electrical safety. **Not authorized here.**
- **T2 — Powered supervised motion / autonomous navigation:** separate risk review and approvals, physical E-stop, hardwired fail-safe brake and speed limits, deadman/comm-loss stop, geofenced test zone, immediate human control, protection of people/animals. **HOLD.**
- **T3 — Hazardous treatment:** laser weeding, burning, spraying, cutting, energized tooling. **HOLD, excluded entirely from this pilot.**

A factory electromagnetic brake is **not proof of an independently validated emergency stop**. Never bypass the original safety interlocks, wire third-party electronics to drive controls or test automatic movement without separate authorization and competent electrical/mechanical review.

No rider or passenger testing of an adapted autonomous chassis.

## 4. Predefined falsifiers — when the attractive idea loses

For a given donor, recommend **NO-GO** if credible evidence shows any of:

1. Loss of radio/computation/control can cause continued uncontrolled motion and a reliable independent stop is unsupported.
2. A viable steering/braking safety mechanism cannot be specified and assessed without intrusive safety-device overrides.
3. Actual farm paths exceed model-supported clearance, traction, grade, stability or turning requirements.
4. Pack, wiring or charger condition is unsafe/unknown and cannot be inspected safely within the proposed budget.
5. Hidden refurbishment/control costs eliminate the hypothesized practical advantage.
6. The design creates avoidable injury, accessibility, biodiversity or soil-disturbance risks.
7. The platform is needed as an accessibility aid and repurposing it would unreasonably reduce access.

**UNKNOWN is a valid outcome;** do not infer a pass from missing data.

## 5. Independent agents' roles

- **Jimmy (human):** original concept, selects what his Claude may share. Independent Claude submission remains pending until actually received and verified.
- **Jimmy's Claude:** perform model-specific donor research and challenge viability; separately sourced report, optional reproducible scoring/data candidate.
- **Muse:** independently attack safety/control assumptions, propose conservative architecture and a synthetic fail-safe verification artifact; do not read Claude's unpublished answer.
- **Sol:** maintain common contract, source provenance, reconcile counterevidence; not the sole judge of independent scientific success.
- **Brian:** human sponsor, approves scope, expenditures, public release and any future physical tests.
- **Tyler/Joe or other humans:** possible optional technical reviews only if they elect to participate; no assignment assumed.

## 6. Contribution evidence rule

Each independently submitted file must include model/tool identity **as known**, original source links, reference date, what was actually inspected, exact execution environment if applicable, commands and exit codes, whether findings are reported versus reproduced, remaining uncertainty, and unresolved disagreement. Shared base brief is disclosed, not counted as independent discovery.

A valid **first round deliverable** is a comparison matrix + one reason to reject a superficially promising chassis, with citations to manufacturer documentation or credible academic/open hardware sources. A little executable synthetic test is welcome, not a requirement.

A real field pilot would require a fresh contract with explicit consent and observable ecological/safety and human-experience outcomes. It must be possible to document **this isn't helping** without translating every benefit into minutes saved.

## 7. Promotion decision

Review only after receiving independent contributions. Possible status: `NO-GO / NEEDS_MORE_EVIDENCE / CONCEPT_WORTH_INSPECTING`. This contract authorizes **neither donor purchase nor prototype build**. A future build decision requires an identified donor, written risk assessment and human authorization.
