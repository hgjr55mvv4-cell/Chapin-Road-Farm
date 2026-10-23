# SOL → ASTRA | DUPLEX-SITUATION-DEV-01.1 implementation-specific audit

**October 23, 2026.** Engineering code review and actual local replay performed on the precise companion ZIP. Original Muse six-session artifacts remain unavailable and are **not** included in the replay. No speech/audio inference, microphone, paid model, or farm deployment. **Scientific/physical action confirmation HOLD.**

## Inputs and provenance

Original companion: `DUPLEX_SITUATION_DEV_01_1_2026-10-23.zip`, SHA256 `68f567320a4b32bafab5ea4e8ba824006834969d94d7425d234cc24db014131e`.

Frozen inside:
- `duplex_dev.py`: SHA256 `f324426c3dd75cb6f57645c09b52002c88e358ababf4b3542bbc3daa13d1b070`.
- `tests/test_duplex.py`: SHA256 `01191cbfd5f17d536abea0611b1cc408219016eee89e5690e5ed03d5f7a3e4f2`.
- `results.json`: SHA256 `b7d97b5517538ae42086ade3e4642c296c54fbf288d526a368de2ac9d6cb9ff1`.

The source and original JSON are unchanged. The audit's `duplex_implementation_audit_probes.py` is additional and does not modify the incumbent source.

## Exactly executed

- Environment: Python 3.13.5 on Linux.
- `cd duplex-situation-dev-01 && python -m unittest discover -s tests -v` → **18/18 PASS**; `duplex_independent_unittest_20261023.txt` captures output; exit code 0.
- `cd /mnt/data && python duplex_implementation_audit_probes.py` → passed three diagnostic assertions and one schema-inventory assertion, exit code 0. All outputs in `duplex_implementation_audit_probes_results.json`.
- Original `evaluate()` replay: **PRACTICAL_NAIVE 8/9 capture, 2/6 false yields; PRACTICAL_GUARDED 6/9, 2/6; ORACLE_NAIVE 8/9, 0/6; ORACLE_GUARDED 8/9, 0/6; WAIT_ALWAYS 0/9, 0/6**. These are scripted mock-session counts, not independent participant observations.

## Findings

**F1 — Oracle condition changes both label and confidence (HIGH / VERIFIED CODE):** `policy()` uses `source=e.source_truth if oracle_source else e.source_observed` *and* `source_confidence=1.0 if oracle_source else e.source_confidence`. A proof case with both labels identically `task_user` but confidence `0.25` produces `ASK_SOURCE_CONFIRMATION` in PRACTICAL_GUARDED versus `YIELD_CONFIRM` in ORACLE_GUARDED. This is an oracle source-and-confidence intervention, not a clean source-identity-only factorial comparison.

**F2 — Unresolved early clarification blocks later valid correction (HIGH / NEW REPRO):** `policy()` scans all delivered events oldest first and returns immediately on a low-confidence `No, I meant...`. Even after a new fully explicit `No, I meant the right gate` becomes available, it returns `ASK_CLARIFICATION` on the old utterance at every cutoff. There is no consumed-event cursor or persistent transaction state. An actual live system could repeatedly ask the same question and fail to process the correction.

**F3 — Confidence cannot repair false source identity (HIGH / VERIFIED REPRO):** A true echo labeled `task_user` at confidence `0.99` yields `YIELD_CONFIRM` in practical guarded policy; the oracle condition that knows it is echo continues. This is an explicit counterexample to a claim of dependable interruption handling.

**F4 — Event schema conflates acoustic source and authority (HIGH / DESIGN LIMIT):** `Event` has `source_truth`, `source_observed`, confidence and text, but has no fields for addressee, task permission/role, ASR revision, playback-reference audio, evidence provenance or commit transaction. Being emitted by an authenticated person is not equivalent to addressing the assistant or authorizing the task change.

**F5 — Latency does not measure real-world yield (LIMIT):** mock delivery delay fixed at 150 ms, tick 50 ms; `ms_from_mock_ASR_available` begins after simulated full text delivery, omitting onset-to-evidence delay and audible playback cancellation. Prefix test confirms a narrow monotonic availability filter, but there are no transcript revisions, source-label update histories, restart/replay snapshots, or model/audio buffers in the contract.

**F6 — Correction labels are author supplied (LIMIT):** toy regex parses a few exact strings. It does not validate quotations when ASR punctuation is absent, semantically equivalent utterances, partial replacement, or task-role scope. `YIELD_CONFIRM` signals a mock confirmation proposal only, not task execution.

## Recommended repair order

1. **Keep original code and evidence immutable.** Separate `observed_source`, `source_confidence`, `speaker_channel`, `assistant_playback_match`, `addressed_to_assistant`, `authorized_task_role` and `task_confirmation`. Oracle experiments should change one variable at a time; confidence should remain fixed for source-only intervention.
2. Add a **stateful event cursor and correction-transaction ledger**. Deduplicate earlier clarification requests, process later utterances and record supersessions/revisions without rewriting past decisions. Regress F2.
3. Factor action policy into separate decisions: `PAUSE_PLAYBACK`, `ASK_FOR_CLARIFICATION`, `PROPOSE_CORRECTION`, `CONFIRM_TASK_CHANGE`, `COMMIT_TASK_CHANGE`. No physical execution in DEV. Include a deliberate null action and errors for premature commit.
4. Freeze **PLAYBACK-REFERENCE-01** before acoustic coding. Practical reference-matching baseline vs bounded adaptive echo suppressor on identical causal 16-kHz PCM speech and playback stream; evaluator-only clean stems. Treat speaker and authorization as separate unknown labels. Source-group splitting, fixed false echo triggering / independent speech detection / double-talk confusion / decision delay / CPU and minimum useful coverage. First verify exact file-level rights for any downloaded subset.
5. Later compare audio model to streaming ASR+VAD+playback reference using identical causal prefixes and separate acoustic-onset, transcript-delivery, policy decision and audible-stop clocks.

## Data starting points (external, not executed)

- LibriSpeech SLR12 official corpus: `https://openslr.org/12/`, **CC BY 4.0**; the listed `dev-clean` archive is ~337 MB. Actual audio access and small subset mechanism not yet checked in this audit. Reading speech is not conversational correction ground truth.
- Full-Duplex-Bench v1.5: `https://github.com/DanielLin94144/Full-Duplex-Bench/blob/main/v1_v1.5/dataset/README.md`; maintainer labels synthetic v1.5 data MIT, with paired `input.wav`, `clean_input.wav` and overlap timestamps. Does not by itself certify task-authority labels, real humans' intentions or an echo-only playlist reference condition.

## Status

**REPAIR** oracle comparisons, correction state, action semantics before promoting policy. **GO** only for designing a separately versioned and rights-cleared PLAYBACK-REFERENCE acoustic experiment. **NOT RUN:** any real-audio AEC, speaker/source diarization, transcript revision analysis, human task sessions, farm operations, or Dessa model execution. No need to assume speech-native learning succeeds.