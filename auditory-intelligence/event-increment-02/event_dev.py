"""AUDITORY-EVENT-INCREMENT-02 v0.1 — SYNTHETIC tone-class event association.
No speech, music, human intention, physical source identity, fault diagnosis or
streaming prediction. Declared generator schedules are used only for scoring.
"""
from __future__ import annotations
import argparse
from array import array
from dataclasses import dataclass
import io
import json
import math
import random
import struct
import time
import wave

RATE = 8000
FRAME = 320
HOP = 160
MAX_BYTES = 262144
FREQUENCIES = (310, 440, 620, 760)
A, B, C, DISTRACTOR = 440, 620, 760, 310
RMS_THRESHOLD = 0.08
MAG_THRESHOLD = 0.080
FREQ_RATIO = 1.6
MAX_VALID_SECONDS = 3
WAVE_SINES = {f: [math.sin(2*math.pi*f*i/RATE) for i in range(20000)] for f in FREQUENCIES}
TEMPLATE = {f: (tuple(math.sin(2*math.pi*f*i/RATE) for i in range(FRAME)),
                tuple(math.cos(2*math.pi*f*i/RATE) for i in range(FRAME)))
            for f in (A, B)}

@dataclass(frozen=True)
class Event:
    tone_hz: int
    start: float
    end: float
    amplitude: float
    dropout: tuple[float, float] | None = None
    ramp_s: float = 0.0
    echo_amp: float = 0.0

@dataclass(frozen=True)
class Case:
    pair: int
    kind: str
    wav: bytes
    a: Event
    b: Event | None
    events: tuple[Event, ...]
    intended_positive: bool
    perturbation: str


def _synth(events: tuple[Event, ...], noise: float, seed: int) -> bytes:
    n = 17600
    rng = random.Random(seed)
    buf = [rng.uniform(-noise, noise) for _ in range(n)]
    for e in events:
        first = max(0, round(e.start * RATE))
        last = min(n, round(e.end * RATE))
        for i in range(first, last):
            t = i/RATE
            if e.dropout and e.dropout[0] <= t < e.dropout[1]:
                continue
            envelope = min(1., max(0., (t-e.start)/e.ramp_s)) if e.ramp_s else 1.
            buf[i] += e.amplitude * envelope * WAVE_SINES[e.tone_hz][i]
            if e.echo_amp:
                delayed = i-round(.06*RATE)
                if delayed >= first:
                    buf[i] += e.amplitude*e.echo_amp*WAVE_SINES[e.tone_hz][delayed]
    out = io.BytesIO()
    with wave.open(out, 'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(RATE)
        w.writeframes(array('h', [max(-32768,min(32767,round(v*32767))) for v in buf]).tobytes())
    return out.getvalue()


def pair_cases(index: int, seed: int = 20261023) -> tuple[Case, Case]:
    rng = random.Random(seed + index*1187)
    jitter = rng.uniform(-.05,.05)
    a_start = .28 + jitter
    a_end = a_start + .35
    b_start = 1.07 + rng.uniform(-.09,.09)
    b_end = b_start + .31
    amplitude = rng.uniform(.26,.44)
    b_amplitude = rng.choice([.055,.11,.24,.36])
    noise = rng.choice([.003,.018,.055])
    dropout = ((a_start+.12,a_start+.19) if index%5==0 else None)
    ramp = .07 if index%7==0 else 0.0
    echo = .20 if index%9==0 else 0.0
    a = Event(A,a_start,a_end,amplitude,dropout,ramp,echo)
    b = Event(B,b_start,b_end,b_amplitude,None,ramp,echo)
    distractors = ()
    if index%4 in (0,1):
        distractors=(Event(DISTRACTOR,.75,.94,rng.uniform(.18,.50)),)
    common = (a,)+distractors
    p_events = common+(b,)
    mode = index%3
    if mode==0:
        n_events = common
        perturb = 'intended_B_absent'
    elif mode==1:
        n_events = common+(Event(C,b_start,b_end,b_amplitude),)
        perturb = 'B_replaced_by_C'
    else:
        early = Event(B,.07,.21,b_amplitude)
        n_events = common+(early,)
        perturb = 'B_precedes_A'
    return (Case(index,'positive',_synth(p_events,noise,seed+index*733),a,b,p_events,True,
                 'dropout/ramp/echo/distractor/gain/noise'),
            Case(index,'negative',_synth(n_events,noise,seed+index*733),a,None,n_events,False,perturb))


def _read(wav_bytes: bytes | None) -> tuple[str,tuple[float,...]]:
    if not wav_bytes:
        return 'MISSING',()
    if type(wav_bytes) is not bytes:
        return 'BAD_TYPE',()
    if len(wav_bytes)>MAX_BYTES:
        return 'TOO_LARGE',()
    if len(wav_bytes)<44 or wav_bytes[:4]!=b'RIFF' or wav_bytes[8:12]!=b'WAVE':
        return 'MALFORMED',()
    if struct.unpack_from('<I',wav_bytes,4)[0]+8!=len(wav_bytes):
        return 'CONTAINER_LENGTH_MISMATCH',()
    try:
        with wave.open(io.BytesIO(wav_bytes),'rb') as w:
            if w.getnchannels()!=1 or w.getsampwidth()!=2 or w.getframerate()!=RATE or w.getcomptype()!='NONE':
                return 'UNSUPPORTED',()
            frames=w.getnframes()
            if frames>MAX_VALID_SECONDS*RATE: return 'TOO_LONG',()
            raw=w.readframes(frames)
            if len(raw)!=frames*2: return 'TRUNCATED',()
    except (wave.Error,ValueError,EOFError):
        return 'MALFORMED',()
    samples=array('h');samples.frombytes(raw)
    if sum(abs(v)>=32766 for v in samples)>=4:
        return 'CLIPPED',()
    if len(samples)<2000: return 'TOO_SHORT',()
    return 'OK',tuple(v/32767 for v in samples)


def _regions(activities: list[bool], dt: float, min_frames=2, bridge=0) -> tuple[tuple[float,float],...]:
    flags=activities[:]
    if bridge:
        last=None
        for i,active in enumerate(flags):
            if active:
                if last is not None and 0<i-last-1<=bridge:
                    for k in range(last+1,i):flags[k]=True
                last=i
    regions=[];start=None
    for i,active in enumerate(flags+[False]):
        if active and start is None:start=i
        if not active and start is not None:
            if i-start>=min_frames:
                regions.append((round(start*dt,3),round(i*dt,3)))
            start=None
    return tuple(regions)


def energy(wav_bytes: bytes | None) -> dict:
    status,samples=_read(wav_bytes)
    if status!='OK':return {'sensor_status':status,'decision':'ABSTAIN','gap':None,'regions':[]}
    activities=[]
    for i in range(0,len(samples)-80+1,80):
        f=samples[i:i+80]
        activities.append(math.sqrt(sum(v*v for v in f)/len(f))>RMS_THRESHOLD)
    regs=_regions(activities,.01,min_frames=3)
    if len(regs)!=2:return {'sensor_status':'OK','decision':'ABSTAIN','gap':None,'regions':regs}
    gap=round(regs[1][0]-regs[0][1],3)
    return {'sensor_status':'OK','decision':'MATCH_A_THEN_B' if gap>=0 else 'ABSTAIN',
            'gap':gap if gap>=0 else None,'regions':regs,'event_identity':'UNVERIFIED'}


def frequency(wav_bytes: bytes | None) -> dict:
    status,samples=_read(wav_bytes)
    if status!='OK':return {'sensor_status':status,'decision':'ABSTAIN','gap':None,'detected':{}}
    labels={A:[],B:[]}
    for start in range(0,len(samples)-FRAME+1,HOP):
        f=samples[start:start+FRAME]
        powers={}
        for tone, (sin,cos) in TEMPLATE.items():
            re=sum(v*c for v,c in zip(f,cos))
            im=sum(v*c for v,c in zip(f,sin))
            powers[tone]=2*math.hypot(re,im)/FRAME
        for tone in (A,B):
            other=B if tone==A else A
            labels[tone].append(powers[tone]>=MAG_THRESHOLD and
                                powers[tone]>=FREQ_RATIO*powers[other])
    segments={tone:_regions(flags,HOP/RATE,2,4) for tone,flags in labels.items()}
    ordered= [(a,b) for a in segments[A] for b in segments[B] if b[0]>a[1]]
    if not ordered:
        return {'sensor_status':'OK','decision':'NO_MATCH','gap':None,'detected':segments}
    a,b=min(ordered,key=lambda p:(p[0][0],p[1][0]))
    return {'sensor_status':'OK','decision':'MATCH_A_THEN_B','gap':round(b[0]-a[1],3),
            'detected':segments,'selected':(a,b),'identity_scope':'SYNTHETIC_TONE_CLASSES_ONLY'}


def score(cases, fn):
    counts={'positives':0,'negatives':0,'match_on_positive':0,'match_with_right_times':0,
            'wrong_time_positive':0,'unverified_identity_positive':0,'false_match_negative':0,
            'abstain_positive':0,'abstain_negative':0,'no_match_positive':0,'negative_correct_no_match':0}
    failures=[];elapsed=0.
    for case in cases:
        start=time.perf_counter();o=fn(case.wav);elapsed+=time.perf_counter()-start
        if case.intended_positive:
            counts['positives']+=1
            if o['decision']=='MATCH_A_THEN_B':
                counts['match_on_positive']+=1
                if 'selected' in o:
                    a,b=o['selected']
                    valid=abs(a[0]-case.a.start)<=.100 and abs(b[0]-case.b.start)<=.100
                else:
                    valid=None
                if valid is True:counts['match_with_right_times']+=1
                elif valid is None:
                    counts['unverified_identity_positive']+=1
                    if len(failures)<8:failures.append({'pair':case.pair,'case':'positive','error':'unverified_source_identity','out':o['gap']})
                else:
                    counts['wrong_time_positive']+=1
                    if len(failures)<8:failures.append({'pair':case.pair,'case':'positive','error':'wrong_event_time','out':o['gap']})
            elif o['decision']=='ABSTAIN':counts['abstain_positive']+=1
            else:counts['no_match_positive']+=1
        else:
            counts['negatives']+=1
            if o['decision']=='MATCH_A_THEN_B':
                counts['false_match_negative']+=1
                if len(failures)<8:failures.append({'pair':case.pair,'case':'negative','error':'false_assurance','out':o['gap'],'setting':case.perturbation})
            elif o['decision']=='ABSTAIN':counts['abstain_negative']+=1
            else:counts['negative_correct_no_match']+=1
    counts['coverage']=round(1-(counts['abstain_positive']+counts['abstain_negative'])/(counts['positives']+counts['negatives']),5)
    counts['runtime_seconds']=round(elapsed,4)
    return {'counts':counts,'example_errors':failures}


def evaluate(pairs=400,seed=20261023):
    if type(pairs) is not int or pairs<=0 or pairs>1000:raise ValueError('1..1000 integer pairs required')
    cases=[]
    for i in range(pairs):cases.extend(pair_cases(i,seed))
    e=score(cases,energy);f=score(cases,frequency)
    return {'version':'AUDITORY-EVENT-INCREMENT-02-v0.1',
            'status':'EXPOSED_SYNTHETIC_ENGINEERING_ONLY',
            'contract_seed':seed,'matched_pair_scenarios':pairs,'captures':pairs*2,
            'baselines':{'T':'generic same transcript for all; cannot infer tone class',
                         'G':'gold aggregate activity boundaries cannot provide tone identity',
                         'E':'10ms RMS two-region baseline',
                         'F':'40ms 2-frequency simple fixed-template classifier'},
            'energy':e,'frequency':f,
            'limitations':['Source labels from generator schedules, not human source identity.',
                           'All 400 paired cases public DEV with co-designed classifier; no independent holdout.',
                           'F is fixed simple class-specific matched template; not a general frequency detector.',
                           'Correct event association on these tone fixtures does not identify a machine fault.',
                           'No streaming, human speech, conversation, voice capture, music or field deployment.']}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--pairs',type=int,default=400)
    p.add_argument('--seed',type=int,default=20261023)
    p.add_argument('--out')
    a=p.parse_args();out=json.dumps(evaluate(a.pairs,a.seed),indent=2)+'\n'
    if a.out:
        from pathlib import Path
        Path(a.out).write_text(out,encoding='utf8')
    print(out,end='')

if __name__=='__main__':main()
