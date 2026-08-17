from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step

OUT = ROOT / 'run-data' / 'cross_domain' / 'phase_memory_longitudinal_flow'
DIM=4
BACKGROUND=100.0
WAVE_AMP=10.0
RING_R=2.0
SIGMA=0.55
DOMAIN_L1=24
WAVE_SUPPORT_L1=10
FRAMES=12
FLOW_PERIOD=12
FLOW_AMP=0.01
MEASURE_L1=7
MAX_DERIV=3

CASES=[
 {'name':'flow_only','m':None,'step_deg':0.0,'flow_on':True},
 {'name':'m3_wave_only','m':3,'step_deg':10.0,'flow_on':False},
 {'name':'m3_with_longitudinal_flow','m':3,'step_deg':10.0,'flow_on':True},
 {'name':'m4_wave_only','m':4,'step_deg':15.0,'flow_on':False},
 {'name':'m4_with_longitudinal_flow','m':4,'step_deg':15.0,'flow_on':True},
]


def fixed_domain():
    r=range(-DOMAIN_L1,DOMAIN_L1+1)
    return [tuple(int(v) for v in c) for c in product(r,repeat=4) if sum(abs(v) for v in c)<=DOMAIN_L1]
DOMAIN=fixed_domain(); DOMAIN_SET=set(DOMAIN); INDEX={c:i for i,c in enumerate(DOMAIN)}
MEASURE=[c for c in DOMAIN if sum(abs(v) for v in c)<=MEASURE_L1]


def wave_component(m,theta):
    if m is None: return {}
    comp={}
    for c in product(range(-5,6),repeat=4):
        x,y,z,w=(float(v) for v in c)
        rho=math.hypot(x,y)
        d2=(rho-RING_R)**2+z*z+w*w
        env=math.exp(-0.5*d2/(SIGMA*SIGMA))
        if env<1e-10: continue
        ang=math.atan2(y,x)
        val=WAVE_AMP*env*(1.0+0.35*math.cos(m*(ang-theta)))
        if val>1e-10: comp[tuple(int(v) for v in c)]=val
    return comp


def apply_component(phi,old,new):
    for c in set(old)|set(new): phi[c]+=new.get(c,0.0)-old.get(c,0.0)


def impose_longitudinal_flow(prev,frame,on):
    merged=dict(prev)
    if not on: return merged,0.0,0
    s=math.sin(2.0*math.pi*frame/FLOW_PERIOD)
    amp=FLOW_AMP*abs(s)
    if amp<1e-15: return merged,0.0,0
    di=7 if s>0.0 else 6
    step=1 if di==7 else -1
    count=0
    for c in DOMAIN:
        target=(c[0],c[1],c[2],c[3]+step)
        if target in DOMAIN_SET:
            merged[(c,di)]=merged.get((c,di),0.0)+amp
            count+=1
    return merged,amp,count


def full_phi(phi): return np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)
def sample_phi(phi): return np.asarray([phi[c] for c in MEASURE],dtype=np.float64)


def save_flow(path,flow):
    items=[(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v!=0.0]
    if not items:
        np.savez_compressed(path,source_index=np.empty(0,dtype=np.int32),direction=np.empty(0,dtype=np.uint8),amount=np.empty(0,dtype=np.float64)); return
    np.savez_compressed(path,source_index=np.asarray([x[0] for x in items],dtype=np.int32),direction=np.asarray([x[1] for x in items],dtype=np.uint8),amount=np.asarray([x[2] for x in items],dtype=np.float64))


def derivative_reconstruction(hist):
    flat=np.asarray(hist,dtype=np.float64); diffs=[flat]
    for _ in range(MAX_DERIV): diffs.append(np.diff(diffs[-1],axis=0))
    idx=np.arange(flat.shape[1]); train=(idx%5)!=0; test=~train; out={}
    for k in range(MAX_DERIV+1):
        Xs=[]; ys=[]
        for t in range(k,len(flat)-1):
            Xs.append(np.stack([flat[t]]+[diffs[o][t-o] for o in range(1,k+1)],axis=1)); ys.append(flat[t+1])
        if not Xs: out[str(k)]={'available':False}; continue
        X=np.concatenate(Xs); y=np.concatenate(ys); tr=np.tile(train,len(Xs)); te=np.tile(test,len(Xs))
        A=np.column_stack([np.ones(tr.sum()),X[tr]]); coef,*_=np.linalg.lstsq(A,y[tr],rcond=None)
        pred=np.column_stack([np.ones(te.sum()),X[te]])@coef
        rmse=float(np.sqrt(np.mean((pred-y[te])**2))); sd=float(np.std(y[te]))
        out[str(k)]={'available':True,'rmse':rmse,'normalized_rmse':rmse/sd if sd else 0.0,'coef':[float(v) for v in coef]}
    return out


def corr(rows,a,b):
    x=np.asarray([r[a] for r in rows],dtype=float); y=np.asarray([r[b] for r in rows],dtype=float)
    if np.std(x)==0.0 or np.std(y)==0.0: return None
    return float(np.corrcoef(x,y)[0,1])


def run_case(spec):
    case_dir=OUT/spec['name']; flow_dir=case_dir/'flows'; case_dir.mkdir(parents=True,exist_ok=True); flow_dir.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old_wave={}; hist=[]; rows=[]; births=0; phi_in=[]; phi_out=[]
    for frame in range(FRAMES):
        theta=math.radians(spec['step_deg']*frame); nw=wave_component(spec['m'],theta); apply_component(phi,old_wave,nw); old_wave=nw
        hist.append(sample_phi(phi)); phi_in.append(full_phi(phi))
        op_prev,flow_amp,flow_edges=impose_longitudinal_flow(prev,frame,spec['flow_on']); save_flow(flow_dir/f'frame_{frame:02d}_input.npz',op_prev)
        before=sum(phi.values()); phi,next_flow,diag=operator_step(phi,op_prev,dimension=DIM); phi_out.append(full_phi(phi)); save_flow(flow_dir/f'frame_{frame:02d}_output.npz',next_flow)
        births+=diag.births; b=np.asarray(diag.beta_samples,dtype=float)
        rows.append({'frame':frame,'flow_amplitude':flow_amp,'flow_edges':flow_edges,'live_transfer':float(diag.live_transfer),'beta_mean':float(b.mean()) if b.size else 0.0,'beta_std':float(b.std()) if b.size else 0.0,'conservation_error':float(sum(phi.values())-before),'births':diag.births})
        prev=next_flow
    theta=math.radians(spec['step_deg']*FRAMES); nw=wave_component(spec['m'],theta); apply_component(phi,old_wave,nw); hist.append(sample_phi(phi))
    np.savez_compressed(case_dir/'phi_history.npz',phi_input=np.stack(phi_in),phi_output=np.stack(phi_out))
    closure=float(np.sqrt(np.mean((hist[-1]-hist[0])**2)))
    return {'case':spec,'frames':FRAMES,'births_total':births,'boundary_unreachable':(WAVE_SUPPORT_L1+FRAMES)<DOMAIN_L1,'cycle_closure_rmse_pre_operator':closure,'rows':rows,'graph_scan':{'flow_amp_to_beta_mean':corr(rows,'flow_amplitude','beta_mean'),'flow_amp_to_live_transfer':corr(rows,'flow_amplitude','live_transfer'),'beta_mean_to_live_transfer':corr(rows,'beta_mean','live_transfer')},'derivative_reconstruction_phi':derivative_reconstruction(hist)}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result={'experiment':'phase_memory_longitudinal_flow','status':'synthetic flow-input test; no physical emergence claim','definitions':{
      'phase_field':'periodic previous-flow component along the fourth lattice axis; positive half-cycle uses +w, negative half-cycle uses -w; magnitude = FLOW_AMP*abs(sin phase)',
      'injection':'added only to previous_flow before operator evaluation; operator formula unchanged',
      'wave':'non-rigid closed m-peak potential wave; no rigid-body rotation',
      'fixed_domain':'all points with L1 norm <=24 pre-exist; no boundary rule',
      'journal':'domain_coordinates.npz defines row index; every case stores complete phi input/output arrays and sparse raw flow input/output for every frame'
    },'parameters':{'flow_period_frames':FLOW_PERIOD,'flow_amplitude':FLOW_AMP,'frames':FRAMES,'domain_l1_radius':DOMAIN_L1,'domain_points':len(DOMAIN),'wave_support_l1':WAVE_SUPPORT_L1},'cases':{}}
    np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,dtype=np.int16),measurement_coord=np.asarray(MEASURE,dtype=np.int16))
    for s in CASES: result['cases'][s['name']]=run_case(s)
    (OUT/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
