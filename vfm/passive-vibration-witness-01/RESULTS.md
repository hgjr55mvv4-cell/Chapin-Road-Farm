# DEV-01 result: software tests PASS; mechanical qualification HOLD
**2026-10-23:** 16/16 local Python tests passed; 80 seeded (20261023) post-freeze **synthetic** cases executed in about 0.27 seconds. No purchased hardware, field run or independent replication.

| Class (16 cases each) | Shock-only triggers | Tuned peak triggers | Tuned dwell triggers |
|---|---:|---:|---:|
| Sustained on-band | 16 | 16 | 16 |
| Ordinary off-band | 11 | 0 | 0 |
| Short half-sine impact | 16 | 9 | 0 |
| Severe off-band overload | 16 | 16 | 13 |
| **Healthy matched on-band** | **16** | **16** | **16** |

All values mean simulated **activations**, not true positive mechanical fault diagnoses. The sustained vibration witness passes the pre-stated synthetic gate. The matched healthy case and off-band overload invalidate fault-specific interpretation. Requiring twelve above-threshold extrema is **software logic only**, not proof of a working battery-free latch.

Status: **ENGINEERING-ONLY PASS** for the assumed ideal physics, **UNKNOWN** for physical thresholds/aging/reliability, **HOLD** for on-machine installation and diagnostic use. No source modification after frozen selection. Run `python confirm.py` for deterministic exact case-level output. These are correlated toy model trials, not 80 independent experiments.

The central null result is informational: a one-bit exposure witness cannot distinguish identical waveforms produced by different underlying machinery states. The simplest mechanical peak latch must remain the physical baseline until its real cost/benefit is measured.