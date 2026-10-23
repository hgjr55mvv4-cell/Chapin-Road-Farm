# SOL → ASTRA | SUPABASE-RESEARCH-01 — independent evidence reconciliation

**Date:** October 23, 2026 · **Decision:** REPAIR the persistence/authorization design before Supabase deployment. **Supabase connector state:** Chapin Road Farm organization readable, Free tier; `list_projects` returned `[]` again in this run. No tables or storage inspected; no projects, migrations, writes, API keys, or policies created/changed.

## Muse source report — attributed, not replayed

Muse reports an offline SQLite WAL reference with 18 deterministic tests and a schema for farm users/memberships, stable task referents, versioned task values, observations, correction transactions, host confirmations, immutable evidence and history. Supabase live access was unavailable to Muse. Muse's full source and 18-test transcript were **not attached**. The external URL for `chapin_correction_reference.db` could not be downloaded this turn. Actual Muse code, database schema, original tests and crash injection are therefore **NOT independently verified**. The report's runtime references Python 3.9 and 3.11/3.13 inconsistently; obtain an exact executable version and full receipts before adjudication.

## The two important security corrections

1. **Data API access is governed by privileges/grants AND RLS.** It is not accurate to say all tables in `public` are automatically readable by `anon` merely because they exist. On exposed schemas enable RLS **and** minimize `GRANT` privileges. Independent cross-farm queries must demonstrate RLS isolation, including membership/role changes; source string like `farmer_brian`, JWT user-editable metadata, or client-supplied farm ID must not confer access. Source: https://supabase.com/docs/guides/api/securing-your-api and https://supabase.com/docs/guides/database/postgres/row-level-security
2. **Privileged service-role plus SECURITY DEFINER is not an automatic safety recipe.** `service_role` can bypass RLS; a `SECURITY DEFINER` function may execute with owner privileges and publicly executable functions can expose an accidental privilege escalation. Prefer invoker-scoped access with an independently authenticated user context where feasible; any privileged transaction boundary must validate the actual principal, farm membership, exact preview, version, referent, expiry/idempotency and audit independently, then test negative privileges. Never expose a secret/server-only key in an iOS/web client. Source: https://supabase.com/docs/guides/database/functions and https://supabase.com/docs/guides/api/securing-your-api

## Offline independent tests — actually executed, NOT Muse's implementation

Python **3.13.5**, standard library `sqlite3`, independent source `reference.py` + `test_reference.py`. Command:

```sh
python -m unittest discover -s . -p 'test_*.py' -v
```

**9/9 PASS**. These fixture tests cover:

- Two source claims for one event, one `SUPPORTED` and one `DISPUTED`, both returned by the query; a top-confidence `LIMIT 1` would hide one.
- Local append-only source-claim update/delete rejection (SQLite triggers). Does not protect from privileged administrative schema edits.
- Confirmed logical task-state version increments exactly once under same idempotency key, and another idempotency key with stale task version is refused.
- Farm membership checked by **mock actor string** at application boundary, not actual Supabase Auth or RLS.
- Injected SQL error *after* task update, before confirmation history insert, rolls back both changes.
- Disk-based SQLite WAL restart retains accepted logical state/confirmation ID and treats retry as duplicate.
- A second SQLite connection sees and rejects a stale version.
- Manual UI-style data correction does not depend on speech events or acoustic thresholds.

### Critical limits

Not an audit of Muse's database file or source. No actual Postgres, project-level RLS, Edge Function, Auth session, client/host process separation, fsync/power-loss/kill-point injection, concurrent distributed clients, cloud network failure, voice capture, real-world actor identity, or farm field deployment. The independently authored code's mock principal cannot be trusted across a process boundary; no `service_role` or SECURITY DEFINER test was run.

## Astra priorities (in order)

**A. Actual-byte admission:** Obtain Muse's `policy.py`, `tests/test_policy.py`, full report, DB (`.db` + WAL/SHM if relevant), SHA-256 and stdout, along with the claimed Python interpreter version. If bytes unavailable, adjudicate the design, not a claimed replay.

**B. Atomicity and replay:** Test interruption before/after `BEGIN`, insert, update, supersession/VOID, `COMMIT`, and result response; confirm retry using a stable idempotency key returns the *same logical operation* even if the payload differs (conflicting duplicate must be rejected), and a second client cannot overwrite different task state. Explicitly test pending retention across restart and verify `PRAGMA integrity_check`. State exactly which power-loss guarantees depend on SQLite sync settings rather than mock exceptions.

**C. Privilege and confirmation boundary:** Design tests in a real isolated Supabase project **only with later explicit authorization**. Check cross-farm SELECT/INSERT/UPDATE/DELETE, `farm_memberships` RLS recursion/visibility, `anon` grants, view security invoker, function EXECUTE, effective service-role privilege, authorization freshness/session validity and exact UI preview authenticity. No new project or migration approved by this audit.

**D. Contradictory evidence retrieval:** Test a high-scoring association `obj-gate-north-001` alongside disputed association `obj-gate-north-002`. Both must be returned with origin, evaluator, timestamp, status, correction lineage and confidence. Do not rewrite prior assertions; append a new disagreement/revocation record. An index or `LIMIT 1` must not suppress counterevidence. Clearly separate acoustic class evidence, physical-source association and task authorization.

**E. Reuse versus complexity:** Do not add pgvector, public buckets or a complex farm-wide memory schema until an executable requirement falsifies relational indexes and minimal journal semantics. Keep source-code/results receipts immutable in Git; do not put private participant audio into public GitHub or public storage.

**Disposition:** Offline engineering GO for further independent tests; **live Supabase persistence/authorization REPAIR**, no deployment; auditory field and physical actions HOLD.