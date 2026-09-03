from __future__ import annotations

import math
import numpy as np

from scanner.self_reflexive_operator import operator_step, directions, opposite_indices, add

R = 4
COORDS = [(a,b,c,d) for a in range(-R,R+1) for b in range(-R,R+1) for c in range(-R,R+1) for d in range(-R,R+1)]
DS = directions(4)
OPP = opposite_indices(4)
INTERIOR = [x for x in COORDS if max(map(abs,x)) <= 2]
INTERIOR_SET = set(INTERIOR)


def make_constant(base=1.0):
    return {x: base for x in COORDS}


def make_affine(axis=0, eps=0.02, base=1.0):
    return {x: base + eps*x[axis] for x in COORDS}


def make_bump(amp=0.35, sigma=1.5, base=1.0):
    out = {}
    for x in COORDS:
        r2 = sum(v*v for v in x)
        out[x] = base + amp*math.exp(-r2/(2*sigma*sigma))
    return out


def run(phi0, steps=4):
    phi = dict(phi0)
    flow = {}
    hist = []
    for _ in range(steps):
        phi, flow, diag = operator_step(phi, flow, dimension=4)
        hist.append((phi, flow, diag))
    return hist


def node_orientation(flow, x):
    vals = np.array([max(flow.get((x,a),0.0),0.0) for a in range(8)], float)
    s = vals.sum()
    if s <= 1e-15:
        return np.zeros(4), 0.0
    p = vals/s
    vec = np.zeros(4)
    for a,dv in enumerate(DS):
        vec += p[a]*np.array(dv,float)
    return vec, s


def descriptors(phi, flow):
    gp=[]; p2=[]; orient={}; activity={}
    for x in INTERIOR:
        vec, act = node_orientation(flow,x)
        orient[x]=vec; activity[x]=act
        px=phi[x]
        for dv in DS:
            y=add(x,dv)
            gp.append(abs(px-phi[y])/(abs(px)+abs(phi[y])+1e-15))
        for a in (0,2,4,6):
            y1=add(x,DS[a]); y2=add(x,DS[OPP[a]])
            p2.append(abs(phi[y1]-2*px+phi[y2])/(abs(phi[y1])+2*abs(px)+abs(phi[y2])+1e-15))
    m1=[np.linalg.norm(orient[x]) for x in INTERIOR]
    rough=[]; actrough=[]
    for x in INTERIOR:
        for dv in DS:
            y=add(x,dv)
            if y in INTERIOR_SET:
                rough.append(np.linalg.norm(orient[x]-orient[y]))
                denom=activity[x]+activity[y]+1e-15
                actrough.append(abs(activity[x]-activity[y])/denom)
    meanmag=float(np.mean(m1))
    vecmean=np.mean(np.stack([orient[x] for x in INTERIOR]),axis=0)
    globalcoh=float(np.linalg.norm(vecmean)/(meanmag+1e-15)) if meanmag>0 else 0.0
    return {
        'P_grad1': float(np.mean(gp)),
        'P_second': float(np.mean(p2)),
        'J_orient_mag': meanmag,
        'J_global_coherence': globalcoh,
        'J_orient_rough': float(np.mean(rough)),
        'J_activity_rough': float(np.mean(actrough)),
        'mean_activity': float(np.mean([activity[x] for x in INTERIOR])),
    }


def swap_x_w(c):
    return (c[3], c[1], c[2], c[0])

DIR_MAP={0:6,1:7,2:2,3:3,4:4,5:5,6:0,7:1}


def compare_mapped(a_hist,b_hist):
    rows=[]
    for step,((pa,fa,_),(pb,fb,_)) in enumerate(zip(a_hist,b_hist),1):
        dp=max(abs(pa[x]-pb[swap_x_w(x)]) for x in pa)
        df=0.0
        for (x,a),v in fa.items():
            df=max(df,abs(v-fb.get((swap_x_w(x),DIR_MAP[a]),0.0)))
        rows.append((step,dp,df))
    return rows


def main():
    cases={
        'E': run(make_constant()),
        'N': run(make_affine(0)),
        'M': run(make_affine(3)),
        'G': run(make_bump()),
    }
    for name,hist in cases.items():
        print('\n',name)
        for step,(phi,flow,diag) in enumerate(hist,1):
            print(step,descriptors(phi,flow),'births=',diag.births,'dQ=',diag.total_after-diag.total_before)
    print('\nN<->M coordinate-permutation control')
    for row in compare_mapped(cases['N'],cases['M']):
        print('step=%d max_dP=%.17g max_dJ=%.17g' % row)


if __name__ == '__main__':
    main()
