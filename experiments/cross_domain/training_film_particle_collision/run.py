from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step, directions

OUT = ROOT / 'run-data' / 'cross_domain' / 'training_film_particle_collision'
DIM=3; BACKGROUND=100.0; OBJ_TOTAL=120.0; SIGMA=0.58; RING_R=1.7
DOMAIN_L1=30; TRAIN_FRAMES=10; FREE_FRAMES=30; TOTAL_FRAMES=TRAIN_FRAMES+FREE_FRAMES
START_X=7.0; TRAIN_STEP=0.45; ROT_STEP_DEG=30.0; MEASURE_L1=14
CASES=[
    {'name':'same_rotation_pp','rot_a':+1.0,'rot_b':+1.0},
    {'name':'opposite_rotation_pm','rot_a':+1.0,'rot_b':-1.0},
]

DS=directions(DIM)

def fixed_domain():
    r=range(-DOMAIN_L1,DOMAIN_L1+1)
    return [tuple(int(v) for v in c) for c in product(r,repeat=DIM)
            if sum(abs(v) for v in c)<=DOMAIN_L1]
DOMAIN=fixed_domain(); DOMAIN_SET=set(DOMAIN); INDEX={c:i for i,c in enumerate(DOMAIN)}


def component(center_x: float, theta: float):
    comp={}
    cx=float(center_x)
    for c in product(range(-12,13), repeat=3):
        x,y,z=(float(v) for v in c)
        dx=x-cx; rho=math.hypot(dx,y)
        d2=(rho-RING_R)**2 + z*z
        env=math.exp(-0.5*d2/(SIGMA*SIGMA))
        ang=math.atan2(y,dx)
        val=env*(1.0+0.35*math.cos(3*(ang-theta)))
        if val>1e-12:
            comp[tuple(int(v) for v in c)]=val
    s=sum(comp.values()); k=OBJ_TOTAL/(s+1e-30)
    return {c:v*k for c,v in comp.items() if c in DOMAIN_SET}


def apply_film_frame(phi, old_a, old_b, new_a, new_b):
    # The teacher film supplies only the complete scalar field image.
    # No velocity, force, collision, annihilation or drift rule is added.
    coords=set(old_a)|set(old_b)|set(new_a)|set(new_b)
    for c in coords:
        phi[c] += (new_a.get(c,0.0)+new_b.get(c,0.0))-(old_a.get(c,0.0)+old_b.get(c,0.0))


def dense(phi):
    return np.asarray([phi[c] for c in DOMAIN], dtype=np.float64)


def positive_metrics(phi):
    pts=[]; weights=[]
    total_pos=0.0
    for c in DOMAIN:
        e=phi[c]-BACKGROUND
        if e>0:
            pts.append(c); weights.append(e); total_pos+=e
    if not weights:
        return {'positive_excess':0.0,'centroid_x':0.0,'x_variance':0.0,'central_positive':0.0,'outer_positive':0.0}
    w=np.asarray(weights,float); p=np.asarray(pts,float)
    cx=float(np.sum(p[:,0]*w)/np.sum(w))
    vx=float(np.sum(((p[:,0]-cx)**2)*w)/np.sum(w))
    central=0.0; outer=0.0
    for c,e in zip(pts,weights):
        r=math.sqrt(sum(float(v*v) for v in c))
        if r<=3.0: central+=e
        if r>=6.0: outer+=e
    return {'positive_excess':float(total_pos),'centroid_x':cx,'x_variance':vx,
            'central_positive':float(central),'outer_positive':float(outer)}


def half_centroids(phi):
    out={}
    for label,sgn in [('left',-1),('right',+1)]:
        sw=sx=0.0
        for c in DOMAIN:
            if (sgn<0 and c[0]>=0) or (sgn>0 and c[0]<=0): continue
            e=max(phi[c]-BACKGROUND,0.0)
            sw+=e; sx+=e*c[0]
        out[label+'_weight']=float(sw)
        out[label+'_centroid_x']=float(sx/(sw+1e-30))
    out['separation']=float(out['right_centroid_x']-out['left_centroid_x'])
    return out


def negative_deficit(phi):
    return float(sum(max(BACKGROUND-phi[c],0.0) for c in DOMAIN))


def core_count_proxy(phi):
    # Post-hoc diagnostic only: count separated positive-excess peaks along x after y,z integration.
    xs=range(-MEASURE_L1,MEASURE_L1+1)
    prof=[]
    for x in xs:
        prof.append(sum(max(phi[c]-BACKGROUND,0.0) for c in DOMAIN if c[0]==x and abs(c[1])+abs(c[2])<=5))
    a=np.asarray(prof,float)
    peaks=[]
    for i in range(1,len(a)-1):
        if a[i]>a[i-1] and a[i]>=a[i+1] and a[i]>0:
            peaks.append((xs[i],float(a[i])))
    peaks.sort(key=lambda q:q[1], reverse=True)
    return {'peak_count_raw':len(peaks),'top_peaks':peaks[:4],'x_profile':prof}


def run_case(case):
    cdir=OUT/case['name']; cdir.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old_a={}; old_b={}; rows=[]; frames=[]
    for frame in range(TOTAL_FRAMES):
        teaching=frame<TRAIN_FRAMES
        if teaching:
            xa=-START_X + TRAIN_STEP*frame
            xb=+START_X - TRAIN_STEP*frame
            ta=math.radians(case['rot_a']*ROT_STEP_DEG*frame)
            tb=math.radians(case['rot_b']*ROT_STEP_DEG*frame)
            new_a=component(xa,ta); new_b=component(xb,tb)
            apply_film_frame(phi,old_a,old_b,new_a,new_b)
            old_a,old_b=new_a,new_b
            imposed={'xa':xa,'xb':xb,'theta_a_deg':case['rot_a']*ROT_STEP_DEG*frame,
                     'theta_b_deg':case['rot_b']*ROT_STEP_DEG*frame}
        else:
            imposed=None
        before=sum(phi.values())
        phi,nxt,diag=operator_step(phi,prev,dimension=DIM)
        frames.append(dense(phi))
        pm=positive_metrics(phi); hm=half_centroids(phi); cc=core_count_proxy(phi)
        rows.append({'frame':frame,'phase':'teacher_film' if teaching else 'free_release',
                     'teacher_frame':imposed,'positive':pm,'halves':hm,'negative_deficit':negative_deficit(phi),
                     'core_proxy':cc,'births':diag.births,'live_transfer':float(diag.live_transfer),
                     'conservation_error':float(sum(phi.values())-before)})
        prev=nxt
    np.savez_compressed(cdir/'phi_movie.npz',coords=np.asarray(DOMAIN,dtype=np.int16),phi=np.stack(frames))
    return rows


def analyze(rows):
    free=rows[TRAIN_FRAMES:]
    sep=np.asarray([r['halves']['separation'] for r in free],float)
    central=np.asarray([r['positive']['central_positive'] for r in free],float)
    outer=np.asarray([r['positive']['outer_positive'] for r in free],float)
    deficit=np.asarray([r['negative_deficit'] for r in free],float)
    total=np.asarray([r['positive']['positive_excess'] for r in free],float)
    imin=int(np.argmin(sep)); rmin=free[imin]
    # Collision is descriptive: the two half-centroids reach their minimum separation during free release.
    return {
        'release_separation_start':float(sep[0]),
        'minimum_separation':float(sep[imin]),'minimum_separation_free_frame':int(imin),
        'release_separation_end':float(sep[-1]),
        'approach_after_release':bool(np.min(sep)<sep[0]-1e-9),
        'recede_after_minimum':bool(sep[-1]>sep[imin]+1e-9),
        'central_positive_at_minimum':float(central[imin]),
        'outer_positive_at_minimum':float(outer[imin]),
        'positive_excess_start':float(total[0]),'positive_excess_end':float(total[-1]),
        'negative_deficit_start':float(deficit[0]),'negative_deficit_max':float(np.max(deficit)),
        'core_proxy_at_minimum':rmin['core_proxy'],
        'core_proxy_final':free[-1]['core_proxy'],
        'collision_like_contact':bool(sep[imin] <= 2.0*RING_R),
    }


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    results={}; stats={}
    for case in CASES:
        rows=run_case(case); results[case['name']]=rows; stats[case['name']]=analyze(rows)
    summary={
        'experiment':'training_film_particle_collision',
        'status':'synthetic 3D teacher-film then free-release test; unchanged operator',
        'operator':'scanner.self_reflexive_operator.operator_step unchanged',
        'teacher_protocol':'ten complete scalar-field frames containing two approaching m=3 particle patterns; displacement and phase are present only in those images; after frame 9 no field image, velocity, force, collision or annihilation rule is imposed',
        'cases':CASES,
        'parameters':{'dimension':DIM,'background':BACKGROUND,'object_total_each':OBJ_TOTAL,'ring_radius':RING_R,
                      'sigma':SIGMA,'train_frames':TRAIN_FRAMES,'free_frames':FREE_FRAMES,'start_abs_x':START_X,
                      'teacher_displacement_per_frame':TRAIN_STEP,'rotation_step_deg':ROT_STEP_DEG,
                      'domain_l1':DOMAIN_L1,'domain_points':len(DOMAIN)},
        'analysis':stats,
        'raw_rows':results,
        'interpretation_guard':'collision/contact/peak counts are post-hoc diagnostics only; no such rule is visible to dynamics'
    }
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
