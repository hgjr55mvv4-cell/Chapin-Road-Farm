"""Deterministically export per-case evidence; generator truth used only for audit."""
import argparse
import csv
from event_dev import pair_cases, energy, frequency

def write_cases(path, pairs=400, seed=20261023):
    columns=['pair','seed','kind','intended_positive','negative_type','a_start','b_start',
             'energy_sensor','energy_decision','energy_gap','frequency_sensor','frequency_decision',
             'frequency_gap','frequency_a_start','frequency_b_start','frequency_time_correct']
    with open(path,'w',newline='',encoding='utf-8') as fp:
        writer=csv.DictWriter(fp,fieldnames=columns)
        writer.writeheader()
        for i in range(pairs):
            for case in pair_cases(i,seed):
                e=energy(case.wav);f=frequency(case.wav)
                sa,sb=(f.get('selected') or (None,None))
                correct=bool(sa and sb and case.b and
                             abs(sa[0]-case.a.start)<=.1 and abs(sb[0]-case.b.start)<=.1)
                writer.writerow({'pair':i,'seed':seed,'kind':case.kind,
                                 'intended_positive':case.intended_positive,
                                 'negative_type':case.perturbation if not case.intended_positive else '',
                                 'a_start':case.a.start,'b_start':case.b.start if case.b else '',
                                 'energy_sensor':e['sensor_status'],'energy_decision':e['decision'],
                                 'energy_gap':e.get('gap'),'frequency_sensor':f['sensor_status'],
                                 'frequency_decision':f['decision'],'frequency_gap':f.get('gap'),
                                 'frequency_a_start':sa[0] if sa else '',
                                 'frequency_b_start':sb[0] if sb else '',
                                 'frequency_time_correct':correct})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='cases.csv');p.add_argument('--pairs',type=int,default=400)
    a=p.parse_args();write_cases(a.out,a.pairs)
