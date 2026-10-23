# Proposed Supabase/PostgreSQL migration boundaries — DESIGN ONLY

**NOT DEPLOYED.** Zero project IDs available. Nothing here certifies RLS, authentication or any live database feature. Consult current Supabase documentation and test real role-specific policies once a project is authorized.

## What to preserve

Stable farm IDs and task referent IDs, not just display names; row-versioned current task values; untrusted speech proposals; separate confirmation receipts carrying immutable canonical request hashes; append-only correction history; all evidence assertions including contradictory claims. A dispute belongs to an assertion, not the shared event record; a later conclusion never deletes prior evidence.

## Proposed authorization architecture

1. An actual authentication provider verifies user sessions and assigns a stable principal. **Never treat microphone speaker labels or user-editable JWT metadata as authorization.**
2. A *trusted server-side host route* (not the transcript-ingestion API) proves a user reviewed the exact field, referent, old/new value, original version and confirmation token, checking expiration and nonce reuse. Offline synthetic `reviewed=True` and `principal` strings are not such proof.
3. Use the calling user's authenticated context plus farm-membership checks. For browser/mobile reads and user-accessible exposed tables, combine **minimal grants** with **row-level security**. Authenticated-only without ownership filtering is not authorization. Exclude `anon` unless public data specifically requires it.
4. For logical value updates, use one narrowly scoped SQL transaction (`SELECT ... FOR UPDATE`, CAS expected version, one confirmation id, immutable receipt/history, tentative supersession resolution) behind a reviewed trusted endpoint. **Prefer `SECURITY INVOKER`**; any use of a privileged service role or `SECURITY DEFINER` requires a separate threat review, explicit JWT validation and farm-scoped checks, a locked-down search path and revoked unnecessary EXECUTE grants. A `service_role` connection bypasses RLS, so it is *not* automatically a security measure.
5. RLS on all exposed tables, with `USING` and `WITH CHECK` as appropriate; policies must be tested as multiple real users and farms. Never assume a SQLite membership helper is an RLS test.
6. File and public exposure: no public audio buckets. If assets are needed later, private storage, attribution evidence, explicit retention/consent controls and storage-object policies must be reviewed first. No pgvector until ordinary relational retrieval is proven insufficient.
7. Crash and notification semantics: PostgreSQL commit atomically persists state and confirmation, but network uncertainty after COMMIT still requires a caller-supplied durable idempotency key. Exactly-once logical change does **not** guarantee exactly-once audible or UI notification.

## Specific falsifiers to run only after authorizing a live project

- `anon` user attempts to read protected farm task/evidence; fail.
- Authenticated farm-A editor attempts read/change farm-B task/evidence; fail.
- Authenticated farm-A viewer tries to commit; fail.
- A transcript-derived role/identity input attempts direct Data API value update; fail.
- Two authenticated sessions concurrently confirm different values from version N; one logical commit maximum.
- Lose the HTTP result immediately after COMMIT and resend same exact confirmation ID: stored result returned without second mutation.
- A high-confidence disputed source claim and lower-confidence counterclaim both show in the authorized evidence view.
- Attempt to call a privileged function as `anon`, as a wrong-farm account, or with forged ownership, and ensure least privilege holds.

## References (current as inspected 2026-10-23)

- https://supabase.com/docs/guides/api/securing-your-api — grants + RLS, not one without the other
- https://supabase.com/docs/guides/database/postgres/row-level-security — exposed-schema RLS
- https://supabase.com/docs/guides/database/functions — prefer invoker security; limit privileged functions
- https://supabase.com/docs/guides/getting-started/api-keys — API keys identify app component; Auth establishes human principal

**Recommendation:** keep current effort SQLite/offline, gather Muse's exact source bytes, then independently verify tests. Cloud project creation, schema migration, service role provisioning and policy changes require explicit separate approval.