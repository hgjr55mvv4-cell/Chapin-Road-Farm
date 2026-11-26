# Artifact-reference lookup, DEV interface 1

Invoke `python3 validate_refs.py REPOSITORY`. Supply one UTF-8 JSON object on stdin with exactly two members, `commit` and `paths`. Duplicate JSON members are ambiguous. A repository is the supplied worktree root, linked worktree root, bare repository or Git directory. Lookup uses local objects and ignores Git environment overrides, replacement objects, and the index.

* `commit` is a full hexadecimal object ID in the repository's storage format (40 for SHA-1, 64 for SHA-256, either case). A locally identified non-commit, including an annotated tag, is invalid. An unavailable commit leaves the answer unknown. Named or abbreviated revisions are invalid.
* `paths` is a nonempty ordered JSON array of strings. Use exact root-relative Git names encoded in UTF-8. Slash separates components. Empty components, dot, dot-dot, NUL and unpaired surrogates are invalid. Spaces, backslashes, newlines, Git metacharacters and leading hyphens are literal. No filesystem normalization or fallback. The input is validated as a whole before any lookup. Repeated paths are permitted and each occurrence receives a row.
* PRESENT means the exact named tree entry exists. Rows give its Git mode, advertised type and object ID. Trees, symlinks and gitlinks are entries too. Traversal continues only through trees. The existence of a leaf entry does not require its payload or a submodule checkout. Evidence needed to read a parent tree must be available. Unrelated subtrees need not be readable.
* One JSON report goes to stdout. A resolved commit is identified even if a necessary tree later proves unreadable. A rejected request or unavailable commit has zero rows. After resolving the pin, inspect every requested path in order, including when only some lookups are decidable.

| Verdict | Exit | Meaning |
|---|---:|---|
| PRESENT | 0 | Every requested entry exists at the pin. |
| MISSING | 1 | At least one entry is absent and all required trees were readable. |
| INVALID_INPUT | 2 | Malformed request, wrong pin type/format, or incorrect invocation. |
| EVIDENCE_UNAVAILABLE | 3 | Repository, Git, commit, or a required tree cannot supply an answer. Takes precedence over MISSING for mixed rows. |

The evidence is limited to tree membership. Content availability, meaning, completeness against an external inventory, authorization and execution require their own evidence. Assumes a trustworthy local Git executable and repository. DEV scope is bounded handoffs and ordinary-size trees, with no streaming, resource-exhaustion guarantee, cryptographic object audit, or coverage for arbitrary non-UTF-8 filenames.
