from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step

OUT = ROOT / 'run-data' / 'cross_domain' / 'r3_compact_r4_carrier_families'
DIM = 4
L1_RADIUS = 18
BACKGROUND = 100.0
TOTAL_EXCESS = 40.0
TRAIN_FRAMES = 8
RELEASE_FRAMES = 2
PERIOD = 2
R3_L1_SUPPORT = 3
W_SUPPORT = 3

MODES = ('compact','linear','pulsing','sqrt')

DOMAIN = [c for c in product(range(-L1_RADIUS,L1_RADIUS+1), repeat=4)
          if sum(abs(v) for v in c) <= L1_RADIUS]
DOMAIN_SET = set(DOMAIN)


def width(frame, mode):
    if mode == 'compact': return 0.60
    if mode == 'linear': return 0.60 + 0.10*frame
    if mode == 'pulsing': return max(0.28, 0.60*(1.0 + 0.45*math.sin(math.pi*frame/2.0)))
    if mode == 'sqrt': return 0.60 + 0.18*math.sqrt(frame)
    raise ValueError(mode)


def component(frame, mode):
    theta = 2.0*math.pi*frame/PERIOD
    sw = width(frame, mode)
    raw=[]
    for x,y,z in product(range(-R3_L1_SUPPORT,R3_L1_SUPPORT+1), repeat=3):
        if abs(x)+abs(y)+abs(z) > R3_L1_SUPPORT:
            continue
        g3 = math.exp(-0.5*(x*x+y*y+z*z))
        ang = math.atan2(y,x) if x or y else 0.0
        mod = 1.0 + 0.20*math.cos(2.0*(ang-theta))
        for w in range(-W_SUPPORT,W_SUPPORT+1):
            gw = math.exp(-0.5*w*w/(sw*sw))
            val = g3*mod*gw
            if val > 1e-9:
                raw.append(((x,y,z,w),val))
    scale = TOTAL_EXCESS/sum(v for _,v in raw)
    return {c:v*scale for c,v in raw}, sw


def apply_component(phi, old, new):
    for c in set(old)|set(new):
        phi[c] += new.get(c,0.0)-old.get(c,0.0)


def metrics(phi):
    excess=[(c,v-BACKGROUND) for c,v in phi.items() if v > BACKGROUND+1e-10]
    q=sum(e for _,e in excess)
    if q <= 0.0:
        return {'Q_plus':0.0,'R3_rms':0.0,'W_rms':0.0,'R4_rms':0.0,'PR3':0.0,'PR4':0.0}
    proj={}
    for c,e in excess:
        proj[c[:3]]=proj.get(c[:3],0.0)+e
    vals=np.asarray([e for _,e in excess],float)
    vals3=np.asarray(list(proj.values()),float)
    r3=math.sqrt(sum(e*sum(u*u for u in c[:3]) for c,e in excess)/q)
    w=math.sqrt(sum(e*c[3]*c[3] for c,e in excess)/q)
    return {
        'Q_plus':float(q),
        'R3_rms':float(r3),
        'W_rms':float(w),
        'R4_rms':float(math.hypot(r3,w)),
        'PR3':float(vals3.sum()**2/(np.square(vals3).sum()+1e-30)),
        'PR4':float(vals.sum()**2/(np.square(vals).sum()+1e-30)),
    }


def run_mode(mode):
    phi={c:BACKGROUND for c in DOMAIN}
    prev={}; old={}; rows=[]
    for frame in range(TRAIN_FRAMES):
        comp, sw = component(frame, mode)
        apply_component(phi,old,comp); old=comp
        pre=metrics(phi)
        phi,prev,diag=operator_step(phi,prev,dimension=DIM)
        rows.append({'frame':frame,'phase':'train','input_w_sigma':sw,
                     'pre_operator':pre,'post_operator':metrics(phi),
                     'births':diag.births,'conservation_error':diag.total_after-diag.total_before})
    apply_component(phi,old,{})
    for k in range(RELEASE_FRAMES):
        phi,prev,diag=operator_step(phi,prev,dimension=DIM)
        rows.append({'frame':TRAIN_FRAMES+k,'phase':'release','input_w_sigma':None,
                     'pre_operator':None,'post_operator':metrics(phi),
                     'births':diag.births,'conservation_error':diag.total_after-diag.total_before})
    r0=rows[TRAIN_FRAMES]['post_operator']; r1=rows[-1]['post_operator']
    return {'mode':mode,'rows':rows,'release_ratio':{
        'R3_rms':r1['R3_rms']/r0['R3_rms'],
        'W_rms':r1['W_rms']/r0['W_rms'],
        'PR3':r1['PR3']/r0['PR3'],
        'PR4':r1['PR4']/r0['PR4'],
        'Q_plus':r1['Q_plus']/r0['Q_plus'],
    }}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    results={m:run_mode(m) for m in MODES}
    payload={
        'experiment':'r3_compact_r4_carrier_families',
        'status':'representation-family pilot; no physical compactness law claimed',
        'operator':'unchanged scanner.self_reflexive_operator.operator_step',
        'provenance':{
            'R3 compact training profile':'A',
            'R4 carrier family':'A',
            'operator response':'S/E candidate',
            'R3/R4 compactness readouts':'measurement only',
        },
        'guardrail':{
            'no_stabilizer':True,'no_mass_or_energy_formula':True,'no_metric_formula':True,
            'support_L1_max':R3_L1_SUPPORT+W_SUPPORT,
            'distance_to_boundary':L1_RADIUS-(R3_L1_SUPPORT+W_SUPPORT),
            'total_operator_frames':TRAIN_FRAMES+RELEASE_FRAMES,
            'boundary_causally_unreachable':(TRAIN_FRAMES+RELEASE_FRAMES)<(L1_RADIUS-(R3_L1_SUPPORT+W_SUPPORT)),
        },
        'parameters':{'L1_RADIUS':L1_RADIUS,'BACKGROUND':BACKGROUND,'TOTAL_EXCESS':TOTAL_EXCESS,
                      'TRAIN_FRAMES':TRAIN_FRAMES,'RELEASE_FRAMES':RELEASE_FRAMES,'PERIOD':PERIOD},
        'results':results,
    }
    (OUT/'result.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps({m:results[m]['release_ratio'] for m in MODES},indent=2))

if __name__=='__main__':
    main()
