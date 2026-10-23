# Auditory Intelligence: DataSED recording-admission gate

**Status:** Code executed; **14/14 deterministic fixture tests passed locally** (October 23, 2026). **Real DataSED candidates: 0 admitted / NOT RUN.** The user-relayed Astra audit mentioned nine candidate recordings but did not include their IDs, original full A–J report, or original audio bytes here. Do not invent nine filenames or treat a metadata record as an audio validation.

This is the independent response to [Astra's AUDITORY-REAL-01 review](../ASTRA_REAL_01_RELAY_DIGEST.md). Astra reproduced the original ESC-10 real-recording results and recommended repairing ground-truth provenance before adding audio features. Its deeper critique is that even a whole-clip sound class does not prove an energetic selected subsection contains an instance of that class.

## What the gate does

Checks validity, completeness, timestamp ranges, independent source lineage, rights-evidence fields, audio hash and PCM decode, bounded source size, independently recorded audio-review receipts for positive event intervals, and **explicit manual verification** of negative intervals. It refuses to equate unlabeled space with negative ground truth. Detects train/eval leakage when records share a declared original recording ID. Every reject/HOLD has machine-readable reasons.

No classification model is implemented. Input labels remain assertions requiring external auditing; the code does not actually listen, independently establish recording identity, or authenticate the reviewer.

## Reproduce offline

```sh
cd auditory-intelligence/dataset-admission-01
python -m unittest discover -s tests -v
python admission.py --manifest YOUR_CANDIDATES.json --annotations YOUR_POLYPHONIC_LABELS.csv --audio-dir YOUR_VERIFIED_WAV_FOLDER --out admission_report.json
```

The second command is intentionally **not runnable successfully until independent real metadata, original audio, source documentation, and manual review receipts exist**. It writes a status report and exits 2 on HOLD. We have no nine-source manifest to populate truthfully.

Manifest shape (SCHEMA EXAMPLE ONLY; not a real recording):

```json
{
  "dataset": "DataSED",
  "dataset_revision": "exact-record-and-archive-hash",
  "candidates": [
    {
      "sound_name": "S-0001.wav",
      "split": "train",
      "audio_sha256": "64 lowercase hex digits of the actual downloaded WAV",
      "provenance": {
        "lineage_status": "VERIFIED",
        "original_recording_id": "actual unambiguous session/source ID",
        "evidence_ref": "original documentary lineage evidence",
        "rights_status": "VERIFIED",
        "rights_ref": "original file/license evidence",
        "editing_history": "actual source transformation history, including no-edit evidence"
      },
      "independent_listening_checks": [
        {
          "decision": "EVENT_PRESENT",
          "class_name": "exact time-label CSV class",
          "start_s": 0.5,
          "end_s": 1.25,
          "audio_sha256": "hash of audio actually reviewed",
          "reviewer_id": "independent reviewer identity",
          "receipt_ref": "durable review receipt"
        }
      ]
    }
  ]
}
```

Negative intervals can be admitted **only** with an explicit `CLASS_ABSENT_VERIFIED` check for the target class, timing, reviewed-audio hash and reviewer receipt. A sparse label table never supplies negatives automatically. Real positive annotations should match the reviewer timing within a 0.5-second initial engineering gate (not a biological accuracy claim).

## Reasons for HOLD

Includes `MISSING_AUDIO`, `AUDIO_HASH_MISMATCH`, `TRUNCATED_AUDIO`, `AUDIO_TOO_LARGE_FOR_BOUNDED_ADMISSION`, `UNVERIFIED_LINEAGE_OR_RIGHTS`, `POSITIVE_LABELS_NOT_INDEPENDENTLY_VERIFIED`, `NO_VERIFIED_NEGATIVES`, `ANNOTATION_OUTSIDE_AUDIO`, `TRAIN_EVAL_LINEAGE_LEAKAGE` and `INVALID_ANNOTATION_ROW`. File-level report keeps both admitted and rejected rows; all held-out eligibility remains undecided until an external provenance audit.

## External evidence and dataset version warning

[Zenodo DataSED v1](https://zenodo.org/records/15346092) describes **717** recordings with 44.1 kHz mono WAV and manually annotated mono/polyphonic time labels; the [2025 Scientific Data paper](https://doi.org/10.1038/s41597-025-05991-w) describes **712** files. The paper and repository explicitly warn that some material was edited and some intervals are unlabeled. **Archive membership and the per-file source lineage cannot be assumed from the filename.** Do not redistribute the multi-gigabyte dataset or claim an unspecified license applies to every underlying recording. Exact per-file rights remain to be established.

## Next independent step

Recover Astra's original review package and its nine candidate names, choose only those with inspectable source lineage and labels, then check a small number of **rights-cleared audio bytes** independently before classifier training. Preserve any rejection as an informative negative outcome. Strong simple ZCR/time-feature classifier remains the baseline; the old nine-frequency representation stays on STOP.

