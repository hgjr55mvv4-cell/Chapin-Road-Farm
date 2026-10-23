"""Independent arithmetic-only check of a concentrated phrase-template null.

Does not run or reproduce Astra's original program or any music/perception test.
"""
import argparse
import json
from math import sqrt

def collision_probability(weights, phrases):
    """iid template matches across phrases, for two independent compositions."""
    if not weights or any(not 0 <= w <= 1 for w in weights) or abs(sum(weights)-1) > 1e-10:
        raise ValueError('weights must form a probability distribution')
    if type(phrases) is not int or phrases < 1:
        raise ValueError('phrases must be a positive integer')
    return sum(w*w for w in weights) ** phrases

def wilson_interval(count, n, z=1.96):
    if type(n) is not int or type(count) is not int or n <= 0 or not 0 <= count <= n:
        raise ValueError('invalid counts')
    p = count/n
    denom = 1 + z*z/n
    mid = (p + z*z/(2*n))/denom
    radius = z*sqrt((p*(1-p)+z*z/(4*n))/n)/denom
    return [mid-radius, mid+radius]

def summary():
    weights=[0.7]+[0.3/7]*7
    n=2048
    reported={'null_alerts':565,'exact_collisions':274,'nonexact_alerts':291}
    p=collision_probability(weights,3)
    return {
        'status':'INDEPENDENT_ARITHMETIC_CHECK_ONLY',
        'assumptions':'three iid phrase positions per independent song, common template probability 0.7, seven others 0.3/7',
        'template_weights':weights,
        'phrases_per_song':3,
        'probability_exact_three_phrase_collision':p,
        'expected_exact_collisions_in_2048':n*p,
        'reported':reported,
        'reported_exact_collision_rate':reported['exact_collisions']/n,
        'reported_fixed_cutoff_null_alert_rate':reported['null_alerts']/n,
        'reported_alert_rate_wilson_95':wilson_interval(reported['null_alerts'],n),
        'internal_consistency':reported['exact_collisions']+reported['nonexact_alerts']==reported['null_alerts'],
        'limits':[
            'Counts from user-relayed Astra report; source archive/case-level CSV not retrieved.',
            'Independent phrase sampling is an assumption not verified from upstream source.',
            'No human musical response, audio decoding or cross-model scientific test.'
        ]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',default=None)
    a=p.parse_args()
    encoded=json.dumps(summary(),indent=2)+'\n'
    if a.out:
        from pathlib import Path
        Path(a.out).write_text(encoded,encoding='utf8')
    print(encoded,end='')

if __name__=='__main__':main()
