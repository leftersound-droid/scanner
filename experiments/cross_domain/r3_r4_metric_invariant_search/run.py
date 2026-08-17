from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step, directions, add

OUT = ROOT / 'run-data' / 'cross_domain' / 'r3_r4_metric_invariant_search'
DIM = 4
BACKGROUND = 100.0
WAVE_AMP = 10.0
RING_R = 2.0
SIGMA = 0.55
DOMAIN_L1 = 20
WAVE_SUPPORT_L1 = 10
FRAMES = 8
MEASURE_L1 = 7
REF_AMP = 0.01
M = 3
STEP_DEG = 10.0
DS = directions(DIM)

# Synthetic reference states only.  They do not modify the operator law.
WORLDS = [
    {'name':'none', 'dirs':[]},
    {'name':'isotropic', 'dirs':list(range(8))},
    {'name':'plus_w', 'dirs':[7]},
    {'name':'minus_w', 'dirs':[6]},
    {'name':'plus_x', 'dirs':[1]},
    {'name':'minus_x', 'dirs':[0]},
    {'name':'plus_y', 'dirs':[3]},
    {'name':'minus_y', 'dirs':[2]},
]


def fixed_domain():
    r = range(-DOMAIN_L1, DOMAIN_L1 + 1)
    return [tuple(int(v) for v in c) for c in product(r, repeat=4)
            if sum(abs(v) for v in c) <= DOMAIN_L1]

DOMAIN = fixed_domain()
DOMAIN_SET = set(DOMAIN)
INDEX = {c:i for i,c in enumerate(DOMAIN)}
MEASURE = [c for c in DOMAIN if sum(abs(v) for v in c) <= MEASURE_L1]
MEASURE_SET = set(MEASURE)


def wave_component(theta):
    comp = {}
    for c in product(range(-5,6), repeat=4):
        x,y,z,w = (float(v) for v in c)
        rho = math.hypot(x,y)
        d2 = (rho-RING_R)**2 + z*z + w*w
        env = math.exp(-0.5*d2/(SIGMA*SIGMA))
        if env < 1e-10:
            continue
        ang = math.atan2(y,x)
        val = WAVE_AMP * env * (1.0 + 0.35*math.cos(M*(ang-theta)))
        if val > 1e-10:
            comp[tuple(int(v) for v in c)] = val
    return comp


def apply_component(phi, old, new):
    for c in set(old) | set(new):
        phi[c] += new.get(c,0.0) - old.get(c,0.0)


def inject_reference(prev, spec):
    merged = dict(prev)
    if not spec['dirs']:
        return merged, 0
    # Same total nominal amplitude per source for all nonzero reference worlds.
    per_dir = REF_AMP / len(spec['dirs'])
    count = 0
    for c in DOMAIN:
        for di in spec['dirs']:
            y = add(c, DS[di])
            if y in DOMAIN_SET:
                merged[(c,di)] = merged.get((c,di),0.0) + per_dir
                count += 1
    return merged, count


def full_phi(phi):
    return np.asarray([phi[c] for c in DOMAIN], dtype=np.float64)


def save_flow(path, flow):
    items = [(INDEX[c],di,v) for (c,di),v in flow.items() if c in INDEX and v != 0.0]
    if not items:
        np.savez_compressed(path,
            source_index=np.empty(0,dtype=np.int32),
            direction=np.empty(0,dtype=np.uint8),
            amount=np.empty(0,dtype=np.float64))
        return
    np.savez_compressed(path,
        source_index=np.asarray([x[0] for x in items],dtype=np.int32),
        direction=np.asarray([x[1] for x in items],dtype=np.uint8),
        amount=np.asarray([x[2] for x in items],dtype=np.float64))


def raw_sector_observables(phi, prev):
    # These are measurements only; they are not fed back into the operator.
    delta3 = delta4 = 0.0
    delta3_sq = delta4_sq = 0.0
    prev3 = prev4 = 0.0
    alpha3_sum = alpha4_sum = 0.0
    beta3_sum = beta4_sum = 0.0
    alpha_donors = beta_donors = 0
    edge3 = edge4 = 0

    for x in MEASURE:
        value = phi[x]
        live = []
        sum_delta = 0.0
        for di,d in enumerate(DS):
            y = add(x,d)
            if y not in phi:
                continue
            dd = value - phi[y]
            if dd > 0.0:
                live.append((di,dd))
                sum_delta += dd
                if di < 6:
                    delta3 += dd; delta3_sq += dd*dd; edge3 += 1
                else:
                    delta4 += dd; delta4_sq += dd*dd; edge4 += 1
        if sum_delta <= 0.0:
            continue
        a3 = sum(dd/sum_delta for di,dd in live if di < 6)
        a4 = sum(dd/sum_delta for di,dd in live if di >= 6)
        alpha3_sum += a3; alpha4_sum += a4; alpha_donors += 1

        ps = sum(max(prev.get((x,di),0.0),0.0) for di,_ in live)
        if ps > 0.0:
            b3 = sum(max(prev.get((x,di),0.0),0.0)/ps for di,_ in live if di < 6)
            b4 = sum(max(prev.get((x,di),0.0),0.0)/ps for di,_ in live if di >= 6)
            beta3_sum += b3; beta4_sum += b4; beta_donors += 1

    for (x,di),v in prev.items():
        if x not in MEASURE_SET or v <= 0.0:
            continue
        if di < 6: prev3 += v
        else: prev4 += v

    return {
        'delta3_sum':delta3, 'delta4_sum':delta4,
        'delta3_rms':math.sqrt(delta3_sq/max(edge3,1)),
        'delta4_rms':math.sqrt(delta4_sq/max(edge4,1)),
        'previous_flow3_sum':prev3, 'previous_flow4_sum':prev4,
        'alpha3_mean':alpha3_sum/max(alpha_donors,1),
        'alpha4_mean':alpha4_sum/max(alpha_donors,1),
        'beta3_mean':beta3_sum/max(beta_donors,1),
        'beta4_mean':beta4_sum/max(beta_donors,1),
        'alpha_donors':alpha_donors, 'beta_donors':beta_donors,
    }


def output_sector(next_flow):
    j3 = j4 = 0.0
    j3_sq = j4_sq = 0.0
    n3 = n4 = 0
    for (x,di),v in next_flow.items():
        if x not in MEASURE_SET or v <= 0.0:
            continue
        if di < 6:
            j3 += v; j3_sq += v*v; n3 += 1
        else:
            j4 += v; j4_sq += v*v; n4 += 1
    return {
        'next_flow3_sum':j3, 'next_flow4_sum':j4,
        'next_flow3_rms':math.sqrt(j3_sq/max(n3,1)),
        'next_flow4_rms':math.sqrt(j4_sq/max(n4,1)),
        'next_flow_total':j3+j4,
    }


def candidate_values(x,y):
    eps = 1e-30
    return {
        'sum':x+y,
        'euclidean_norm':math.sqrt(x*x+y*y),
        'abs_difference':abs(x-y),
        'product':x*y,
        'ratio_3_over_4':x/(abs(y)+eps),
        'ratio_4_over_3':y/(abs(x)+eps),
        'quadratic_difference':y*y-x*x,
    }


def matched_reference_dispersion(world_results):
    # For each frame, compare the same observable combination across synthetic
    # reference worlds. Lower relative dispersion = more reference-stable.
    pair_defs = {
        'delta_sum':('delta3_sum','delta4_sum'),
        'delta_rms':('delta3_rms','delta4_rms'),
        'previous_flow_sum':('previous_flow3_sum','previous_flow4_sum'),
        'next_flow_sum':('next_flow3_sum','next_flow4_sum'),
        'next_flow_rms':('next_flow3_rms','next_flow4_rms'),
        'alpha_mean':('alpha3_mean','alpha4_mean'),
        'beta_mean':('beta3_mean','beta4_mean'),
    }
    scan = []
    for pname,(a,b) in pair_defs.items():
        for form in candidate_values(1.0,1.0).keys():
            frame_scores=[]; frame_means=[]
            for f in range(FRAMES):
                vals=[]
                for w in WORLDS:
                    row=world_results[w['name']]['rows'][f]
                    v=candidate_values(float(row[a]),float(row[b]))[form]
                    if math.isfinite(v): vals.append(v)
                if len(vals) < 2: continue
                arr=np.asarray(vals,dtype=float)
                mean=float(np.mean(arr)); sd=float(np.std(arr))
                scale=max(float(np.mean(np.abs(arr))),1e-30)
                frame_scores.append(sd/scale); frame_means.append(mean)
            if frame_scores:
                scan.append({
                    'pair':pname,'form':form,
                    'mean_relative_dispersion_across_references':float(np.mean(frame_scores)),
                    'max_relative_dispersion_across_references':float(np.max(frame_scores)),
                    'mean_value':float(np.mean(frame_means)),
                    'definition_only': (pname in ('alpha_mean','beta_mean') and form=='sum'),
                })
    scan.sort(key=lambda z:(z['definition_only'],z['mean_relative_dispersion_across_references']))
    return scan


def run_world(spec):
    case_dir=OUT/spec['name']; flow_dir=case_dir/'flows'
    case_dir.mkdir(parents=True,exist_ok=True); flow_dir.mkdir(parents=True,exist_ok=True)
    phi={c:BACKGROUND for c in DOMAIN}; prev={}; old_wave={}; rows=[]; births=0; phi_in=[]; phi_out=[]
    for frame in range(FRAMES):
        theta=math.radians(STEP_DEG*frame)
        nw=wave_component(theta); apply_component(phi,old_wave,nw); old_wave=nw
        op_prev,ninj=inject_reference(prev,spec)
        obs=raw_sector_observables(phi,op_prev)
        phi_in.append(full_phi(phi)); save_flow(flow_dir/f'frame_{frame:02d}_input.npz',op_prev)
        before=sum(phi.values())
        phi,next_flow,diag=operator_step(phi,op_prev,dimension=DIM)
        phi_out.append(full_phi(phi)); save_flow(flow_dir/f'frame_{frame:02d}_output.npz',next_flow)
        outobs=output_sector(next_flow)
        births += diag.births
        row={'frame':frame,'injected_edges':ninj,'live_transfer':float(diag.live_transfer),
             'conservation_error':float(sum(phi.values())-before),'births':diag.births}
        row.update(obs); row.update(outobs)
        # Explicit algebraic controls. These are not evidence of emergence.
        row['alpha_complement_sum']=row['alpha3_mean']+row['alpha4_mean']
        row['beta_complement_sum']=row['beta3_mean']+row['beta4_mean'] if row['beta_donors'] else 0.0
        rows.append(row)
        prev=next_flow
    np.savez_compressed(case_dir/'phi_history.npz',phi_input=np.stack(phi_in),phi_output=np.stack(phi_out))
    return {'world':spec,'frames':FRAMES,'births_total':births,
            'boundary_unreachable':(WAVE_SUPPORT_L1+FRAMES)<DOMAIN_L1,'rows':rows}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(OUT/'domain_coordinates.npz',coord=np.asarray(DOMAIN,dtype=np.int16),measurement_coord=np.asarray(MEASURE,dtype=np.int16))
    worlds={}
    for spec in WORLDS:
        worlds[spec['name']]=run_world(spec)
    scan=matched_reference_dispersion(worlds)
    result={
        'experiment':'r3_r4_metric_invariant_search',
        'status':'synthetic reference-state scan; no metric, time, Lorentz law or c is injected or claimed',
        'operator':'unchanged scanner.self_reflexive_operator.operator_step',
        'hypothesis_under_test':'a useful emergent length candidate should live in the x/y/z sector and a complementary time candidate in the w sector; a genuine invariant should remain stable across reference states without being a definitional normalization identity',
        'definitions':{
            'r3_sector':'directions -x,+x,-y,+y,-z,+z',
            'r4_complement_sector':'directions -w,+w',
            'reference_states':'synthetic previous_flow backgrounds only; same nominal REF_AMP for every nonzero world',
            'candidate_search':'finite Scanner-side library: sum, Euclidean norm, absolute difference, product, two ratios, quadratic difference. This library is analysis software, not operator physics.',
            'algebraic_controls':'alpha3+alpha4=1 by alpha normalization on active donors; beta3+beta4=1 where positive previous flow exists on active live edges. These are explicitly excluded as emergent metric evidence.',
            'invariance_score':'for each frame, relative standard deviation of a candidate across all synthetic reference worlds; reported score is mean across frames. Lower is more reference-stable.',
            'journal':'full domain coordinates, complete phi input/output each frame, sparse raw previous_flow and next_flow each frame, plus all summary observables'
        },
        'parameters':{'dimension':DIM,'background_phi':BACKGROUND,'reference_amplitude':REF_AMP,'frames':FRAMES,'domain_l1_radius':DOMAIN_L1,'domain_points':len(DOMAIN),'wave_support_l1':WAVE_SUPPORT_L1,'measurement_l1_radius':MEASURE_L1,'wave_m':M,'wave_step_deg_per_frame':STEP_DEG},
        'worlds':worlds,
        'candidate_scan':scan,
        'top_nondefinitional_candidates':scan[:20],
    }
    (OUT/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'experiment':result['experiment'],'parameters':result['parameters'],'world_checks':{k:{'births_total':v['births_total'],'boundary_unreachable':v['boundary_unreachable']} for k,v in worlds.items()},'top_nondefinitional_candidates':result['top_nondefinitional_candidates']},indent=2))

if __name__=='__main__':
    main()
