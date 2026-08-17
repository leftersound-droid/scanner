from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step, directions

OUT = ROOT / 'run-data' / 'cross_domain' / 'r4_pulse_rotation_free_release'
DIM=4; BACKGROUND=100.0; OBJ_TOTAL=160.0; SIGMA=0.62
DOMAIN_L1=38; ROT_STEP_DEG=30.0; TRAIN_FRAMES=12; FREE_FRAMES=12; TOTAL_FRAMES=24
FLOW_PERIOD=12; FLOW_AMP=0.01; MEASURE_L1=6
DS=directions(DIM)

# Reuses the already-established synthetic R4 longitudinal pulsation definition from
# phase_memory_longitudinal_flow: previous-flow input along +/-w with
# amplitude FLOW_AMP*abs(sin(2*pi*frame/FLOW_PERIOD)).
# No angular momentum, torque, damping, inertia, EM law or free-rotation law is added.
CASES=[
  {'name':'release_rotation_keep_r4_pulse','keep_pulse_after_release':True},
  {'name':'release_rotation_and_r4_pulse','keep_pulse_after_release':False},
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


def actual_source_support_l1():
    support=0
    for frame in range(TRAIN_FRAMES):
        comp=object_component(math.radians(ROT_STEP_DEG*frame))
        if comp:
            support=max(support,max(sum(abs(v) for v in c) for c in comp))
    return support


def apply_component(phi,old,new):
    for c in set(old)|set(new):
        phi[c]+=new.get(c,0.0)-old.get(c,0.0)


def impose_r4_pulse(prev, frame, on):
    merged=dict(prev)
    if not on: return merged,0.0,0,None
    s=math.sin(2.0*math.pi*frame/FLOW_PERIOD)
    amp=FLOW_AMP*abs(s)
    if amp<1e-15: return merged,0.0,0,0
    di=7 if s>0.0 else 6
    step=1 if di==7 else -1
    count=0
    for c in DOMAIN:
        target=(c[0],c[1],c[2],c[3]+step)
        if target in DOMAIN_SET:
            merged[(c,di)]=merged.get((c,di),0.0)+amp
            count+=1
    return merged,amp,count,step


def save_flow(path,flow):
    items=[(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v!=0.0]
    np.savez_compressed(path,
        source_index=np.asarray([q[0] for q in items],dtype=np.int32),
        direction=np.asarray([q[1] for q in items],dtype=np.uint8),
        amount=np.asarray([q[2] for q in items],dtype=np.float64))


def m3_moment(phi):
    q=0j; weight=0.0
    for c in LOCAL:
        x,y,z,w=c
        if x==0 and y==0: continue
        excess=phi[c]-BACKGROUND
        if excess<=0: continue
        ang=math.atan2(y,x)
        q += excess*complex(math.cos(3*ang),math.sin(3*ang)); weight += excess
    amp=abs(q)/(weight+1e-30)
    phase=(math.atan2(q.imag,q.real)/3.0) if abs(q)>0 else 0.0
    phase=phase%(2*math.pi/3)
    return {'amplitude':float(amp),'phase_deg_mod_120':float(math.degrees(phase)),
            'positive_excess_weight':float(weight)}


def unwrap_m3_phase(degs):
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
        in_history = frame < TRAIN_FRAMES
        if in_history:
            theta=math.radians(ROT_STEP_DEG*frame)
            new=object_component(theta); apply_component(phi,old,new); old=new
            imposed_theta_deg=ROT_STEP_DEG*frame
        else:
            imposed_theta_deg=None

        pulse_on = in_history or case['keep_pulse_after_release']
        op_prev,pulse_amp,pulse_edges,pulse_w_sign=impose_r4_pulse(prev,frame,pulse_on)
        before=sum(phi.values())
        pin.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_input.npz',op_prev)
        phi,nxt,diag=operator_step(phi,op_prev,dimension=DIM)
        pout.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_output.npz',nxt)
        rows.append({'frame':frame,'phase':'history' if in_history else 'free',
                     'rotation_forced':bool(in_history),'imposed_theta_deg':imposed_theta_deg,
                     'r4_pulse_on':bool(pulse_on),'r4_pulse_amplitude':float(pulse_amp),
                     'r4_pulse_edges':int(pulse_edges),'r4_pulse_w_sign':pulse_w_sign,
                     'm3_post':m3_moment(phi),'births':diag.births,
                     'live_transfer':float(diag.live_transfer),
                     'conservation_error':float(sum(phi.values())-before)})
        births+=diag.births; prev=nxt
    np.savez_compressed(cdir/'phi_history.npz',phi_input=np.stack(pin),phi_output=np.stack(pout))
    phases=[r['m3_post']['phase_deg_mod_120'] for r in rows]
    uw=unwrap_m3_phase(phases)
    for r,u in zip(rows,uw): r['m3_post']['phase_deg_unwrapped_analysis']=u
    return {'case':case,'rows':rows,'births_total':births}


def free_stats(rows):
    free=rows[TRAIN_FRAMES:]
    p=np.asarray([r['m3_post']['phase_deg_unwrapped_analysis'] for r in free],float)
    a=np.asarray([r['m3_post']['amplitude'] for r in free],float)
    f=np.arange(len(p),dtype=float)
    steps=np.diff(p)
    return {
      'phase_slope_deg_per_frame_analysis':float(np.polyfit(f,p,1)[0]),
      'phase_steps_deg':[float(x) for x in steps],
      'signed_mean_phase_step_deg':float(np.mean(steps)),
      'mean_abs_phase_step_deg':float(np.mean(np.abs(steps))),
      'amplitude_start':float(a[0]),'amplitude_end':float(a[-1]),'amplitude_mean':float(np.mean(a)),
      'amplitude_retention_end_over_start':float(a[-1]/(a[0]+1e-30)),
      'positive_direction_step_fraction':float(np.mean(steps>0.0)) if len(steps) else 0.0
    }


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,dtype=np.int16),local_coord=np.asarray(LOCAL,dtype=np.int16))
    source_support=actual_source_support_l1()
    guard=source_support+TOTAL_FRAMES < DOMAIN_L1
    if not guard: raise RuntimeError('fixed domain too small for causal boundary isolation')
    results={c['name']:run_case(c) for c in CASES}
    stats={k:free_stats(v['rows']) for k,v in results.items()}
    no_births=all(v['births_total']==0 for v in results.values())
    summary={
      'experiment':'r4_pulse_rotation_free_release',
      'status':'synthetic pulse/history-release test; operator unchanged; no angular momentum, torque, damping, inertia, EM law or target free-rotation law injected',
      'operator':'unchanged scanner.self_reflexive_operator.operator_step',
      'question':'after one forced 360-degree rotation while the established periodic R4 previous-flow pulsation is present, does rotation persist when rotational forcing is removed, and does persistence differ when the R4 pulsation remains vs is also removed?',
      'r4_pulse_definition':'same as phase_memory_longitudinal_flow: +/-w previous-flow input, magnitude FLOW_AMP*abs(sin(2*pi*frame/FLOW_PERIOD))',
      'cases':CASES,
      'parameters':{'train_frames':TRAIN_FRAMES,'free_frames':FREE_FRAMES,'rotation_step_deg':ROT_STEP_DEG,
                    'r4_flow_period_frames':FLOW_PERIOD,'r4_flow_amplitude':FLOW_AMP,
                    'domain_l1':DOMAIN_L1,'domain_points':len(DOMAIN),'measure_l1':MEASURE_L1,
                    'actual_source_support_l1':source_support},
      'checks':{'boundary_unreachable':guard,'zero_births_required_for_validity':no_births,
                'births':{k:v['births_total'] for k,v in results.items()}},
      'free_stats':stats,
      'raw_rows':{k:v['rows'] for k,v in results.items()},
      'journal':'complete phi input/output, sparse flow input/output, imposed rotation history, R4 pulse metadata and m3 measurement every frame/case'
    }
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
