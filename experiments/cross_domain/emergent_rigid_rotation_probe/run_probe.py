from __future__ import annotations

# Necessary-condition probe for the hypothesis that a stable object must carry
# internal P/J dynamics plus autonomous rigid-body-like periodic motion.
#
# IMPORTANT: this does NOT define a physical metric or physical angle.  The
# toroidal lattice is only a boundary-free representation used for the short
# causal pilot.  Readout is split into:
#   (1) graph/direction-pair invariants (primary), and
#   (2) an m=3 grid-orientation diagnostic (representation diagnostic only).
# No stabilizer, damping, force law, torque law, inertia law, or continued
# teacher is added after the initial P/J state.

import math
import numpy as np

DIRS=[(0,-1),(0,1),(1,-1),(1,1),(2,-1),(2,1),(3,-1),(3,1)]


def step(P, prev=None):
    neigh=np.stack([np.roll(P,-s,axis=a) for a,s in DIRS],axis=-1)
    delta=np.maximum(P[...,None]-neigh,0.0)
    live=delta>0.0
    sd=delta.sum(-1); nl=live.sum(-1)
    C=np.divide(sd,nl,out=np.zeros_like(sd),where=nl>0)
    alpha=np.divide(delta,sd[...,None],out=np.zeros_like(delta),where=sd[...,None]>0)
    if prev is None:
        beta=np.zeros_like(delta)
    else:
        pl=np.where(live,np.maximum(prev,0.0),0.0)
        ps=pl.sum(-1)
        beta=np.divide(pl,ps[...,None],out=np.zeros_like(pl),where=ps[...,None]>0)
    J=C[...,None]*alpha/(1.0+beta)
    out=J.sum(-1)
    scale=np.ones_like(out)
    m=(out>P)&(out>0)
    scale[m]=P[m]/out[m]
    J*=scale[...,None]
    dP=-J.sum(-1)
    for di,(a,s) in enumerate(DIRS):
        dP += np.roll(J[...,di],s,axis=a)
    return P+dP,J


def initial_state(n=21, rotation_amp=0.10, phase_amp=0.22):
    q=np.arange(n)-n//2
    X=np.meshgrid(q,q,q,q,indexing='ij')
    x,y,z,w=[a.astype(float) for a in X]
    rxy=np.sqrt(x*x+y*y)
    env=np.exp(-0.5*((rxy-3.5)**2/0.9**2 + z*z/1.3**2 + w*w/1.6**2))
    theta=np.arctan2(y,x)

    # Compact object with an internal m=3 phase marker.  This marker is used
    # only to make orientation loss visible; its grid phase is NOT classified
    # as an emergent physical angle.
    P=1.0+0.8*env*(1.0+phase_amp*np.cos(3.0*theta))

    # Initial P/J phase state: tangential circulation in the x-y graph plane
    # plus a longitudinal +/- fourth-direction component.  This is an initial
    # state only; it is never re-imposed after frame 0.
    prev=np.zeros(P.shape+(8,),dtype=float)
    vx=-y; vy=x
    choose_x=np.abs(vx)>=np.abs(vy)
    A=rotation_amp*env
    prev[...,0]=np.where(choose_x & (vx<0),A,0.0)
    prev[...,1]=np.where(choose_x & (vx>0),A,0.0)
    prev[...,2]=np.where((~choose_x) & (vy<0),A,0.0)
    prev[...,3]=np.where((~choose_x) & (vy>0),A,0.0)
    L=0.025*env*np.abs(np.sin(theta))
    prev[...,6]+=np.where(np.sin(theta)<0,L,0.0)
    prev[...,7]+=np.where(np.sin(theta)>0,L,0.0)
    return P,prev,(x,y,z,w)


def circulation_rms(J):
    # Axis-permutation-invariant aggregate over all local antipodal direction
    # pairs and all elementary graph plaquettes.  Unit edge differences here
    # are topological differences, not physical distances.
    F=np.stack([J[...,1]-J[...,0],J[...,3]-J[...,2],J[...,5]-J[...,4],J[...,7]-J[...,6]],axis=-1)
    vals=[]
    for a in range(4):
        for b in range(a+1,4):
            dFb=np.roll(F[...,b],-1,axis=a)-F[...,b]
            dFa=np.roll(F[...,a],-1,axis=b)-F[...,a]
            vals.append(np.mean((dFb-dFa)**2))
    return float(np.sqrt(np.mean(vals)))


def graph_readout(P,J):
    u=np.maximum(P-1.0,0.0)
    mass=float(u.sum())+1e-30
    norm2=float(np.sum(u*u))+1e-30
    dirichlet=0.0
    for a in range(4):
        dirichlet += float(np.sum((u-np.roll(u,-1,axis=a))**2))
    dirichlet/=norm2
    participation=(mass*mass/norm2)/P.size
    totalJ=float(J.sum())
    pair=np.array([J[...,0:2].sum(),J[...,2:4].sum(),J[...,4:6].sum(),J[...,6:8].sum()],float)
    pair_sorted=np.sort(pair/(pair.sum()+1e-30))
    return {
        'dirichlet':dirichlet,
        'participation_fraction':participation,
        'J_per_excess':totalJ/mass,
        'circulation_rms':circulation_rms(J),
        'pair_sorted':pair_sorted.tolist(),
    }


def orientation_diagnostic(P,X):
    x,y,_,_=X
    u=np.maximum(P-1.0,0.0); s=float(u.sum())+1e-30
    th=np.arctan2(y,x)
    q=(u*np.exp(1j*3.0*th)).sum()/s
    return float(abs(q)),float((np.angle(q)/3.0)%(2.0*math.pi/3.0))


def run(rotation_amp,steps=50):
    P,prev,X=initial_state(rotation_amp=rotation_amp)
    initial_circ=circulation_rms(prev)
    rows=[]
    for frame in range(steps):
        P,J=step(P,prev)
        amp,phase=orientation_diagnostic(P,X)
        rows.append({'frame':frame,'shape_m3_amp_diag':amp,'shape_m3_phase_diag':phase,**graph_readout(P,J)})
        prev=J
    return initial_circ,rows


def main():
    for a in (0.0,0.01,0.04,0.10,0.25):
        initial_circ,rows=run(a)
        phase=np.unwrap(3*np.asarray([r['shape_m3_phase_diag'] for r in rows]))/3.0
        print({
            'rotation_amp':a,
            'initial_circulation':initial_circ,
            'first_output_circulation':rows[0]['circulation_rms'],
            'final_circulation':rows[-1]['circulation_rms'],
            'net_grid_phase_deg_DIAGNOSTIC_ONLY':float(np.degrees(phase[-1]-phase[0])),
            'grid_phase_range_deg_DIAGNOSTIC_ONLY':float(np.degrees(phase.max()-phase.min())),
            'shape_marker_retention':rows[-1]['shape_m3_amp_diag']/rows[0]['shape_m3_amp_diag'],
        })


if __name__=='__main__':
    main()
