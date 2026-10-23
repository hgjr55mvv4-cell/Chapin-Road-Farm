"""LOOM-01: stdlib, SYMBOLIC interval-pattern DEV (no audio or human responses).
Generator, labels and detector were co-designed. All cases are EXPOSED DEV.
"""
import argparse
import json
import random
from collections import Counter

VERSION = 'LOOM-01-v0.1-DEV'
STEP_VALUES = (-3, -2, -1, 1, 2, 3)
TRANSPOSES = (2, 5, 7, 9)
N_STEPS = 12
DETECTOR_CUTOFF = 0.83  # engineering-only cutoff, not statistical qualification


def melody(start, steps):
    out = [start]
    for step in steps:
        out.append(out[-1] + step)
    return tuple(out)


def intervals(notes):
    return tuple(b-a for a,b in zip(notes, notes[1:]))


def ordered_similarity(a, b):
    x,y = intervals(a),intervals(b)
    if not x or len(x) != len(y):
        raise ValueError('two nonempty equal-length interval sequences required')
    return sum(i == j for i,j in zip(x,y)) / len(x)


def histogram_similarity(a, b):
    x,y = Counter(intervals(a)), Counter(intervals(b))
    n = sum(x.values())
    if not n or n != sum(y.values()):
        raise ValueError('equal nonzero event count required')
    return sum(min(x[k],y[k]) for k in x.keys() | y.keys()) / n


def absolute_pitch_similarity(a,b):
    if len(a) != len(b):
        raise ValueError('equal note count required')
    return sum(x == y for x,y in zip(a,b)) / len(a)


def make_triplet(rng):
    steps = tuple(rng.choice(STEP_VALUES) for _ in range(N_STEPS))
    shift = rng.choice(TRANSPOSES)
    start = rng.randint(56,65)
    source = melody(start,steps)
    positive = melody(start+shift,steps)
    shuffled = list(steps)
    rng.shuffle(shuffled)  # allow accidental matches; don't filter on detected outcome
    null = melody(start+shift,shuffled)
    return source, positive, null, shift


def evaluate(seed=20261023,n=64,threshold=DETECTOR_CUTOFF):
    if n<=0:raise ValueError('positive n required')
    rng=random.Random(seed)
    positive,null,histp,histn,absp,absn=[],[],[],[],[],[]
    for _ in range(n):
        a,b,c,_=make_triplet(rng)
        positive.append(ordered_similarity(a,b))
        null.append(ordered_similarity(a,c))
        histp.append(histogram_similarity(a,b))
        histn.append(histogram_similarity(a,c))
        absp.append(absolute_pitch_similarity(a,b))
        absn.append(absolute_pitch_similarity(a,c))
    return {
        'version':VERSION,'status':'ENGINEERING_DEV_EXPOSED',
        'seed':seed,'independent_generated_triplets':n,
        'per_triplet':'one source with a transposed exact-relative positive and a transposed shuffled-order null',
        'note_events_per_song':N_STEPS+1,'comparison_threshold':threshold,
        'ordered_detector':{
            'true_positive_triplets':sum(x>=threshold for x in positive),'positive_total':n,
            'false_positive_triplets':sum(x>=threshold for x in null),'null_total':n,
            'positive_mean_similarity':round(sum(positive)/n,6),
            'null_mean_similarity':round(sum(null)/n,6),
            'null_max_similarity':round(max(null),6)},
        'histogram_control':{
            'positive_mean':round(sum(histp)/n,6),'null_mean':round(sum(histn)/n,6),
            'note':'both equal by construction: unordered step histograms cannot detect planted order'},
        'absolute_pitch_control':{
            'positive_mean':round(sum(absp)/n,6),'null_mean':round(sum(absn)/n,6),
            'note':'positive sequence deliberately shifted in absolute pitch'},
        'limitations':[
            'Symbols are known directly from generator; no WAV produced or decoded.',
            'Labels, generator and detector were co-designed; not prospective confirmation.',
            'This demonstrates preservation of transposed note-interval order, not emotion or affinity.',
            'Null sequences share exact interval histograms; no planted ordered motif, but chance matches allowed.',
            'Null is NOT a guarantee of zero musical pattern or statistical model of real songs.',
            'Songs from one triplet are dependent; denominator is triplets, not individual song pairs.']
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seed',type=int,default=20261023)
    p.add_argument('--sets',type=int,default=64)
    p.add_argument('--cutoff',type=float,default=DETECTOR_CUTOFF)
    a=p.parse_args()
    if not 0<a.cutoff<=1:p.error('cutoff must be (0,1]')
    print(json.dumps(evaluate(a.seed,a.sets,a.cutoff),indent=2))


if __name__=='__main__':main()
