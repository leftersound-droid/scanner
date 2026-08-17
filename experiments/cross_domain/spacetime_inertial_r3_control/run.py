from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step, directions, add

OUT = ROOT / 'run-data' / 'cross_domain' / 'spacetime_inertial_r3_control'
DIM=4; BACKGROUND=100.0; OBJ_TOTAL=160.0; SIGMA=0.62
DOMAIN_L1=22; SUPPORT_L1=10; FRAMES=8; MEASURE_L1=8; REF_AMP=0.01
DS=directions(DIM)

# Same object, same isotropic relational background, only constant R3 translation cadence changes.
# Cadence is a synthetic control parameter measured in lattice-coordinate shift per frame;
# it is NOT identified with physical speed.
CADENCES=[0.0,0.25,0.5,0.75,1.0]


def fixed_domain():
    r=range(-DOMAIN_L1,DOMAIN_L1+1)
    return [tuple(int(v) for v in c) for c in product(r,repeat=4)
            if sum(abs(v) for v in c)<=DOMAIN_L1]
DOMAIN=fixed_domain(); DOMAIN_SET=set(DOMAIN); INDEX={c:i for i,c in enumerate(DOMAIN)}
MEASURE=[c for c in DOMAIN if sum(abs(v) for v in c)<=MEASURE_L1]; MEASURE_SET=set(MEASURE)


def raw_object(cx: float):
    # Fixed m=3 closed non-rigid ring shape translated along +x only.
    comp={}
    for c in product(range(-7,8), repeat=4):
        x,y,z,w=(float(v) for v in c)
        xx=x-cx
        rho=math.hypot(xx,y); r0=2.0
        d2=(rho-r0)**2+z*z+w*w
        env=math.exp(-0.5*d2/(SIGMA*SIGMA))
        ang=math.atan2(y,xx)
        val=env*(1.0+0.35*math.cos(3*ang))
        if val>1e-12: comp[tuple(int(v) for v in c)] = val
    s=sum(comp.values())
    if s<=0: return {}
    k=OBJ_TOTAL/s
    return {c:v*k for c,v in comp.items()}


def apply_component(phi,old,new):
    for c in set(old)|set(new): phi[c]+=new.get(c,0.0)-old.get(c,0.0)


def inject_isotropic(prev):
    merged=dict(prev); per=REF_AMP/8.0; n=0
    for c in DOMAIN:
        for di in range(8):
            if add(c,DS[di]) in DOMAIN_SET:
                merged[(c,di)] = merged.get((c,di),0.0)+per; n+=1
    return merged,n


def save_flow(path,flow):
    items=[(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v!=0.0]
    np.savez_compressed(path,
        source_index=np.asarray([q[0] for q in items],dtype=np.int32),
        direction=np.asarray([q[1] for q in items],dtype=np.uint8),
        amount=np.asarray([q[2] for q in items],dtype=np.float64))


def sector_state(phi,prev,next_flow=None):
    d3=d4=p3=p4=0.0; a3=a4=b3=b4=0.0; ad=bd=0
    for x in MEASURE:
        value=phi[x]; live=[]; sd=0.0
        for di,d in enumerate(DS):
            y=add(x,d)
            if y not in phi: continue
            dd=value-phi[y]
            if dd>0:
                live.append((di,dd)); sd+=dd
                if di<6: d3+=dd
                else: d4+=dd
        if sd<=0: continue
        a3+=sum(dd/sd for di,dd in live if di<6); a4+=sum(dd/sd for di,dd in live if di>=6); ad+=1
        ps=sum(max(prev.get((x,di),0.0),0.0) for di,_ in live)
        if ps>0:
            b3+=sum(max(prev.get((x,di),0.0),0.0)/ps for di,_ in live if di<6)
            b4+=sum(max(prev.get((x,di),0.0),0.0)/ps for di,_ in live if di>=6); bd+=1
    for (x,di),v in prev.items():
        if x in MEASURE_SET and v>0:
            if di<6:p3+=v
            else:p4+=v
    j3=j4=0.0
    if next_flow is not None:
        for (x,di),v in next_flow.items():
            if x in MEASURE_SET and v>0:
                if di<6:j3+=v
                else:j4+=v
    return {
      'D3':d3,'D4':d4,'P3':p3,'P4':p4,
      'A3':a3/max(ad,1),'A4':a4/max(ad,1),
      'B3':b3/max(bd,1),'B4':b4/max(bd,1),
      'J3':j3,'J4':j4,
    }


def candidate_values(x,y):
    eps=1e-30
    return {
      'sum':x+y,
      'euclidean_norm':math.sqrt(x*x+y*y),
      'abs_difference':abs(x-y),
      'product':x*y,
      'ratio_3_over_4':x/(abs(y)+eps),
      'ratio_4_over_3':y/(abs(x)+eps),
      'quadratic_difference':y*y-x*x,
    }

PAIR_DEFS={
 'D':('D3','D4'),'P':('P3','P4'),'A':('A3','A4'),'B':('B3','B4'),'J':('J3','J4')
}


def run_case(cadence):
    name=f'cadence_{cadence:.2f}'.replace('.','p')
    case=OUT/name; flowdir=case/'flows'; case.mkdir(parents=True,exist_ok=True); flowdir.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old={}; rows=[]; births=0; pin=[]; pout=[]
    for frame in range(FRAMES):
        cx=cadence*frame
        new=raw_object(cx); apply_component(phi,old,new); old=new
        op_prev,ninj=inject_isotropic(prev)
        before=sum(phi.values())
        pre=sector_state(phi,op_prev,None)
        pin.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(flowdir/f'{frame:02d}_input.npz',op_prev)
        phi,nxt,diag=operator_step(phi,op_prev,dimension=DIM)
        post=sector_state(phi,op_prev,nxt)
        state=dict(pre); state['J3']=post['J3']; state['J4']=post['J4']
        row={'frame':frame,'cadence':cadence,'center_x':cx,'injected_edges':ninj,'births':diag.births,'live_transfer':float(diag.live_transfer),'conservation_error':float(sum(phi.values())-before),'state':state}
        # Raw candidate library only; none is privileged as metric.
        row['candidates']={p:candidate_values(float(state[a]),float(state[b])) for p,(a,b) in PAIR_DEFS.items()}
        rows.append(row); births+=diag.births
        pout.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(flowdir/f'{frame:02d}_output.npz',nxt)
        prev=nxt
    np.savez_compressed(case/'phi_history.npz',phi_input=np.stack(pin),phi_output=np.stack(pout))
    return {'cadence':cadence,'rows':rows,'births_total':births,'boundary_unreachable':SUPPORT_L1+int(math.ceil(cadence*(FRAMES-1)))+FRAMES<DOMAIN_L1}


def scan_inertial(results):
    scan=[]
    for pair in PAIR_DEFS:
        for form in candidate_values(1.0,1.0):
            frame_scores=[]; trends=[]
            for f in range(1,FRAMES):
                vals=[]; cs=[]
                for c in CADENCES:
                    row=results[str(c)]['rows'][f]
                    vals.append(float(row['candidates'][pair][form])); cs.append(c)
                arr=np.asarray(vals,float); scale=max(float(np.mean(np.abs(arr))),1e-30)
                frame_scores.append(float(np.std(arr))/scale)
                if np.std(arr)>0 and np.std(cs)>0:
                    trends.append(float(np.corrcoef(np.asarray(cs,float),arr)[0,1]))
            scan.append({'pair':pair,'form':form,'mean_relative_dispersion_across_cadences':float(np.mean(frame_scores)),'max_relative_dispersion_across_cadences':float(np.max(frame_scores)),'mean_cadence_correlation':float(np.mean(trends)) if trends else 0.0,'definition_only':(pair in ('A','B') and form=='sum')})
    scan.sort(key=lambda z:(z['definition_only'],z['mean_relative_dispersion_across_cadences']))
    return scan


def graph_vectors(results):
    # Dimensionless R3/R4 relational graph from the same raw state.
    names=['D3','D4','P3','P4','A3','A4','B3','B4','J3','J4']
    edges=[('D3','A3'),('D4','A4'),('D3','A4'),('D4','A3'),('P3','B3'),('P4','B4'),('P3','B4'),('P4','B3'),('A3','J3'),('B3','J3'),('A4','J4'),('B4','J4')]
    idx={n:i for i,n in enumerate(names)}
    out={}
    for c in CADENCES:
        vecs=[]
        for row in results[str(c)]['rows']:
            v=np.asarray([row['state'][n] for n in names],float); norm=max(float(np.linalg.norm(v)),1e-30); vn=v/norm
            ev=np.asarray([vn[idx[a]]*vn[idx[b]] for a,b in edges],float)
            vecs.append(np.concatenate([vn,ev]))
        out[str(c)]=np.stack(vecs)
    return out


def graph_dispersion(g):
    scores=[]
    for f in range(1,FRAMES):
        arr=np.stack([g[str(c)][f] for c in CADENCES]); mu=arr.mean(axis=0); den=max(float(np.linalg.norm(mu)),1e-30)
        scores.append(float(np.mean(np.linalg.norm(arr-mu,axis=1)/den)))
    return {'mean':float(np.mean(scores)),'max':float(np.max(scores))}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,dtype=np.int16),measurement_coord=np.asarray(MEASURE,dtype=np.int16))
    results={str(c):run_case(c) for c in CADENCES}
    scan=scan_inertial(results); g=graph_vectors(results)
    for c in CADENCES: np.savez_compressed(OUT/f'graph_{str(c).replace(".","p")}.npz',graph=g[str(c)])
    summary={
      'experiment':'spacetime_inertial_r3_control',
      'status':'synthetic inertial-control scan; no physical velocity, time, length, Lorentz law, c, mass or metric signature injected or claimed',
      'operator':'unchanged scanner.self_reflexive_operator.operator_step',
      'control':'same m=3 ring, same total excess potential, same isotropic relational background; only constant +x translation cadence changes',
      'cadences':CADENCES,
      'definitions':{
        'cadence':'lattice-coordinate center shift per frame, analysis/control parameter only',
        'r3_sector':'x/y/z directions','r4_sector':'w directions',
        'ratio_scan':'R3/R4 and R4/R3 are scanned alongside sum, norm, difference, product and quadratic difference; no ratio is privileged',
        'graph':'dimensionless node composition plus explicit operator-dependency edge products; Scanner measurement only'
      },
      'parameters':{'frames':FRAMES,'domain_points':len(DOMAIN),'measure_l1':MEASURE_L1,'object_total_excess':OBJ_TOTAL,'reference_amplitude':REF_AMP},
      'checks':{str(c):{'births':results[str(c)]['births_total'],'boundary_unreachable':results[str(c)]['boundary_unreachable']} for c in CADENCES},
      'candidate_scan':scan,
      'top_nondefinitional_candidates':scan[:20],
      'graph_dispersion_across_cadences':graph_dispersion(g),
      'journal':'complete phi input/output and sparse flows for every frame/cadence plus raw R3/R4 state and candidate values'
    }
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
