# Muse Constellation Lab v0.2 — Independent Engineering Contribution
## TLR-R2-MUSE-AGENT-01

**Author: Muse, the newly available separate Muse app. NOT Meta AI.**
Historical work previously called "Muse" was produced by Meta AI.
This package does not take credit for it, does not copy it, and
does not claim to audit a verified GitHub package of it.

**Scope: synthetic only. No real listener data, no audio, no
copyrighted recordings or lyrics, no model training, no
deployment, no public intake, no live services. Budget: $0.**

## What was actually executed, by whom

- Executor: Muse (this app), on a Linux VM with Python 3.12.3
  (stdlib only, offline), and GitHub access via the Muse
  GitHub connector (GitHub App, not a personal token).
- GitHub identity verified via `get_me`: login
  `hgjr55mvv4-cell`, id 246049396.
- Repository: `hgjr55mvv4-cell/Chapin-Road-Farm`
- Base branch: `research/listening-room-round02`
- Base commit (head of that branch at check time, 2026-10-25):
  `d1493efcf15e115aaef25d2b2d6701e0b69cca90`
  ("docs(tlr): new Muse agent independent GitHub/VM
  engineering and draft PR assignment", 2026-10-25T12:53:38Z)
- The draft PR, if created, targets that branch, from
  `agent/muse-constellation-review-01`, with files under
  `research/the-listening-room/experiments/muse-agent-01/`.
  Nothing is pushed to `main`, nothing is merged, Claude's
  unfinished application is not altered, the v0.1 contract
  is not changed in place.

## Source provenance — read this first

**SOURCE UNAVAILABLE for Meta AI's Constellation Lab v0.1 as a
verified GitHub source package.**

- `research/the-listening-room/constellation_lab.py` on
  `research/listening-room-round02`: **NOT PRESENT** — the
  connector returned "Failed to get file contents. The path
  does not point to a file or directory, or the file does
  not exist in the repository."
- `research/the-listening-room/test_constellation_lab.py`:
  **NOT PRESENT** — same connector error.
- Repo-scoped code search for `constellation_lab` in
  `hgjr55mvv4-cell/Chapin-Road-Farm` returned
  `total_count: 0` (with `incomplete_results: true`, so the
  search alone is not proof; the two get_file_contents
  failures and the staging-tree listing are the primary
  evidence).

Therefore this package is **not** an original-source audit.
The adversarial probes in §C below were run against the
conversation-supplied local copy in `~/workspace/listening-room/`
(the pasted Meta AI code from the original chat, as reported
in the prior round). That copy is described only as
"conversation-supplied, provenance unverified", never as a
verified GitHub package. No code from that copy was pasted
into `muse_lab.py`.

### §3 reading list, as checked 2026-10-25 via the connector

Paths are under `research/the-listening-room/` unless noted.
"PARTIAL" means a head excerpt was verified via the connector
in this run; the full text was not read in this run.
"FULLY READ" for the contract/schema/example/META-AI prompt
rests on the prior round's full browser read, confirmed by
a matching connector excerpt in this run.

| File | Status | MCP-reported SHA (first bytes) |
|---|---|---|
| `prompts/NEW-MUSE-AGENT-01.md` | FULLY READ | 413d8839805c11a44b4ebdcef1e0ce383da8d2f1 |
| `prompts/META-AI-ROUND-02.md` | FULLY READ (prior round) | — |
| `docs/CONTRIBUTION-CONTRACT-v0.1.md` | FULLY READ (prior round) | 647ce5c50b7fbd9f1dce1d91735a6bd22d148328 |
| `schemas/listening-contribution.schema.json` | FULLY READ (prior round) | — |
| `examples/synthetic-contribution.json` | FULLY READ (prior round) | — |
| `README.md` (research staging) | PARTIAL | 5aa2d568be245a38333a551295546ee1425d7f05 |
| `CONTRIBUTING.md` | PARTIAL | 777c36ad302375425c352d5286e8bca0ba27f78f |
| `docs/ROUND-02-PLAN.md` | PARTIAL | c220cc1b7be2bbc6596c67916e76a43f6d8df9e4 |
| `docs/MODEL-ATTRIBUTION-CORRECTION-2026-10-25.md` | PARTIAL | dcfa33d8b503436a316236230927bb71bb1db8bf |
| `docs/MUSE-REVIEW-01.md` (author: Meta AI, historically named) | PARTIAL | f2d338764ef950a1cda287af4aaf1a3b36f8ea35 |
| `docs/GROK-REVIEW-02.md` | PARTIAL | 615c101c623fa61d19084268300f2320e4e0ac40 |
| `docs/DEEPSEEK-DEV-AUDIT-01.md` | PARTIAL | 0afe77afdf73b920c673e3968d557a1a0b1892dc |
| `prompts/DEEPSEEK-ROUND-02.md` | PARTIAL | 7f093ff7f19c8bccac65c54b3e6d538389d788c2 |
| `constellation_lab.py` | NOT PRESENT at checked location | — |
| `test_constellation_lab.py` | NOT PRESENT at checked location | — |

Repo-root `README.md` / `CONTRIBUTING.md` were not separately
checked; do not assume they are the same as the research
staging files above.

## How to run (exact commands)

```bash
python3 -m unittest test_muse_lab -v
python3 muse_lab.py
```

Environment: Python 3.12.3, stdlib only, no network, no
packages. Seeds are fixed in code; `run_experiments()` uses
seeds (1, 2, 3, 4, 5) by default. Unit of evidence: SESSION
for next-pick, CORRECTION EVENT for replacements, LISTENER
for aggregation. Holdout splits are chronological by session.
Results are reported as mean, min, max, and approximate 95%
CI (mean ± 1.96 × SE, SE from the per-listener means), not
as a single seed.

## Defects reproduced, static risks, unverified concerns

### Reproduced (executed against the conversation-supplied copy)

1. **Unhashable playlist members crash the validator.**
   `playlist.song_ids = [{"song_id": "s1"}]` or `[["s1"]]`
   raised `TypeError: unhashable type: 'dict'/'list'` from
   `set(ids)`. A fail-closed validator must return an error,
   not crash. Fixed in `muse_lab.py`: IDs are checked to be
   strings before any set operation.
2. **Generator sessions become empty sessions.**
   `add_session("g1", generator)` stored
   `frozenset()` — the generator was consumed by the first
   iteration, and the stored session was silently empty.
   Fixed: iterables are materialised exactly once, validated,
   then stored.
3. **Corrections accept arbitrary session IDs.**
   `add_correction("A", "B", "nonexistent-session-999")`
   was accepted with no check against known sessions.
   Fixed: session-scoped corrections must reference a known
   session, or be explicitly session-less (`session_id=None`).
4. **Session-local suppression described, not implemented.**
   After `add_correction("A", "C", "s1")`, the co-occurrence
   ranker for seed `[B]` still returned `['A', 'C']` — `A`
   was not suppressed for session `s1`, because rankers
   took no session context. Fixed: `recommend(..., session_id)`
   excludes that session's session-local rejected tracks,
   while the global ranking does not (testably different).
5. **Audio-claim gate recognises only a narrow set.**
   `{"type": "acoustic_observation", "authorized_audio": True}`
   returned **no errors** in the conversation-supplied copy,
   while `audio_observation` was rejected. Fixed: any claim
   type or field name indicating an audio/acoustic/spectral/
   embedding measurement is rejected at Stage 0, regardless
   of `authorized_audio`. Free-text listener words are NOT
   scanned — only claim types and field names — so a listener
   saying "tempo" in their own words is not censored.

### NOT a defect (checked, held up)

- Partial mutation on a bad session: adding a session with
  an unknown track raised before appending, leaving the
  prior state unchanged. Muse's implementation preserves
  this and extends it to corrections (snapshot-tested).

### Static risks (code inspection, not executed as failures)

- Metadata-permutation / association-invariance tests in the
  conversation-supplied copy are partly tautological: its
  rankers take no metadata parameter, so permuting metadata
  cannot change their output. Muse's version labels the
  equivalent test as a structural property in its docstring,
  not as behavioural evidence of blindness.
- Single-seed reporting with population SD and no CI in the
  prior report is not, by itself, a code defect, but it is
  insufficient for a generalisation claim. Muse reports
  multi-seed means with CIs (see RUN_LOG.txt).

### Unverified concerns (do not assert)

- Whether the conversation-supplied local copy is byte-identical
  to Meta AI's original pasted code: **UNKNOWN**. No hash of
  an original source package was available to compare against.
- DeepSeek's reported flaws in the assignment (§4) were not
  independently verified here; they are reported, not reproduced.
- Nothing here says anything about real listeners, real audio,
  or recommendation quality in production. All numbers are
  about recovering constructed synthetic regularity.

## What Muse's implementation does (P0–P3)

- **P0 fail-closed validator + Stage-0 gate:** synthetic-only,
  `research_use`/`public_release`/`model_training` all false,
  malformed types, duplicates, missing references, nested
  unhashable values, illegal enums, ambiguous recording
  versions (same title+artist, unverified identity), corrections
  to nonexistent sessions/IDs, hostile text (accepted as text,
  never used as a trait, never used in ranking). Invalid input
  fails gracefully with an error list (validator) or a
  ValueError before any mutation (state methods). No partial
  mutation.
- **P1 correction/privacy semantics:** temporary *not tonight*
  (session-local suppression, revoked by the session ending,
  not by a global veto) vs durable *never* (global veto,
  blocks every ranker until explicitly revoked). Silence and
  click-outs are recorded as events only; they never count as
  preference and never change a ranking. Deletion
  (`delete_all`) clears sessions, corrections, vetoes, reports,
  suppressions, and the edge ledger; derived counts are
  computed from current state only, so after deletion they are
  zero — there is no separate cache or append-only log
  retaining personal text in this implementation. What cannot
  be erased externally: any copy a reviewer has already made
  of a draft PR, and GitHub's own retention of a PR/commit
  once published — that is stated here, not hidden.
- **P2 recommendation integrity:** baselines are session
  popularity, global rejected-agnostic replacement popularity,
  shuffled sessions (duplicate-free swaps, preserving sizes
  and per-ID counts), shuffled correction pairs (preserving
  marginal counts, derangement repair, raises rather than
  silently dropping an unrepairable correction), matched
  decoys (via the A1 tag-shuffle control), and — crucially —
  an alternative generative world with **no stable constellations**
  (see Idea 1). Held-out sessions, chronological splits,
  multiple seeds, no test-to-train leakage (train/test
  session IDs are disjoint by construction), per-listener
  aggregation, and NOT EVALUABLE where a metric cannot
  discriminate (see the abstention design below).
- **Abstention, not forced ranking:** `recommend()` returns
  only candidates with provenance > 0. Everything else is
  listed separately as "no provenance — not recommended".
  If that list is empty, `abstain=True` and no popularity or
  ID-order list is presented as a recommendation. A forced
  ranking with zero evidence would be fabrication.
- **P3 constrained A1 (explicit preferences):** `a1_explicit_ranker`
  uses ONLY explicitly stated user tokens, negative constraints,
  and curator tags (metadata, explicitly NOT audio evidence).
  It CAN propose unseen songs, which provenance cannot — that
  is a capability difference, not a same-information win, and
  it is scored separately, never mixed with provenance scores.
  When each can propose an unseen song: A1 can, whenever the
  track carries a curator tag matching an explicit token and
  is not vetoed/negatively constrained; provenance can never
  propose a song with zero co-occurrence or correction-pair
  history. User-reported meaning (their words) is kept separate
  from inferred audio (which is never inferred here at all).

## Synthetic results (seeds 1–5, full log in RUN_LOG.txt)

| Experiment | Result |
|---|---|
| Next-pick Hit@3, stable world, 60 listeners (12/seed) | popularity 0.327, provenance **0.878**, shuffled-session control 0.348 |
| Replacement Hit@1, stable world | session popularity 0.008, global replacement 0.233, pair-specific **0.718** |
| Idea 1, random world Hit@3, 30 listeners | popularity 0.263, provenance 0.260 — provenance does NOT beat popularity |
| Idea 2, context world Recall@3, 30 listeners | blind 0.412, conditioned 0.411 — conditioned does NOT reliably beat blind |
| Idea 2, stable world Recall@3 (control) | blind 0.409, conditioned 0.409 — identical, as expected |

Interpretation, plainly: provenance recovers constructed
stable regularity well, and pair-specific replacement beats
global replacement, on synthetic data only. The two original
ideas are where the interesting results are, and one of them
fails — see below. None of this is evidence about real listeners.

## Two original hypothesis cards

### Card 1 — No-constellation null world (Idea 1, SUPPORTED as a control)

- **Hypothesis:** If sessions are random (no stable
  constellations), an ID-only provenance ranker must NOT
  beat popularity, and must NOT invent constellations.
- **Incumbent:** Reporting only stable-world wins, which
  cannot distinguish "recovers real structure" from
  "finds structure in noise".
- **Challenger:** A random-world control, run with the same
  rankers, seeds, and metrics as the stable world.
- **Controlled information:** Same catalogue, same session
  sizes, same train/test split; only the generative process
  changes (random sampling vs stable constellations).
- **Eligible cases:** Synthetic listeners only; no real data.
- **Negative control:** The random world itself.
- **Success metric:** Provenance Hit@3 minus popularity Hit@3
  in the random world, across seeds.
- **Falsifier:** If provenance beats popularity by more than
  0.15 in the random world, the ranker is inventing structure
  and the stable-world win is suspect.
- **Result:** Difference = −0.003 (0.260 vs 0.263). Control holds.
- **Privacy/effort cost:** Zero additional; same synthetic code.
- **What synthetic evidence cannot prove:** That real
  listeners have, or lack, stable constellations. This control
  only guards against inventing them from noise.

### Card 2 — Context-split edge ledger (Idea 2, NOT SUPPORTED in naive form)

- **Hypothesis:** A context-conditioned provenance ranker
  (only sessions from the queried context) beats a
  context-blind ranker on context-dependent listeners, and
  does not beat it on stable listeners.
- **Incumbent:** Context-blind provenance (all sessions).
- **Challenger:** Hard-filter context conditioning, with a
  typed edge ledger separating kept-together / replaced /
  not-tonight / never, each carrying a session context label.
  Both rankers receive the same context label; blind ignores
  it, so the comparison is about use, not access.
- **Controlled information:** Same sessions, same seeds;
  only the ranking filter changes.
- **Eligible cases:** Synthetic context-dependent listeners
  with overlapping constellations (4 shared tracks), where
  the seed alone cannot disambiguate context. An earlier
  disjoint-constellation version was discarded after it
  failed with blind == conditioned — the seed already
  identified the context, so conditioning added nothing.
- **Negative control:** Stable listeners (context labels None),
  where conditioned must equal blind.
- **Success metric:** Recall@3 (Hit@3 saturates for ambiguous
  seeds — a blind ranker almost always gets at least one true
  co-member in the top 3, even when mixing contexts).
- **Falsifier:** Conditioned Recall@3 must exceed blind by a
  clear margin on context listeners, and equal blind on stable
  listeners. A single-seed win does not count.
- **Result: NOT SUPPORTED.** Across seeds 1–5, conditioned
  0.411 vs blind 0.412 (CIs overlapping); stable control
  0.409 vs 0.409, as expected. A single-seed run (seed 7)
  showed a conditioned win by chance — which is exactly why
  multi-seed reporting matters.
- **Why it plausibly fails:** Conditioning halves the training
  data (one context only), increasing variance, while blind
  already benefits from overlap tracks, which are often in
  the truth set. The naive hard filter trades data for
  specificity and loses.
- **Revised direction (not claimed as proven):** Partial
  pooling — blend blind and conditioned scores, or condition
  only when per-context sample size is sufficient and the
  seed is ambiguous across contexts. That is the next
  falsifiable test, not a conclusion.
- **Privacy/effort cost:** Context labels are session
  metadata the listener already supplied; no new data
  collection, no intrusiveness beyond what the session
  already records. Treating past preference as immutable is
  avoided by construction: a "not tonight" edge is
  session-local, and a context-specific edge does not
  generalise to other contexts unless it persists there.
- **What synthetic evidence cannot prove:** That real
  listeners' preferences are context-dependent in this way,
  or that context labels in real use would be accurate.

## Files in this package

- `muse_lab.py` — independent implementation (validator,
  claim gate, state, edge ledger, rankers, A1, synthetic
  worlds, multi-seed experiments).
- `test_muse_lab.py` — 27 tests, all passing (see RUN_LOG
  header for the exact run).
- `RUN_LOG.txt` — exact experiment output, seeds 1–5.
- `MANIFEST.json` — SHA-256 checksums for the files above.
- `README.md` — this file.

## Security / privacy / Stage-0 limitations

- Stage 0: no audio observation is permitted from tags,
  words, embeddings, or a self-asserted `authorized_audio`
  flag. The gate checks claim types and field names, not
  free text, and not the meaning of a listener's words.
- No secrets, credentials, real histories, third-party data,
  copyrighted recordings/lyrics, telemetry, or network calls
  in any committed file. All tracks are invented (`T01`–`T30`,
  "Invented Track NN", "Invented Artist N").
- A draft PR on a public repository is public. Do not use it
  as an intake channel for real listening data. Any copy of
  a published commit is outside this implementation's ability
  to erase.
- If GitHub write access had been unavailable, this package
  was to be returned as a ZIP/patch with checksums instead.
  GitHub access was available (see final report), so the
  draft PR path is used; the local tree here is the same
  content, checksummed in MANIFEST.json.

## Decision

**GO FOR INDEPENDENT ENGINEERING REVIEW** — synthetic only.
The repaired P0/P1 behaviour is testable and passing, the
stable-world synthetic results are consistent with the prior
report's direction (without claiming replication of its
unverified source), and both original ideas were run to a
conclusion, including one negative result. This is not a
claim about real listeners, real audio, or production
recommendation quality, and it must not be promoted as one.
