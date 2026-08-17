from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step, directions, add

OUT = ROOT / 'run-data' / 'cross_domain' / 'spacetime_graph_second_order'
DIM=4; BACKGROUND=100.0; OBJ_TOTAL=160.0; SIGMA=0.62
DOMAIN_L1=20; SUPPORT_L1=10; FRAMES=8; MEASURE_L1=7; REF_AMP=0.01; STEP_DEG=10.0
DS=directions(DIM)

# Measurement worlds only. They do not change operator_step.
WORLDS=[
 {'name':'none','dirs':[]},
 {'name':'isotropic','dirs':list(range(8))},
 {'name':'plus_w','dirs':[7]},
 {'name':'plus_x','dirs':[1]},
 {'name':'plus_y','dirs':[3]},
]

# Three synthetic object probes with deliberately different geometry.
# Every frame is normalized to the same total excess potential OBJ_TOTAL.
SHAPES=['ring_m3','ring_m4','double_lobe']


def fixed_domain():
    r=range(-DOMAIN_L1,DOMAIN_L1+1)
    return [tuple(int(v) for v in c) for c in product(r,repeat=4)
            if sum(abs(v) for v in c)<=DOMAIN_L1]
DOMAIN=fixed_domain(); DOMAIN_SET=set(DOMAIN); INDEX={c:i for i,c in enumerate(DOMAIN)}
MEASURE=[c for c in DOMAIN if sum(abs(v) for v in c)<=MEASURE_L1]; MEASURE_SET=set(MEASURE)


def raw_shape(shape,theta):
    comp={}
    for c in product(range(-5,6),repeat=4):
        x,y,z,w=(float(v) for v in c)
        if shape.startswith('ring'):
            rho=math.hypot(x,y); r0=2.0
            d2=(rho-r0)**2+z*z+w*w
            env=math.exp(-0.5*d2/(SIGMA*SIGMA))
            m=3 if shape=='ring_m3' else 4
            ang=math.atan2(y,x)
            val=env*(1.0+0.35*math.cos(m*(ang-theta)))
        else:
            # Two translating/rotating Gaussian lobes; same carrier dimension,
            # different topology from a ring. This is a synthetic control only.
            ct,st=math.cos(theta),math.sin(theta)
            cx,cy=1.6*ct,1.6*st
            d21=(x-cx)**2+(y-cy)**2+z*z+w*w
            d22=(x+cx)**2+(y+cy)**2+z*z+w*w
            val=math.exp(-0.5*d21/(SIGMA*SIGMA))+math.exp(-0.5*d22/(SIGMA*SIGMA))
        if val>1e-12: comp[tuple(int(v) for v in c)]=val
    s=sum(comp.values())
    if s<=0: return {}
    k=OBJ_TOTAL/s
    return {c:v*k for c,v in comp.items()}


def apply_component(phi,old,new):
    for c in set(old)|set(new): phi[c]+=new.get(c,0.0)-old.get(c,0.0)


def inject_reference(prev,spec):
    merged=dict(prev)
    if not spec['dirs']: return merged,0
    per=REF_AMP/len(spec['dirs']); n=0
    for c in DOMAIN:
        for di in spec['dirs']:
            if add(c,DS[di]) in DOMAIN_SET:
                merged[(c,di)]=merged.get((c,di),0.0)+per; n+=1
    return merged,n


def save_flow(path,flow):
    items=[(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v!=0.0]
    np.savez_compressed(path,
        source_index=np.asarray([q[0] for q in items],dtype=np.int32),
        direction=np.asarray([q[1] for q in items],dtype=np.uint8),
        amount=np.asarray([q[2] for q in items],dtype=np.float64))


def sector_graph_state(phi,prev,next_flow=None):
    # Operator-derived dependency graph nodes:
    # D3,D4 -> A3,A4 -> J3,J4 ; P3,P4 -> B3,B4 -> J3,J4.
    # Cross-sector coupling comes only from the shared alpha/beta normalizations.
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
    return np.asarray([d3,d4,p3,p4,a3/max(ad,1),a4/max(ad,1),b3/max(bd,1),b4/max(bd,1),j3,j4],dtype=float)

NODE_NAMES=['D3','D4','P3','P4','A3','A4','B3','B4','J3','J4']
# Edge list is not fitted: it is the explicit dependency structure of operator_step.
GRAPH_EDGES=[('D3','A3'),('D4','A4'),('D3','A4'),('D4','A3'),
             ('P3','B3'),('P4','B4'),('P3','B4'),('P4','B3'),
             ('A3','J3'),('B3','J3'),('A4','J4'),('B4','J4')]
EDGE_IDX=[(NODE_NAMES.index(a),NODE_NAMES.index(b)) for a,b in GRAPH_EDGES]


def safe_scale(v):
    s=float(np.linalg.norm(v)); return s if s>1e-30 else 1.0


def graph_signature(states):
    # No learned coefficients. For every frame, build a dimensionless graph
    # signature from node composition and operator-dependency edge products.
    out=[]
    for v in states:
        vn=v/safe_scale(v)
        edges=np.asarray([vn[i]*vn[j] for i,j in EDGE_IDX],dtype=float)
        out.append(np.concatenate([vn,edges]))
    return np.asarray(out)


def order_signatures(states):
    g=graph_signature(states)
    d1=np.diff(g,axis=0)
    d2=np.diff(g,n=2,axis=0)
    return g,d1,d2


def normalized_dispersion(vectors):
    # Distance of each matched condition from its group mean, normalized by
    # mean vector magnitude. Used only as a comparative analysis score.
    arr=np.asarray(vectors,dtype=float); mu=np.mean(arr,axis=0)
    denom=max(float(np.linalg.norm(mu)),1e-30)
    ds=np.linalg.norm(arr-mu,axis=1)/denom
    return float(np.mean(ds)),float(np.max(ds))


def run_case(shape,spec):
    case=OUT/shape/spec['name']; flowdir=case/'flows'; case.mkdir(parents=True,exist_ok=True); flowdir.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old={}; rows=[]; states=[]; births=0; pin=[]; pout=[]
    for frame in range(FRAMES):
        new=raw_shape(shape,math.radians(STEP_DEG*frame)); apply_component(phi,old,new); old=new
        op_prev,ninj=inject_reference(prev,spec)
        before=sum(phi.values()); pin.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(flowdir/f'{frame:02d}_input.npz',op_prev)
        # input state first; output J appended after operator step
        base=sector_graph_state(phi,op_prev,None)
        phi,nxt,diag=operator_step(phi,op_prev,dimension=DIM)
        final=sector_graph_state(phi,op_prev,nxt)
        # Keep D/P/A/B from pre-step and J from output step.
        state=base.copy(); state[8:10]=final[8:10]
        states.append(state)
        pout.append(np.asarray([phi[c] for c in DOMAIN],dtype=np.float64)); save_flow(flowdir/f'{frame:02d}_output.npz',nxt)
        births+=diag.births
        rows.append({'frame':frame,'injected_edges':ninj,'births':diag.births,'live_transfer':float(diag.live_transfer),'conservation_error':float(sum(phi.values())-before),'graph_nodes':dict(zip(NODE_NAMES,[float(x) for x in state]))})
        prev=nxt
    np.savez_compressed(case/'phi_history.npz',phi_input=np.stack(pin),phi_output=np.stack(pout))
    arr=np.stack(states); g,d1,d2=order_signatures(arr)
    np.savez_compressed(case/'graph_history.npz',nodes=arr,graph0=g,graph_d1=d1,graph_d2=d2)
    return {'shape':shape,'world':spec['name'],'births_total':births,'boundary_unreachable':SUPPORT_L1+FRAMES<DOMAIN_L1,'rows':rows,'graph0':g.tolist(),'graph_d1':d1.tolist(),'graph_d2':d2.tolist()}


def compare(results):
    # 1) Reference invariance within each shape at matched frames.
    ref_scores={}
    # 2) Shape invariance within each reference at matched frames.
    shape_scores={}
    # 3) Joint invariance across all shape/reference conditions.
    joint={}
    for order,key,nf in [(0,'graph0',FRAMES),(1,'graph_d1',FRAMES-1),(2,'graph_d2',FRAMES-2)]:
        vals=[]
        for shape in SHAPES:
            scores=[]
            for f in range(nf):
                vectors=[np.asarray(results[shape][w['name']][key][f]) for w in WORLDS]
                scores.append(normalized_dispersion(vectors)[0])
            ref_scores[f'order_{order}_{shape}']=float(np.mean(scores))
        for w in WORLDS:
            scores=[]
            for f in range(nf):
                vectors=[np.asarray(results[s][w['name']][key][f]) for s in SHAPES]
                scores.append(normalized_dispersion(vectors)[0])
            shape_scores[f'order_{order}_{w["name"]}']=float(np.mean(scores))
        frame_scores=[]
        for f in range(nf):
            vectors=[np.asarray(results[s][w['name']][key][f]) for s in SHAPES for w in WORLDS]
            frame_scores.append(normalized_dispersion(vectors)[0])
        joint[f'order_{order}']={'mean':float(np.mean(frame_scores)),'max':float(np.max(frame_scores))}
    return ref_scores,shape_scores,joint


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,dtype=np.int16),measurement_coord=np.asarray(MEASURE,dtype=np.int16))
    results={}
    for shape in SHAPES:
        results[shape]={}
        for spec in WORLDS:
            results[shape][spec['name']]=run_case(shape,spec)
    ref_scores,shape_scores,joint=compare(results)
    summary={
      'experiment':'spacetime_graph_second_order',
      'status':'synthetic graph-invariance control; no physical time, length, Lorentz law, mass, c, metric signature, or differential equation injected or claimed',
      'operator':'unchanged scanner.self_reflexive_operator.operator_step',
      'hypothesis':'emergent space/time may be represented by a small R3/R4 relational graph rather than a scalar ratio; if second-order relational binding is relevant, a graph signature built from second frame-differences may be more invariant to reference state and probe geometry than zeroth/first order signatures',
      'graph_nodes':NODE_NAMES,'graph_edges':GRAPH_EDGES,
      'orders':{'0':'dimensionless node composition plus operator-dependency edge products','1':'first frame difference of order-0 graph signature','2':'second frame difference of order-0 graph signature'},
      'controls':{'shapes':SHAPES,'shape_normalization':'same total excess potential every frame; this does not define equal physical mass','worlds':[w['name'] for w in WORLDS],'reference_normalization':'same nominal total previous-flow amplitude per source in each nonzero world','boundary_guard':f'{SUPPORT_L1}+{FRAMES}<{DOMAIN_L1}'},
      'parameters':{'frames':FRAMES,'domain_points':len(DOMAIN),'measure_l1':MEASURE_L1,'object_total_excess':OBJ_TOTAL,'reference_amplitude':REF_AMP},
      'reference_dispersion_by_shape':ref_scores,
      'shape_dispersion_by_reference':shape_scores,
      'joint_dispersion_by_order':joint,
      'checks':{s:{w['name']:{'births':results[s][w['name']]['births_total'],'boundary_unreachable':results[s][w['name']]['boundary_unreachable']} for w in WORLDS} for s in SHAPES},
      'journal':'full phi input/output and sparse flows for every frame/case plus graph node/order histories'
    }
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
