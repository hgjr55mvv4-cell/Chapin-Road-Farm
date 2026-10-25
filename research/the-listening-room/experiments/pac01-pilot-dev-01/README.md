# PAC-01-DEV-01 — Synthetic Listening Experiment Harness

Version 0.1.0. Synthetic only. $0. No real recordings, lyrics, streaming
activity, personal histories, audio, brain or physiological data, model
training, deployment, or scientific confirmation. Scientific qualification
and any real-listener execution are on HOLD.

This is an instrument for testing future theories about listening. It
does not contain a theory of consciousness, emotion, musical reward, or
personal meaning, and it must not be read as one.

## What it is

A small Python (standard library only) harness that compares two
recommendation conditions over the same synthetic catalog:

- **A1 — conversational preference baseline.** The harness does *not*
  implement the conversational system. It accepts an externally supplied
  ranking and preserves its order, catalog eligibility, stated
  preferences, version, and provenance exactly.
- **B-metadata — same context plus synthetic musical descriptors.**
  The experimental difference is explicit and auditable: in the mock
  rankers, B adds one point for a synthetic tempo within 12 BPM of a
  preferred tempo and one point for a preferred synthetic key, on top of
  the same genre-preference score A1 uses. Nothing else differs.

Both conditions use the same eligible catalog snapshot, the same stated
preferences, and comparable ranking opportunities (top-8 recommendation
lists from the mock rankers). Neither condition sees evaluation outcomes.

## Files

- `pac01_harness.py` — the harness (catalog, rankings, comparison,
  observations, sessions).
- `test_pac01_harness.py` — 36 adversarial deterministic tests.
- `demo.py` — synthetic demonstration: one successful comparison and
  one deliberately failed comparison.
- `RUN_LOG.txt` — execution receipts (Python version, commands, exit
  codes, counts, observed results).
- `MANIFEST.json` — SHA-256 hashes and byte counts for these artifacts.

## Architecture and information boundaries

```
synthetic catalog (frozen snapshot)
        |
  mock rankers (A1, B-metadata)  -- rankings are frozen as tuples
        |
  build_comparison() -- snapshot check, eligibility check, artist cap,
        shared songs stored once with both provenances, balanced pairs,
        seeded shuffle, condition-blind listener view
        |  (or INSUFFICIENT_BALANCE -- refusal, never substitution)
  Session -- observations only; outcomes never flow back into rankings
        |
  binary_summary() -- unique heard songs only; see below
```

Boundaries enforced in code, not just in documentation:

1. **Freeze before queue.** Rankings are immutable tuples. Mutating a
   caller's list after `build_ranking` cannot change the ranking, and
   recording observations cannot change a frozen ranking or queue
   (both tested).
2. **Shared recommendations are not duplicated.** A song recommended by
   both conditions appears once in the queue, with provenance
   `("A1", "B-metadata")`.
3. **Balance is structural.** The queue is shared songs plus balanced
   pairs (one A1-unique, one B-unique, in rank order). A pair is admitted
   atomically under the artist cap: if either side fails the cap, neither
   side is added. Leftovers are reported as `dropped_due_to_cap` or
   `unbalanced_remainder`, never silently replaced with unrelated songs.
   If no pair survives, `build_comparison` raises `InsufficientBalance`.
4. **Presentation is seeded and blind.** `presentation_order` is a
   `random.Random(seed)` shuffle of the queue. The same seed + inputs
   replays identically. `listener_view()` returns presentation order
   only — no condition labels.
5. **Hearing is not queue membership.** A song in the queue starts as
   `UNKNOWN`. Opening a link is not modelled as hearing at all, because
   it is not evidence of hearing. Only an explicit report with
   `heard_enough=True` can produce `KEPT_AFTER_LISTENING` or
   `PASSED_AFTER_LISTENING`; attempting either without it raises
   `ValidationError`.
6. **Absence is not a negative.** There is no historical playlist in
   this harness, and no negative label is ever derived from absence.
   `NOT_HEARD_ENOUGH`, `MAYBE`, `ALREADY_FAMILIAR`, and `UNKNOWN` are
   excluded from binary calculations, never counted as passes.
7. **Shared songs do not discriminate.** `binary_summary()` counts only
   condition-unique songs that were kept or passed after listening.
   Shared songs are reported separately. A keep rate is `None` (not
   zero) when a condition has no binary evidence.
8. **Corrections are explicit and audited.** Once a song is in a terminal
   state (`KEPT_AFTER_LISTENING`, `PASSED_AFTER_LISTENING`,
   `ALREADY_FAMILIAR`), `record()` refuses to overwrite it; `correct()`
   replaces it and the old observation remains in `history()`.
9. **Deletion is complete for session state.** `delete_session()` /
   `delete_all()` clear observations and history and block further use
   of the session (`DeletedSessionError`). The synthetic catalog is not
   listener data and is retained.

## Observation states

`KEPT_AFTER_LISTENING`, `PASSED_AFTER_LISTENING`, `MAYBE`,
`NOT_HEARD_ENOUGH`, `ALREADY_FAMILIAR`, `UNKNOWN`. Invalid states are
rejected, as are keep/pass reports without sufficient exposure, reports
for songs outside the queue, and silent overwrites of terminal states.

## Extension points (documented, not implemented as features)

The `Observation` dataclass carries four optional, explicitly reported,
never-scored fields: `passage_note` (a listener-identified passage),
`replay_desire` (True/False only if stated, else None),
`free_text_reason` (the listener's own description of why a song
matters), and `preference_change` (an explicitly stated change over
time). They are stored verbatim. The harness derives no emotion score,
meaning score, neural variable, or psychological profile from them, and
no binary count changes because of them (tested). A future integration
that collects real free text must separately address privacy and
consent; this synthetic harness does not.

The separable processes named in the assignment (immediate attraction,
anticipation/surprise, pleasure/intensity, personal association, replay
desire, lasting significance) are **not** implemented as stages, scores,
or inferred states. They are accommodated only in the minimal sense
above: a listener could voluntarily report a passage, a replay desire,
a reason, or a preference change, and the schema can hold it without
interpreting it. Adding inferred emotional or neural variables would be
a scope expansion, not a refinement of this harness.

## Fairness assumptions (read before using any output)

- The two mock rankers are placeholders. Their difference (key/tempo
  points) is a stand-in for "additional musical information", not a
  real conversational system or a real acoustic model.
- Top-8 truncation is a ranking-opportunity choice: both conditions
  return eight recommendations. A real comparison must justify its own
  truncation, and unequal truncation would break comparability.
- The per-artist cap (default 2) is a crude control. It does not
  control genre, era, tempo, or artist-network confounds — the very
  confounds the PAC-01 findings report flagged (three guardin tracks in
  six; yesterday–guardin and yesterday–Lil Xtra collaborations). A real
  comparison needs a scene-matched control design, not just this cap.
- The demo's binary counts (one kept A1-unique song, one passed
  B-unique song) are mock results over fictional recordings with
  n = 1 per condition. They demonstrate that the machinery runs. They
  are not evidence that either condition works, learns, or is superior,
  and no significance claim is made or supported.
- Condition blindness here is a property of `listener_view()` only.
  The researcher view is deliberately labelled (provenance is the
  audit trail). A real deployment would need UI-level separation so
  the listener never sees the researcher view; that is out of scope
  for this in-memory harness.

## Limitations (invariants that are NOT fully guaranteed)

- **Cross-version shuffle stability.** Seeded replay is deterministic
  within a Python version. Python's `random` shuffle algorithm is not
  guaranteed stable across major versions, so replay claims are tied
  to the Python version recorded in `RUN_LOG.txt` (3.12.3).
- **In-memory deletion only.** There is no persistence layer, log file,
  or backup in this harness, so there is nothing else to purge — but
  that also means a future deployment with logging or storage would
  need its own deletion audit. This harness does not guarantee deletion
  from systems it does not own.
- **No real blinding or consent machinery.** Simulated listeners cannot
  be deceived or consented; the harness models the data flow a real
  system would need, it does not provide it.
- **No statistical inference.** The harness reports counts and rates
  with no confidence intervals, no significance test, and no
  multiple-comparison control. Any future claim of a condition effect
  would need a separate, pre-registered analysis plan.
- **Artist cap can refuse valid science.** If the cap (or any
  eligibility rule) leaves no balanced pair, the harness refuses rather
  than weakening the design silently. That refusal is a feature, but
  it means some real catalogs will need a redesigned cap, not a
  workaround in this code.

## Independent replay

```bash
cd research/the-listening-room/experiments/pac01-pilot-dev-01
python3 -m unittest test_pac01_harness -v   # expect: 36 tests, OK
python3 demo.py                              # success + INSUFFICIENT_BALANCE
python3 - <<'EOF'
import hashlib, json, pathlib
manifest = json.loads(pathlib.Path("MANIFEST.json").read_text())
for name, entry in manifest["files"].items():
    data = pathlib.Path(name).read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry["sha256"], name
    assert len(data) == entry["bytes"], name
print("manifest verified")
EOF
```

## Relationship to other Listening Room work

This harness is independent of draft PR #72 (the Constellation Lab
review branch `agent/muse-constellation-review-01`). It does not
import, modify, merge, or depend on that branch's code, which remains
unqualified. The earlier PAC-01 findings report (recording identity and
musical evidence for six real recordings) is a separate, research-only
deliverable; no real recording, artist, title, or listener data from it
appears in the synthetic catalog here. All artists, titles, keys, and
tempos in `demo_catalog()` are fictional.
