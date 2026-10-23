# HARBOR-HARD-NULL-01 — reported negative result and independent mathematical check

**Astra result:** human-relayed engineering report; upstream executable ZIP **not received in the currently available attachments**. **Our code here is Sol-authored arithmetic only**, NOT Astra's `hard_null.py`, and cannot reproduce five-family simulations or case-level CSV output.

- [Attributed report digest](../docs/ASTRA_HARD_NULL_01_RELAY_DIGEST.md)
- [Sol independent scientific review](../docs/SOL_HARD_NULL_01_ADJUDICATION.md)
- [Original LOOM-01 symbolic DEV implementation](../loom-01/README.md)

## Run Sol's independent check

```sh
cd harbor-co-listener/hard-null-01
python -m unittest discover -s tests -v
python collision_check.py
```

The check calculates `(0.7² + 7 × (0.3/7)²)^3 ≈ 0.127155` for exact three-phrase collisions **if** three phrase positions and two songs are sampled independently from the stated distribution. This implies approximately 260.4 expected exact collisions in 2,048 pairs; the relayed Astra report says 274. It also recomputes its 565/2,048 null-alert proportion and Wilson interval, and checks that 274 + 291 = 565.

Sol locally ran **5/5** deterministic unit tests in Python 3.13.5/Linux. [Independent local output](receipts/sol_arithmetic_2026-10-23.json) is a re-computable arithmetic receipt, **not** original Astra execution evidence. Github CI will verify the submitted code independently when enabled.

## Archive intake blocker

The relayed report mentions `hard-null-01` source, tests, 30,710 pair rows and 49,088 candidate rows in a downloadable package, but no usable download link or file bytes were attached to the message visible here. **Do not misstate this folder as the original archive.**

When a rights-cleared archive is delivered:
1. Preserve the exact ZIP and its SHA-256. Inspect file membership, origin/license, paths and any sensitive material before adding anything public.
2. Freeze upstream source/receipts as obtained; note any newline differences and don't edit originals to make them pass.
3. Execute the advertised original commands, capture full stdout/stderr, version and exit codes, independently recalculate per-population and query-level counts.
4. Add a separate post-replay status document; if results fail, publish the discrepancy rather than overwriting the reported digest.

No original archive recovery is implied by this README. The code here uses only standard Python, no paid model calls, no audio or participants.
