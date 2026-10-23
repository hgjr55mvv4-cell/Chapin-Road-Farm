# LOOM-01 — are apparent cross-song patterns more than matched chance similarity?

**Status: ENGINEERING DEV / EXPOSED fixtures / NOT HUMAN SCIENCE.** Inspired by Kimi's first-principles Round 01. This first version tests a **tiny symbolic representation claim**, not waveform-based music cognition, AI listening, psychology or model learning. Zero external libraries or services.

## What it actually does

- Synthesize `64` independent **symbolic triplets** (one source melody, its exact interval-sequence transposition, and a shuffled-interval control). Each melody has 13 symbolic pitches / 12 successive pitch steps.
- All three share the same *multiset of pitch intervals*. The shuffled control is **not rejected** when chance happens to preserve the same ordered sequence, so the measured false-positive count is honest for this generator.
- The **ordered interval comparator** preserves pitch-step order and is invariant to transposition; the **histogram comparator** sees the planted and shuffled cases as identical by design, while the **absolute-pitch comparator** is sensitive to key changes.
- A fixed `0.83` threshold is an arbitrary engineering-only display threshold, not a learned classifier, preregistered scientific gate or proof of calibration.

The “null” means **no intentionally planted identical ordered sequence**, *not* “no pattern exists” or “same base rates as real music.” The positive is trivially identical under this representation by construction, so the result is a simple representation sanity check. Do not report AUROC, statistical certainty, or independent model generalization from this generator.

## Run

From this folder with Python 3, no Internet/dependencies:

```sh
python -m unittest discover -s tests -v
python loom.py --seed 20261023 --sets 64
```

Local Python 3.13.5/Linux execution actually ran **7/7 standard-library tests** and 64 generated triplets with the following reported counts:

| Measure | Result | Interpretation |
|---|---:|---|
| Exact transposed ordered-step positives at similarity ≥0.83 | 64/64 | Expected by the generator: every positive shares entire ordered step sequence |
| Shuffled order nulls incorrectly classified as positive | 0/64 | Observed for **this seed/generator only**, not a general false-alarm guarantee |
| Unordered histogram similarity, both groups | 1.0 | Histogram baseline cannot distinguish them |
| Absolute pitch exact-match similarity, transposed positives | 0.0 | Deliberate pitch-shift breaks absolute pitch identity |

Original [local unit-test stdout/stderr](receipts/local_unittest_2026-10-23.txt) and [evaluation JSON](receipts/local_eval_2026-10-23.json) are included. GitHub CI should independently execute the committed code on Python 3.11 and 3.13; do not claim CI passed before inspecting actual job output.

## What is next (NOT IMPLEMENTED)

A scientifically meaningful follow-up would need (i) synthetic **audio waveform** rendering/decoding and known note extraction error, (ii) independently generated, more musically realistic null corpora and cultural/genre prior calibrations, (iii) true held-out generator families and locked metric/selection rules, and only later (iv) consented human response data with exposure, state and order alternatives. Instrumental cues and perceived meaning cannot be read off the symbolic melody alone.

No copyrighted recordings, participant data, API calls or training were used. All source/test labels are public DEV. An independent agent should attempt to break our definitions/controls and report exact execution before we interpret it as anything stronger.
