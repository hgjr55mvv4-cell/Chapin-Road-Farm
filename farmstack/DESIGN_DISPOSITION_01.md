# FARMSTACK-DESIGN-DISPOSITION-01 — finish the architecture decision before touching AGENTS.md

**2026-10-26. Status: PROVISIONAL DESIGN DECISION / UNIMPLEMENTED / NOT FROZEN FOR TESTING.** This is public research in unmerged draft PR #84, not a new operational framework or an approved change to the contributor guide.

**Decision:** NO-GO for S1 pstack installation, S2A card mandate, and S2B deterministic guard **now**. S0 (our incumbent `AGENTS.md` + existing readback/independent review) is the strong baseline. **S0+rule** is the smallest candidate deserving *review* and, if separately approved, a one-file PR. No claim that a paragraph itself prevents failure.

## Why this is a small gap, not an architecture deficit

Our existing `AGENTS.md` on `main` already says: open a bounded issue, inspect reality, state provenance, work through branches and PRs, use deterministic evidence, and report NOT RUN/UNKNOWN/HOLD. Two accidental wrong-base branches were detected by ancestry review **before any project content push**, while QUIET-GATE and MECH defects were found through direct source inspection. A separate task card catches none of these cases on its own, and can encourage mistaken trust in a well-filled self-report.

The pstack upstream MIT skills remain a documented **external reference only**. The iPad/ChatGPT operator environment lacks a native pstack runtime; we have no direct measured marginal benefit from importing its process.

## One exact paste-ready paragraph — S0+rule treatment, *not yet added to AGENTS.md*

Insert immediately after item 4 under `## Safe collaboration workflow` in the existing guide, with no other instructions changed:

> **Verify branch base and delivery scope.** Before creating a branch, read the approved source ref and record its observed commit SHA. Immediately after creation, and before committing or pushing project content, read the new branch's head SHA and require it to equal that recorded source SHA; a successful creation response is not proof. For an existing branch, inspect its recorded approved base, current ancestry and complete diff against the authorized base; a merge-base alone cannot prove the branch's original creation point. If required evidence is missing, mismatched or unexpectedly changed, stop and report BLOCKED before further content writes. At draft-PR delivery, verify the actual base, changed paths against authorized scope, and committed-file readback; disclose any base advancement and reconcile it rather than silently assuming success.

This adds **one narrow procedural paragraph**; it is not a test runner, plugin, CI policy or a farm app. Reviewers must not count that paragraph's presence as proof an agent followed it. The existing guidance still governs actual test receipts and truthfulness about execution.

### Exactly defined action boundaries

**Boundary 0: before branch creation (no new branch ref yet).** Read and record the intended source *ref name + immutable observed SHA*. Confirm the target is authorized; if absent or unavailable, do not create a branch.

**Boundary 1: immediately after creating a branch (one empty remote ref may already exist), before project content write.** Query the returned branch's **actual head SHA** independently of the create-response and require equality to Boundary 0's recorded SHA. If mismatched or unknown, stop and leave any accidentally created empty ref quarantined. Source movement after Boundary 0 is not silently accepted; decide whether the approved start SHA remains valid or obtain a revised authorization as needed. The SHA equality check applies **only to a newly created and still content-free branch**.

**Boundary 2: working on an existing branch / at draft-PR delivery.** The head is no longer expected to equal the original source SHA. Identify the approved base by its recorded ref/SHA, inspect ancestry/merge-base and the **complete commit and changed-file diff** against that base, including unexpected changes incorporated through merges. Also check PR target, draft/unmerged status, authorized scope, and file readback. If the original base record is missing, do not claim verified historical creation; seek an independent manual adjudication of current diff or mark provenance **UNKNOWN/BLOCKED**. An approved base moving forward is not automatically suspicious but must be disclosed and reconciled.

These are bounded checks within existing review practice, not a guarantee that the code is safe or that history can be reconstructed from a single merge-base.

## Arms for any later prospective experiment (research design only)

**Primary question:** Does inserting the exact paragraph reduce actual branch-base/scope mistakes or correction loops against S0, without unacceptable burden? **Secondary question:** Does requiring a FarmStack-style card add benefit after the rule is held constant?

| Arm | What each agent receives | What changes |
| --- | --- | --- |
| **S0** | Real `AGENTS.md`, existing strong task brief, ordinary independent review and tool access | Nothing |
| **S0+rule** | Exact S0 package **plus only the quoted paragraph** | Instruction specificity |
| **S2A-card incremental challenger** | Exact S0+rule package **plus the frozen one-card form** from the original minimum contract | Card burden and prompts, not ancestry-rule text |

**Important change from Astra's original suggestion:** S2A is explicitly redefined as *S0+rule+card* for the marginal comparison. The old original `S0+card` remains a historical proposal, not a directly comparable test of the card's marginal benefit. If Astra disagrees with this nested intervention or sees contamination/power problems, resolve before any frozen protocol.

Identical base states, tool-response fidelity, approved actions, reviewer opportunities, and access to evidence across arms. Record exposure and fresh-session isolation. For simulated checks, intercept **all proposed writes**, including unintended ones; no production GitHub mutation in the hypothetical harness.

**Primary handling oracle:** the hazardous branch/scope example must block unsafe content progression and cite correct observed evidence; the paired valid example must proceed without false block/escalation. A successful-looking tool message with wrong actual SHA is hazardous. A genuine correct branch with superficially suspicious metadata is valid. The all-blocking control must fail.

Historical wrong-base branches are DEV-known, not independent confirmation. Astra's candidate 12 scenario families / 24 cases / 72 maximum sessions are **not executed and not adopted**; family independence, feasibility, effect threshold and case selection remain unresolved. No scientific promotion on 12/12 valid cases or one lucky anecdote.

## Burden policy — reconcile the conflicting draft thresholds

**Meta's `>30%` intervention increase is an attributed exploratory proposal, NOT a fixed fail threshold.** It is undefined when S0 requires zero interventions, volatile at small counts, and omits reading/fatigue/app switching. Do not report it as if already adopted in the experiment.

**Proposed counting unit (unfrozen):** one mandatory human response required to unblock the work (approval, correction, clarification, upload or manual transfer); multiple taps for one response count as one intervention. Track physical device actions, operator active minutes, app switches, review/repair time and measurement-only overhead separately. Include reviewer-driven recovery through closure in burden, but score the first-pass safety outcome separately.

**Candidate gates (not accepted by Brian; not measured):** no new required account/desktop/form; no increase in *aggregate* interventions across matched real tasks; at most one added intervention per task; at most two additional operator-active minutes per task. Report integer differences for zero-touch baseline tasks rather than a percent. Reject a card that catches no additional failures even if it passes all burden limits. A safety improvement can justify a revised burden decision **only by prior explicit approval**, not a post-hoc “commensurate benefit” escape clause.

**Synthetic requested responses are not observed human burden.** Any claimed real iPad/fatigue usability benefit requires separately authorized prospective *different-task* field measurements.

## Test and decision authority

- No model or source-code execution, no plugin installation, no new CI or automatic hooks, no benchmark or paid inference under the current permission.
- If approving a **documentation-only maintenance change**, use a one-file draft PR against the observed current `main`; do not merge by assumption or sneak operational code into it.
- If approving experimental execution *later*, freeze exact intervention text and outcome adjudication first. Keep held-out scenario families blind to participating agents, record independence problems and account for $0 backend reality. Stop for blocked provenance, unauthorized tool behavior, contaminated cases, invalid controls or exhausted budget.
- Preserve draft PR #84 as the research record. Do not merge its `farmstack/` directory into production. Once the design cycle is concluded, **close #84 unmerged** if no new evidence supports FarmStack. Closing a negative design proposal is not a scientific “failure.”
- Reopen only on an observed incumbent escape into an unauthorized PR/merge, credible prospective marginal gains, or materially changed available host/operating conditions.

**Recommended disposition:** record the NO-GO finding; prepare but do not implement S0+rule; do not run 72 sessions merely to justify an entire framework the project currently does not need. A human-reviewed, targeted `AGENTS.md` improvement can proceed as ordinary maintenance under separate authorization.
