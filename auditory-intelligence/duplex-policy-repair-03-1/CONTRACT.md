# DUPLEX-REPAIR-03.1 — supersession atomicity regression gate

**October 23, 2026. Synthetic/mock-only development.** v03 remains frozen as a reproducible counterexample. This is a small, nonblind source/test repair, not independent confirmation. $0 cost.

**Failure contract:** Untrusted speech may *request* or *link* a supersession but cannot revoke an already pending transaction. It cannot grant user authority, identify acoustic sources or authenticate a host principal. The recognized linked event's `observed_ms` must postdate its target; both must have same explicitly supplied thread, referent, and matching known field.

**Atomic host confirmation contract:** Host port must verify exact `(field,new,rejected)` contents, originating referent, original logical field value and version at confirmation time, with separately supplied authority. Before logical commit, recheck the pending predecessor link; if predecessor was already committed or withdrawn, reject new transaction. If accepted, mark old proposal VOID and new COMMITTED at same host event; never silently mutate task state from speech alone.

**Negative tests:** unknown-source `supersedes` cannot void; confirmed replacement can void once; stale replacement after target committed is refused. Include 54 prior mock regressions unchanged. The synthesized host authorizer is not real authentication and is not resistant to arbitrary in-process Python execution. Speech source labels are externally supplied mock metadata, not acoustic measurements.

**HOLD:** real assistant echo discrimination, user identity/role evidence, crash-safe journal, natural ASR quotes/revisions, proper UI authentication, human accessibility evaluation, speech-native inference and farm operation.
