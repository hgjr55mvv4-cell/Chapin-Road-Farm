# AUDITORY-BOUNDARY-DEV-01 — Synthetic energy-boundary sensitivity

**Status: EXPOSED_ENGINEERING_DEV.** Scientific confirmation and use for real conversational turn-taking: **HOLD**. This is a public negative/sensitivity case for the existing [AUDITORY-DEV-01 detector](../audio_dev.py), not a change to that detector or a new model.

## Finding

Two programmed tone bursts are separated by **0.480 s**. The first ends at **0.620 s** and the second begins at **1.100 s**. In the challenger, only the amplitude of the first tone's final **80 ms** (0.540–0.620 s) changes. Its programmed end time does not.

| Final-tail amplitude | RMS-threshold event end | Measured gap | Illustrative action |
|---:|---:|---:|---|
| 100% (unmodified control) | 0.620 s | 0.480 s | WAIT |
| 50% | 0.620 s | 0.480 s | WAIT |
| 30% | 0.620 s | 0.480 s | WAIT |
| 10% | 0.540 s | 0.560 s | READY_NOT_OBLIGATED_TO_REPLY |
| 0% | 0.540 s | 0.560 s | READY_NOT_OBLIGATED_TO_REPLY |

At 10%, the last eight 10-ms frames have RMS around 0.029–0.031, below the detector's fixed threshold **0.08**. It therefore marks the first event inactive 80 ms early. The detector correctly measures its *own energy-threshold boundary*, but that boundary is not necessarily the synthesizer's programmed end or what a human perceives. The routing action flips because the measured gap crosses the authored 0.50-second LONG rule. **Human perception was not measured.**

## Reproduce from a public checkout

Python 3, standard library only. No microphone, data download, user data, API key, or network during execution.

```sh
cd auditory-intelligence/dev-01
python3 -m unittest discover -s tests -v
python3 boundary-sensitivity-01/verify.py --check
```

The first command should report **12/12 passing** unchanged baseline unit tests. The second generates all five WAVs in memory, checks the original generator against its unmodified control **byte-for-byte**, verifies the detector's SHA-256 and all five observed gap/action outcomes, and compares its generated JSON **byte-for-byte** with [the committed observed receipt](receipts/observed.json). It writes no WAVs to disk. On success it prints the JSON to stdout and a PASS line to stderr; any mismatch produces a nonzero exit.

The [reproducer](verify.py) is intentionally separate from the original [detector](../audio_dev.py), [12 original tests](../tests/test_audio_dev.py), and [original receipt](../receipts/local_eval.json), all preserved unchanged. Run from any current directory using the script's absolute or repository-relative path. The original detector source expected SHA-256 is `ec824b080e73209c05053bed259c1105c93d9c1d009f88a5272fdb9dea41c021`. This is pinned to that baseline; later detector edits require a new comparison, not silent reuse of the receipt.

### What was actually tested

Sol executed the exact public baseline source and original test bytes in an isolated **Python 3.12.14 in-memory replay**: **12/12 passed**. The sensitivity reproducer then matched its machine-generated receipt byte-for-byte, including all five cases, against those exact source bytes. An outside agent can repeat the two public commands above without the original private research handoff. This is **engineering reproduction**, not an independent held-out scientific experiment; the counterexample and expected results were exposed during development.

## Experimental contract and limitations

- **Incumbent:** unchanged 10-ms, RMS > 0.08 energy detector and its existing clean pure-tone tests.
- **DEV challenger:** paired clean vs attenuated-tail generators with fixed seed 42, noise 0.008, signal amplitude 0.42, frequencies 440/620 Hz, physical schedule and deterministic route mapping. Only the first tail's amplitude factor varies.
- **Scope:** sensitivity of energy-derived boundaries and downstream illustrative action; not source identity, perception, speech recognition, intent, or conversational benefit.
- **Success/quality floor:** original 12 tests pass; clean generated WAV is byte-identical to incumbent generator; source hash matches; five comparisons and receipt match; zero private or live recordings, network calls or paid dependencies.
- **Falsifiers:** a different measured gap/action on exact public bytes, a receipt mismatch, an altered baseline, or failure of original tests. Either outcome should be reported, not hidden.
- **Selection and cost:** these five exposed development cases were chosen after seeing a reported counterexample, so they are **not reserved confirmation cases**. Two Python commands, no added dependency, no monetary cost, and no persistent detector/runtime change. Reassessment against new, reserved cases and a transcript-plus-accurate-timestamps comparator would be needed before considering any alternate method.
- **Possible alternative:** a lower threshold or hysteresis may recover the attenuated tail but can falsely treat noise as activity. No challenger detector is being promoted by this result.

The motivating Grok outside-agent account was relayed through Brian; its authorship and execution report are **not** substituted for executable source/receipts. The previous private evidence package had a documented prose-inventory error and was corrected separately; no such private package, injected payload, participant material, or unverifiable file inventory is published here.

If you reproduce a different result, please provide the Git commit, Python version, exact command, stdout/stderr, and the observed JSON or its hash via a reviewed issue/PR. A null or disagreement is welcome. See [AGENTS.md](../../../AGENTS.md).
