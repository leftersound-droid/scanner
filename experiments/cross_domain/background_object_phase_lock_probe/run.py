from __future__ import annotations

import json, math
from pathlib import Path
import numpy as np

# Structural synchronization probe for the unchanged live-neighbour
# self-reflexive transfer algebra.  The periodic 4D torus and the imposed
# longitudinal background pulse are control/teacher representations only.
# No synchronization, inertia, torque, damping, stabilizer, or physical law
# is added to the operator.

DIRS=[(0,-1),(0,1),(1,-1),(1,1),(2,-1),(2,1),(3,-1),(3,1)]
N=9
BACKGROUND=100.0
TOBJ=48
FLOW_AMP=0.015
OUT=Path(__file__).resolve().parent/'result.json'

coords=np.arange(N)-N//2
X,Y,Z,W=np.meshgrid(coords,coords,coords,coords,indexing='ij')
RHO=np.sqrt(X*X+Y*Y)
ANG=np.arctan2(Y,X)
SHAPE=(N,)*4


def step(P,prev):
    neigh=np.stack([np.roll(P,-s,axis=a) for a,s in DIRS],axis=-1)
    delta=np.maximum(P[...,None]-neigh,0.0)
    live=delta>0.0
    sd=delta.sum(axis=-1)
    nl=live.sum(axis=-1)
    capacity=np.divide(sd,nl,out=np.zeros_like(sd),where=nl>0)
    alpha=np.divide(delta,sd[...,None],out=np.zeros_like(delta),where=sd[...,None]>0)
    if prev is None:
        beta=np.zeros_like(delta)
    else:
        pl=np.where(live,np.maximum(prev,0.0),0.0)
        ps=pl.sum(axis=-1)
        beta=np.divide(pl,ps[...,None],out=np.zeros_like(pl),where=ps[...,None]>0)
    J=capacity[...,None]*alpha/(1.0+beta)
    out=J.sum(axis=-1)
    scale=np.ones_like(out)
    m=(out>P)&(out>0.0)
    scale[m]=P[m]/out[m]
    J*=scale[...,None]
    dP=-J.sum(axis=-1)
    for i,(a,s) in enumerate(DIRS):
        dP+=np.roll(J[...,i],s,axis=a)
    return P+dP,J


def object_component(theta):
    env=np.exp(-0.5*((RHO-1.7)**2+Z*Z+W*W)/(0.65**2))
    # m=1 plus weak m=2 marker gives a unique 2pi representation-phase.
    return 6.0*env*(1.0+0.25*np.cos(ANG-theta)+0.08*np.cos(2.0*(ANG-theta)))


def add_background(prev,frame,Tb,phase0,amp):
    merged=np.zeros(SHAPE+(8,),float) if prev is None else prev.copy()
    s=math.sin(2.0*math.pi*frame/Tb+phase0)
    if abs(s)>1e-15 and amp>0.0:
        merged[...,7 if s>0.0 else 6]+=amp*abs(s)
    return merged


def readout(P,J):
    ex=np.maximum(P-BACKGROUND,0.0)
    wt=float(ex.sum())
    q=np.sum(ex*np.exp(1j*ANG))
    return {
        'phase':float(np.angle(q)),
        'marker_amplitude':float(abs(q)/(wt+1e-30)),
        'shape_concentration':float(np.sum(ex*ex)/(wt*wt+1e-30)),
        'mean_J_activity':float(J.sum(axis=-1).mean()),
    }


def run_case(Tb,phase0=0.0,amp=FLOW_AMP):
    P=np.full(SHAPE,BACKGROUND)
    prev=None
    old=np.zeros(SHAPE)
    rows=[]
    # Exactly one full teacher period with TOBJ unique phase samples.
    for frame in range(TOBJ):
        theta=2.0*math.pi*frame/TOBJ
        new=object_component(theta)
        P+=new-old
        old=new
        P,prev=step(P,add_background(prev,frame,Tb,phase0,amp))
        rows.append({'stage':'train','frame':frame,'teacher_theta':theta,**readout(P,prev)})
    # Teacher off.  Background pulse continues unchanged.
    for k in range(TOBJ):
        frame=TOBJ+k
        P,prev=step(P,add_background(prev,frame,Tb,phase0,amp))
        rows.append({'stage':'free','frame':frame,'teacher_theta':None,**readout(P,prev)})

    ph=np.unwrap(np.asarray([r['phase'] for r in rows]))
    free=rows[TOBJ:]
    free_ph=ph[TOBJ:]
    progress=float((free_ph[-1]-free_ph[0])/(2.0*math.pi))
    bg=2.0*math.pi*np.arange(TOBJ,2*TOBJ)/Tb+phase0
    rel=np.unwrap(np.asarray([r['phase'] for r in free])-bg)
    return {
        'Tb':float(Tb),'Tobj_over_Tb':float(TOBJ/Tb),'phase0':float(phase0),'flow_amp':float(amp),
        'free_orientation_progress_cycles':progress,
        'relative_phase_drift_cycles_1to1':float((rel[-1]-rel[0])/(2.0*math.pi)),
        'marker_retention':float(free[-1]['marker_amplitude']/(free[0]['marker_amplitude']+1e-30)),
        'shape_concentration_retention':float(free[-1]['shape_concentration']/(free[0]['shape_concentration']+1e-30)),
        'J_activity_retention':float(free[-1]['mean_J_activity']/(free[0]['mean_J_activity']+1e-30)),
    }


def main():
    period_sweep=[8,12,16,24,32,40,42,44,46,47,47.5,48,48.5,49,50,52,54,56,64,72,96,128]
    phase_sweep=[2.0*math.pi*k/8.0 for k in range(8)]
    amp_sweep=[0.0,0.005,0.015,0.05,0.15,0.5]
    result={
        'status':'structural control; no physical emergence claim',
        'operator':'same alpha/beta/capacity live-neighbour algebra as scanner; vectorized periodic representation',
        'teacher':{'object_period_frames':TOBJ,'unique_phase_samples_per_period':TOBJ,'teacher_periods':1},
        'background':'sinusoidal previous-flow along +/- fourth direction; continues after object teacher release',
        'period_sweep':[run_case(Tb) for Tb in period_sweep],
        'phase_sweep_at_1to1':[run_case(TOBJ,p) for p in phase_sweep],
        'amplitude_control_near_1to1':[run_case(Tb,0.0,a) for a in amp_sweep for Tb in (46,48,50)],
    }
    OUT.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
