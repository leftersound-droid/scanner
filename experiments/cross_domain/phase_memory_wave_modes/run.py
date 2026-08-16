from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from scanner.self_reflexive_operator import operator_step

OUT = ROOT / "run-data" / "cross_domain" / "phase_memory_wave_modes"
DIM = 4
BACKGROUND = 100.0
PHASE_AMP = 0.01
WAVE_AMP = 10.0
RING_R = 2.0
SIGMA = 0.55
DOMAIN_L1 = 19
MAX_DERIV = 3

# Reused training protocol: m=3 advances 10 deg/frame, m=4 advances 15 deg/frame.
# Because an m-fold field pattern repeats after 360/m degrees of orientation,
# the complete FIELD-state cycles are 12 and 6 frames respectively.
CASES = [
    {"name":"m3_wave_only", "m":3, "step_deg":10.0, "phase_on":False},
    {"name":"m3_with_phase", "m":3, "step_deg":10.0, "phase_on":True},
    {"name":"m4_wave_only", "m":4, "step_deg":15.0, "phase_on":False},
    {"name":"m4_with_phase", "m":4, "step_deg":15.0, "phase_on":True},
]

def fixed_domain():
    pts=[]
    r=range(-DOMAIN_L1, DOMAIN_L1+1)
    for c in product(r, repeat=4):
        if sum(abs(v) for v in c) <= DOMAIN_L1:
            pts.append(tuple(int(v) for v in c))
    return pts

DOMAIN = fixed_domain()
INDEX = {c:i for i,c in enumerate(DOMAIN)}

def initial_phi():
    return {c:BACKGROUND for c in DOMAIN}

def wave_component(m:int, theta:float):
    comp={}
    for c in DOMAIN:
        x,y,z,w=(float(v) for v in c)
        if abs(x)+abs(y)+abs(z)+abs(w) > 5:
            continue
        rho=math.hypot(x,y)
        d2=(rho-RING_R)**2+z*z+w*w
        envelope=math.exp(-0.5*d2/(SIGMA**2))
        if envelope < 1e-12 or rho == 0.0:
            continue
        ang=math.atan2(y,x)
        mod=0.5*(1.0+math.cos(m*(ang-theta)))
        val=WAVE_AMP*envelope*mod
        if val > 1e-12:
            comp[c]=val
    return comp

def delta_component(old,new):
    return {c:new.get(c,0.0)-old.get(c,0.0) for c in (set(old)|set(new))}

def apply_delta(phi,d):
    signed=0.0; absolute=0.0
    for c,dv in d.items():
        phi[c]+=dv; signed+=dv; absolute+=abs(dv)
    return signed,absolute

def apply_uniform(phi,dv):
    if dv==0.0: return 0.0,0.0
    for c in phi: phi[c]+=dv
    return dv*len(phi), abs(dv)*len(phi)

def state_vector(phi):
    return np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)

def interior_mask(radius=5):
    return np.asarray([sum(abs(v) for v in c)<=radius for c in DOMAIN],dtype=bool)

MASK=interior_mask()

def deriv_reconstruct(history):
    h=history[:,MASK]
    diffs=[h]
    for _ in range(MAX_DERIV): diffs.append(np.diff(diffs[-1],axis=0))
    out={}
    spatial=np.arange(h.shape[1]); train=(spatial%5)!=0; test=~train
    for k in range(MAX_DERIV+1):
        blocks=[]; targets=[]
        for t in range(k,h.shape[0]-1):
            cols=[h[t]]+[diffs[j][t-j] for j in range(1,k+1)]
            blocks.append(np.stack(cols,axis=1)); targets.append(h[t+1])
        if not blocks:
            out[str(k)]={"available":False}; continue
        X=np.concatenate(blocks); y=np.concatenate(targets)
        tr=np.tile(train,len(blocks)); te=np.tile(test,len(blocks))
        A=np.column_stack([np.ones(tr.sum()),X[tr]])
        coef,_,rank,_=np.linalg.lstsq(A,y[tr],rcond=None)
        pred=np.column_stack([np.ones(te.sum()),X[te]])@coef
        rmse=float(np.sqrt(np.mean((pred-y[te])**2)))
        sd=float(np.std(y[te])); nrmse=rmse/sd if sd>0 else 0.0
        out[str(k)]={"available":True,"rank":int(rank),"rmse":rmse,"normalized_rmse":nrmse,"coef":[float(v) for v in coef]}
    return out

def run_case(spec):
    m=spec["m"]; step=math.radians(spec["step_deg"])
    cycle_frames=int(round((2*math.pi/m)/step))
    frames=cycle_frames
    # There are `frames` main operator applications plus one terminal readback.
    # With wave support inside L1<=5, no disturbance may reach the fixed-domain edge.
    margin=DOMAIN_L1-5
    operator_applications=frames+1
    if not (operator_applications < margin):
        raise RuntimeError(f"boundary guard failed: operator_applications={operator_applications}, margin={margin}")
    phi=initial_phi(); prev_flow={}; old_wave={}; old_phase=0.0
    inputs=[]; outputs=[]; rows=[]
    case_dir=OUT/spec["name"]; case_dir.mkdir(parents=True,exist_ok=True)
    for frame in range(frames):
        theta=frame*step
        new_wave=wave_component(m,theta)
        w_signed,w_abs=apply_delta(phi,delta_component(old_wave,new_wave)); old_wave=new_wave
        if spec["phase_on"]:
            phase=PHASE_AMP*math.sin(2*math.pi*frame/frames)
        else:
            phase=0.0
        p_signed,p_abs=apply_uniform(phi,phase-old_phase); old_phase=phase
        pin=state_vector(phi); total_before=float(sum(phi.values()))
        phi,next_flow,diag=operator_step(phi,prev_flow,dimension=DIM)
        pout=state_vector(phi)
        aa=np.asarray(diag.alpha_samples); bb=np.asarray(diag.beta_samples); jj=np.asarray(list(next_flow.values()))
        rows.append({
            "frame":frame,"theta":theta,"phase":phase,
            "wave_external_signed":w_signed,"wave_external_abs":w_abs,
            "phase_external_signed":p_signed,"phase_external_abs":p_abs,
            "live_transfer":float(diag.live_transfer),"births":int(diag.births),
            "alpha_mean":float(aa.mean()) if aa.size else 0.0,
            "alpha_std":float(aa.std()) if aa.size else 0.0,
            "beta_mean":float(bb.mean()) if bb.size else 0.0,
            "beta_std":float(bb.std()) if bb.size else 0.0,
            "j_mean":float(jj.mean()) if jj.size else 0.0,
            "j_std":float(jj.std()) if jj.size else 0.0,
            "total_before":total_before,"total_after":float(sum(phi.values())),
            "conservation_error":float(sum(phi.values())-total_before),
        })
        inputs.append(pin); outputs.append(pout); prev_flow=next_flow
    theta=frames*step
    new_wave=wave_component(m,theta)
    apply_delta(phi,delta_component(old_wave,new_wave)); old_wave=new_wave
    phase=0.0
    apply_uniform(phi,phase-old_phase)
    terminal_input=state_vector(phi)
    terminal_before=float(sum(phi.values()))
    phi,terminal_flow,terminal_diag=operator_step(phi,prev_flow,dimension=DIM)
    terminal_output=state_vector(phi)
    state_hist=np.stack([inputs[0],*outputs,terminal_output],axis=0)
    np.savez_compressed(case_dir/"full_fixed_domain_history.npz",
        coords=np.asarray(DOMAIN,dtype=np.int16),
        phi_input=np.stack(inputs),phi_output=np.stack(outputs),
        terminal_input=terminal_input,terminal_output=terminal_output,
        state_history=state_hist)
    closure=float(np.sqrt(np.mean((terminal_input-inputs[0])**2)))
    result={
        "case":spec,"cycle_frames":frames,"operator_applications":operator_applications,
        "fixed_domain_points":len(DOMAIN),"domain_l1_radius":DOMAIN_L1,
        "wave_support_l1_max":5,"causal_margin":margin,
        "boundary_unreachable":operator_applications < margin,
        "births_total":int(sum(r["births"] for r in rows)+terminal_diag.births),
        "max_abs_conservation_error":max([abs(r["conservation_error"]) for r in rows]+[abs(sum(phi.values())-terminal_before)]),
        "cycle_closure_rmse_pre_operator":closure,
        "derivative_reconstruction_phi":deriv_reconstruct(state_hist),
        "rows":rows,
    }
    (case_dir/"journal.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    return result

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    results={s["name"]:run_case(s) for s in CASES}
    summary={
        "experiment":"phase_memory_wave_modes",
        "status":"synthetic phase-memory test; no physical emergence claim",
        "definitions":{
            "wave":"closed non-rigid m-peak potential wave on x-y ring, embedded in R4",
            "m3":"three maxima; 10 degree orientation phase step; field repeats after 12 frames",
            "m4":"four maxima; 15 degree orientation phase step; field repeats after 6 frames",
            "phase_field":"uniform small-amplitude sinusoidal potential offset, imposed externally",
            "fixed_domain":"all R4 lattice points with L1 norm <= 19 exist from frame zero; no intended birth and no boundary rule",
            "derivative_test":"affine reconstruction of next local phi from phi and discrete temporal differences through order 3; analysis only",
        },
        "parameters":{
            "background":BACKGROUND,"phase_amplitude":PHASE_AMP,"wave_peak_amplitude":WAVE_AMP,
            "ring_radius":RING_R,"sigma":SIGMA,"domain_l1_radius":DOMAIN_L1,
        },
        "cases":{k:{
            "cycle_frames":v["cycle_frames"],"births_total":v["births_total"],
            "boundary_unreachable":v["boundary_unreachable"],
            "cycle_closure_rmse_pre_operator":v["cycle_closure_rmse_pre_operator"],
            "derivative_reconstruction_phi":v["derivative_reconstruction_phi"],
        } for k,v in results.items()},
    }
    (OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
