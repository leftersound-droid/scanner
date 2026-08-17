from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
from scanner.self_reflexive_operator import operator_step

OUT=ROOT/'run-data'/'cross_domain'/'r4_pulse_rotation_release'
DIM=4; BACKGROUND=100.0; OBJ_TOTAL=160.0; SIGMA=0.62
DOMAIN_L1=32; MEASURE_L1=6
ROT_STEP_DEG=30.0; TRAIN_FRAMES=12; FREE_FRAMES=12; TOTAL_FRAMES=24
FLOW_PERIOD=12; FLOW_AMP=0.01
CASES=[
 {'name':'release_pulse_continues','pulse_after_release':True},
 {'name':'release_pulse_off','pulse_after_release':False},
]

def fixed_domain():
    r=range(-DOMAIN_L1,DOMAIN_L1+1)
    return [tuple(int(v) for v in c) for c in product(r,repeat=4) if sum(abs(v) for v in c)<=DOMAIN_L1]
DOMAIN=fixed_domain(); DOMAIN_SET=set(DOMAIN); INDEX={c:i for i,c in enumerate(DOMAIN)}
LOCAL=[c for c in DOMAIN if sum(abs(v) for v in c)<=MEASURE_L1]

def object_component(theta):
    comp={}
    for c in product(range(-7,8),repeat=4):
        x,y,z,w=(float(v) for v in c); rho=math.hypot(x,y)
        d2=(rho-2.0)**2+z*z+w*w
        env=math.exp(-0.5*d2/(SIGMA*SIGMA))
        ang=math.atan2(y,x)
        val=env*(1.0+0.35*math.cos(3*(ang-theta)))
        if val>1e-12: comp[tuple(int(v) for v in c)]=val
    s=sum(comp.values()); k=OBJ_TOTAL/s
    return {c:v*k for c,v in comp.items()}

def apply_component(phi,old,new):
    for c in set(old)|set(new): phi[c]+=new.get(c,0.0)-old.get(c,0.0)

def impose_r4_pulse(prev,frame,on):
    merged=dict(prev)
    if not on: return merged,0.0,0,None
    s=math.sin(2.0*math.pi*frame/FLOW_PERIOD); amp=FLOW_AMP*abs(s)
    if amp<1e-15: return merged,0.0,0,None
    di=7 if s>0 else 6; step=1 if di==7 else -1; count=0
    for c in DOMAIN:
        target=(c[0],c[1],c[2],c[3]+step)
        if target in DOMAIN_SET:
            merged[(c,di)]=merged.get((c,di),0.0)+amp; count+=1
    return merged,amp,count,('+w' if step>0 else '-w')

def m3_moment(phi):
    q=0j; weight=0.0
    for c in LOCAL:
        x,y,z,w=c
        if x==0 and y==0: continue
        excess=phi[c]-BACKGROUND
        if excess<=0: continue
        ang=math.atan2(y,x)
        q+=excess*complex(math.cos(3*ang),math.sin(3*ang)); weight+=excess
    amp=abs(q)/(weight+1e-30)
    phase=(math.atan2(q.imag,q.real)/3.0 if abs(q)>0 else 0.0)%(2*math.pi/3)
    return {'amplitude':float(amp),'phase_deg_mod_120':float(math.degrees(phase)),'positive_excess_weight':float(weight)}

def unwrap(degs):
    out=[]
    for d in degs:
        if not out: out.append(float(d)); continue
        cand=[d+120*k for k in range(-12,13)]
        out.append(float(min(cand,key=lambda x:abs(x-out[-1]))))
    return out

def save_flow(path,flow):
    items=[(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v!=0.0]
    np.savez_compressed(path,
      source_index=np.asarray([x[0] for x in items],dtype=np.int32),
      direction=np.asarray([x[1] for x in items],dtype=np.uint8),
      amount=np.asarray([x[2] for x in items],dtype=np.float64))

def run_case(spec):
    cdir=OUT/spec['name']; fdir=cdir/'flows'; cdir.mkdir(parents=True,exist_ok=True); fdir.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old={}; rows=[]; pin=[]; pout=[]; births=0
    for frame in range(TOTAL_FRAMES):
        training=frame<TRAIN_FRAMES
        if training:
            new=object_component(math.radians(ROT_STEP_DEG*frame)); apply_component(phi,old,new); old=new
            imposed_theta=ROT_STEP_DEG*frame
        else:
            imposed_theta=None
        pulse_on=training or spec['pulse_after_release']
        op_prev,pamp,pedges,pdir=impose_r4_pulse(prev,frame,pulse_on)
        pre=m3_moment(phi); pin.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_input.npz',op_prev)
        before=sum(phi.values()); phi,nxt,diag=operator_step(phi,op_prev,dimension=DIM)
        post=m3_moment(phi); pout.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_output.npz',nxt)
        rows.append({'frame':frame,'phase':'training' if training else 'free','rotation_forced':training,'imposed_theta_deg':imposed_theta,
          'r4_pulse_on':pulse_on,'r4_pulse_amplitude':pamp,'r4_pulse_direction':pdir,'r4_pulse_edges':pedges,
          'm3_pre':pre,'m3_post':post,'live_transfer':float(diag.live_transfer),'births':diag.births,
          'conservation_error':float(sum(phi.values())-before)})
        births+=diag.births; prev=nxt
    phases=[r['m3_post']['phase_deg_mod_120'] for r in rows]; un=unwrap(phases)
    for r,u in zip(rows,un): r['m3_post']['phase_deg_unwrapped_analysis']=u
    np.savez_compressed(cdir/'phi_history.npz',phi_input=np.stack(pin),phi_output=np.stack(pout))
    free=rows[TRAIN_FRAMES:]; p=np.asarray([r['m3_post']['phase_deg_unwrapped_analysis'] for r in free]); a=np.asarray([r['m3_post']['amplitude'] for r in free]); x=np.arange(len(p),dtype=float)
    return {'case':spec,'rows':rows,'births_total':births,'free_stats':{
      'phase_slope_deg_per_frame_analysis':float(np.polyfit(x,p,1)[0]),
      'phase_steps_deg':[float(v) for v in np.diff(p)],
      'signed_mean_phase_step_deg':float(np.mean(np.diff(p))),
      'mean_abs_phase_step_deg':float(np.mean(np.abs(np.diff(p)))),
      'amplitude_start':float(a[0]),'amplitude_end':float(a[-1]),'amplitude_mean':float(a.mean()),
      'amplitude_retention_end_over_start':float(a[-1]/(a[0]+1e-30))}}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,dtype=np.int16),local_coord=np.asarray(LOCAL,dtype=np.int16))
    guard=7+TOTAL_FRAMES<DOMAIN_L1
    if not guard: raise RuntimeError('fixed domain too small for causal boundary isolation')
    results={c['name']:run_case(c) for c in CASES}
    a=results['release_pulse_continues']['free_stats']; b=results['release_pulse_off']['free_stats']
    summary={'experiment':'r4_pulse_rotation_release',
      'status':'synthetic hypothesis test; R4 periodic previous-flow definition reused unchanged from phase_memory_longitudinal_flow; no angular momentum, torque, damping, EM law or free-rotation law injected',
      'question':'after identical one-cycle forced rotation + R4 pulse history, does continuing R4 periodic flow preserve autonomous m=3 rotation/structure better than switching the pulse off at release?',
      'operator':'unchanged scanner.self_reflexive_operator.operator_step',
      'r4_pulse_definition':'previous_flow component along fourth lattice axis; +w/-w alternates by sin(2*pi*frame/12), magnitude 0.01*abs(sin phase)',
      'parameters':{'train_frames':TRAIN_FRAMES,'free_frames':FREE_FRAMES,'rotation_step_deg':ROT_STEP_DEG,'flow_period':FLOW_PERIOD,'flow_amp':FLOW_AMP,'domain_l1':DOMAIN_L1,'domain_points':len(DOMAIN),'measure_l1':MEASURE_L1},
      'checks':{'boundary_unreachable':guard,'births':{k:v['births_total'] for k,v in results.items()}},
      'free_stats':{k:v['free_stats'] for k,v in results.items()},
      'comparative':{'phase_slope_difference_continue_minus_off':a['phase_slope_deg_per_frame_analysis']-b['phase_slope_deg_per_frame_analysis'],
        'amplitude_retention_ratio_continue_over_off':a['amplitude_retention_end_over_start']/(b['amplitude_retention_end_over_start']+1e-30)},
      'journal':'complete phi input/output, sparse flow input/output, pulse/forcing metadata and m3 moment each frame/case'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
