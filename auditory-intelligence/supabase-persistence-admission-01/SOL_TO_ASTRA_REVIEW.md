# SOL → ASTRA | SUPABASE-PERSISTENCE-ADMISSION-01 — independent executable audit

**From:** Brian & Sol · **Date:** October 23, 2026 · **Status:** $0 offline-only scientific / engineering DEV · **Live Supabase:** NOT RUN · **Muse SQLite:** NOT RUN · **Our independent SQLite:** RUN LOCAL · **Farm deployment:** HOLD

## Evidence transfer

**Brian must attach two distinct packages** if available:

1. **Muse's ORIGINAL** SUPABASE-RESEARCH-01 source, SQLite DB, tests and reports. Muse reported an 18-test offline SQLite investigation, but those exact source bytes **have not been supplied to Sol**. Do not call a reconstruction of Muse's implementation a replay.
2. **Sol's independent package:** `SUPABASE_PERSISTENCE_ADMISSION_01_2026-10-23.zip`, SHA-256 `5f3f49397757b5ab685417337d637f80761484f7d2cc163aa3b5fc4ca758a301`, delivered to Brian in the conversation. Its `store.py` SHA-256 is `9d664e2c94ab3e0e0bb032f584252b9d3961328a673d82d11834bed259fa0cef`, `tests/test_store.py` SHA-256 `33ee371f3a5311085e1b87c52287a3165f314ce4a0087680c370b58690fc00d5`.

```sh
unzip SUPABASE_PERSISTENCE_ADMISSION_01_2026-10-23.zip -d independent
cd independent
python -m unittest discover -s tests -v
python demo.py
sha256sum -c receipts/CHECKSUMS.sha256
```

Sol executed **33/33 tests on Python 3.13.5, SQLite 3.46.1**, and a synthetic demonstration. Original committed contract was frozen before implementation; this code is exposed DEV, not independent blind confirmation. The portable ZIP contains source and exact local receipts, but the GitHub PR includes **documentation only**, not the implementation code. Do not claim GitHub source CI qualification.

## What is measured

- An untrusted speech proposal remains pending without changing a task field, even when `source_claim` is confidently wrong.
- A **mock membership-controlled host-change function** applies an exact expected-value/version CAS atomically with one confirmation receipt and value-history append. Duplicate command IDs return the stored result; differing same-ID payloads reject.
- Pending work survives reconnect. Simulated exceptions at three inside-transaction boundaries roll back, and an actual child process terminated with `os._exit(79)` before SQLite commit leaves the transaction undone. A response deliberately lost after commit is resolved by replaying the same idempotency ID.
- Two concurrent threads confirming from the same version yield one commit and one stale rejection on this machine; no distribution/network test.
- A conflicting pair of assertions on the same acoustic event—the higher-confidence one marked `DISPUTED` and a lower-confidence one marked `SUPPORTED`—remains fully retrievable as two source-object association records, with group-level `source_conflict`, `has_dispute`, `requires_review`.
- The package deliberately demonstrates its own weakness: anyone with raw access to the SQLite file can directly query/modify data and bypass the Python membership checks. A `principal` string and boolean `reviewed` are **not** identity or an actual trusted UI gesture.

## Your independent adversarial assignment

A — **Evidence and reproduction.** Hash and replay the exact Sol ZIP. If Muse's ZIP is supplied, reproduce that separately and attribute differences by implementation. Confirm 33 cases and active code version; use the exact stdout. State what was and was not run.

B — **Trust boundary attacks.** The mock `host_change()` is callable as an ordinary Python method, and `seed()`/`add_member_fixture()` are same-process helpers. Demonstrate why a client-facing implementation cannot expose these methods or direct database-write credentials to transcript ingestion. Demand independent Supabase Auth and a truly separated trusted host route; don't claim a hard security boundary exists here.

C — **Idempotency and transaction failure.** Attack command-ID reuse with modified principal/farm/content/expiration, uncertain response after COMMIT, duplicate requests, alternate principal, and out-of-order host transactions. Check that rejected commands cannot leak confirmation existence to an unauthorized actor. Separate simulated exception rollback, OS process crash, real disk corruption, fsync/power loss and hosted Postgres serializability; no overclaiming.

D — **Source identity / evidence counterexample.** Test the actual claim pair using source `obj-gate-north-001` vs `002`: one `0.98/DISPUTED`, other `0.64/SUPPORTED`. Can any ordinary retrieval or join hide the disputed record? Test another assessor adding a later contradiction, and confirm the append-only triggers block updates/deletes. Check what happens if caller forges `evaluator_id` or lies about `source_sha256` — the implementation does not verify raw audio bytes.

E — **Referent ambiguity.** Same display label, distinct referent IDs. Cross-farm object or proposal IDs. Supersession must be explicitly linked, monotonic in observation time, and only become final at host-confirmed commit. Try a pending source claim that is already stale when presented.

F — **Schema constraints and real RLS feasibility.** Review proposed [Postgres design](supabase-persistence-admission-01/POSTGRES_DESIGN.md) against current Supabase documentation: Data API grants + RLS, membership isolation, authenticated viewer/editor capabilities, no `anon` for private tasks, no exposed `SECURITY DEFINER` or service role assumed safe. Test actual policies only after separate project access and approval; until then **NOT RUN**. No project creation.

G — **Accessibility and offline continuity.** Verify manual host edit without audio, pending/committed work under offline replay, and external write conflict after reconnection. Distinguish **exactly-once local logical mutation** from guaranteed user notification, actual authentication, or durable replication.

H — **Smallest repair.** Find at least one concrete false-assurance case with executable probe. Do not simply expand the schema or propose vector search. Recommend GO/REPAIR/STOP **for offline prototype quality only**; cloud authorization, real acoustic source and field control remain HOLD.

## Scientific caution

Retaining counterclaims protects auditability; it does not authenticate evaluators or establish physical source truth. The experiment's "confirmed" logical edit is only a locally simulated trusted host operation, not real human authorization. No Supabase databases were created or modified.

**End your response:** `ASTRA → SOL | SUPABASE-PERSISTENCE-ADMISSION-01 | INDEPENDENT AUDIT — EXECUTION STATUS EXPLICIT`
