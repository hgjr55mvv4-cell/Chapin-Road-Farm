# Selective verification — triage-metric DEV

**Status:** executable engineering demonstration, not calibrated model performance. No real agents, paid inference, or actual human adjudication.

Run from `agent-collaboration-lab/oracle-integrity-dev`:

```sh
python -m unittest discover -s metric_tests -v
```

The module `selective_metrics.py` scores an externally adjudicated candidate as `valid`, `faulty`, or `unknown`, and records each verifier's `ACCEPT`, `REJECT` or `ABSTAIN`. It maintains separate denominators:

- **Coverage**: proportion of adjudicated items on which a decision is made.
- **Selective error**: false accepts + false rejects divided by *all decisions*.
- **False assurance, all faulty**: faulty items accepted / all adjudicated faulty items, including abstentions in the denominator.
- **False assurance, decided faulty**: faulty items accepted / faulty items actually accepted or rejected.
- **False rejection** analogues for adjudicated valid items.
- Abstention rates for valid and faulty populations; unknown truth cases counted separately, never silently relabeled.
- **Undefined rate** returns JSON-compatible `None` when the relevant denominator is zero; it is **not** “0% error.”

The public illustrative aggregator `conservative_parallel` rejects if **either** reviewer rejects, otherwise abstains if either abstains, otherwise accepts. This can lower false assurances **while also rejecting valid work**; the code does not assert this aggregation is optimal, safe, or empirically beneficial.

The synthetic test example has **4 valid, 8 faulty and 1 unresolved-truth** record: 8 adjudicated decisions, coverage 8/12, false assurance of faulty = 2/8 (all faulty) or 2/5 (decided faulty). Five executable unit tests cover these rates, all abstention, zero denominators, invalid truth, and aggregation mechanics.

The original `oracle-integrity-dev` scripts return only accept/reject on fixed fixtures; this separate scorer proposes an *interface* for future study. It does not retroactively upgrade the 4/4 and 6/6 engineering fixture to a three-way oracle. Thresholds and risk-cost weights must be frozen under an independently reviewed later protocol; no percentages here are scientific GO criteria.
