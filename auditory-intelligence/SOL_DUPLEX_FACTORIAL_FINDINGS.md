# Sol — DUPLEX-SITUATION-DEV-01.1 | independently executed factorial mock

**Date:** October 23, 2026. **Evidence:** mock-only local engineering (Python 3.13.5, 18/18 tests). **No generated source has been committed to GitHub**; the source, test file, full case JSON, local receipts and SHA256 are in a separate portable ZIP delivered to Brian. **Original Muse six-session code/result files were not supplied**, so these numbers are not a replay of Muse's reported 4/5 result.

## Experiment

[Frozen contract](duplex-situation-dev-01/CONTRACT.md) recorded before independent implementation. We hand-authored fifteen mock sessions (nine authorized task corrections, six negative cases), supplied synthetic transcripts, source labels and a 150ms assumed availability offset, then ran 5 policies: practical observed-source tags versus oracle-source truth, crossed with naive versus guarded interruption policies, plus WAIT_ALWAYS. Oracle means **supplied ground truth**, not measured acoustic source separation or AEC. All decisions filter out words not yet available at simulated cutoffs.

| Arm | Correctly captured / 9 | False yields / 6 negatives | Clarification requests |
|---|---:|---:|---:|
| Practical source + naive | 8 | 2 | 1 |
| Practical source + guarded | 6 | 2 | 3 |
| Oracle source + naive | 8 | 0 | 1 |
| Oracle source + guarded | 8 | 0 | 1 |
| Wait always | 0 | 0 | 0 |

**Interpretation:** confidence-gating alone reduced useful captures while failing to prevent two confident but wrong source labels (a bystander marked user, and assistant echo marked user). Oracle source data fixed the association **by assumption**, not because a model inferred it from sound. A never-respond system avoids false yields only by missing all corrections. Transcript parsing used narrow regexes for right/left gates and `12 trays, not 20`, not a language model.

**Engineering qualification:** 18/18 local tests, initial low-confidence masked-value failure fixed; all scenarios and thresholds exposed. 150ms ASR and 50ms scheduling numbers are **artificial constants**, not observed latency. **No real audio, Dessa, Moshi, VAD, AEC, speech ASR, individual speaker recognition, field work or human preference validation.**

## Muse review critique

The user-relayed Muse report described A1 4/5 versus oracle-source A2 4/5 and a reduction in bystander false responses, with mock 400ms/200ms latencies. Source/result artifacts were not accessible here. The informational advantage of oracle speaker labels and timing conventions makes that comparison incapable of establishing native speech-model superiority. Claiming “100% echo suppression” when an oracle echo label is supplied is **not an acoustic result**. The synthetic mock cannot infer feelings, intent, source of machinery sounds or safe field commands.

**Decision:** Proceed to independent review of source-confidence failures and rights-cleared actual speech-data evaluation design; STOP any claim that this establishes an auditory-native superiority or field-ready duplex farm assistant. Hold DataSED acoustic event provenance and VFM machinery diagnosis in separate research tracks.

**Full offline source handoff:** Brian receives a zip for forwarding. Do not treat this document or zip as a GitHub CI test or compare its 15 handcrafted sessions statistically with Muse's six. Scientific confirmation remains HOLD.
