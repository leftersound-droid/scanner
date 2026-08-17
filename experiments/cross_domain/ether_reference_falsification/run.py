from __future__ import annotations

import json, math, sys
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from scanner.self_reflexive_operator import operator_step

OUT = ROOT / 'run-data' / 'cross_domain' / 'ether_reference_falsification'
DIM = 4
BACKGROUND = 100.0
WAVE_AMP = 10.0
RING_R = 2.0
SIGMA = 0.55
DOMAIN_L1 = 20
WAVE_SUPPORT_L1 = 10
FRAMES = 8
MEASURE_L1 = 7
ETHER_AMP = 0.01
M = 3
STEP_DEG = 10.0

# Synthetic control worlds only. The operator is unchanged.
WORLDS = [
    {'name': 'absolute_unidirectional_background', 'mode': 'absolute'},
    {'name': 'isotropic_relational_background', 'mode': 'isotropic'},
    {'name': 'no_background', 'mode': 'none'},
]


def fixed_domain():
    r = range(-DOMAIN_L1, DOMAIN_L1 + 1)
    return [tuple(int(v) for v in c) for c in product(r, repeat=DIM)
            if sum(abs(v) for v in c) <= DOMAIN_L1]

DOMAIN = fixed_domain()
DOMAIN_SET = set(DOMAIN)
INDEX = {c: i for i, c in enumerate(DOMAIN)}
MEASURE = [c for c in DOMAIN if sum(abs(v) for v in c) <= MEASURE_L1]
MEASURE_SET = set(MEASURE)


def wave_component(theta):
    comp = {}
    for c in product(range(-5, 6), repeat=4):
        x, y, z, w = (float(v) for v in c)
        rho = math.hypot(x, y)
        d2 = (rho - RING_R) ** 2 + z*z + w*w
        env = math.exp(-0.5 * d2 / (SIGMA * SIGMA))
        if env < 1e-10:
            continue
        ang = math.atan2(y, x)
        val = WAVE_AMP * env * (1.0 + 0.35 * math.cos(M * (ang - theta)))
        if val > 1e-10:
            comp[tuple(int(v) for v in c)] = val
    return comp


def apply_component(phi, old, new):
    for c in set(old) | set(new):
        phi[c] += new.get(c, 0.0) - old.get(c, 0.0)


def inject_background(prev, mode):
    merged = dict(prev)
    injected = 0
    if mode == 'none':
        return merged, injected

    if mode == 'absolute':
        directions = [7]  # +w only: explicitly preferred direction
        per_edge = ETHER_AMP
    elif mode == 'isotropic':
        directions = list(range(2 * DIM))  # equal flow in every directed axis
        per_edge = ETHER_AMP / len(directions)
    else:
        raise ValueError(mode)

    for c in DOMAIN:
        for di in directions:
            axis = di // 2
            sign = 1 if (di % 2) else -1
            t = list(c)
            t[axis] += sign
            target = tuple(t)
            if target in DOMAIN_SET:
                merged[(c, di)] = merged.get((c, di), 0.0) + per_edge
                injected += 1
    return merged, injected


def full_phi(phi):
    return np.asarray([phi[c] for c in DOMAIN], dtype=np.float64)


def save_flow(path, flow):
    items = [(INDEX[c], di, v) for (c, di), v in flow.items()
             if c in INDEX and v != 0.0]
    if not items:
        np.savez_compressed(path,
            source_index=np.empty(0, dtype=np.int32),
            direction=np.empty(0, dtype=np.uint8),
            amount=np.empty(0, dtype=np.float64))
        return
    np.savez_compressed(path,
        source_index=np.asarray([x[0] for x in items], dtype=np.int32),
        direction=np.asarray([x[1] for x in items], dtype=np.uint8),
        amount=np.asarray([x[2] for x in items], dtype=np.float64))


def direction_totals(flow):
    totals = np.zeros(2 * DIM, dtype=np.float64)
    for (c, di), amount in flow.items():
        if c in MEASURE_SET:
            totals[di] += amount
    return totals


def bias_vector(totals):
    total = float(totals.sum())
    if total == 0.0:
        return [0.0] * DIM
    out = []
    for axis in range(DIM):
        minus = totals[2 * axis]
        plus = totals[2 * axis + 1]
        out.append(float((plus - minus) / total))
    return out


def anisotropy_norm(vec):
    return float(np.linalg.norm(np.asarray(vec, dtype=np.float64)))


def dominant_direction(vec):
    a = np.asarray(vec, dtype=float)
    if np.all(a == 0.0):
        return None
    k = int(np.argmax(np.abs(a)))
    sign = '+' if a[k] > 0 else '-'
    return f'{sign}{"xyzw"[k]}'


def run_world(spec):
    case_dir = OUT / spec['name']
    flow_dir = case_dir / 'flows'
    case_dir.mkdir(parents=True, exist_ok=True)
    flow_dir.mkdir(parents=True, exist_ok=True)

    phi = {c: BACKGROUND for c in DOMAIN}
    prev = {}
    old_wave = {}
    rows = []
    births_total = 0
    phi_in = []
    phi_out = []

    for frame in range(FRAMES):
        theta = math.radians(STEP_DEG * frame)
        new_wave = wave_component(theta)
        apply_component(phi, old_wave, new_wave)
        old_wave = new_wave

        phi_in.append(full_phi(phi))
        op_prev, injected_edges = inject_background(prev, spec['mode'])
        save_flow(flow_dir / f'frame_{frame:02d}_input.npz', op_prev)

        before = sum(phi.values())
        phi, next_flow, diag = operator_step(phi, op_prev, dimension=DIM)
        phi_out.append(full_phi(phi))
        save_flow(flow_dir / f'frame_{frame:02d}_output.npz', next_flow)

        totals = direction_totals(next_flow)
        vec = bias_vector(totals)
        beta = np.asarray(diag.beta_samples, dtype=float)
        rows.append({
            'frame': frame,
            'injected_edges': injected_edges,
            'live_transfer': float(diag.live_transfer),
            'beta_mean': float(beta.mean()) if beta.size else 0.0,
            'direction_totals': [float(v) for v in totals],
            'bias_vector_xyzw': vec,
            'anisotropy_norm': anisotropy_norm(vec),
            'dominant_direction': dominant_direction(vec),
            'conservation_error': float(sum(phi.values()) - before),
            'births': int(diag.births),
        })
        births_total += int(diag.births)
        prev = next_flow

    np.savez_compressed(case_dir / 'phi_history.npz',
                        phi_input=np.stack(phi_in), phi_output=np.stack(phi_out))

    mean_vec = np.mean(np.asarray([r['bias_vector_xyzw'] for r in rows], dtype=float), axis=0)
    frame_norms = np.asarray([r['anisotropy_norm'] for r in rows], dtype=float)
    return {
        'world': spec,
        'frames': FRAMES,
        'births_total': births_total,
        'boundary_unreachable': (WAVE_SUPPORT_L1 + FRAMES) < DOMAIN_L1,
        'mean_bias_vector_xyzw': [float(v) for v in mean_vec],
        'mean_anisotropy_norm': float(frame_norms.mean()),
        'max_anisotropy_norm': float(frame_norms.max()),
        'dominant_mean_direction': dominant_direction(mean_vec),
        'rows': rows,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUT / 'domain_coordinates.npz',
                        coord=np.asarray(DOMAIN, dtype=np.int16),
                        measurement_coord=np.asarray(MEASURE, dtype=np.int16))

    result = {
        'experiment': 'ether_reference_falsification',
        'status': 'synthetic control only; tests detectability of a preferred background direction; no Lorentz law is injected or claimed',
        'operator': 'unchanged scanner.self_reflexive_operator.operator_step',
        'definitions': {
            'absolute_world': 'same previous-flow background ETHER_AMP is injected only in +w on every available domain edge; this deliberately creates an absolute preferred direction',
            'isotropic_world': 'same total nominal background amplitude is split equally over all 8 directed nearest-neighbor axes; background is nonzero but has no preferred direction by construction',
            'no_background_world': 'no synthetic previous-flow component is added',
            'internal_observable': 'direction-resolved next_flow inside the measurement region; bias axis a=(J_+a-J_-a)/sum(J_all); no coordinate or Lorentz transformation is assumed',
            'falsification_question': 'can the internal flow data recover a stable preferred direction above the wave-only and isotropic controls?',
            'journal': 'full domain coordinates, complete phi input/output for each frame, and sparse raw previous_flow/next_flow arrays are stored',
        },
        'parameters': {
            'dimension': DIM,
            'background_phi': BACKGROUND,
            'ether_amplitude': ETHER_AMP,
            'frames': FRAMES,
            'domain_l1_radius': DOMAIN_L1,
            'domain_points': len(DOMAIN),
            'wave_support_l1': WAVE_SUPPORT_L1,
            'measurement_l1_radius': MEASURE_L1,
            'wave_m': M,
            'wave_step_deg_per_frame': STEP_DEG,
        },
        'worlds': {},
    }

    for spec in WORLDS:
        result['worlds'][spec['name']] = run_world(spec)

    # Purely comparative Scanner readout; baseline is the same wave with no synthetic background.
    base = np.asarray(result['worlds']['no_background']['mean_bias_vector_xyzw'], dtype=float)
    for name, data in result['worlds'].items():
        v = np.asarray(data['mean_bias_vector_xyzw'], dtype=float)
        residual = v - base
        data['bias_minus_wave_only_xyzw'] = [float(x) for x in residual]
        data['residual_anisotropy_vs_wave_only'] = float(np.linalg.norm(residual))
        data['residual_dominant_direction'] = dominant_direction(residual)

    (OUT / 'summary.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
