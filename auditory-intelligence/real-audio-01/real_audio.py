"""Real ESC-10 environmental recordings in controlled, time-labeled mixtures.

Clip-level Freesound source categories are NOT natural event-onset labels.
Experimenter-created insertion slots are NOT true acoustic source localization.
"""
import argparse,hashlib,json,math,struct,wave
from pathlib import Path

RATE=8000
LENGTH=.8
SLOTS=(.4,1.60)
DURATION=2.8
CATEGORIES=('dog','chainsaw')
FREQS=(150,250,400,620,900,1250,1750,2500,3250)
ENERGY_THRESHOLD=.034
MIN_MARGIN=.07
NORM_PEAK=.8

def decode(path):
    with wave.open(str(path),'rb') as w:
        if w.getnchannels()!=1 or w.getsampwidth()!=2 or w.getcomptype()!='NONE':
            raise ValueError('Expected mono PCM16 WAV')
        sr=w.getframerate();n=w.getnframes()
        if sr not in (44100,8000) or n>sr*6 or n<sr//2:
            raise ValueError('Unexpected sampling rate or recording length')
        data=w.readframes(n)
        if len(data)!=2*n:raise ValueError('Incomplete PCM frames')
    samples=struct.unpack('<'+str(n)+'h',data)
    if sr==RATE:return [x/32768 for x in samples]
    ratio=sr/RATE;out=[]
    for i in range(int(n/ratio)):
        a=int(i*ratio);b=min(n,max(a+1,int((i+1)*ratio)))
        out.append(sum(samples[a:b])/((b-a)*32768))
    return out

def rms(a):
    return math.sqrt(sum(x*x for x in a)/len(a)) if a else 0.

def excerpt(samples,length=int(RATE*LENGTH)):
    if len(samples)<length:raise ValueError('Too short')
    starts=range(0,len(samples)-length+1,RATE//4)
    start=max(starts,key=lambda i:rms(samples[i:i+length]))
    segment=samples[start:start+length]
    peak=max(abs(v) for v in segment)
    if peak<.002:raise ValueError('No usable source segment')
    return [v/peak*NORM_PEAK for v in segment],round(start/RATE,3)

def goertzel(samples,freq):
    c=2*math.cos(2*math.pi*freq/RATE)
    p=q=0.
    for x in samples:
        v=x+c*p-q;q=p;p=v
    return max(0.,p*p+q*q-c*p*q)

def features(samples):
    width=800;samples=samples[:len(samples)//width*width]
    if len(samples)<2*width:raise ValueError('Short feature segment')
    powers=[0.]*len(FREQS);energy=[];cross=0
    for i in range(0,len(samples),width):
        f=samples[i:i+width];energy.append(rms(f))
        cross+=sum((f[j]>=0)!=(f[j-1]>=0) for j in range(1,len(f)))
        for k,hz in enumerate(FREQS):powers[k]+=goertzel(f,hz)
    total=sum(powers)+1e-12
    logs=[math.log1p(1000*p/total) for p in powers]
    mag=math.sqrt(sum(v*v for v in logs))+1e-12
    avg=sum(energy)/len(energy)
    return [v/mag for v in logs]+[cross/len(samples),
       math.sqrt(sum((v-avg)**2 for v in energy)/len(energy))]

def cosine(a,b):
    return sum(x*y for x,y in zip(a,b))/(math.sqrt(sum(x*x for x in a)*sum(y*y for y in b))+1e-12)

def train(data,records):
    prototypes={}
    for category in CATEGORIES:
        chosen=[x for x in records.values() if x['role']=='train' and x['category']==category]
        if len({x['source_id'] for x in chosen})<2:
            raise ValueError('At least two unique training source IDs per class')
        vectors=[features(data[x['filename']][0]) for x in chosen]
        prototypes[category]=[sum(v[k] for v in vectors)/len(vectors) for k in range(len(vectors[0]))]
    return prototypes

def classify(slot,prototypes,method='multiband'):
    if rms(slot)<ENERGY_THRESHOLD:return 'none'
    vector=features(slot)
    if method=='zcr':
        d={name:abs(vector[-2]-p[-2]) for name,p in prototypes.items()}
        return min(d,key=d.get)
    scores={c:cosine(vector[:9],prototypes[c][:9]) for c in CATEGORIES}
    if abs(scores['dog']-scores['chainsaw'])<MIN_MARGIN:return 'abstain'
    return max(scores,key=scores.get)

def mix(labels,events,rain,gain):
    n=int(DURATION*RATE)
    output=[.08*rain[i%len(rain)] for i in range(n)]
    for slot,label in enumerate(labels):
        if label=='none':continue
        start=int(SLOTS[slot]*RATE)
        for i,v in enumerate(events[label]):output[start+i]+=gain*v
    clipped=sum(abs(v)>1 for v in output)
    return [max(-1.,min(1.,v)) for v in output],clipped

def evaluate(audio_dir,manifest):
    document=json.loads(Path(manifest).read_text())
    records=document['sources']
    data={}
    for x in records:
        path=Path(audio_dir)/x['filename']
        if not path.is_file():raise FileNotFoundError('REAL RECORDING MISSING; NO SYNTHETIC FALLBACK: '+str(path))
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        segment,offset=excerpt(decode(path))
        data[x['filename']]=(segment,offset,sha)
    indexed={r['filename']:r for r in records}
    prototypes=train(data,indexed)
    held={c:[r for r in records if r['role']=='eval' and r['category']==c] for c in ('dog','chainsaw','rain')}
    for label in ('dog','chainsaw','rain'):
        if len(held[label])<2:raise ValueError('Not enough held-out sources')
    for category in CATEGORIES:
        training={r['source_id'] for r in records if r['role']=='train' and r['category']==category}
        testing={r['source_id'] for r in held[category]}
        if training & testing:raise ValueError('Source ID leakage across train and eval')
    schedules=[('dog','chainsaw'),('chainsaw','dog'),('dog','dog'),('chainsaw','chainsaw'),
               ('dog','none'),('none','chainsaw'),('none','none'),('chainsaw','none')]
    counts={k:dict(true_A_then_B=0,miss_A_then_B=0,false_A_then_B=0,true_no_match=0,abstaining_queries=0)
            for k in ('energy','zcr','multiband')}
    rows=[]
    for source_group in range(2):
        heldout={c:data[held[c][source_group]['filename']][0] for c in CATEGORIES}
        background=data[held['rain'][source_group]['filename']][0]
        for expected in schedules:
            for gain in (.25,.50,.85):
                mixture,clipped=mix(expected,heldout,background,gain)
                if clipped:raise ValueError('Clipped constructed recording - invalid')
                windows=[mixture[int(t*RATE):int((t+LENGTH)*RATE)] for t in SLOTS]
                truth=expected==('dog','chainsaw')
                outputs={}
                for name in counts:
                    if name=='energy':
                        guesses=tuple('active' if rms(s)>=ENERGY_THRESHOLD else 'none' for s in windows)
                        match=guesses==('active','active')
                    else:
                        guesses=tuple(classify(s,prototypes,name) for s in windows)
                        match=guesses==('dog','chainsaw')
                    outputs[name]={'labels':guesses,'matched':match}
                    cc=counts[name]
                    if 'abstain' in guesses:cc['abstaining_queries']+=1
                    if truth:cc['true_A_then_B' if match else 'miss_A_then_B']+=1
                    else:cc['false_A_then_B' if match else 'true_no_match']+=1
                rows.append({'source_group':source_group,'slot_sources':expected,'gain':gain,
                             'planted_dog_then_chainsaw':truth,'predictions':outputs})
    sources=[dict(filename=r['filename'],role=r['role'],category=r['category'],source_id=r['source_id'],
                  original_author=r['author'],original_license=r['license'],
                  sha256=data[r['filename']][2],excerpt_offset_s=data[r['filename']][1]) for r in records]
    return {'status':'EXPOSED_REAL_AUDIO_CONTROLLED_MIXTURE_DEV','provenance':document['provenance'],
            'sources':sources,'design':{
                'queries':len(rows),'positives':sum(x['planted_dog_then_chainsaw'] for x in rows),
                'negatives':sum(not x['planted_dog_then_chainsaw'] for x in rows),
                'distinct_eval_source_groups':2,'repeated_sources_across_conditions':True,
                'all_baselines_given_slot_boundaries':True,'human_annotated_onsets':False},
            'methods':counts,'rows':rows,
            'limitations':['Dataset categories are clip-level only; natural event onsets not verified.',
            'Experimenter planted slot timing and event class; these are not spontaneous soundscapes.',
            'Evaluation clips are held out by source ID but repeatedly reused across test rows.',
            'No per-query independence, real-world statistical error bounds or source-object identities.',
            'Low-cost box-average downsampling can distort frequencies above its passband.',
            'No evidence about speech understanding, human emotions or actual machine diagnosis.']}

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--audio-dir',required=True);a.add_argument('--manifest',default='sources.json')
    a.add_argument('--out',default='results.json')
    args=a.parse_args()
    result=evaluate(args.audio_dir,args.manifest)
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print('AUDITORY_REAL_RESULTS:',json.dumps(result['methods'],sort_keys=True))
    print('AUDITORY_REAL_DESIGN:',json.dumps(result['design'],sort_keys=True))
    print('SOURCE_SHA256S:',json.dumps({x['filename']:x['sha256'] for x in result['sources']},sort_keys=True))
if __name__=='__main__':main()
