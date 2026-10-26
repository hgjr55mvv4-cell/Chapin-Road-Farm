# QUIET-GATE-01.1 — Consent integrity repair: review summary

**Version:** v0.1.1 (repair of v0.1, PR #82). **No merge. Deployment HOLD.**
**Scope:** `gate.js`, `app.js`, `gate.test.js`, new `app.test.js`,
README, receipts, manifest. No new features, no persistence, no
background processes, no external services, no design changes.

## 1. The defects (Sol source review, PR #82 comment 6406945153 — confirmed)

### Defect A — Clear left PROACTIVE active with opt-in false
**Root cause (two parts, both real):**
1. `gate.js` v0.1 `clearSyntheticState()` reset `proactiveOptIn`
   to false but left `mode` untouched, so the state machine itself
   could hold `mode = PROACTIVE, proactiveOptIn = false`.
2. `queuePrompt()` and `deliverNext()` gated only on `mode`, never
   on `proactiveOptIn`, so that inconsistent state could still
   produce prompts. `app.js` called `clearSyntheticState()` directly
   from the Clear button, and `render()` kept Simulate enabled in
   PROACTIVE mode — so the defect was reachable from the UI, not
   just theoretical.

### Defect B — Unchecking the opt-in box did not stop PROACTIVE
**Root cause:** `app.js` had no `change` handler on the opt-in
checkbox. Unchecking it changed a visual control while the state
machine remained in PROACTIVE with prompting enabled. The
always-visible Off button mitigated this, but a consent control
that can be withdrawn without effect is misleading, and consent
was represented by the interface rather than enforced by the state
machine.

**Adjacent defect found during the repair (not in Sol's comment):**
v0.1 `render()` blanket-unchecked the opt-in box whenever the mode
was not PROACTIVE. That silently cleared a fresh opt-in whenever any
other control re-rendered the page, and it meant checking the box
did not enable the Proactive button until some other render
happened. Fixed by removing the blanket uncheck and managing the
box explicitly in the mode handlers.

## 2. The repairs (smallest coherent change)

**State machine (`gate.js`):**
- `clearSyntheticState()` is now transient-only: it discards pending
  prompts, rate-limit timestamps, suppression, and counts, but does
  NOT change mode and does NOT revoke consent. Clearing data and
  revoking consent are now distinct operations, by design.
- Leaving PROACTIVE for any other mode (OFF, ON_REQUEST, or future)
  revokes consent and clears transient state. This is what makes
  revocation immediate and what prevents stale prompts reappearing
  after re-entry.
- Consent invariant enforced in code, not just UI: `queuePrompt()`
  throws `CONSENT_REQUIRED` and `deliverNext()` returns
  `CONSENT_REVOKED` when mode is PROACTIVE but opt-in is false, so
  even a hypothetical inconsistent state cannot produce a prompt.

**UI (`app.js`):**
- Clear button now calls `setMode("OFF")` (revoke + clear) and
  unchecks the box, instead of calling `clearSyntheticState()`.
- Checkbox `change` listener: unchecking while PROACTIVE switches
  to OFF immediately (pending prompts discarded by the state
  machine); checking alone only re-renders (enables the Proactive
  button) and does not enter any mode.
- ON_REQUEST handler unchecks the box, so re-entering PROACTIVE
  always needs a fresh deliberate opt-in. The always-visible Off
  button is unchanged.

**Full transition audit (post-repair):**
OFF→ON_REQUEST (no consent, no prompts possible); OFF→PROACTIVE
(requires gate opt-in + checked box); ON_REQUEST→PROACTIVE
(requires fresh opt-in; ON_REQUEST cannot queue, so nothing stale);
PROACTIVE→ON_REQUEST (revokes, discards pending, unchecks);
PROACTIVE→OFF (same); PROACTIVE→Clear (now OFF); PROACTIVE→box
unchecked (now OFF); PROACTIVE→PROACTIVE re-press (no revocation,
pending correctly preserved); reload / new instance (fresh gate,
OFF, opt-in false, nothing persisted — verified by source scan).

## 3. Testing

- Original 14 tests preserved and passing (one, "cleared on OFF and
  by explicit clear", now exercises the new transient-only meaning
  of clear and still passes).
- 8 new gate regression tests + 6 new UI-wiring tests
  (`app.test.js`, stub DOM, no browser): 28/28 passing.
- The new tests were run against the original v0.1 files from the
  branch: 6 fail on v0.1 in exactly the defect areas (both UI
  defect tests, the Clear test, the transient-clear distinction,
  the queued-revocation test, and the checkbox-enables-button
  behaviour). One additional failure in that throwaway run was a
  harness artifact (index.html/style.css not copied into the temp
  directory), not a product defect. The strengthened
  PROACTIVE→ON_REQUEST→PROACTIVE resurrection test was added after
  that run and passes on v0.1.1.
- Commands and full output: `RUN_LOG_01.1.txt`. The original
  `RUN_LOG.txt` (14-test v0.1 receipt) is preserved unchanged as
  historical evidence.

## 4. Remaining limitations (unchanged)

- Browser, iPhone/iPad, VoiceOver, keyboard-navigation, and measured
  contrast testing remain NOT RUN. The UI-wiring tests use a stub
  DOM; they prove wiring logic, not real-device behaviour.
- Passing tests do not establish accessibility or human benefit.
- The source-scan test covers named API tokens only and is not a
  general security proof (Sol's nonblocking note, agreed).
- Deployment and any H3 human-outcome claim remain HOLD.

## 5. Secondary note — MECH-INTERP-01 (PR #81), per assignment §8

No mock code was built, no v0.2 thresholds were adopted, and no
model execution was initiated. Those decisions are left for Astra's
independent review, as instructed. Brief assessment of Sol's seven
follow-up objections (comment 6406944781): **none appears
technically mistaken.** In particular, objection 4 corrects an
actual error in my MOCK_PREFLIGHT_SPEC test T7 — swapping a gold
label does not change a case-ID hash, so T7 needs a
reference-integrity signature over content + gold label + case ID +
rubric revision, not an ID-hash expectation. Objection 2 likewise
corrects my v0.2 proposal: the "report a vacant cell at weight 0"
option changes the precommitted estimand and should be removed in
favour of invalid/UNKNOWN or pre-registered replenishment before
outcomes. Objections 1 (cell exhaustiveness), 3 (content-level
commitment, not ID-only hash), 5 (floors/power at small n), 6
(control costs), and 7 (shared-evidence independence) are all
sound and consistent with the review's own direction. One
superseded item from my audit: Sol gives the dedicated template
path as `.github/ISSUE_TEMPLATE/mech-interp-research.md`, which
resolves my audit's G6 (path unverified) — the path is now known,
though the template remains inactive on the default-branch chooser
while PR #79 is draft.
