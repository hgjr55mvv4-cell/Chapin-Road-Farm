# AUDITORY-EVENT-INCREMENT-02 — source-*class* association, synthetic DEV

**Status: EXECUTED ENGINEERING DEV / FULLY EXPOSED CASES / HUMAN AND MACHINE DIAGNOSIS HOLD.** This is a $0 Python-stdlib-only experiment on *constructed tones*, not actual speech, musical comprehension, source-object localization, bearing-fault identification or true situational awareness.

The [frozen v0.1 contract](CONTRACT.md) was committed before the detector implementation. It defines 440 Hz source class A followed by 620 Hz B as a positive, with absence, replacement by 760 Hz C, or B-before-A as negatives. Matched pairs (400 pairs, 800 WAVs) share the underlying scenario background and perturbation sources; generator schedules are ground truth, independent of either detector's event segmentation.

## Actually tested

- **E — RMS region detector**: the baseline reports a match if *any two energy regions* appear in order. Its `event_identity='UNVERIFIED'` means a numeric gap does not constitute a successful A→B association.
- **F — simple fixed-template A/B frequency detector**: 40 ms sine/cosine matching, 20 ms hop; select ordered A and B class regions if the synthetic signal supports both. This is a known-two-frequency detector, not a source separator or learned speech/audio model.
- **T / G** are explicit information controls only: generic external text and unlabeled oracle aggregate-activity timestamps respectively **cannot determine tone classes**. We do *not* invent classification accuracy for either. A future labeled-event timestamp baseline would be a different, richer information arm.

Controls include wrong-class substitution, absent target, reversed tone order, 310 Hz distractor, amplitude changes (including hard-to-detect quiet targets), controlled random noise, ramped attacks, dropouts, mild synthetic echoes and bounded transport-input errors. Event-class identity remains distinct from **physical source identity** even when frequency labels are correct.

### Reproduce locally (no packages, APIs or network)

```bash
cd auditory-intelligence/event-increment-02
python -m unittest discover -s tests -v
python event_dev.py --pairs 400 --seed 20261023 --out results.json
python export_cases.py --pairs 400 --out cases.csv
```

Local execution on Python 3.13.5/Linux: **18/18 tests passed**; 400 positive + 400 negative captures processed. The fixed-template F method recognized 314/400 planted pairs with correct reported A/B start times (within 100 ms), missed 86/400 planted positives, and incorrectly accepted **0/400 negatives on this exposed generator**. Its measured test-set latency and detailed results are in [results.json](results.json). This is not an estimated field false-positive rate, and a more adversarial generator may break it.

E produced 168 positive pair-level "MATCH" outputs **with identity unverified**, 232 positive abstentions; it issued a false A→B match on 184/400 negative captures and abstained on 216/400. Calling E's unverified matches "correctly identified" would reproduce exactly the inferential error Astra identified.

All fixtures and thresholds were co-designed and are public **EXPOSED DEV**. Evaluation is retrospective and has access to the entire recording. Prefix-consistency tests prevent future samples from being rhetorically treated as observed earlier; no streaming turn-end prediction is implemented. The code supports only short mono PCM16 8kHz WAV and is deliberately narrower than a real microphone pipeline.

### Real audio is the next *different* task

[External dataset selection and licensing ledger](DATASETS.md) identifies stronger real event-label datasets (DataSED, DCASE SELD/DESED/FUSS) and separate VFM machine-condition datasets (DCASE Task 2 bearing/gearbox, MIMII, IDMT). **None were downloaded or used**. A real audio benchmark will require a new task/spec, legal/data version checks, source-label adjudication and new representations; resampling real recordings into this A/B tone detector would not validate physical source attribution.

### GO/STOP

**Engineering pass:** the simple class-specific detector can exploit spectral information that aggregate energy timing lacks in deliberately synthesized sounds, with observed misses clearly counted.

**HOLD:** any claim that the system identifies the true physical source, human intention, machinery failure, microphone sensor health, or machine safety. Do not promote an elaborate model until it beats this simple baseline under a separately frozen, independently sourced evaluation population and honest abstention/resource accounting. Preserve negatives, misses and invalid cases rather than hiding them.