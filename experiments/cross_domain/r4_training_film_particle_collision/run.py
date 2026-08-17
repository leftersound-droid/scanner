from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step, directions

OUT = ROOT / 'run-data' / 'cross_domain' / 'r4_training_film_particle_collision'
DIM=4; BACKGROUND=100.0; OBJ_TOTAL=150.0; SIGMA=0.62; RING_R=2.0
DOMAIN_L1=26; TRAIN_FRAMES=12; FREE_FRAMES=24; TOTAL_FRAMES=TRAIN_FRAMES+FREE_FRAMES
START_X=7.5; TRAIN_STEP=0.45; ROT_STEP_DEG=30.0; FLOW_PERIOD=12; FLOW_AMP=0.01
MEASURE_L1=12
CASES=[
    {'name':'same_rotation_pp','rot_a':+1.0,'rot_b':+1.0},
    {'name':'opposite_rotation_pm','rot_a':+1.0,'rot_b':-1.0},
]
DS=directions(DIM)


def fixed_domain():
    r=range(-DOMAIN_L1,DOMAIN_L1+1)
    return [tuple(int(v) for v in c) for c in product(r,repeat=4)
            if sum(abs(v) for v in c)<=DOMAIN_L1]
DOMAIN=fixed_domain(); DOMAIN_SET=set(DOMAIN)


def component(center_x: float, theta: float):
    comp={}; cx=float(center_x)
    for c in product(range(-12,13),repeat=4):
        x,y,z,w=(float(v) for v in c)
        dx=x-cx; rho=math.hypot(dx,y)
        d2=(rho-RING_R)**2+z*z+w*w
        env=math.exp(-0.5*d2/(SIGMA*SIGMA))
        ang=math.atan2(y,dx)
        val=env*(1.0+0.35*math.cos(3*(ang-theta)))
        if val>1e-12:
            ci=tuple(int(v) for v in c)
            if ci in DOMAIN_SET: comp[ci]=val
    s=sum(comp.values()); k=OBJ_TOTAL/(s+1e-30)
    return {c:v*k for c,v in comp.items()}


def apply_film_frame(phi, old_a, old_b, new_a, new_b):
    coords=set(old_a)|set(old_b)|set(new_a)|set(new_b)
    for c in coords:
        phi[c] += (new_a.get(c,0.0)+new_b.get(c,0.0))-(old_a.get(c,0.0)+old_b.get(c,0.0))


def impose_r4_pulse(prev, frame, on):
    merged=dict(prev)
    if not on: return merged,0.0,0
    s=math.sin(2.0*math.pi*frame/FLOW_PERIOD)
    amp=FLOW_AMP*abs(s)
    if amp<1e-15: return merged,0.0,0
    di=7 if s>0 else 6
    step=1 if di==7 else -1
    count=0
    for c in DOMAIN:
        target=(c[0],c[1],c[2],c[3]+step)
        if target in DOMAIN_SET:
            merged[(c,di)]=merged.get((c,di),0.0)+amp
            count+=1
    return merged,amp,count


def positive_metrics(phi):
    pts=[]; weights=[]; total=0.0; central=0.0; outer=0.0
    for c in DOMAIN:
        e=phi[c]-BACKGROUND
        if e<=0: continue
        pts.append(c); weights.append(e); total+=e
        r=math.sqrt(sum(float(v*v) for v in c))
        if r<=3.0: central+=e
        if r>=7.0: outer+=e
    if not weights:
        return {'positive_excess':0.0,'centroid_x':0.0,'central_positive':0.0,'outer_positive':0.0}
    w=np.asarray(weights,float); p=np.asarray(pts,float)
    cx=float(np.sum(p[:,0]*w)/np.sum(w))
    return {'positive_excess':float(total),'centroid_x':cx,'central_positive':float(central),'outer_positive':float(outer)}


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


def m3_half(phi, sign):
    q=0j; weight=0.0
    for c in DOMAIN:
        if (sign<0 and c[0]>=0) or (sign>0 and c[0]<=0): continue
        x,y,z,w=c
        e=phi[c]-BACKGROUND
        if e<=0: continue
        cx=-4.0 if sign<0 else 4.0
        ang=math.atan2(y,x-cx)
        q += e*complex(math.cos(3*ang),math.sin(3*ang)); weight+=e
    amp=abs(q)/(weight+1e-30)
    phase=math.degrees(math.atan2(q.imag,q.real)/3.0) if abs(q)>0 else 0.0
    return {'amplitude':float(amp),'phase_deg':float(phase)}


def negative_deficit(phi):
    return float(sum(max(BACKGROUND-phi[c],0.0) for c in DOMAIN))


def run_case(case):
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old_a={}; old_b={}; rows=[]
    for frame in range(TOTAL_FRAMES):
        teaching=frame<TRAIN_FRAMES
        if teaching:
            xa=-START_X+TRAIN_STEP*frame; xb=+START_X-TRAIN_STEP*frame
            ta=math.radians(case['rot_a']*ROT_STEP_DEG*frame)
            tb=math.radians(case['rot_b']*ROT_STEP_DEG*frame)
            new_a=component(xa,ta); new_b=component(xb,tb)
            apply_film_frame(phi,old_a,old_b,new_a,new_b)
            old_a,old_b=new_a,new_b
            teacher={'xa':xa,'xb':xb,'theta_a_deg':case['rot_a']*ROT_STEP_DEG*frame,
                     'theta_b_deg':case['rot_b']*ROT_STEP_DEG*frame}
        else:
            teacher=None
        op_prev,pulse_amp,pulse_edges=impose_r4_pulse(prev,frame,teaching)
        before=sum(phi.values())
        phi,nxt,diag=operator_step(phi,op_prev,dimension=DIM)
        rows.append({'frame':frame,'phase':'teacher_film' if teaching else 'free_release',
                     'teacher_frame':teacher,'r4_pulse_on':bool(teaching),
                     'r4_pulse_amplitude':float(pulse_amp),'r4_pulse_edges':int(pulse_edges),
                     'positive':positive_metrics(phi),'halves':half_centroids(phi),
                     'm3_left':m3_half(phi,-1),'m3_right':m3_half(phi,+1),
                     'negative_deficit':negative_deficit(phi),'births':diag.births,
                     'live_transfer':float(diag.live_transfer),
                     'conservation_error':float(sum(phi.values())-before)})
        prev=nxt
    return rows


def analyze(rows):
    free=rows[TRAIN_FRAMES:]
    sep=np.asarray([r['halves']['separation'] for r in free],float)
    central=np.asarray([r['positive']['central_positive'] for r in free],float)
    outer=np.asarray([r['positive']['outer_positive'] for r in free],float)
    total=np.asarray([r['positive']['positive_excess'] for r in free],float)
    deficit=np.asarray([r['negative_deficit'] for r in free],float)
    imin=int(np.argmin(sep))
    return {
        'release_separation_start':float(sep[0]),
        'minimum_separation':float(sep[imin]),
        'minimum_separation_free_frame':int(imin),
        'release_separation_end':float(sep[-1]),
        'approach_after_release':bool(np.min(sep)<sep[0]-1e-9),
        'recede_after_minimum':bool(sep[-1]>sep[imin]+1e-9),
        'collision_like_contact':bool(sep[imin]<=2.0*RING_R),
        'central_positive_at_minimum':float(central[imin]),
        'outer_positive_at_minimum':float(outer[imin]),
        'positive_excess_start':float(total[0]),
        'positive_excess_end':float(total[-1]),
        'negative_deficit_start':float(deficit[0]),
        'negative_deficit_max':float(np.max(deficit)),
        'm3_left_start':free[0]['m3_left'],'m3_left_end':free[-1]['m3_left'],
        'm3_right_start':free[0]['m3_right'],'m3_right_end':free[-1]['m3_right'],
    }


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    results={}; stats={}
    for case in CASES:
        rows=run_case(case); results[case['name']]=rows; stats[case['name']]=analyze(rows)
    summary={
        'experiment':'r4_training_film_particle_collision',
        'status':'synthetic R4 teacher-film + J4 pulse then total free release; unchanged operator',
        'operator':'scanner.self_reflexive_operator.operator_step unchanged',
        'teacher_protocol':'12 complete R4 scalar-field frames with two approaching m=3 patterns plus the established alternating +/-w previous-flow pulse; after frame 11 no image displacement, phase forcing, J4 pulse, force, collision or annihilation rule is imposed',
        'cases':CASES,
        'parameters':{'dimension':DIM,'background':BACKGROUND,'object_total_each':OBJ_TOTAL,'ring_radius':RING_R,
                      'sigma':SIGMA,'train_frames':TRAIN_FRAMES,'free_frames':FREE_FRAMES,'start_abs_x':START_X,
                      'teacher_displacement_per_frame':TRAIN_STEP,'rotation_step_deg':ROT_STEP_DEG,
                      'r4_flow_period_frames':FLOW_PERIOD,'r4_flow_amplitude':FLOW_AMP,
                      'domain_l1':DOMAIN_L1,'domain_points':len(DOMAIN)},
        'analysis':stats,'raw_rows':results,
        'interpretation_guard':'all collision/contact quantities are post-hoc diagnostics only; dynamics sees no collision/annihilation/inertia rule'
    }
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
