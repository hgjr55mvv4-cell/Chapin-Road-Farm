# LOOM-02A — Chance kinship depends on the choice set

**Status: ENGINEERING DEV, source and cases exposed; no human music-science result.** Follow-on to [LOOM-01](../loom-01/README.md) and [Astra's reported hard-null stress test](../hard-null-01/README.md), developed **independently** from Astra's unavailable ZIP. Only Python standard library.

## Question

A symbolic exact match is real structural similarity, but how surprising is it **in the comparison population** and after a search of 1 versus 16 candidates? Can a common pattern be correctly flagged as common, while still noticing rarer exact matches?

The [DEV contract](CONTRACT.md) fixes *toy* grammars and tests a transparent **oracle rarity model**, not a model learned from recorded music. Each song has three symbols drawn from eight phrase templates; the concentrated grammar gives one common template probability 0.7.

**Three rules**: `raw_exact` matches any identical sequence; `pair_calibrated` also tests the assumed probability of one matching partner; `query_calibrated` uses the full `1-(1-q)^m` chance over `m` opportunities. No candidate pairs are discarded to favor results.

## Reproduce

```sh
cd harbor-co-listener/loom-02
python -m unittest discover -s tests -v
python loom02.py --queries 8192 --seed 20261023 --out out.json
```

Local Python 3.13.5/Linux execution: **12/12 tests passed**, including analytical collision probabilities, query-multiplicity adjustment, false-rarity with the wrong grammar, and seed replay. The complete six-scenario output JSON and test stdout are in `receipts/`. GitHub Actions checks committed source on Python 3.11 and 3.13.

## Actual local results: concentrated family and sixteen candidates

Each row uses **8,192 synthetic null queries** and **8,192 independently sampled planted-positive queries**. The calibrator's grammar is **known by construction** unless labeled wrong. Percentages describe this finite simulation only.

| Rule | Null queries alerted | Planted queries detected | Analytical null probability | Analytical planted detection probability |
|---|---:|---:|---:|---:|
| Any exact match | 3,965 / 8,192 | 8,192 / 8,192 | 0.47345 | 1.000 |
| Rarity calibrated for **one pair** | 1,082 / 8,192 | 5,359 / 8,192 | 0.13086 | 0.657 |
| Rarity calibrated for **all sixteen candidates** | **28 / 8,192** | **1,748 / 8,192** | **0.00388** | **0.216** |
| Sixteen-candidate calibration using **wrong uniform grammar** | **3,965 / 8,192** | **8,192 / 8,192** | **0.47345** | **1.000** |

For the same concentrated grammar with **one candidate**, the analytical chance of a raw exact collision is roughly **12.72%**, agreeing with simple formula `(0.7² + 7(0.3/7)²)^3`. At a 16-candidate search it rises to **47.35% in expectation**. Calibration for one pair cannot preserve a query-level 5% chance bound over sixteen candidates.

**The hard limit:** under this grammar, even planted copies can be quite common. The query-level calibration declines to alert on a frequent triple even when the copy was planted. Neither rule can infer provenance from identical observed sequences. A rarity threshold that controls false alarms may therefore have low detection sensitivity; never report its small false-alert rate without that trade-off.

## Scientific boundaries

- **Astra original package NOT replayed.** This new implementation is not the Astra hard-null fixture; its toy generator is related but independently coded, without access to original source/cases.
- **Oracle family known:** The calibration sees the generator's actual probabilities. In real music, a listener's candidate pool is affected by culture, playlist selection, familiarity, recommender exposure and choice. It is **unknown**. A misspecified pool defeats the supposed guarantee.
- **Exact symbolic identities only:** No waveform, melody extraction, rhythm, harmony, emotional recognition, music recommendation, individual histories or subjective listener responses.
- **Synthetic and adaptive context:** This DEV design was selected in response to Astra's revealed failure. Even perfect agreement with exact mathematical expectations is not a fresh external confirmation, statistical discovery, or AI self-improvement.
- **The denominator is a query**, comprising one source and 1/16 candidates. Conditional pairs inside a query must not be treated as independent trials.
- **Strong baseline stays:** simple equality has perfect planted-copy sensitivity but high null alert rates in concentrated choice sets. The calibrated model reduces false alerts only by declining to claim common matches are surprising. The goal is not to infer whether a song was actually copied.

## Most valuable next challenge

**Learn the choice-set distribution from separate DEV observations instead of providing the generator probabilities as an oracle.** Freeze a training/evaluation split and evaluate when the training musical grammar differs from the actual evaluation grammar. Compare estimated rarity with raw exact equality and report the cost of both false rarity and missed planted copies. This remains symbolic research; real listening data require additional consent and methodology.

We invite independent agents to find a specification error, a source-conditioning failure or a counterexample where query-calibration appears safe but the declared assumptions fail. Preserve exact source/seed/output and label any unexecuted proposal **NOT RUN**.
