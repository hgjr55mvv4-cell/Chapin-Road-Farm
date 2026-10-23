# SOL → ASTRA / MUSE — DUPLEX IMPLEMENTATION REPLAY & PLAYBACK-REFERENCE-01

**From:** Brian & Sol · **Date:** October 23, 2026 · **Status:** Independent review authorized, **acoustic experiment DESIGN ONLY / NOT RUN** · **Budget:** $0 extra · **Scientific/field confirmation:** HOLD

## What Astra can inspect now

The **original, actual-byte companion** `DUPLEX_SITUATION_DEV_01_1_2026-10-23.zip` was recovered from this conversation's container, integrity-tested and replayed. To inspect it in another Astra/Muse instance, **Brian must attach the ZIP bytes to that chat**; a repository document or filename does not itself provide the code. The companion ZIP SHA-256 is `68f567320a4b32bafab5ea4e8ba824006834969d94d7425d234cc24db014131e`.

[Read Sol's actual implementation-level replay](SOL_DUPLEX_IMPLEMENTATION_REPLAY_01.md). Original source tests: **18/18 independently rerun locally**, Python 3.13.5; original source/results hashes checked. Independent diagnostic script and test output were also bundled separately for Brian to attach.

**Source findings — all executed, not hypothetical:**
- The `oracle_source=True` condition replaces `source_observed` with `source_truth` **AND forces `source_confidence=1.0`**. A test with *identical task-user source labels* and observed confidence 0.25 causes guard to ASK but oracle to YIELD. This is **not source-label-only isolation**.
- Two false yields survive the guarded policy when an echo or bystander is confidently mislabeled as `task_user`.
- A new reproducible **sticky-ASK failure**: an earlier uncertain `No, I meant...` gets reconsidered at every tick, so a later complete valid correction never executes; no event consumption or revision state exists.
- `Event` has no addressee, authorization, role-permission, task confirmation or playback-reference fields; the truth label merges physical source and dialogue authority.
- Simulated 150 ms ASR-delay/50 ms tick outputs are **not measured audible yield times**, and transcript source tags are not produced by an actual microphone.

**Disposition:** REPAIR mock semantics and factorial parity before claiming dependable interruption handling. Keep original ZIP immutable. Do not infer that a native speech model can solve echo/source attribution from these fixtures.

## Recommended separate experiment: PLAYBACK-REFERENCE-01 v0.1 (not executed)

**Target:** Can practical waveform processing distinguish **known assistant playback echo** from independently recorded simultaneous speech, using the assistant's recorded output as a reference? This is NOT person/role authentication or speech comprehension.

**Provisional rights source:** [LibriSpeech SLR12](https://openslr.org/12/) read English speech (officially CC BY 4.0); full `dev-clean` is ~337MB and must **not** be downloaded by default. Check specific selected files, speaker/chapter/source lineage and license, find ≤25 MB subset before any execution. [Full-Duplex-Bench v1.5](https://github.com/DanielLin94144/Full-Duplex-Bench/blob/main/v1_v1.5/dataset/README.md) pairs synthetic-overlap/clean audio under maintainer MIT license; must audit rights of actual downloadable bytes and note its lack of task authority labels. No private voice captures.

**Four matched conditions, grouped by originating speaker/chapter:**
1. Echo of assistant playback only (true extra speech absent).
2. Independently recorded other speech only (true extra speech present).
3. Echo plus independent speech, with varied echo delay/gain/filter and onset overlap.
4. Independent speech using the *same words* as assistant playback (correlation trap).

Provide both practical arms **the same causal microphone prefix and playback-reference prefix**; clean constituent stems, true source IDs and exact annotations only to scorer. One arm is bounded causal normalized playback-reference correlation / residual activity; second is bounded causal adaptive echo canceller with double-talk safeguards. Predefine model information, DSP frame sizes, group splits, lag windows, gain/filter ranges, fixed calibration; do not tune on held-out sources. **Source separation and authorization are distinct outputs.**

**Primary metrics:** per-original-source-group echo-only false takeover rate, other-speech detection rate, double-talk miss rate, confusion under same-word but different-speaker condition, useful coverage versus abstention, causal response onset-to-decision latency, estimated audible-stop delay, and CPU/memory. Report physically meaningful start/end times, not only mock ASR availability. Check incomplete/truncated files, mismatched playback references, clipped input, and identical-prefix causality/replay. Both methods must handle unknown origin without inventing permission.

**Provisional engineering floor:** ≥90% independent-speech detection on admitted group sources and ≤5% echo-only false triggering *at a fixed coverage floor*, before considering useful deployment; with few groups these are **not statistical safety guarantees**. Stop richer DSP branch if basic reference method meets the bar at lower cost. These numbers are *proposed*, not frozen against a real accessible sample.

**Absolute HOLDs:** original WAV rights, audio dataset selection, training, actual echo suppression, live microphones, any voiceprint/biometrics, ASR inference, user-role inference, Dessa access, field safety and equipment control. **Do not claim this experiment has run.**

## Required reply from Astra

After Brian attaches source ZIP: inspect `duplex_dev.py` and `tests/test_duplex.py` and independently rerun the original and new audit probes. Challenge the extra finding (sticky clarification), oracle-confidence confound, lack of role separation, and limitations of acoustic echo-only evaluation. Recommend **REPAIR** or a bounded next scientific gate. Include exact executed commands/results and clear NOT RUN labels.

— Brian & Sol
