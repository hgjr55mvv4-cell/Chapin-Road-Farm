# TLR-R2 DeepSeek DEV-00 — Independent replay and audit (2026-10-25)

**Status:** synthetic engineering diagnostics only; no scientific confirmation, audio, real listeners or intake.

I transcribed the complete Python listing in the user-pasted DeepSeek report into a local file and executed it using Python 3. This was **not** an original source package, so byte-level reproduction of DeepSeek's artifact remains UNKNOWN. The reproduced code exited 0 and reported **14/14**, contradicting the report's expected **15/15**.

Additional adversarial executions against that transcription:
- Set `track.identity_status` to `flying`: `validate` returned **no errors**.
- Mark track and recording verified, and set `authorized_audio=True`, without supplying any actual audio evidence: `claim_admissible(audio_observation)` returned **(True, "stage1 admitted")**. This is an unsafe admission bypass.
- Reference non-existent `s404` through `meaning_links`: validator returned **no errors**.
- B-structured adds empty entities/relations; `score` ignores that structure. No meaningful representation comparison is implemented.
- Correction targeting a nonexistent event is silently ignored in the effective state.
- A `declined` reason can coexist with retained human text. The reported refusal test checks only whether the word `personality` occurs in raw JSON.

Other issues for review: no tested deletion/export, no cycle detection, no enforceable audio receipts, no audio rights/provenance support, and potential meaning-information leakage through A1's `set_cohesion` boolean derived from `connection_in_own_words`.

**Adjudication: REVISE** before any engineering qualification. P0: Stage 0 must reject *all* acoustic claims, regardless of self-asserted flags; no Stage 1 unlock is authorized. Tests must challenge the invariants, not merely assert literals or build a fixture that guarantees the expected result.

Original DeepSeek source: present only as a user-pasted message; locally transcribed replay available to Brian from the current chat session, not automatically accessible in another model's environment. Do not treat 14/14 as a quality floor or as an original-source receipt.

Scientific collection, deployment, real audio analysis and model training remain HOLD.