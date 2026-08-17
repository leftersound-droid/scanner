from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step, directions, add

OUT = ROOT / 'run-data' / 'cross_domain' / 'charged_candidate_r3_field_propagation'
DIM=4; BACKGROUND=100.0; OBJ_TOTAL=160.0; SIGMA=0.62
DOMAIN_L1=24; FRAMES=10; MOVE_CADENCE=0.5; ROT_STEP_DEG=30.0
DS=directions(DIM)
SHELL_RADII=[4,6,8,10]

# Working-hypothesis probe only. No electric field, charge, photon, Maxwell law,
# light speed, Coulomb law or propagation law is inserted.
CASES=[
    {'name':'A_rot_asym_moving','asymmetric':True,'rotating':True,'moving':True},
    {'name':'B_rot_asym_rest','asymmetric':True,'rotating':True,'moving':False},
    {'name':'C_sym_nonrot_moving','asymmetric':False,'rotating':False,'moving':True},
]


def fixed_domain():
    r=range(-DOMAIN_L1,DOMAIN_L1+1)
    return [tuple(int(v) for v in c) for c in product(r,repeat=4)
            if sum(abs(v) for v in c)<=DOMAIN_L1]
DOMAIN=fixed_domain(); DOMAIN_SET=set(DOMAIN); INDEX={c:i for i,c in enumerate(DOMAIN)}


def source_component(case, frame):
    cx=(MOVE_CADENCE*frame) if case['moving'] else 0.0
    theta=math.radians(ROT_STEP_DEG*frame) if case['rotating'] else 0.0
    comp={}
    for c in product(range(-7,8),repeat=4):
        x,y,z,w=(float(v) for v in c)
        xx=x-cx
        rho=math.hypot(xx,y); r0=2.0
        d2=(rho-r0)**2+z*z+w*w
        env=math.exp(-0.5*d2/(SIGMA*SIGMA))
        if case['asymmetric']:
            ang=math.atan2(y,xx)
            val=env*(1.0+0.35*math.cos(3*(ang-theta)))
        else:
            val=env
        if val>1e-12: comp[tuple(int(v) for v in c)]=val
    s=sum(comp.values())
    if s<=0:return {},cx,theta
    k=OBJ_TOTAL/s
    return {c:v*k for c,v in comp.items()},cx,theta


def apply_component(phi,old,new):
    for c in set(old)|set(new):
        phi[c]+=new.get(c,0.0)-old.get(c,0.0)


def save_flow(path,flow):
    items=[(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v!=0.0]
    np.savez_compressed(path,
        source_index=np.asarray([q[0] for q in items],dtype=np.int32),
        direction=np.asarray([q[1] for q in items],dtype=np.uint8),
        amount=np.asarray([q[2] for q in items],dtype=np.float64))


def r3_shell_points(radius,cx):
    pts=[]
    for c in DOMAIN:
        x,y,z,w=c
        if w!=0: continue
        rr=math.sqrt((x-cx)**2+y*y+z*z)
        if abs(rr-radius)<=0.55: pts.append(c)
    return pts


def r4_axis_points(radius,cx):
    pts=[]
    # matched-distance control along the fourth coordinate, near source x position
    x0=int(round(cx))
    for s in (-1,1):
        c=(x0,0,0,s*radius)
        if c in DOMAIN_SET: pts.append(c)
    return pts


def shell_metrics(phi,flow,cx):
    out={}
    for r in SHELL_RADII:
        p3=r3_shell_points(r,cx); p4=r4_axis_points(r,cx)
        def metrics(pts):
            if not pts:return {'n':0,'mean_abs_phi_excess':0.0,'rms_phi_excess':0.0,'out_flow':0.0}
            vals=np.asarray([phi[p]-BACKGROUND for p in pts],float)
            ps=set(pts)
            f=sum(v for (p,di),v in flow.items() if p in ps and v>0)
            return {'n':len(pts),'mean_abs_phi_excess':float(np.mean(np.abs(vals))),
                    'rms_phi_excess':float(np.sqrt(np.mean(vals*vals))),'out_flow':float(f)}
        out[str(r)]={'R3':metrics(p3),'R4_axis':metrics(p4)}
    return out


def run_case(case):
    cdir=OUT/case['name']; fdir=cdir/'flows'; cdir.mkdir(parents=True,exist_ok=True); fdir.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old={}; rows=[]; births=0
    pin=[]; pout=[]
    for frame in range(FRAMES):
        new,cx,theta=source_component(case,frame); apply_component(phi,old,new); old=new
        before=sum(phi.values())
        pin.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_input.npz',prev)
        phi,nxt,diag=operator_step(phi,prev,dimension=DIM)
        pout.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(fdir/f'{frame:02d}_output.npz',nxt)
        rows.append({'frame':frame,'center_x':cx,'theta_rad':theta,'births':diag.births,
                     'live_transfer':float(diag.live_transfer),'conservation_error':float(sum(phi.values())-before),
                     'shells':shell_metrics(phi,nxt,cx)})
        births+=diag.births; prev=nxt
    np.savez_compressed(cdir/'phi_history.npz',phi_input=np.stack(pin),phi_output=np.stack(pout))
    return {'case':case,'rows':rows,'births_total':births}


def analyze(results):
    # Arrival is a comparative Scanner measurement, not a physical threshold:
    # first frame where A exceeds both controls at the same shell in R3.
    arrivals={}; contrasts={}
    for r in SHELL_RADII:
        k=str(r); arrivals[k]=None; series=[]
        for f in range(FRAMES):
            a=results['A_rot_asym_moving']['rows'][f]['shells'][k]['R3']['rms_phi_excess']
            b=results['B_rot_asym_rest']['rows'][f]['shells'][k]['R3']['rms_phi_excess']
            c=results['C_sym_nonrot_moving']['rows'][f]['shells'][k]['R3']['rms_phi_excess']
            contrast=a-max(b,c)
            series.append(float(contrast))
            if arrivals[k] is None and contrast>0:
                arrivals[k]=f
        contrasts[k]=series
    # Raw R3-vs-R4 response ratios for A; not interpreted as electric-field law.
    ratios={}
    for r in SHELL_RADII:
        k=str(r); vals=[]
        for row in results['A_rot_asym_moving']['rows']:
            a=row['shells'][k]['R3']['rms_phi_excess']; b=row['shells'][k]['R4_axis']['rms_phi_excess']
            vals.append(float(a/(b+1e-30)))
        ratios[k]=vals
    return arrivals,contrasts,ratios


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,dtype=np.int16))
    # Numerical validity guard only: source support + max translation + causal steps must fit fixed domain.
    guard=7+math.ceil(MOVE_CADENCE*(FRAMES-1))+FRAMES < DOMAIN_L1
    if not guard: raise RuntimeError('fixed domain too small for causal boundary isolation')
    results={c['name']:run_case(c) for c in CASES}
    arrivals,contrasts,ratios=analyze(results)
    summary={'experiment':'charged_candidate_r3_field_propagation',
      'status':'synthetic source-response control; no electric field, charge, photon, Maxwell/Coulomb law, c or propagation law injected or claimed',
      'operator':'unchanged scanner.self_reflexive_operator.operator_step',
      'working_hypothesis':'rotating asymmetric R4 object is a charged-particle candidate; one necessary condition for an electric-field interpretation is a source-dependent response propagating in R3',
      'cases':CASES,'parameters':{'frames':FRAMES,'domain_l1':DOMAIN_L1,'domain_points':len(DOMAIN),'move_cadence':MOVE_CADENCE,'rotation_step_deg':ROT_STEP_DEG,'shell_radii':SHELL_RADII},
      'checks':{'boundary_unreachable':guard,'births':{k:v['births_total'] for k,v in results.items()}},
      'r3_arrival_frame_A_above_both_controls':arrivals,
      'r3_contrast_series_A_minus_max_controls':contrasts,
      'A_r3_over_r4_axis_rms_series':ratios,
      'journal':'complete phi input/output, sparse flows, source center/orientation and shell measurements for every frame/case'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
