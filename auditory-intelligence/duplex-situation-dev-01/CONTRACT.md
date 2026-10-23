# DUPLEX-SITUATION-DEV-01.1 — factorial mock-only streaming contract

**Frozen design, 2026-10-23.** Scientific status: **EXPOSED ENGINEERING DEV / NOT SPEECH PERCEPTION**. Source: user-relayed Muse DESSA-SPEECH-NATIVE-01 Round 01 (reported 6 sessions, 4/5 corrections on A1/A2); **original Muse code and files not supplied**, so this is an independent, non-replication experiment. Budget: $0. No real speech WAVs, microphones, people, model inference, hardware, farm controls or paid services.

## Research question

On timestamped mock event records, is better behavior caused by (1) *information about the source* or (2) *the decision policy*? Compare both along separate axes; never give one policy better sources by accident.

## Simulated input, oracle, and causality

Each synthetic session has timed, mock-**transcribed** utterances with `start_ms`, `end_ms`, `available_ms = end_ms + 150` (chosen synthetic ASR delivery latency; NOT measured), `observed_source`, `observed_confidence` and an **independent oracle source** `task_user|assistant_self|echo|bystander|unknown|machine`. Lexical words become visible **only after available_ms**; no partial word or future tokens. Source oracle is used for evaluation only, except in the explicitly labeled **ORACLE_SOURCE diagnostic condition**. Action/yield latency is **simulated processing latency**, not an observed model/system runtime.

Events may include: user corrections to left/right gate, direction, or 12/20 trays; bystander fake corrections; own-output echo; backchannels; quotes using literal correction keywords; low-confidence/unknown-source correction; split/incomplete utterances; negation, and identical prefixes with divergent future correction content. Ground-truth expected outcomes come from the authored scenario and are never passed to practical policies.

No evidence of real acoustic source separation, AEC, speech recognition, human intention, accessibility needs or physical-world diagnostic accuracy.

## Factorial comparator arms

- **PRACTICAL+NAIVE:** observed (imperfect) source labels + eager interruption whenever correction lexicon appears, despite uncertainty. Counterfactual safety-negative comparator.
- **PRACTICAL+GUARDED:** *same exact observed labels* + confidence threshold 0.80, reject bystander/echo/own audio, hold on unknown, ignore quoted lexical phrases, never act on a machine.
- **ORACLE+NAIVE:** *perfect true source* + same eager policy, **information diagnostic**.
- **ORACLE+GUARDED:** *perfect true source* + guarded policy, **non-deployable information diagnostic**.
- **WAIT_ALWAYS:** no response to any mock event; safety/coverage negative control.

Thus oracle-vs-practical isolates availability of source info under the *same* policy; guarded-vs-naive isolates action policy with *identical* source info. Do not call oracle improvements model competence.

## Outputs, denominators, and falsifiers

At each decision cutoff `t`, only events with `available_ms <= t` may affect decisions. `YIELD_CONFIRM` is a proposed simulated interruption with structured correction tuple; **never a physical action**. `ASK_SOURCE_CONFIRMATION` is an uncertainty/abstention action, not correct capture; `CONTINUE` means no yield. Quoted occurrence of correction lexicon must not be interpreted as a user command.

Report per arm: `capture_count / ground_truth_actionable_corrections`, `missed_correcting_sessions`, false yield on negative sessions (bystander, echo, backchannel, quote, irrelevant), request-for-clarification count, text-value fidelity for direction/number/negation, and simulated yield latency from **event available_ms**, with true source mislabel error counts reported separately. Output **session-level** receipts; no hundreds-of-frames IID claims.

Include a **no-future-leakage test**: two authored utterance sequences identical in all available observations up to cutoff must give identical prefix actions, despite distinct future correct values. Any future-token leak blocks progression.

Fixture scoring may show that oracle source information helps, but **does not qualify source detection**. A system that waits always has capture=0; a reckless system can have useful capture and unacceptable false takeovers. Positive and negative opportunities remain explicit.

## STOP/GO boundaries

- **GO** means only that the deterministic mock, its source/policy attribution, causal reading, and evidence receipts are reproducible.
- **STOP** promotion of any spoken-language or full-duplex model claim until a rights-cleared, independently time-labeled *actual audio* test is designed and executed against practical streaming ASR/VAD/AEC/source baselines.
- **No evidence** that an M4 Max requirement translates to iPad/phone capability, and no permission to infer emotions, speaker identity, diagnose a person, or execute farm machinery controls.
