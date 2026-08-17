from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step, directions, add

OUT = ROOT / 'run-data' / 'cross_domain' / 'rotation_history_free_release'
DIM=4; BACKGROUND=100.0; OBJ_TOTAL=160.0; SIGMA=0.62
DOMAIN_L1=24; ROT_STEP_DEG=30.0; TRAIN_FRAMES=12; FREE_FRAMES=12; TOTAL_FRAMES=TRAIN_FRAMES+FREE_FRAMES
MEASURE_L1=6
DS=directions(DIM)

# A full externally prescribed 360-degree rotation is used as history.
# The m=3 shape itself has a 120-degree symmetry; this is recorded explicitly.
# During release no rotation law, angular momentum law, torque, damping, or target phase is applied.
CASES=[
  {'name':'train_then_release','forced_rotation':True,'release':True},
  {'name':'forced_continue','forced_rotation':True,'release':False},
  {'name':'static_release_control','forced_rotation':False,'release':True},
]


def fixed_domain():
    r=range(-DOMAIN_L1,DOMAIN_L1+1)
    return [tuple(int(v) for v in c) for c in product(r,repeat=4)
            if sum(abs(v) for v in c)<=DOMAIN_L1]
DOMAIN=fixed_domain(); DOMAIN_SET=set(DOMAIN); INDEX={c:i for i,c in enumerate(DOMAIN)}
LOCAL=[c for c in DOMAIN if sum(abs(v) for v in c)<=MEASURE_L1]


def object_component(theta: float):
    comp={}
    for c in product(range(-7,8),repeat=4):
        x,y,z,w=(float(v) for v in c)
        rho=math.hypot(x,y); r0=2.0
        d2=(rho-r0)**2+z*z+w*w
        env=math.exp(-0.5*d2/(SIGMA*SIGMA))
        ang=math.atan2(y,x)
        val=env*(1.0+0.35*math.cos(3*(ang-theta)))
        if val>1e-12: comp[tuple(int(v) for v in c)]=val
    s=sum(comp.values()); k=OBJ_TOTAL/s
    return {c:v*k for c,v in comp.items()}


def apply_component(phi,old,new):
    for c in set(old)|set(new):
        phi[c]+=new.get(c,0.0)-old.get(c,0.0)


def save_flow(path,flow):
    items=[(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v!=0.0]
    np.savez_compressed(path,
        source_index=np.asarray([q[0] for q in items],dtype=np.int32),
        direction=np.asarray([q[1] for q in items],dtype=np.uint8),
        amount=np.asarray([q[2] for q in items],dtype=np.float64))


def m3_moment(phi):
    # Scanner-side measurement only. Measures the phase/amplitude of the existing m=3 asymmetry.
    q=0j; weight=0.0
    for c in LOCAL:
        x,y,z,w=c
        if x==0 and y==0: continue
        excess=phi[c]-BACKGROUND
        if excess<=0: continue
        ang=math.atan2(y,x)
        q += excess*complex(math.cos(3*ang),math.sin(3*ang))
        weight += excess
    amp=abs(q)/(weight+1e-30)
    phase=(math.atan2(q.imag,q.real)/3.0) if abs(q)>0 else 0.0
    # canonical modulo 120 degrees
    period=2*math.pi/3
    phase=phase%period
    return {'amplitude':float(amp),'phase_rad_mod_120':float(phase),'phase_deg_mod_120':float(math.degrees(phase)),'positive_excess_weight':float(weight)}


def local_flow_m3(flow):
    # Directional flow-weighted m=3 phase around the object; analysis only.
    q=0j; total=0.0
    localset=set(LOCAL)
    for (c,di),v in flow.items():
        if c not in localset or v<=0: continue
        x,y,z,w=c
        if x==0 and y==0: continue
        ang=math.atan2(y,x)
        q += v*complex(math.cos(3*ang),math.sin(3*ang)); total+=v
    amp=abs(q)/(total+1e-30)
    phase=(math.atan2(q.imag,q.real)/3.0) if abs(q)>0 else 0.0
    phase=phase%(2*math.pi/3)
    return {'amplitude':float(amp),'phase_deg_mod_120':float(math.degrees(phase)),'total_positive_flow':float(total)}


def unwrap_m3_phase(degs):
    # Unwrap a modulo-120 measurement by choosing the nearest continuation.
    # This is analysis only and is not fed back to the operator.
    out=[]
    for d in degs:
        if not out: out.append(float(d)); continue
        candidates=[d+120*k for k in range(-12,13)]
        out.append(float(min(candidates,key=lambda x:abs(x-out[-1]))))
    return out


def run_case(case):
    cdir=OUT/case['name']; fdir=cdir/'flows'; cdir.mkdir(parents=True,exist_ok=True); fdir.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old={}; rows=[]; pin=[]; pout=[]; births=0
    for frame in range(TOTAL_FRAMES):
        forced = frame < TRAIN_FRAMES or (not case['release'])
        if case['forced_rotation'] and forced:
            theta=math.radians(ROT_STEP_DEG*frame)
            new=object_component(theta); apply_component(phi,old,new); old=new
            imposed_theta_deg=ROT_STEP_DEG*frame
        elif (not case['forced_rotation']) and frame==0:
            theta=0.0; new=object_component(theta); apply_component(phi,old,new); old=new; imposed_theta_deg=0.0
        else:
            # release: no component replacement or orientation update
            imposed_theta_deg=None
        before=sum(phi.values())
        pre_m=m3_moment(phi)
        pin.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_input.npz',prev)
        phi,nxt,diag=operator_step(phi,prev,dimension=DIM)
        post_m=m3_moment(phi); flow_m=local_flow_m3(nxt)
        pout.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_output.npz',nxt)
        rows.append({'frame':frame,'phase':'history' if frame<TRAIN_FRAMES else 'free_or_control',
                     'externally_forced_this_frame':bool(forced and case['forced_rotation']),
                     'imposed_theta_deg':imposed_theta_deg,'m3_pre':pre_m,'m3_post':post_m,'flow_m3':flow_m,
                     'births':diag.births,'live_transfer':float(diag.live_transfer),
                     'conservation_error':float(sum(phi.values())-before)})
        births+=diag.births; prev=nxt
    np.savez_compressed(cdir/'phi_history.npz',phi_input=np.stack(pin),phi_output=np.stack(pout))
    phases=[r['m3_post']['phase_deg_mod_120'] for r in rows]
    unwrap=unwrap_m3_phase(phases)
    for r,u in zip(rows,unwrap): r['m3_post']['phase_deg_unwrapped_analysis']=u
    return {'case':case,'rows':rows,'births_total':births}


def free_phase_stats(rows):
    free=rows[TRAIN_FRAMES:]
    p=np.asarray([r['m3_post']['phase_deg_unwrapped_analysis'] for r in free],float)
    a=np.asarray([r['m3_post']['amplitude'] for r in free],float)
    f=np.arange(len(p),dtype=float)
    slope=float(np.polyfit(f,p,1)[0]) if len(p)>1 else 0.0
    steps=np.diff(p)
    return {'phase_slope_deg_per_frame_analysis':slope,
            'mean_abs_phase_step_deg':float(np.mean(np.abs(steps))) if len(steps) else 0.0,
            'signed_mean_phase_step_deg':float(np.mean(steps)) if len(steps) else 0.0,
            'phase_steps_deg':[float(x) for x in steps],
            'amplitude_mean':float(np.mean(a)),'amplitude_start':float(a[0]),'amplitude_end':float(a[-1]),
            'amplitude_retention_end_over_start':float(a[-1]/(a[0]+1e-30))}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,dtype=np.int16),local_coord=np.asarray(LOCAL,dtype=np.int16))
    guard=7+TOTAL_FRAMES < DOMAIN_L1
    if not guard: raise RuntimeError('fixed domain too small for causal boundary isolation')
    results={c['name']:run_case(c) for c in CASES}
    stats={k:free_phase_stats(v['rows']) for k,v in results.items()}
    summary={'experiment':'rotation_history_free_release',
      'status':'synthetic history-release test; no angular momentum, torque, inertia, damping, charge, EM law or target free-rotation rule injected',
      'operator':'unchanged scanner.self_reflexive_operator.operator_step',
      'question':'after one externally prescribed 360-degree rotation history, does the field state carry an autonomous rotating/periodic m=3 relation after forcing is removed?',
      'important_note':'m=3 object has 120-degree pattern symmetry; 12 history frames at 30 deg/frame are one imposed 360-degree geometric rotation = three pattern cycles',
      'cases':CASES,
      'parameters':{'train_frames':TRAIN_FRAMES,'free_frames':FREE_FRAMES,'rotation_step_deg':ROT_STEP_DEG,'domain_l1':DOMAIN_L1,'domain_points':len(DOMAIN),'measure_l1':MEASURE_L1},
      'checks':{'boundary_unreachable':guard,'births':{k:v['births_total'] for k,v in results.items()}},
      'free_phase_stats':stats,
      'raw_phase_series':{k:[r['m3_post'] for r in v['rows']] for k,v in results.items()},
      'journal':'complete phi input/output, sparse flow, imposed-history metadata, m3 scalar-field moment and flow moment every frame/case'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
