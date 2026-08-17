from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
from scanner.self_reflexive_operator import operator_step,directions,add

OUT=ROOT/'run-data'/'cross_domain'/'spacetime_edge_relation_change'
DIM=4; BACKGROUND=100.0; OBJ_TOTAL=160.0; SIGMA=0.62
DOMAIN_L1=20; SUPPORT_L1=10; FRAMES=8; MEASURE_L1=7; REF_AMP=0.01; STEP_DEG=10.0
DS=directions(DIM)
WORLDS=[{'name':'none','dirs':[]},{'name':'isotropic','dirs':list(range(8))},{'name':'plus_w','dirs':[7]},{'name':'plus_x','dirs':[1]},{'name':'plus_y','dirs':[3]}]
SHAPES=['ring_m3','ring_m4','double_lobe']
NODES=['D3','D4','P3','P4','A3','A4','B3','B4','J3','J4']
EDGES=[('D3','A3'),('D4','A4'),('D3','A4'),('D4','A3'),('P3','B3'),('P4','B4'),('P3','B4'),('P4','B3'),('A3','J3'),('B3','J3'),('A4','J4'),('B4','J4')]
EIDX=[(NODES.index(a),NODES.index(b)) for a,b in EDGES]


def fixed_domain():
    r=range(-DOMAIN_L1,DOMAIN_L1+1)
    return [tuple(int(v) for v in c) for c in product(r,repeat=4) if sum(abs(v) for v in c)<=DOMAIN_L1]
DOMAIN=fixed_domain(); DSET=set(DOMAIN); INDEX={c:i for i,c in enumerate(DOMAIN)}
MEASURE=[c for c in DOMAIN if sum(abs(v) for v in c)<=MEASURE_L1]; MSET=set(MEASURE)


def raw_shape(shape,theta):
    comp={}
    for c in product(range(-5,6),repeat=4):
        x,y,z,w=(float(v) for v in c)
        if shape.startswith('ring'):
            rho=math.hypot(x,y); d2=(rho-2.0)**2+z*z+w*w; env=math.exp(-.5*d2/(SIGMA*SIGMA))
            m=3 if shape=='ring_m3' else 4; val=env*(1+.35*math.cos(m*(math.atan2(y,x)-theta)))
        else:
            ct,st=math.cos(theta),math.sin(theta); cx,cy=1.6*ct,1.6*st
            d1=(x-cx)**2+(y-cy)**2+z*z+w*w; d2=(x+cx)**2+(y+cy)**2+z*z+w*w
            val=math.exp(-.5*d1/(SIGMA*SIGMA))+math.exp(-.5*d2/(SIGMA*SIGMA))
        if val>1e-12: comp[tuple(int(v) for v in c)]=val
    s=sum(comp.values()); k=OBJ_TOTAL/s
    return {c:v*k for c,v in comp.items()}


def apply_component(phi,old,new):
    for c in set(old)|set(new): phi[c]+=new.get(c,0.0)-old.get(c,0.0)


def inject_reference(prev,spec):
    out=dict(prev)
    if not spec['dirs']: return out,0
    per=REF_AMP/len(spec['dirs']); n=0
    for c in DOMAIN:
        for di in spec['dirs']:
            if add(c,DS[di]) in DSET:
                out[(c,di)]=out.get((c,di),0.0)+per; n+=1
    return out,n


def save_flow(path,flow):
    q=[(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v!=0.0]
    np.savez_compressed(path,source_index=np.asarray([x[0] for x in q],np.int32),direction=np.asarray([x[1] for x in q],np.uint8),amount=np.asarray([x[2] for x in q],float))


def state(phi,prev,next_flow=None):
    d3=d4=p3=p4=a3=a4=b3=b4=0.0; ad=bd=0
    for x in MEASURE:
        val=phi[x]; live=[]; sd=0.0
        for di,d in enumerate(DS):
            y=add(x,d)
            if y not in phi: continue
            dd=val-phi[y]
            if dd>0:
                live.append((di,dd)); sd+=dd
                if di<6:d3+=dd
                else:d4+=dd
        if sd<=0: continue
        a3+=sum(dd/sd for di,dd in live if di<6); a4+=sum(dd/sd for di,dd in live if di>=6); ad+=1
        ps=sum(max(prev.get((x,di),0.0),0.0) for di,_ in live)
        if ps>0:
            b3+=sum(max(prev.get((x,di),0.0),0.0)/ps for di,_ in live if di<6)
            b4+=sum(max(prev.get((x,di),0.0),0.0)/ps for di,_ in live if di>=6); bd+=1
    for (x,di),v in prev.items():
        if x in MSET and v>0:
            if di<6:p3+=v
            else:p4+=v
    j3=j4=0.0
    if next_flow is not None:
        for (x,di),v in next_flow.items():
            if x in MSET and v>0:
                if di<6:j3+=v
                else:j4+=v
    return np.asarray([d3,d4,p3,p4,a3/max(ad,1),a4/max(ad,1),b3/max(bd,1),b4/max(bd,1),j3,j4],float)


def normalize_nodes(v):
    n=float(np.linalg.norm(v)); return v/(n if n>1e-30 else 1.0)


def first_order_edges(v):
    # First degree = direct relation. No fitted coefficients: each edge is
    # the product of its two dimensionless endpoint values.
    z=normalize_nodes(v)
    return np.asarray([z[i]*z[j] for i,j in EIDX],float)


def second_order_edge_change(edge_history):
    # User definition: second degree = change of the direct relation itself.
    return np.diff(edge_history,axis=0)


def dispersion(vectors):
    a=np.asarray(vectors,float); mu=np.mean(a,axis=0); den=max(float(np.linalg.norm(mu)),1e-30)
    d=np.linalg.norm(a-mu,axis=1)/den
    return float(np.mean(d)),float(np.max(d))


def run_case(shape,spec):
    case=OUT/shape/spec['name']; fd=case/'flows'; case.mkdir(parents=True,exist_ok=True); fd.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old={}; states=[]; edges=[]; rows=[]; pin=[]; pout=[]; births=0
    for f in range(FRAMES):
        new=raw_shape(shape,math.radians(STEP_DEG*f)); apply_component(phi,old,new); old=new
        op_prev,ninj=inject_reference(prev,spec); before=sum(phi.values())
        pin.append(np.asarray([phi[c] for c in DOMAIN],float)); save_flow(fd/f'{f:02d}_input.npz',op_prev)
        base=state(phi,op_prev,None); phi,nxt,diag=operator_step(phi,op_prev,dimension=DIM); fin=state(phi,op_prev,nxt)
        v=base.copy(); v[8:10]=fin[8:10]; e=first_order_edges(v)
        states.append(v); edges.append(e); births+=diag.births
        pout.append(np.asarray([phi[c] for c in DOMAIN],float)); save_flow(fd/f'{f:02d}_output.npz',nxt)
        rows.append({'frame':f,'injected_edges':ninj,'births':diag.births,'live_transfer':float(diag.live_transfer),'conservation_error':float(sum(phi.values())-before),'nodes':dict(zip(NODES,map(float,v))),'first_order_edges':dict((f'{a}->{b}',float(x)) for (a,b),x in zip(EDGES,e))})
        prev=nxt
    states=np.stack(states); edges=np.stack(edges); changes=second_order_edge_change(edges)
    np.savez_compressed(case/'phi_history.npz',phi_input=np.stack(pin),phi_output=np.stack(pout))
    np.savez_compressed(case/'relation_history.npz',nodes=states,first_order_edges=edges,second_order_edge_change=changes)
    return {'rows':rows,'first_order_edges':edges.tolist(),'second_order_edge_change':changes.tolist(),'births_total':births,'boundary_unreachable':SUPPORT_L1+FRAMES<DOMAIN_L1}


def compare(results):
    out={'reference':{},'shape':{},'joint':{},'per_edge_joint':{}}
    for label,key,nf in [('first','first_order_edges',FRAMES),('second','second_order_edge_change',FRAMES-1)]:
        for s in SHAPES:
            vals=[]
            for f in range(nf): vals.append(dispersion([results[s][w['name']][key][f] for w in WORLDS])[0])
            out['reference'][f'{label}_{s}']=float(np.mean(vals))
        for w in WORLDS:
            vals=[]
            for f in range(nf): vals.append(dispersion([results[s][w['name']][key][f] for s in SHAPES])[0])
            out['shape'][f'{label}_{w["name"]}']=float(np.mean(vals))
        vals=[]
        for f in range(nf): vals.append(dispersion([results[s][w['name']][key][f] for s in SHAPES for w in WORLDS])[0])
        out['joint'][label]={'mean':float(np.mean(vals)),'max':float(np.max(vals))}
        # Per-edge scalar CV-like dispersion across all matched shape/reference cases.
        per=[]
        for ei,(a,b) in enumerate(EDGES):
            fs=[]
            for f in range(nf):
                arr=np.asarray([results[s][w['name']][key][f][ei] for s in SHAPES for w in WORLDS],float)
                den=max(float(np.mean(np.abs(arr))),1e-30); fs.append(float(np.std(arr))/den)
            per.append({'edge':f'{a}->{b}','mean_relative_dispersion':float(np.mean(fs))})
        per.sort(key=lambda x:x['mean_relative_dispersion']); out['per_edge_joint'][label]=per
    return out


def main():
    OUT.mkdir(parents=True,exist_ok=True); np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,np.int16),measurement_coord=np.asarray(MEASURE,np.int16))
    results={s:{w['name']:run_case(s,w) for w in WORLDS} for s in SHAPES}
    scores=compare(results)
    summary={'experiment':'spacetime_edge_relation_change','status':'synthetic relation-invariance control; no physical time, length, Lorentz law, mass, c, metric signature or differential equation injected or claimed','operator':'unchanged scanner.self_reflexive_operator.operator_step','definitions':{'first_degree':'direct operator-dependency edge relation, represented only for measurement as the product of dimensionless endpoint values','second_degree':'frame-to-frame change of that same direct edge relation; NOT a second finite difference of a whole-graph signature','r3_r4':'3-sector = x/y/z directions; 4-sector = w directions','edge_set':'fixed from the operator dependency structure; no edge learned or fitted'},'shapes':SHAPES,'worlds':[w['name'] for w in WORLDS],'graph_nodes':NODES,'graph_edges':EDGES,'parameters':{'frames':FRAMES,'domain_points':len(DOMAIN),'object_total_excess':OBJ_TOTAL,'reference_amplitude':REF_AMP,'boundary_guard':f'{SUPPORT_L1}+{FRAMES}<{DOMAIN_L1}'},'scores':scores,'checks':{s:{w['name']:{'births':results[s][w['name']]['births_total'],'boundary_unreachable':results[s][w['name']]['boundary_unreachable']} for w in WORLDS} for s in SHAPES},'journal':'complete phi input/output, sparse flows, node states, direct edge relations and edge-relation changes for every case/frame'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8'); print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
