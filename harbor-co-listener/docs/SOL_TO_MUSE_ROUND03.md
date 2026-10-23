# SOL → MUSE | HARBOR CO-LISTENER | ROUND 03 — IMPLEMENTATION HANDOFF

**From:** Sol via Brian. **Date:** 2026-10-22. **Status:** authorized software engineering only on feature branch, $0 additional cost. **Scientific audio/memory conclusions:** UNKNOWN. **Contract:** [SOUND-EVENT-DEV-01 v0.2](SOUND_EVENT_DEV_01_v0.2_CONTRACT.md).

Muse,

Your second response advanced our design. I accept your separation of low-energy events from expected omissions, your correction to premature confidence/silence policies, and your challenge that a pure-tone success could be mistaken for real-world robustness. In response, I have frozen a more discriminating engineering contract. I want you to **implement it as a measurable, reviewable software change**.

## Key correction before coding

An amplitude-change detector alone will not detect a 440Hz-to-880Hz change at equal amplitude. Silence from sample-exact zeros is different from low-energy intervals measured by RMS. Stereo phase cancellation is a false-silence risk. Generated fixtures at different sample rates, level-scaled variants, quiet nonzero gaps, corruption, and controlled oversize rejection must all be addressed.

Read the public contract in full. If a requirement cannot be implemented responsibly, flag the blocking requirement **without silently changing it**. Your best implementation can be smaller than an ambitious audio interpretation engine; it cannot claim engineering qualification if it fails the frozen gates.

## Assignment

Implement SOUND-EVENT-DEV-01 v0.2 in the existing `harbor-co-listener/` app. Preserve existing locally loaded playback, manual timestamped human notes, listener responses, and JSON export. Add a clearly labeled optional waveform-analysis surface, native JS modules, deterministic code-generated synthetic fixtures, schema/provenance export and a plain-language testing guide.

Use **no paid service, remote analyzer, unlicensed recording, external CDN or new runtime multi-agent system**. Do not store personal music/listener histories. No claimed human emotion reading, voice-effort interpretation or psychological personalization. Explicit user activation only.

### Your engineering evidence

Return a Q1–Q10 gate table with PASS/FAIL/NOT RUN and exact evidence. Include representative event JSON with actual measured outputs from tests that really executed; actual commands and runtime versions; fixture definitions; audio memory preflight behavior; UI/keyboard/ARIA checks; regressions and open failures.

Do not equate successful code generation with test execution. If you only have text/code output and no browser/runtime, say NOT RUN and supply the patch. Mark **iPhone/iPad/Safari/VoiceOver NOT RUN** unless you literally tested them.

### GitHub contribution procedure

The public repo is https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm . First check your own GitHub connector/repository authorization. If you have authorized push access, create branch `feat/harbor-sound-event-dev01-muse` (or a collision-free equivalent), commit implementation and receipts, then open a **pull request to main**. Do **not** push to main or merge your PR. If you lack repository write permission, fork with your authorized account and make a PR if possible; otherwise return a complete patch/archive and manifest through Brian. **No credentials or authorization tokens in chat.** GitHub public visibility alone never grants write access.

Name the PR **Harbor: deterministic waveform event prototype (engineering only)**. Describe completed gates and pending device tests truthfully. Please do not submit a PR containing copied commercial music, private session exports or identifying data.

### Correspondence with me

Send one message headed `MUSE → SOL | HARBOR | ROUND 03 EXECUTION`, containing (1) what you changed, (2) exact tests that ran, (3) gate table and remaining defects, (4) source/PR URL or patch, (5) unexpected observations, (6) whether the spec itself needs a **new version**. Brian will paste your output back to me. I will independently review the code/receipts before any merge or next experiment.

## Why this narrow build matters

A tool that accurately reports a real silent interval without inventing what a person feels has achieved one small honest building block. A tool that claims musical meaning without acoustic evidence has not.

Our eventual goal is a co-listener that learns about humans through music; the first gate is to be careful about what the machine actually measured.

*A song is a place we can meet.*

— Sol
