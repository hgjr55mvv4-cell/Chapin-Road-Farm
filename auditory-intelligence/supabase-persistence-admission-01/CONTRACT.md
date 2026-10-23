# SUPABASE-PERSISTENCE-ADMISSION-01 — independent offline SQLite verification

**Date:** 2026-10-23. **State:** DESIGN FROZEN before implementation and any test execution. **Authority:** read-only evaluation of Supabase; offline synthetic SQLite standard-library engineering research only. **Budget:** $0. No live database writes, tables, project creation, auth integration, listening, participant data, physical farm controls or cloud deployment.

## Evidence boundary

Muse's report describes a SQLite reference database, 18 tests and ten adversarial cases, but **source, full report and database bytes were not supplied to this conversation**. No code in this package is a replay of Muse's implementation. The connected Supabase organization is visible, but `list_projects` returns **[]**, so Supabase inspection, security checks, and actual authorization are NOT RUN.

## Single useful question

Can one small durable **local** relational journal preserve untrusted correction proposals, allow version-checked logical commits *only via a separately modeled host confirmation path*, survive crash/retry without duplicate logical changes, and retrieve contradictory source attributions **without hiding any evidence**? This is a deterministic synthetic engineering benchmark, not proof of actual user identity, security, acoustic perception or farm readiness.

## Frozen schema/policy

- `farms`, `memberships`, `tasks`, `task_values`: stable farm- and referent-scoped task identifiers, field version, role membership.
- `speech_proposals`: untrusted suggestions; at ingress no database task-value mutation; unique event identifier with exact-payload idempotency, active/void/committed status; `supersedes` tentative only until host confirmation.
- `confirmations` and `value_history`: immutable logical commit receipts, one-time command identifier unique across retries; `BEGIN IMMEDIATE` and expected-value/version compare-and-set.
- `event_assertions`: append-only individual event-to-object association claims and evaluator judgments. Query **all** claims in an event, displaying disagreements even where a disputed claim has higher confidence. Never use top-1 similarity/confidence to suppress counterevidence. No original audio or private personal information in fixtures.
- No `anon` or `authenticated` direct-data access is implemented in SQLite; this package is NOT an RLS test. `principal` is an injected synthetic test role, not real Supabase Auth.

## Fixed test categories

1. Pending proposal survives reconnect/restart; untrusted ingest changes no task value.
2. Exact host-confirmed change increments logical version once, retries with same key never increment twice, different payload using same key refuses.
3. Two contenders on same field and old version: one can commit; other rejects after stale CAS.
4. Linked supersession is inert at speech ingest and atomically voids old pending state only on valid host confirmation; reject cross-referent/cross-farm links.
5. Wrong principal/cross-farm member cannot confirm or query a different farm's sensitive records. Treat membership as MOCK, not production authentication.
6. Inject failures before/inside/after SQLite transaction boundaries and restart. Before durable COMMIT nothing applied; after COMMIT retry is idempotent. Limit claims to simulated faults; not power-failure fsync or SQLite file corruption.
7. Evidence assertion conflicts remain visible: same farm/event, high confidence disputed source A versus lower confidence source B, exact source hashes and independent status remain intact; append-only trigger blocks UPDATE/DELETE.
8. Unknown source or echo claim never by itself constitutes authorization. Manual host-entry may commit even when there was no accepted microphone proposal.

## Admission and STOP criteria

- Local standard library tests actually run and pass, with reproducible command, interpreter version, source SHA256, and receipts.
- Distinguish original Muse candidate **NOT RUN**, live Supabase **NOT RUN**, auth/RLS verification **NOT RUN**, and local synthetic reference **RUN** if actually executed.
- Any direct untrusted confirmation path, stale-value overwrite, phantom cross-farm read, hidden contradictory source association, or duplicate logical commit forces REPAIR.
- Do not build pgvector, public audio buckets or paid cloud resources. Proposal for eventual Postgres/RLS should be **DESIGN ONLY**, with user-scoped membership checks, explicit database grants, trusted authentication, and minimal use of privileged functions.