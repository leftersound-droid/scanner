from __future__ import annotations

import json
import math
import sys
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from scanner.self_reflexive_operator import operator_step, directions, add

OUT = ROOT / "run-data" / "cross_domain" / "phase_memory_frequency_sweep"
DIM = 4
BACKGROUND = 100.0
WAVE_AMP = 10.0
RING_R = 2.0
SIGMA = 0.55
M = 3
FLOW_PERIOD = 12
FLOW_AMP = 0.01
FRAMES = 14
DOMAIN_L1 = 20
WAVE_SUPPORT_L1 = 5
MEASURE_L1 = 6
RATIOS = [0.75, 1.0, 1.25, 1.5, 2.0]  # Omega_field / Omega_phase
DS = directions(DIM)


def fixed_domain():
    r = range(-DOMAIN_L1, DOMAIN_L1 + 1)
    return [tuple(int(v) for v in c) for c in product(r, repeat=4)
            if sum(abs(v) for v in c) <= DOMAIN_L1]


DOMAIN = fixed_domain()
DOMAIN_SET = set(DOMAIN)
INDEX = {c: i for i, c in enumerate(DOMAIN)}
LOCAL = [c for c in DOMAIN if sum(abs(v) for v in c) <= MEASURE_L1]
LOCAL_SET = set(LOCAL)
LOCAL_INDEX = {c: i for i, c in enumerate(LOCAL)}


def initial_phi():
    return {c: BACKGROUND for c in DOMAIN}


def wave_component(theta: float):
    comp = {}
    for c in product(range(-WAVE_SUPPORT_L1, WAVE_SUPPORT_L1 + 1), repeat=4):
        if sum(abs(v) for v in c) > WAVE_SUPPORT_L1:
            continue
        x, y, z, w = (float(v) for v in c)
        rho = math.hypot(x, y)
        d2 = (rho - RING_R) ** 2 + z*z + w*w
        env = math.exp(-0.5 * d2 / (SIGMA * SIGMA))
        if env < 1e-12:
            continue
        ang = math.atan2(y, x)
        val = WAVE_AMP * env * (1.0 + 0.35 * math.cos(M * (ang - theta)))
        if val > 1e-12:
            comp[tuple(int(v) for v in c)] = val
    return comp


def apply_component(phi, old, new):
    for c in set(old) | set(new):
        phi[c] += new.get(c, 0.0) - old.get(c, 0.0)


def impose_longitudinal_flow(prev, frame: int, on: bool):
    merged = dict(prev)
    signed = FLOW_AMP * math.sin(2.0 * math.pi * frame / FLOW_PERIOD) if on else 0.0
    amp = abs(signed)
    if amp < 1e-15:
        return merged, signed, 0, None
    di = 7 if signed > 0.0 else 6
    step = 1 if signed > 0.0 else -1
    count = 0
    for c in DOMAIN:
        target = (c[0], c[1], c[2], c[3] + step)
        if target in DOMAIN_SET:
            merged[(c, di)] = merged.get((c, di), 0.0) + amp
            count += 1
    return merged, signed, count, ("+w" if step > 0 else "-w")


def full_phi(phi):
    return np.asarray([phi[c] for c in DOMAIN], dtype=np.float64)


def local_phi(phi):
    return np.asarray([phi[c] for c in LOCAL], dtype=np.float64)


def save_flow(path: Path, flow):
    items = [(INDEX[c], di, v) for (c, di), v in flow.items() if c in INDEX and v != 0.0]
    np.savez_compressed(
        path,
        source_index=np.asarray([q[0] for q in items], dtype=np.int32),
        direction=np.asarray([q[1] for q in items], dtype=np.uint8),
        amount=np.asarray([q[2] for q in items], dtype=np.float64),
    )


def local_edge_state(phi, prev):
    alphas = []
    betas = []
    delta_sum = 0.0
    delta_sq = 0.0
    delta_n = 0
    for x in LOCAL:
        value = phi[x]
        live = []
        sd = 0.0
        for di, d in enumerate(DS):
            y = add(x, d)
            if y not in phi:
                continue
            dd = value - phi[y]
            if dd > 0.0:
                live.append((di, dd))
                sd += dd
                delta_sum += dd
                delta_sq += dd * dd
                delta_n += 1
        if sd <= 0.0:
            continue
        ps = sum(max(prev.get((x, di), 0.0), 0.0) for di, _ in live)
        for di, dd in live:
            alphas.append(dd / sd)
            betas.append(max(prev.get((x, di), 0.0), 0.0) / ps if ps > 0.0 else 0.0)
    aa = np.asarray(alphas, float)
    bb = np.asarray(betas, float)
    return {
        "alpha_mean": float(aa.mean()) if aa.size else 0.0,
        "alpha_std": float(aa.std()) if aa.size else 0.0,
        "beta_mean": float(bb.mean()) if bb.size else 0.0,
        "beta_std": float(bb.std()) if bb.size else 0.0,
        "positive_delta_sum": float(delta_sum),
        "positive_delta_rms": float(math.sqrt(delta_sq / max(delta_n, 1))),
        "active_local_edges": int(delta_n),
    }


def local_flow_state(flow):
    vals = []
    j4 = 0.0
    j3 = 0.0
    for (c, di), v in flow.items():
        if c not in LOCAL_SET or v <= 0.0:
            continue
        vals.append(v)
        if di >= 6:
            j4 += v
        else:
            j3 += v
    a = np.asarray(vals, float)
    return {
        "j_sum": float(a.sum()) if a.size else 0.0,
        "j_mean": float(a.mean()) if a.size else 0.0,
        "j_std": float(a.std()) if a.size else 0.0,
        "j3_sum": float(j3),
        "j4_sum": float(j4),
    }


def m3_moment(phi):
    q = 0j
    weight = 0.0
    for c in LOCAL:
        x, y, z, w = c
        if x == 0 and y == 0:
            continue
        excess = phi[c] - BACKGROUND
        if excess <= 0.0:
            continue
        ang = math.atan2(y, x)
        q += excess * complex(math.cos(M * ang), math.sin(M * ang))
        weight += excess
    amp = abs(q) / (weight + 1e-30)
    phase = (math.atan2(q.imag, q.real) / M if abs(q) else 0.0) % (2.0 * math.pi / M)
    return {
        "amplitude": float(amp),
        "phase_deg_mod_120": float(math.degrees(phase)),
        "positive_excess_weight": float(weight),
    }


def unwrap120(degs):
    out = []
    for d in degs:
        if not out:
            out.append(float(d))
            continue
        candidates = [d + 120.0 * k for k in range(-20, 21)]
        out.append(float(min(candidates, key=lambda x: abs(x - out[-1]))))
    return out


def pearson(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if len(a) < 2 or len(a) != len(b) or np.std(a) == 0.0 or np.std(b) == 0.0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def projection_amplitude(values, cycles_per_frame):
    x = np.asarray(values, float)
    if x.size == 0:
        return 0.0
    x = x - x.mean()
    n = np.arange(x.size, dtype=float)
    z = np.exp(-2j * np.pi * cycles_per_frame * n)
    return float(2.0 * abs(np.dot(x, z)) / x.size)


def run_case(ratio: float, phase_on: bool):
    # Omega_phase = 30 deg/frame in signed longitudinal-flow phase.
    # For m-fold field, Omega_field = m * omega_orientation.
    # Therefore orientation step = ratio * 30 / m = ratio * 10 deg/frame for m=3.
    step_deg = ratio * 360.0 / FLOW_PERIOD / M
    name = f"ratio_{ratio:.2f}_{'phase' if phase_on else 'wave_only'}".replace(".", "p")
    cdir = OUT / name
    fdir = cdir / "flows"
    cdir.mkdir(parents=True, exist_ok=True)
    fdir.mkdir(parents=True, exist_ok=True)

    phi = initial_phi()
    prev = {}
    old_wave = {}
    phi_in = []
    phi_out = []
    rows = []
    last_post_local = None
    births = 0

    for frame in range(FRAMES):
        theta = math.radians(step_deg * frame)
        new_wave = wave_component(theta)
        apply_component(phi, old_wave, new_wave)
        old_wave = new_wave

        op_prev, signed_drive, injected_edges, drive_dir = impose_longitudinal_flow(prev, frame, phase_on)
        pin = full_phi(phi)
        lpre = local_phi(phi)
        edge_pre = local_edge_state(phi, op_prev)
        pre_m3 = m3_moment(phi)
        save_flow(fdir / f"{frame:02d}_input.npz", op_prev)
        before = float(sum(phi.values()))

        phi, nxt, diag = operator_step(phi, op_prev, dimension=DIM)
        pout = full_phi(phi)
        lpost = local_phi(phi)
        post_m3 = m3_moment(phi)
        flow_post = local_flow_state(nxt)
        save_flow(fdir / f"{frame:02d}_output.npz", nxt)

        operator_delta = lpost - lpre
        temporal_delta = np.zeros_like(lpost) if last_post_local is None else (lpost - last_post_local)
        last_post_local = lpost.copy()
        aa = np.asarray(diag.alpha_samples, float)
        bb = np.asarray(diag.beta_samples, float)

        row = {
            "frame": frame,
            "ratio_field_over_phase_imposed": ratio,
            "orientation_step_deg_imposed": step_deg,
            "wave_theta_deg_imposed": step_deg * frame,
            "phase_drive_signed": float(signed_drive),
            "phase_drive_abs": float(abs(signed_drive)),
            "phase_drive_direction": drive_dir,
            "phase_drive_edges": int(injected_edges),
            "local_phi_mean_pre": float(lpre.mean()),
            "local_phi_std_pre": float(lpre.std()),
            "local_phi_mean_post": float(lpost.mean()),
            "local_phi_std_post": float(lpost.std()),
            "local_operator_delta_phi_rms": float(np.sqrt(np.mean(operator_delta * operator_delta))),
            "local_temporal_delta_phi_rms": float(np.sqrt(np.mean(temporal_delta * temporal_delta))),
            "m3_pre": pre_m3,
            "m3_post": post_m3,
            **edge_pre,
            **flow_post,
            "global_alpha_mean": float(aa.mean()) if aa.size else 0.0,
            "global_beta_mean": float(bb.mean()) if bb.size else 0.0,
            "live_transfer": float(diag.live_transfer),
            "births": int(diag.births),
            "conservation_error": float(sum(phi.values()) - before),
        }
        rows.append(row)
        births += int(diag.births)
        phi_in.append(pin)
        phi_out.append(pout)
        prev = nxt

    phases = unwrap120([r["m3_post"]["phase_deg_mod_120"] for r in rows])
    for r, u in zip(rows, phases):
        r["m3_post"]["phase_deg_unwrapped_analysis"] = u
    t = np.arange(FRAMES, dtype=float)
    orientation_slope = float(np.polyfit(t, np.asarray(phases), 1)[0])
    field_slope = M * orientation_slope
    phase_slope = 360.0 / FLOW_PERIOD
    measured_ratio = field_slope / phase_slope

    np.savez_compressed(
        cdir / "phi_history.npz",
        coords=np.asarray(DOMAIN, dtype=np.int16),
        local_coords=np.asarray(LOCAL, dtype=np.int16),
        phi_input=np.stack(phi_in),
        phi_output=np.stack(phi_out),
    )
    (cdir / "frames.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    series_keys = [
        "local_phi_std_post", "local_operator_delta_phi_rms", "local_temporal_delta_phi_rms",
        "alpha_mean", "alpha_std", "beta_mean", "beta_std", "j_sum", "j3_sum", "j4_sum",
    ]
    spectra = {}
    f_phase = 1.0 / FLOW_PERIOD
    f_field = ratio / FLOW_PERIOD
    for key in series_keys:
        values = [float(r[key]) for r in rows]
        spectra[key] = {
            "at_phase_f": projection_amplitude(values, f_phase),
            "at_2phase_f": projection_amplitude(values, 2.0 * f_phase),
            "at_imposed_field_f": projection_amplitude(values, f_field),
        }

    signed_drive = [r["phase_drive_signed"] for r in rows]
    abs_drive = [r["phase_drive_abs"] for r in rows]
    correlations = {}
    for key in series_keys:
        vals = [r[key] for r in rows]
        correlations[key] = {
            "with_signed_phase_drive": pearson(vals, signed_drive),
            "with_abs_phase_drive": pearson(vals, abs_drive),
        }

    return {
        "name": name,
        "ratio_field_over_phase_imposed": ratio,
        "phase_on": phase_on,
        "orientation_step_deg_imposed": step_deg,
        "phase_angular_frequency_deg_per_frame": phase_slope,
        "field_angular_frequency_deg_per_frame_imposed": ratio * phase_slope,
        "orientation_slope_deg_per_frame_measured": orientation_slope,
        "field_angular_frequency_deg_per_frame_measured": field_slope,
        "ratio_field_over_phase_measured": measured_ratio,
        "m3_amplitude_mean": float(np.mean([r["m3_post"]["amplitude"] for r in rows])),
        "local_phi_std_mean": float(np.mean([r["local_phi_std_post"] for r in rows])),
        "operator_delta_phi_rms_mean": float(np.mean([r["local_operator_delta_phi_rms"] for r in rows])),
        "temporal_delta_phi_rms_mean": float(np.mean([r["local_temporal_delta_phi_rms"] for r in rows[1:]])),
        "alpha_mean_over_frames": float(np.mean([r["alpha_mean"] for r in rows])),
        "beta_mean_over_frames": float(np.mean([r["beta_mean"] for r in rows])),
        "j_sum_mean": float(np.mean([r["j_sum"] for r in rows])),
        "spectral_projection": spectra,
        "correlations": correlations,
        "births_total": births,
        "max_abs_conservation_error": float(max(abs(r["conservation_error"]) for r in rows)),
        "raw": {"phi_history": f"{name}/phi_history.npz", "flows": f"{name}/flows/", "frames": f"{name}/frames.json"},
    }


def coupling_delta(phase_case, base_case):
    scalars = [
        "m3_amplitude_mean", "local_phi_std_mean", "operator_delta_phi_rms_mean",
        "temporal_delta_phi_rms_mean", "alpha_mean_over_frames", "beta_mean_over_frames", "j_sum_mean",
    ]
    return {k: float(phase_case[k] - base_case[k]) for k in scalars}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    guard = WAVE_SUPPORT_L1 + FRAMES < DOMAIN_L1
    if not guard:
        raise RuntimeError("wave disturbance can reach the fixed-domain edge")

    all_cases = {}
    comparison = []
    for ratio in RATIOS:
        base = run_case(ratio, False)
        phase = run_case(ratio, True)
        all_cases[base["name"]] = base
        all_cases[phase["name"]] = phase
        comparison.append({
            "ratio_field_over_phase": ratio,
            "wave_only": base["name"],
            "with_phase": phase["name"],
            "phase_minus_wave_only": coupling_delta(phase, base),
            "measured_ratio_wave_only": base["ratio_field_over_phase_measured"],
            "measured_ratio_with_phase": phase["ratio_field_over_phase_measured"],
        })

    summary = {
        "experiment": "phase_memory_frequency_sweep",
        "status": "synthetic forced-frequency coupling sweep; no resonance, locking, time, mass, charge, EM, damping or stability law inserted",
        "operator": "unchanged scanner.self_reflexive_operator.operator_step",
        "question": "When the imposed m=3 wave-pattern frequency is swept relative to the fixed fourth-axis previous-flow phase frequency, how do local phi, delta-phi, alpha, beta and J respond, compared with identical wave-only controls?",
        "definitions": {
            "phase_frequency": "signed +/-w previous-flow drive with period 12 frames; Omega_phase = 30 deg/frame",
            "field_frequency": "m times the imposed orientation angular frequency; ratios are Omega_field/Omega_phase",
            "local_field": "all lattice points with L1 norm <= 6",
            "coupling_delta": "with-phase result minus matched wave-only result at the same imposed field frequency",
            "spectral_projection": "analysis-only complex projection at phase, 2x phase and imposed field frequencies; never fed back into the operator",
            "important_limit": "the wave is externally advanced every frame, so phase tracking of the wave itself is not evidence of autonomous locking; only matched phase-on minus wave-only operator response can indicate frequency-dependent coupling in this synthetic protocol",
        },
        "parameters": {
            "dimension": DIM,
            "m": M,
            "ratios_field_over_phase": RATIOS,
            "flow_period_frames": FLOW_PERIOD,
            "flow_amplitude": FLOW_AMP,
            "frames": FRAMES,
            "domain_l1": DOMAIN_L1,
            "domain_points": len(DOMAIN),
            "measure_l1": MEASURE_L1,
            "wave_support_l1": WAVE_SUPPORT_L1,
            "boundary_unreachable_by_wave": guard,
        },
        "cases": all_cases,
        "matched_comparison": comparison,
        "journal": {
            "full_phi": "every case stores complete fixed-domain phi_input and phi_output arrays for every frame",
            "raw_flow": "every case stores sparse previous-flow input and next-flow output for every frame",
            "frame_log": "every case stores local phi, delta-phi, alpha, beta, J, phase drive and m3 phase/amplitude per frame",
            "summary": "this file contains all parameters, derived frequency readouts and matched phase-on minus wave-only comparisons",
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({
        "experiment": summary["experiment"],
        "parameters": summary["parameters"],
        "matched_comparison": comparison,
        "case_compact": {k: {
            "measured_ratio": v["ratio_field_over_phase_measured"],
            "m3_amp": v["m3_amplitude_mean"],
            "phi_std": v["local_phi_std_mean"],
            "operator_dphi": v["operator_delta_phi_rms_mean"],
            "temporal_dphi": v["temporal_delta_phi_rms_mean"],
            "alpha": v["alpha_mean_over_frames"],
            "beta": v["beta_mean_over_frames"],
            "j_sum": v["j_sum_mean"],
            "births": v["births_total"],
        } for k, v in all_cases.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
