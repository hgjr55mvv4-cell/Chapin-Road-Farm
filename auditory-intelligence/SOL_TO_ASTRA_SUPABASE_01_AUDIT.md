# SOL → ASTRA | SUPABASE-RESEARCH-01: Evidence, Auth and Restart-Safe Journal

From Brian & Sol · October 23, 2026 · Independent software audit; $0; no live DB changes.

## Provenance and available material

Muse reported a SQLite WAL reference design, 18 passing self-authored tests, and tables for farm memberships, versioned task values, untrusted speech observations, pending correction transactions, host confirmations, and append-only evidence. **Muse's actual Python source, test files, database snapshot, hashes and stdout were not attached to Sol.** The external link for the database did not download in this session. An independent replay of Muse's 18 tests is NOT RUN.

Sol rechecked the connected Supabase organization: Chapin Road Farm, Free, **0 accessible projects**. No tables, schemas, policies, storage objects or migrations have been examined or changed.

Sol performed a separate standard-library SQLite audit with **9/9 passing tests on Python 3.13.5**. That suite is NOT Muse's source. It covers append-only conflicts, retrieval of contradictory physical source claims, versioned CAS and retry, a second DB connection seeing stale state, database-injected rollback, on-disk WAL restart, mock farm membership, and accessible manual correction. Read the [reconciliation](SOL_SUPABASE_RESEARCH_01_RECONCILIATION.md). Brian has a separate runnable ZIP with tests, result log and checksums.

## Astra's falsification priorities

1. **Source admission first.** Obtain actual Muse reference.py or policy.py, SQLite DB including relevant WAL/SHM if present, schema, test source, interpreter version, SHA-256 and outputs. Then rerun all 18 Muse tests. If not supplied: NOT RUN, no reconstructed replay claims.
2. **Real authorization.** A mock principal such as farmer_brian or a callback checking a name prefix is NOT authentication. Determine the trusted session source, actual task/farm membership, principal revocation, and verified UI preview/gesture. A transcript-supplied role and one-tap boolean cannot grant authority.
3. **Supabase privileges.** Table exposure depends on grants AND RLS. Audit cross-farm SELECT/UPDATE/INSERT and membership policy design. Service-role clients bypass RLS; SECURITY DEFINER functions can bypass RLS and may be broadly executable unless explicitly restricted. Prefer a least-privilege invoker or auditable trusted host boundary; do not use privileged functions merely to bypass a failed RLS check. Sources: https://supabase.com/docs/guides/api/securing-your-api and https://supabase.com/docs/guides/database/functions.
4. **Durability and exactly-once logical change.** Crash before proposal append, after proposal, during confirmation, during CAS update, after commit before response, and after restart retry. Same idempotency key with *different payload* must be rejected rather than treated as harmless replay. Test two independent DB connections and stale versions; distinguish a mock exception rollback from actual power-loss durability.
5. **Source memory and counterevidence.** Given two claims for one acoustic event (obj-gate-north-001 high confidence and obj-gate-north-002 disputed), retrieve both with source, evaluator, timestamps, evidence hash and correction lineage. Do not expose only top-scoring claim. Append reversals rather than mutating earlier assertions.
6. **Manual accessibility.** Independently authenticated UI editing must still work with missing or faulty audio and must confirm exact task/referent, old/new value and expected version. No acoustic residual score may veto a manual correction.
7. **No live infrastructure assumption.** With zero projects visible, do not create a Supabase project, deploy migrations, introduce public storage, generate privileged keys or change any policies without Brian's explicit approval.

## Deliverables

A. Exact source/permissions inventory with RUN/NOT RUN. B. Actual Muse replay if bytes available. C. One independently reproduced exploit or counterexample, with commands and trace. D. Proposed minimal repair and reproducible tests. E. Row-access, transaction and contradictory-evidence query audit. F. GO/REPAIR/STOP for offline persistence only, separate from live Supabase deployment.

Existing public incumbent: https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/tree/main/auditory-intelligence/duplex-policy-repair-03-1 . Issue #58: https://github.com/hgjr55mvv4-cell/Chapin-Road-Farm/issues/58 .

**HOLD:** live Supabase changes, real authentication claims, microphone capture, source attribution, model inference, field machinery and human safety qualification.

— Brian & Sol