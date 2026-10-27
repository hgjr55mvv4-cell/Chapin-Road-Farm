# SUPABASE-PERSISTENCE-ADMISSION-01 — independent offline evidence and persistence test

**Status:** EXPOSED LOCAL SQLITE ENGINEERING; **not** a replay of Muse's implementation; **no live Supabase project**. **Research-only, $0, no private data or physical actions.**

This versioned research responds to Muse's SUPABASE-RESEARCH-01 report and the open [DUPLEX-TRUST-04 issue](https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/58).

- [Pre-implementation contract](CONTRACT.md) was committed before local implementation began.
- Sol built a separate standard-library SQLite reference, locally executed **33/33 tests on Python 3.13.5 / SQLite 3.46.1**, and preserved the case-level stdout, deterministic demo and source SHA-256 receipts in a portable ZIP delivered to Brian.
- **Source and tests are in the portable companion ZIP, not committed in this research PR.** The repository alone is not a complete reproduction; the ZIP must be attached to Astra. Do not report GitHub CI qualification for this offline source unless it is separately uploaded and run.
- [Supabase/Postgres security and schema approach](POSTGRES_DESIGN.md) is **DESIGN ONLY / NOT DEPLOYED**.
- [Astra independent review requirements](SOL_TO_ASTRA_REVIEW.md) specify replay gates and known false-assurance modes.

## What Sol actually tested

1. A source claim or confidently misattributed echo does **not** mutate a task without a separately simulated host-confirmation path. Such a false proposal may still reach UI review.
2. Pending proposals persist through a local SQLite reconnect; duplicate logical commits with the same command ID replay the stored result.
3. Atomic transaction receipt, value update, history append and tentative supersession are tested with exceptions before commit, lost response after commit, and a subprocess termination mid-transaction. This is **not** real power-loss/fsync qualification.
4. Two competing confirmations at an identical prior field version produce **one** accepted commit, the other rejected.
5. Python membership checks isolate read/write methods by synthetic farm; **direct SQLite file access bypasses them**. This is not real authentication or Supabase RLS.
6. Same-event evidence with **0.98 confidence / DISPUTED / object A** and **0.64 confidence / SUPPORTED / object B** returns **both assertions**, preserving their original provenance claims and evaluator disagreement. The code does not independently verify either label, source hash or evaluator.

## STOP / HOLD

- No Muse candidate replay: only its user-relayed narrative and report were available; Muse's code, DB and executable receipts were not attached.
- Supabase connector: connected to Chapin Road Farm Free organization; project list returned **[]** again; no tables, policies, storage, project costs or data inspected.
- No actual identity provider, secure host process, RLS, production migration, live audio source identification, human study, or farm control.
- Do not introduce public audio buckets, pgvector or `service_role` functions until there is a validated need and a tested, least-privilege access design.
