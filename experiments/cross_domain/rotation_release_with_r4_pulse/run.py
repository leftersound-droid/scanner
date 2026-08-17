from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step, directions

OUT = ROOT / 'run-data' / 'cross_domain' / 'rotation_release_with_r4_pulse'
DIM=4; BACKGROUND=100.0; OBJ_TOTAL=160.0; SIGMA=0.62
DOMAIN_L1=32; ROT_STEP_DEG=30.0; TRAIN_FRAMES=12; FREE_FRAMES=12; TOTAL_FRAMES=TRAIN_FRAMES+FREE_FRAMES
MEASURE_L1=6; FLOW_PERIOD=12; FLOW_AMP=0.01
DS=directions(DIM)

# The R4 pulse is exactly the previously used longitudinal-flow representation:
# sinusoidal previous_flow along +/-w, injected before operator evaluation.
# No angular momentum, torque, inertia, damping, charge, EM law, or free-rotation target is injected.
CASES=[
  {'name':'release_pulse_continues','forced_rotation':True,'release_rotation':True,'pulse_train':True,'pulse_free':True},
  {'name':'release_pulse_off','forced_rotation':True,'release_rotation':True,'pulse_train':True,'pulse_free':False},
  {'name':'forced_continue_with_pulse','forced_rotation':True,'release_rotation':False,'pulse_train':True,'pulse_free':True},
  {'name':'static_with_pulse_control','forced_rotation':False,'release_rotation':True,'pulse_train':True,'pulse_free':True},
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


def impose_longitudinal_flow(prev,frame,on):
    merged=dict(prev)
    if not on: return merged,0.0,0,None
    s=math.sin(2.0*math.pi*frame/FLOW_PERIOD)
    amp=FLOW_AMP*abs(s)
    if amp<1e-15: return merged,0.0,0,None
    di=7 if s>0.0 else 6
    step=1 if di==7 else -1
    count=0
    for c in DOMAIN:
        target=(c[0],c[1],c[2],c[3]+step)
        if target in DOMAIN_SET:
            merged[(c,di)]=merged.get((c,di),0.0)+amp
            count+=1
    return merged,amp,count,('+w' if step>0 else '-w')


def save_flow(path,flow):
    items=[(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v!=0.0]
    if not items:
        np.savez_compressed(path,source_index=np.empty(0,dtype=np.int32),direction=np.empty(0,dtype=np.uint8),amount=np.empty(0,dtype=np.float64)); return
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
        q += excess*complex(math.cos(3*ang),math.sin(3*ang))
        weight += excess
    amp=abs(q)/(weight+1e-30)
    phase=(math.atan2(q.imag,q.real)/3.0) if abs(q)>0 else 0.0
    phase=phase%(2*math.pi/3)
    return {'amplitude':float(amp),'phase_deg_mod_120':float(math.degrees(phase)),'positive_excess_weight':float(weight)}


def local_flow_m3(flow):
    q=0j; total=0.0; localset=set(LOCAL)
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


def unwrap120(degs):
    out=[]
    for d in degs:
        if not out: out.append(float(d)); continue
        candidates=[d+120*k for k in range(-16,17)]
        out.append(float(min(candidates,key=lambda x:abs(x-out[-1]))))
    return out


def run_case(case):
    cdir=OUT/case['name']; fdir=cdir/'flows'; cdir.mkdir(parents=True,exist_ok=True); fdir.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old={}; rows=[]; pin=[]; pout=[]; births=0
    for frame in range(TOTAL_FRAMES):
        in_history=frame<TRAIN_FRAMES
        rotation_forced = case['forced_rotation'] and (in_history or not case['release_rotation'])
        if rotation_forced:
            theta=math.radians(ROT_STEP_DEG*frame)
            new=object_component(theta); apply_component(phi,old,new); old=new
            imposed_theta_deg=ROT_STEP_DEG*frame
        elif (not case['forced_rotation']) and frame==0:
            new=object_component(0.0); apply_component(phi,old,new); old=new; imposed_theta_deg=0.0
        else:
            imposed_theta_deg=None

        pulse_on=case['pulse_train'] if in_history else case['pulse_free']
        op_prev,pulse_amp,pulse_edges,pulse_dir=impose_longitudinal_flow(prev,frame,pulse_on)
        before=sum(phi.values()); pre=m3_moment(phi)
        pin.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_input.npz',op_prev)
        phi,nxt,diag=operator_step(phi,op_prev,dimension=DIM)
        post=m3_moment(phi); fm=local_flow_m3(nxt)
        pout.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_output.npz',nxt)
        rows.append({'frame':frame,'phase':'history' if in_history else 'free_or_control',
                     'rotation_forced_this_frame':rotation_forced,'imposed_theta_deg':imposed_theta_deg,
                     'r4_pulse_on':pulse_on,'r4_pulse_amplitude':pulse_amp,'r4_pulse_direction':pulse_dir,'r4_pulse_edges':pulse_edges,
                     'm3_pre':pre,'m3_post':post,'flow_m3':fm,'births':diag.births,
                     'live_transfer':float(diag.live_transfer),'conservation_error':float(sum(phi.values())-before)})
        births+=diag.births; prev=nxt
    phases=[r['m3_post']['phase_deg_mod_120'] for r in rows]; uw=unwrap120(phases)
    for r,u in zip(rows,uw): r['m3_post']['phase_deg_unwrapped_analysis']=u
    np.savez_compressed(cdir/'phi_history.npz',phi_input=np.stack(pin),phi_output=np.stack(pout))
    return {'case':case,'rows':rows,'births_total':births}


def free_stats(rows):
    free=rows[TRAIN_FRAMES:]
    p=np.asarray([r['m3_post']['phase_deg_unwrapped_analysis'] for r in free],float)
    a=np.asarray([r['m3_post']['amplitude'] for r in free],float)
    fp=np.asarray([r['flow_m3']['phase_deg_mod_120'] for r in free],float)
    fa=np.asarray([r['flow_m3']['amplitude'] for r in free],float)
    f=np.arange(len(p),dtype=float); steps=np.diff(p)
    return {'phase_slope_deg_per_frame_analysis':float(np.polyfit(f,p,1)[0]),
            'mean_abs_phase_step_deg':float(np.mean(np.abs(steps))),
            'signed_mean_phase_step_deg':float(np.mean(steps)),
            'phase_steps_deg':[float(x) for x in steps],
            'amplitude_start':float(a[0]),'amplitude_end':float(a[-1]),'amplitude_mean':float(np.mean(a)),
            'amplitude_retention_end_over_start':float(a[-1]/(a[0]+1e-30)),
            'flow_m3_amplitude_mean':float(np.mean(fa)),
            'flow_m3_phase_mod120_series':[float(x) for x in fp]}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,dtype=np.int16),local_coord=np.asarray(LOCAL,dtype=np.int16))
    # Numerical guard for the local object perturbation only; the R4 pulse is intentionally imposed throughout the fixed domain.
    guard=7+TOTAL_FRAMES < DOMAIN_L1
    if not guard: raise RuntimeError('fixed domain too small for local object causal isolation')
    results={c['name']:run_case(c) for c in CASES}
    stats={k:free_stats(v['rows']) for k,v in results.items()}
    summary={'experiment':'rotation_release_with_r4_pulse',
      'status':'synthetic history-release test using the previously established R4 periodic previous-flow representation; no physical mass/charge/EM/inertia law claimed',
      'operator':'unchanged scanner.self_reflexive_operator.operator_step',
      'question':'after one full forced rotation history, does continued R4 periodic flow preserve autonomous m=3 rotation/structure better than switching the R4 pulse off?',
      'r4_pulse_definition':'same as phase_memory_longitudinal_flow: sinusoidal previous_flow along +w/-w, magnitude FLOW_AMP*abs(sin(2pi frame/FLOW_PERIOD))',
      'cases':CASES,
      'parameters':{'train_frames':TRAIN_FRAMES,'free_frames':FREE_FRAMES,'rotation_step_deg':ROT_STEP_DEG,
                    'flow_period_frames':FLOW_PERIOD,'flow_amplitude':FLOW_AMP,'domain_l1':DOMAIN_L1,
                    'domain_points':len(DOMAIN),'measure_l1':MEASURE_L1},
      'checks':{'local_object_boundary_unreachable':guard,'births':{k:v['births_total'] for k,v in results.items()}},
      'free_phase_stats':stats,
      'raw_phase_series':{k:[r['m3_post'] for r in v['rows']] for k,v in results.items()},
      'journal':'complete phi input/output, sparse flow input/output, imposed rotation metadata, R4 pulse metadata, scalar m3 and local flow m3 every frame/case'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
