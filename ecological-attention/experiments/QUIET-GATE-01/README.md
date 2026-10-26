# QUIET-GATE-01 — Quiet-first interaction demo

**Status:** DEV prototype only. Interface mechanics, not an H3 study.
**Budget:** $0 additional. No dependencies. No paid infrastructure.
**Deployment:** HOLD. Not a safety system. Not for field use.

## 0.1.1 Consent-integrity repair (v0.1.1, PR #82 update)

Sol's source review found two consent defects in v0.1, both
confirmed and repaired (see `REVIEW_SUMMARY_01.1.md` for the full
account):

- **Defect A:** Clear left mode PROACTIVE with opt-in false, and
  queue/deliver checked mode only — so prompts could resume after
  consent was cleared. **Fix:** the Clear button now returns the
  system to OFF and revokes consent; `clearSyntheticState()` is
  transient-only (data, not consent); queue/deliver now require
  currently valid opt-in (`CONSENT_REQUIRED` / `CONSENT_REVOKED`).
- **Defect B:** unchecking the opt-in box while PROACTIVE did
  nothing. **Fix:** unchecking immediately switches to OFF and
  discards pending prompts; re-entry needs a fresh opt-in.
- **Invariant (enforced in `gate.js`, not just the UI):** no
  simulated proactive prompt may be queued or delivered without
  currently valid proactive opt-in; leaving PROACTIVE for any mode
  revokes consent and discards pending prompts, so stale prompts
  can never reappear after re-entry.
- **Tests:** original 14 preserved + 8 gate regressions + 6
  UI-wiring tests (`app.test.js`, stub DOM) = **28/28 passing**.
  Original receipt `RUN_LOG.txt` preserved; new receipt
  `RUN_LOG_01.1.txt`. Browser/VoiceOver/real-device checks remain
  NOT RUN (see §3).

## 0. Pre-build assessment: GO, minimal only (independent judgment, not compliance)

The assignment asked whether this component helps answer the earlier
engineering questions, and whether to recommend NO-GO. Assessment:

- **It answers a narrow mechanics question, not the human question.**
  It proves, in testable code, that silence can be a default with
  teeth: OFF clears pending prompts, nothing reactivates on reload,
  proactive prompts need a deliberate opt-in, and a rate cap is
  enforced at its boundary. That is worth building because those
  guarantees are easy to claim in prose and easy to break in code.
- **It does not prejudice H3 if it stays labelled mechanics-only.**
  It recruits nobody, measures nobody, and must not be used as an H3
  stimulus or outcome without a separately approved protocol. The
  page banner and this README say so explicitly.
- **It does not duplicate a trivial toggle.** Mode buttons are common;
  the contribution is the enforced state machine behind them (opt-in
  required in code, not just in the UI; OFF overriding pending work;
  suppression and rate limits as state, not decoration).
- **NO-GO conditions checked, none triggered** (per issue #77): OFF
  is implemented without retained capture; quiet mode has no
  unsolicited prompts; the prototype requires no monitoring of
  anyone's activity.
- **Strongest criticism:** even a fictional demo prompt trains
  attention toward system-legible events — the same
  measurement-changes-attention problem raised in
  GREEN-ATTENTION-RECONCILIATION-02. This demo cannot show that
  quiet helps a person notice more; it can only show that the gate
  behaves as specified. Any claim beyond that would be false.

## 1. What was built

| File | Purpose |
|---|---|
| `index.html` | Mobile-first page, no external resources. Open it directly; it needs no server. |
| `style.css` | Large type (19px), high contrast, 48px minimum targets, visible focus, no animation, reduced-motion rule. |
| `gate.js` | Separately testable deterministic state machine. No DOM, no network, no storage, no timers. Usable in Node and in the browser. |
| `fixtures.js` | Four offline fictional scenarios. Every one is labelled fictional/invented. |
| `app.js` | Wires page buttons to `gate.js`. No records of its own. Its only clock is simulated and moves only via the "Advance simulated time" button. |
| `gate.test.js` | 14 adversarial unit tests (Node test runner, stdlib only). |

### Modes

- **OFF (default on every fresh start and every reload).** No sensing,
  event processing, telemetry, recording, activity history, or
  automatic prompting. The OFF choice is not logged per person —
  there is no per-person log anywhere in this code. Switching to OFF
  clears pending prompts, prompt timestamps, suppression, and the
  proactive opt-in, immediately.
- **ON_REQUEST.** The user may press "Ask for a reflection" and get a
  fictional scenario in return. Nothing is ever offered unprompted.
  A request answer is not counted against the proactive rate limit.
- **PROACTIVE_DEMO.** Requires two deliberate acts: checking the
  opt-in box *and* pressing the Proactive button; `gate.js` itself
  rejects `setMode("PROACTIVE")` without `{ optIn: true }`.
  Simulated prompts only, capped at 3 per simulated hour, with a
  Suppress button, a pending-queue limit of 5, and an always-visible
  Off button. It never silently reactivates: a reload creates a fresh
  gate, which is OFF.

### Rate limit and clock

The cap is 3 delivered simulated prompts per 60 simulated minutes.
The demo clock starts at zero and advances only when the user presses
"Advance simulated time by 15 minutes". This is deliberate: it makes
the demo deterministic and proves no real-time background process is
running. A real deployment would need a separate, reviewed decision
about real clocks — this prototype makes no such claim.

## 2. What was actually tested

Command: `node --test gate.test.js` — Node v24.22.1, 14 tests, 14 pass.
See RUN_LOG.txt for the full output. Covered:

- Fresh start is OFF; a new gate object is OFF (reload-equivalent,
  since no state persists).
- PROACTIVE without opt-in throws and leaves mode unchanged.
- Switching to OFF from ON_REQUEST and from PROACTIVE clears pending
  prompts; nothing is delivered afterwards.
- ON_REQUEST never queues or delivers a spontaneous prompt.
- Rate limit enforced exactly at the boundary (3 delivered, 4th
  blocked with reason RATE_LIMIT) and recovers after the window passes.
- Invalid transitions (unknown mode, request/suppress/queue while OFF,
  suppress while ON_REQUEST) throw with a `code` and leave state
  unchanged.
- In-memory synthetic state cleared on OFF and by explicit clear.
- Suppression blocks delivery; unsuppression restores it.
- Pending prompts deliver first-in, first-out; a full queue drops
  further prompts instead of overflowing.
- Explicit requests are deterministic and cycle through the fixtures.
- Every fixture is labelled fictional/invented.
- Production source contains no persistent-storage, network, or
  device-sensing calls, and the page references no external URL
  (source-level scan; see §3 for its limits).

## 3. NOT RUN — recorded, not assumed absent

Passing unit tests does **not** prove real-device accessibility or
that a human's attention is improved. The following were NOT RUN:

- Real-browser rendering (Safari on iPhone/iPad), real touch targets,
  real keyboard focus order — no browser test harness was run here.
- Screen-reader behaviour (VoiceOver or any other reader).
- Measured colour-contrast ratios (values were chosen for contrast
  but not measured with a tool).
- Any human study, attention outcome, interruption-burden measure,
  ecological utility, or safety assessment. None is claimed.

These are accessibility and human-outcome gaps to close before any
use beyond a code review, not items to wave through.

## 4. Unresolved risks

1. **Misreading as a safety system.** The banner mitigates this; it
   does not eliminate it. Anyone reusing this demo must keep the
   "SIMULATED DEMO ONLY — not a safety system" banner and the
   fictional labels, or remove the demo.
2. **Simulated time is not real time.** The rate cap, as shipped,
   cannot protect anyone in real time. Do not port it to a live
   system without a reviewed real-clock and persistence design —
   which would itself reopen the retention questions this prototype
   deliberately avoids.
3. **Opt-in in the UI vs. in code.** Both layers enforce opt-in, but
   a future UI change could hide the checkbox while keeping the code
   check. Reviewers should re-check both layers after any UI edit.
4. **Attention priming.** Even fictional prompts may train attention
   toward countable events. That is a research question for H3, not
   something this demo resolves.
5. **Accessibility unproven.** See §3. The design choices (native
   buttons, `aria-pressed`, `aria-live="polite"`, no autofocus theft,
   large targets) are intentions, not verified outcomes.

## 5. Licence and reuse — pending, not granted

The repository's public visibility does **not** establish an
open-source licence. No licence is claimed for this code. Any reuse
permission is **pending Brian's approval**. Dependencies: none —
the demo uses only plain HTML/CSS/JavaScript, and the tests use only
the Node.js standard library — so there are no third-party rights to
verify for this package. Do not copy third-party libraries or assets
into this directory without checking their rights first.

## 6. Out of scope, by design

No participants, no real environmental recordings, no automatic
wildlife detection, no physical safety alerts, no farm-equipment
control, no treatment hardware, no cloud-model calls, no analytics,
no camera, microphone, or geolocation, no background data
collection, no integration with the VFM or The Listening Room.
