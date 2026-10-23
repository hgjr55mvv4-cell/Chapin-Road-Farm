"""LOOM-02A: conditional exact-pattern rarity versus search scope.

Pure symbolic DEV. Oracle knows true generator template weights by construction.
Neither structural coincidence nor rarity establishes ancestry or personal meaning.
"""
import argparse
import itertools
import json
import math
import random

VERSION = 'LOOM-02A-v0.1-EXPOSED-DEV'
ALPHA = 0.05  # fixed before outcomes; chosen illustration, not a science gate
N_TEMPLATES = 8
PHRASES = 3
FAMILIES = {
    'uniform': tuple([1 / 8] * 8),
    'concentrated': (0.7, *([0.3 / 7] * 7)),
}


def validate_weights(weights):
    if len(weights) != N_TEMPLATES or any(not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x) or x < 0 for x in weights) or not math.isclose(sum(weights), 1, rel_tol=0, abs_tol=1e-10):
        raise ValueError('expected eight finite nonnegative weights summing to one')


def source_probability(source, weights):
    validate_weights(weights)
    if len(source) != PHRASES or any(type(x) is not int or not 0 <= x < N_TEMPLATES for x in source):
        raise ValueError('source must have exactly three template indices 0..7')
    return math.prod(weights[x] for x in source)


def any_exact_probability_given_source(source, weights, opportunities):
    """Null probability that >=1 of m independent candidates exactly matches source."""
    if type(opportunities) is not int or opportunities < 1:
        raise ValueError('opportunities must be a positive integer')
    p = source_probability(source, weights)
    # More stable for small p than 1-(1-p)**m.
    return -math.expm1(opportunities * math.log1p(-p))


def source_space():
    return itertools.product(range(N_TEMPLATES), repeat=PHRASES)


def analytical_rates(true_weights, assumed_weights, opportunities, alpha=ALPHA):
    """Exact enumeration over the 8**3 source sequences; one source per query.

    FPR = sum(P(source) * P(any exact match | source) * I(alert-eligible)).
    TPR = sum(P(source) * I(alert-eligible)) when one exact is planted.
    """
    validate_weights(true_weights)
    validate_weights(assumed_weights)
    if type(opportunities) is not int or opportunities < 1 or not 0 < alpha < 1:
        raise ValueError('invalid opportunities/alpha')
    agg = {k: {'null_alert_probability': 0.0, 'planted_detection_probability': 0.0} for k in ('raw_exact', 'pair_calibrated', 'query_calibrated')}
    for source in source_space():
        p_src = source_probability(source, true_weights)
        p_any = any_exact_probability_given_source(source, true_weights, opportunities)
        q = source_probability(source, assumed_weights)
        p_query = any_exact_probability_given_source(source, assumed_weights, opportunities)
        eligible = {'raw_exact': True, 'pair_calibrated': q <= alpha, 'query_calibrated': p_query <= alpha}
        for rule, allowed in eligible.items():
            if allowed:
                agg[rule]['null_alert_probability'] += p_src * p_any
                agg[rule]['planted_detection_probability'] += p_src
    return agg


def sample_song(rng, weights):
    return tuple(rng.choices(range(N_TEMPLATES), weights=weights, k=PHRASES))


def choose_alert(source, candidates, assumed_weights, opportunities, alpha=ALPHA):
    if len(candidates) != opportunities:
        raise ValueError('candidate count mismatch: do not silently change search scope')
    hit = any(source == c for c in candidates)
    q = source_probability(source, assumed_weights)
    p_query = any_exact_probability_given_source(source, assumed_weights, opportunities)
    return {
        'raw_exact': hit,
        'pair_calibrated': hit and q <= alpha,
        'query_calibrated': hit and p_query <= alpha,
    }


def simulate(true_weights, assumed_weights, opportunities, n_queries, seed, alpha=ALPHA):
    validate_weights(true_weights)
    validate_weights(assumed_weights)
    if type(n_queries) is not int or n_queries < 1 or type(seed) is not int or type(opportunities) is not int or opportunities < 1:
        raise ValueError('invalid simulation parameters')
    # Independent null/positive streams; no matched pairs discarded; chance exact matches count.
    null_rng, planted_rng = random.Random(seed), random.Random(seed + 1000003)
    counts = {r: {'null_alerts': 0, 'positive_detections': 0} for r in ('raw_exact', 'pair_calibrated', 'query_calibrated')}
    for _ in range(n_queries):
        source = sample_song(null_rng, true_weights)
        nulls = [sample_song(null_rng, true_weights) for _ in range(opportunities)]
        source2 = sample_song(planted_rng, true_weights)
        positives = [sample_song(planted_rng, true_weights) for _ in range(opportunities - 1)]
        positives.insert(planted_rng.randrange(opportunities), source2)
        for rule, result in choose_alert(source, nulls, assumed_weights, opportunities, alpha).items():
            counts[rule]['null_alerts'] += int(result)
        for rule, result in choose_alert(source2, positives, assumed_weights, opportunities, alpha).items():
            counts[rule]['positive_detections'] += int(result)
    return counts


def report(n_queries=8192, seed=20261023, alpha=ALPHA):
    records = []
    for true_family, true_weights in FAMILIES.items():
        for opportunities in (1, 16):
            for assumed_family in ([true_family, 'uniform'] if true_family == 'concentrated' else [true_family]):
                # For concentrated, report both correctly specified and wrong uniform model.
                # Avoid duplicated calibrated-vs-uniform scenario if true_family uniform.
                a = analytical_rates(true_weights, FAMILIES[assumed_family], opportunities, alpha)
                counts = simulate(true_weights, FAMILIES[assumed_family], opportunities, n_queries, seed + opportunities + (17 if true_family == 'concentrated' else 0), alpha)
                records.append({
                    'null_generator': true_family,
                    'assumed_calibration_family': assumed_family,
                    'candidates_per_query': opportunities,
                    'queries_per_condition': n_queries,
                    'analytical': a,
                    'observed': {rule: {
                        **tallies,
                        'null_alert_fraction': tallies['null_alerts'] / n_queries,
                        'positive_detection_fraction': tallies['positive_detections'] / n_queries,
                    } for rule, tallies in counts.items()},
                })
    return {
        'version': VERSION,
        'status': 'ENGINEERING_DEV_ONLY',
        'alpha_per_query': alpha,
        'seed': seed,
        'templates': N_TEMPLATES,
        'phrases_per_song': PHRASES,
        'comparison_unit': 'query (one source, m candidate songs), NOT candidate pairs',
        'scenarios': records,
        'limitations': [
            'This is a NEW independent toy program, not a reproduction of Astra hard-null source or results.',
            'The assumed calibration family is deliberately known from the generator (oracle model).',
            'Exact sequence identity only; ignores rhythm, phrasing in actual audio, emotion and experience.',
            'The source-conditioned probability measures chance coincidence, not the causal history of copying.',
            'Concentrated template probabilities are artificial; NOT an empirical distribution of human music.',
            'Null and positive examples use independent seeded draws; no outputs discarded or tuned after seeing results.',
            'All generated data are exposed DEV; results cannot confirm individual listening significance.',
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--queries', type=int, default=8192)
    ap.add_argument('--seed', type=int, default=20261023)
    ap.add_argument('--out')
    args = ap.parse_args()
    encoded = json.dumps(report(args.queries, args.seed), indent=2) + '\n'
    if args.out:
        from pathlib import Path
        Path(args.out).write_text(encoded, encoding='utf-8')
    print(encoded, end='')


if __name__ == '__main__':
    main()
