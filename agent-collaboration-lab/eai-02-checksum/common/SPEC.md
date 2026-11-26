# Offline checksum-manifest CLI · specification v1

Invoke `python3 check_manifest.py ROOT MANIFEST` with exactly two arguments. Read the manifest once, verify the listed files and write one UTF-8 JSON object followed by a newline to stdout. Use the process exit in the table below. JSON member ordering and insignificant whitespace are free. The command is read-only and operates offline.

## Manifest and file identity

* MANIFEST is a local, readable regular file containing strict UTF-8 JSON without a BOM. The top level has exactly one member, `entries`, a nonempty array. Each element is an object with exactly two members, `path` and `sha256`. Both values are strings. Reject duplicate JSON member names at every level, extra members, invalid UTF-8, unpaired surrogates, trailing non-whitespace and nonstandard JSON constants.
* A digest is exactly 64 lowercase ASCII hexadecimal characters. A path is a nonempty sequence of Unicode scalar values encoded as UTF-8. On the supported POSIX filesystem, U+002F separates components. Reject NUL, empty components, and components equal to dot or dot-dot. This rules out absolute paths and trailing slashes. No trimming, escaping beyond JSON decoding, case folding, Unicode normalization, globbing or expansion. A backslash is a literal filename character.
* Within one manifest each decoded path string must be unique. A repeated path invalidates the whole manifest, including when the digests agree. Distinct names may refer to hard links or carry the same digest.
* Hash all bytes read from each readable regular file with SHA-256, starting at offset zero and continuing to EOF. Compare the 32-byte result represented in lowercase hex. Empty files are valid. Preserve all bytes, including line endings, encoding markers and final newlines. The file's name and metadata are outside the digest.

## Boundary and availability

ROOT and MANIFEST are trusted operator-selected paths. Resolve relative arguments against the invoking directory using ordinary POSIX rules, including symlinks in those two arguments. The resolved ROOT must be a directory with search (execute) access for the process. Directory-listing access is unnecessary. MANIFEST may be outside ROOT. Each entry starts at the resolved root. Follow only directory components and finish at a regular file. A symlink encountered anywhere in an entry (including an internal or dangling link) makes that row UNAVAILABLE. Do not open its target. A non-directory intermediate component or non-regular leaf is also UNAVAILABLE. Do not open special files to determine their contents.

An absent component within an otherwise inspectable path yields MISSING. Permission denial or another inspection, open or read error yields UNAVAILABLE. Use access actually obtained by the process. Evaluate every row in input order. Scope is stable, bounded synthetic files on a case-sensitive, byte-preserving Linux filesystem under an ordinary unprivileged user. Concurrent mutation, mounts changing during a run and adversarial races are outside this experiment.

## Output and precedence

The report has exactly two top-level members, `verdict` and `rows`. Each row has exactly `path`, `status` and `observed_sha256`. Use the submitted path verbatim after JSON decoding. MATCH and MISMATCH carry the actual lowercase digest. MISSING and UNAVAILABLE carry JSON null. A matching report establishes equality to the digest supplied for that path at read time. Authenticity, authorization, semantic correctness and completeness against another inventory require separate evidence.

| Order | Condition | Verdict / exit | Rows |
|---|---|---|---|
| 1 | Wrong argument count or an empty argument string | INVALID_INPUT / 2 | Empty |
| 2 | MANIFEST is absent, inaccessible, non-regular or cannot be fully read | UNAVAILABLE / 3 | Empty |
| 3 | Any manifest syntax, schema, digest, path or uniqueness rule fails | INVALID_INPUT / 2 | Empty, validate the complete manifest before inspecting ROOT |
| 4 | ROOT cannot be resolved or is inaccessible or non-directory | UNAVAILABLE / 3 | Empty |
| 5 | At least one entry is UNAVAILABLE | UNAVAILABLE / 3 | All rows |
| 6 | Otherwise any row is MISSING or MISMATCH | FAILED / 1 | All rows |
| 7 | Every row is MATCH | VERIFIED / 0 | All rows |

**Exposed DEV example.** For a file named `sample` containing the three bytes `61 62 63` (hex), this manifest yields VERIFIED / 0 and one MATCH row with the given digest.

```json
{"entries":[{"path":"sample","sha256":"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}]}
```
