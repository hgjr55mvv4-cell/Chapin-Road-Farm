#!/usr/bin/env python3
"""Post-freeze synthetic confirmation fixture selection; see FROZEN_CONTRACT.md."""
import random, json, hashlib, time
from sim import Event, Design, run
SEED=20261023
rng=random.Random(SEED)
events=[]
for i in range(16):
    f=rng.uniform(89,91); amp=rng.uniform(.8,1.0); dur=rng.uniform(.3,.5)
    events.append(('onband_event',Event(f'onband_event_{i:02}','sine',frequency_hz=f,amplitude_g=amp,duration_s=dur)))
    events.append(('healthy_matched_onband',Event(f'healthy_matched_onband_{i:02}','sine',frequency_hz=f,amplitude_g=amp,duration_s=dur)))
    f=rng.uniform(43,47) if i%2==0 else rng.uniform(148,152)
    events.append(('ordinary_offband',Event(f'ordinary_offband_{i:02}','sine',frequency_hz=f,amplitude_g=rng.uniform(.6,1.0),duration_s=rng.uniform(.3,.5))))
    events.append(('impact',Event(f'impact_{i:02}','impulse',amplitude_g=rng.uniform(5,12),duration_s=.002)))
    events.append(('offband_overload',Event(f'offband_overload_{i:02}','sine',frequency_hz=rng.uniform(43,47),amplitude_g=rng.uniform(3.5,5.0))))
t0=time.monotonic()
rows=[dict(class_name=cls,**run(e)) for cls,e in events]
summary={cls:{k:sum(r[k] for r in rows if r['class_name']==cls) for k in ('plain_impact','tuned_peak','tuned_dwell')}
         for cls in ['onband_event','ordinary_offband','impact','offband_overload','healthy_matched_onband']}
# Structural same-waveform test: both contain exactly the same synthesized input.
for i in range(16):
    a=rows[i*5]; b=rows[i*5+1]
    assert a['peak_displacement_mm']==b['peak_displacement_mm']
    assert all(a[k]==b[k] for k in ('plain_impact','tuned_peak','tuned_dwell'))
out={'status':'SYNTHETIC_MODEL_INTERNAL_CONFIRMATION_ONLY', 'seed':SEED,'frozen_source_sha256':'e17a6812c02badf41efcc6afe2401ab929a09fd0c5137ceb2fd960898f474062', 'fixture_count':len(rows),'class_counts':summary,'elapsed_wall_s':round(time.monotonic()-t0,3), 'rows':rows}
with open('confirm_results.json','w',encoding='utf8') as f:json.dump(out,f,indent=2)
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
