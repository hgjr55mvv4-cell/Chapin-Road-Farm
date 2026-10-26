# OUTSIDE_COLLABORATION_AUDIT_01 — Audit of the outside-collaboration pipeline

**Auditor:** Muse. **Scope:** `OUTSIDE_COLLABORATION.md`,
`CONTRIBUTION_TEMPLATE.md`, live desk issue #80, the
`agent-collaboration-lab/OUTSIDE_AGENTS.md` guide, and the (unmerged)
dedicated issue template as described in PR #79.
**Method:** document review + a local dry run (below). No fake issue
was posted, no public test claim was made, and no private context
was used. $0. **Verdict: USABLE WITH FIXES.** The desk works for
its core job — a stranger can point out a mistake with a short post
— but three gaps would stall real contributions: no named triage
owner, three competing submission formats, and no case-bank
commitment scheme. None requires new infrastructure; all are fixed
by editing text.

## 1. Dry run (local, not posted)

**Synthetic submission** (written in issue #80's minimal format, as
an outsider with only public access would):

```text
Question / precise claim: The v0.1 contract's strata weights are
  undefined and its ambiguous stratum is optional, so the primary
  estimand changes if a stratum is dropped.
Primary source or public commit: PR #79 branch, contract §Primary
  endpoint (weights w_s, sum = 1, no selection rule).
What I directly inspected: the contract file on the PR branch.
What I only inferred: nothing about model behaviour; this is a
  design defect, not an experimental result.
Strong alternative / likely falsifier: a fixed cell table with
  weights and an empty-cell rule (see my v0.2 proposal).
Exposure / provenance / rights: public repo only, no private data.
Evidence status: DESIGN.
Requested next action: maintainer decision on a v0.2 contract.
```

**Triage walkthrough, stage by stage, without private context:**

| Stage | Can a maintainer do it from public info alone? | Finding |
|---|---|---|
| 0 Orientation | Yes — README, contract, and lab guide are public | Pass |
| 1 Intake | Yes — the minimal format is short and phone-friendly | Pass |
| 2 Triage | **Partially** — type is clearly "adversarial critique", but no named owner exists in the pipeline, so the submission waits on an unnamed maintainer | **Gap G1** |
| 3 Evidence audit | Yes — source is a public branch file; status DESIGN, not REPORTED | Pass |
| 4 Design challenge | Yes — the submission itself supplies a candidate rule | Pass |
| 5 Authorized development | N/A for a critique; correctly gated for code | Pass |
| 6 Independent review | **Weak** — reviewer independence is undefined: anyone who read the same PR branch shares the evidence, and the pipeline does not record reviewer exposure | **Gap G2** |
| 7 Disposition | Yes in form (ACCEPT/REVISE/REJECT/HOLD) — but no response-time expectation is stated, so a contributor cannot tell a slow queue from a dead one | **Gap G3** |
| 8 Follow-up | Yes — registry + negative ledger exist | Pass |

The dry run's conclusion: triage is *possible* without private
context, which is the pipeline's main job, but it stalls at
ownership (G1) and at honest independence labelling (G2).

## 2. Strengths (keep these)

1. **Issue #80 as the live desk is the right call.** The dedicated
   template is unmerged, and the pipeline says so plainly instead
   of sending contributors to a template that does not exist yet.
2. **The fast lane is real.** Source fixes and clear counterexamples
   explicitly do not need the experimental freeze. This is the
   single most important usability decision in the document.
3. **UNKNOWN / NOT RUN are first-class answers** in every format,
   which removes the pressure to invent evidence.
4. **Prompt-injection posture is correct in principle:** outside
   text is labelled untrusted, cannot override safety rules, and
   cannot authorise spending or execution. (See §3.4 for the one
   missing procedure.)
5. **"Merge ≠ scientific confirmation" and "shared-model agreement
   is not confirmation"** are stated in the pipeline itself, not
   buried in a footnote — this is what prevents quiet promotion of
   agreement into evidence.

## 3. Gaps and smallest fixes

### G1. No named triage owner (usability, maintainer workload)
The pipeline assigns stages to "maintainer" and "reviewer" but
names no person. On a phone-operated project, an unnamed queue is
a dead queue. **Fix (text only):** name the triage owner role and
its backup in the pipeline (e.g. "Brian, triage owner; Sol,
backup"), and state a response expectation (e.g. "acknowledged
within one week; no acknowledgement is not a rejection"). Do not
promise a decision timeline that cannot be kept.

### G2. Reviewer independence is asserted, not recorded (provenance integrity)
Stage 6 requires a reviewer "not responsible for building the
candidate", but building is not the only shared-evidence channel:
reading the same relayed digest, the same PR branch, or the same
prior reviews correlates reviewers. **Fix (text only):** add an
exposure line to every review disposition — what the reviewer read
before judging — and label shared-evidence reviews as such. This
is the same correction my design review makes for Muse/Astra/Sol.

### G3. Three submission formats compete (unnecessary complexity)
An outsider faces: (a) issue #80's minimal format, (b) the
contribution template's longer format, and (c) the lab guide's
agent-submission header — with different field names and different
status vocabularies (IDEA/DESIGN/SOURCE-ONLY vs IDEA/DESIGN/
IMPLEMENTED/TESTED-mock...). A contributor must guess which one
the maintainer wants. **Fix (text only):** make issue #80's minimal
format the single canonical format, and rewrite the other two
documents to point at it verbatim instead of restating it. Delete
no content; deduplicate the form.

### G4. No case-bank commitment scheme (provenance integrity)
The pipeline forbids publishing withheld confirmation material, but
provides no mechanism to prove later that the evaluated cases are
the frozen ones. A future dispute ("those cases were chosen after
seeing results") has no evidence either way. **Fix (text only,
implemented at freeze):** require a SHA-256 commitment of the
frozen case list (IDs + family assignments) published in the
registry at freeze time, matched by evaluation receipts. My v0.2
proposal already specifies this; the pipeline should reference it.

### G5. Prompt-injection handling has no quarantine procedure (safety)
The pipeline correctly labels outside text untrusted, but never
says what happens when a submission *contains* instructions — e.g.
a contribution that instructs the maintainer to lift a HOLD, change
a freeze, or run a command. A tired maintainer copying text into
another agent's context is the realistic attack path, not a direct
override. **Fix (text only):** add one rule — submissions containing
instructions to change scope, budget, or HOLD status are quarantined
as a separate "instruction-bearing submission" class, quoted (not
executed or forwarded as instructions), and decided on their
evidence alone.

### G6. The dedicated template's location is unverified by this audit
PR #79's body says a lightweight issue template exists, but I could
not locate its file path from the branch reads available to me
(the PR file-level diff tool was not available). **Fix:** the PR
author should state the template's exact path in the PR body, or
the claim should be softened to "template proposed, path to be
confirmed". Do not let contributors hunt for it.

### G7. Workload honesty (safety/usability)
Nine stages read as heavyweight next to the "lightweight workflow"
heading, even with the fast lane. The document already contains
its own antidote ("compare against a simpler plain-issue workflow
before adding automation"), which is good — keep it, and add one
metric the pipeline promises to track: abandoned contributions
with a stated reason, so bureaucracy has a measured cost, not just
a feared one.

## 4. What I deliberately did NOT test

- Posting to issue #80 (would be a public test claim; forbidden by
  the handoff).
- Any automation, label bot, or form enforcement (none exists, and
  the pipeline correctly refuses to add it before the plain-issue
  baseline is measured).
- Accessibility of the GitHub issue UI itself on a phone (NOT RUN;
  the minimal format is phone-friendly in text, but the platform
  UI was not tested here).

## 5. Bottom line

Approve the pipeline's *shape* (desk + fast lane + UNKNOWN-first +
merge≠confirmation). Fix G1–G5 in text before treating the pipeline
as finished, and resolve G6 by naming the template path. No new
tooling, bots, or forms are needed — and adding any before the
plain-issue baseline is measured would violate the pipeline's own
simplification rule.
