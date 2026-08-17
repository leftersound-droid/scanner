from __future__ import annotations

import json
import math
import sys
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from scanner.analyzers import direct_analysis
from scanner.models import Problem
from scanner.self_reflexive_operator import directions, operator_step

OUT_DIR = ROOT / "run-data" / "cross_domain" / "phase_memory_vortex_graph"
SUMMARY_PATH = OUT_DIR / "summary.json"

DIMENSION = 4
HALF_WIDTH = 11                     # 23^4 fixed, fully pre-existing substrate
BACKGROUND = 100.0
FRAMES = 6
PHASE_AMPLITUDE = 0.01              # artificial, no physical calibration
VORTEX_PEAK_EXCESS = 10.0           # artificial, no physical calibration
VORTEX_RADIUS = 2.0
VORTEX_SIGMA = 0.55
VORTEX_MARKER = 0.35                # makes one-axis rotation observable
MEASURE_HALF_WIDTH = 4              # 9^4 interior reconstruction region
MAX_DERIVATIVE_ORDER = 3

# Each case is an imposed artificial protocol.  Frequencies are expressed as
# periods in operator frames, not as physical frequencies.
CASES = [
    {"name": "phase_only_slow", "phase_period": 6, "vortex_period": None},
    {"name": "vortex_only_slow", "phase_period": None, "vortex_period": 6},
    {"name": "coupled_ratio1_fast", "phase_period": 3, "vortex_period": 3},
    {"name": "coupled_ratio1_slow", "phase_period": 6, "vortex_period": 6},
    {"name": "coupled_ratio2", "phase_period": 6, "vortex_period": 3},
    {"name": "coupled_ratio_half", "phase_period": 3, "vortex_period": 6},
]


def coords_axis():
    return np.arange(-HALF_WIDTH, HALF_WIDTH + 1, dtype=np.int16)


def all_coords():
    r = range(-HALF_WIDTH, HALF_WIDTH + 1)
    return [tuple(c) for c in product(r, repeat=4)]


def initial_substrate():
    return {c: BACKGROUND for c in all_coords()}


def dense_phi(phi):
    n = 2 * HALF_WIDTH + 1
    out = np.empty((n, n, n, n), dtype=np.float64)
    for c, v in phi.items():
        idx = tuple(int(x + HALF_WIDTH) for x in c)
        out[idx] = v
    return out


def phase_value(frame, period):
    if period is None:
        return 0.0, 0.0
    theta = 2.0 * math.pi * frame / float(period)
    return PHASE_AMPLITUDE * math.sin(theta), theta


def vortex_component(theta):
    """Closed rotating potential-ring template embedded in the 4D lattice.

    This is an imposed training object, not an emergent particle and not a
    physical vortex law.  Rotation is in the x-y plane; z and w give the
    transverse thickness.  The cosine marker only makes orientation readable.
    """
    comp = {}
    support = 4
    for c in product(range(-support, support + 1), repeat=4):
        x, y, z, w = (float(v) for v in c)
        rho = math.sqrt(x * x + y * y)
        ring_dist2 = (rho - VORTEX_RADIUS) ** 2 + z * z + w * w
        base = VORTEX_PEAK_EXCESS * math.exp(-0.5 * ring_dist2 / (VORTEX_SIGMA ** 2))
        if base < 1e-10:
            continue
        angle = math.atan2(y, x)
        marker = 1.0 + VORTEX_MARKER * math.cos(angle - theta)
        value = base * marker
        if value > 1e-10:
            comp[tuple(int(v) for v in c)] = value
    return comp


def component_delta(old, new):
    keys = set(old) | set(new)
    return {c: new.get(c, 0.0) - old.get(c, 0.0) for c in keys}


def apply_external_delta(phi, delta):
    signed = 0.0
    absolute = 0.0
    for c, dv in delta.items():
        if dv == 0.0:
            continue
        phi[c] += dv
        signed += dv
        absolute += abs(dv)
    return signed, absolute


def apply_uniform_delta(phi, dv):
    if dv == 0.0:
        return 0.0, 0.0
    n = len(phi)
    for c in phi:
        phi[c] += dv
    return float(dv * n), float(abs(dv) * n)


def edge_fields(phi, previous_flow):
    """Raw non-zero local alpha/beta values before one operator frame."""
    ds = directions(DIMENSION)
    rows = []
    for x, value in phi.items():
        live = []
        sum_delta = 0.0
        for di, d in enumerate(ds):
            y = (x[0] + d[0], x[1] + d[1], x[2] + d[2], x[3] + d[3])
            if y not in phi:
                continue
            delta = value - phi[y]
            if delta > 0.0:
                live.append((di, delta))
                sum_delta += delta
        if not live or sum_delta <= 0.0:
            continue
        prev_sum = sum(max(previous_flow.get((x, di), 0.0), 0.0) for di, _ in live)
        for di, delta in live:
            alpha = delta / sum_delta
            beta = max(previous_flow.get((x, di), 0.0), 0.0) / prev_sum if prev_sum > 0.0 else 0.0
            rows.append((x, di, alpha, beta))
    return rows


def save_edge_frame(path, raw_edges, next_flow):
    if not raw_edges:
        np.savez_compressed(
            path,
            coord=np.empty((0, 4), dtype=np.int16),
            direction=np.empty((0,), dtype=np.uint8),
            alpha=np.empty((0,), dtype=np.float64),
            beta=np.empty((0,), dtype=np.float64),
            j_out=np.empty((0,), dtype=np.float64),
        )
        return
    coord = np.asarray([r[0] for r in raw_edges], dtype=np.int16)
    direction = np.asarray([r[1] for r in raw_edges], dtype=np.uint8)
    alpha = np.asarray([r[2] for r in raw_edges], dtype=np.float64)
    beta = np.asarray([r[3] for r in raw_edges], dtype=np.float64)
    j_out = np.asarray([next_flow.get((tuple(int(v) for v in r[0]), int(r[1])), 0.0) for r in raw_edges], dtype=np.float64)
    np.savez_compressed(path, coord=coord, direction=direction, alpha=alpha, beta=beta, j_out=j_out)


def interior_series(history):
    lo = HALF_WIDTH - MEASURE_HALF_WIDTH
    hi = HALF_WIDTH + MEASURE_HALF_WIDTH + 1
    return history[:, lo:hi, lo:hi, lo:hi, lo:hi]


def derivative_reconstruction(history):
    """Diagnostic only: how much temporal derivative depth helps reconstruct phi[t+1].

    A simple affine least-squares map is fit across interior lattice points.
    Train/test split is spatial and deterministic.  It is not inserted into
    the physical operator and is not used to alter any frame.
    """
    h = interior_series(history)
    t_count = h.shape[0]
    spatial_shape = h.shape[1:]
    flat = h.reshape(t_count, -1)
    indices = np.arange(flat.shape[1])
    train_mask = (indices % 5) != 0
    test_mask = ~train_mask
    out = {}

    diffs = [flat]
    for k in range(1, MAX_DERIVATIVE_ORDER + 1):
        d = np.diff(diffs[-1], axis=0)
        diffs.append(d)

    for k in range(MAX_DERIVATIVE_ORDER + 1):
        # For order k, earliest usable current frame is k.
        feature_blocks = []
        targets = []
        for t in range(k, t_count - 1):
            blocks = [flat[t]]
            for order in range(1, k + 1):
                # np.diff^order has its time index shifted by order.
                blocks.append(diffs[order][t - order])
            feature_blocks.append(np.stack(blocks, axis=1))
            targets.append(flat[t + 1])
        if not feature_blocks:
            out[str(k)] = {"available": False}
            continue
        X = np.concatenate(feature_blocks, axis=0)
        y = np.concatenate(targets, axis=0)
        repeated_train = np.tile(train_mask, len(feature_blocks))
        repeated_test = np.tile(test_mask, len(feature_blocks))
        X_train = X[repeated_train]
        y_train = y[repeated_train]
        X_test = X[repeated_test]
        y_test = y[repeated_test]
        A_train = np.column_stack([np.ones(len(X_train)), X_train])
        A_test = np.column_stack([np.ones(len(X_test)), X_test])
        coef, residuals, rank, singular = np.linalg.lstsq(A_train, y_train, rcond=None)
        pred = A_test @ coef
        rmse = float(np.sqrt(np.mean((pred - y_test) ** 2)))
        denom = float(np.std(y_test))
        nrmse = rmse / denom if denom > 0.0 else 0.0
        out[str(k)] = {
            "available": True,
            "features": ["phi"] + [f"d{j}_phi" for j in range(1, k + 1)],
            "coef_affine": [float(v) for v in coef],
            "rank": int(rank),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "rmse": rmse,
            "normalized_rmse": nrmse,
        }
    return out


def frame_rows_to_table(frame_rows):
    keys = list(frame_rows[0])
    return {k: [float(r[k]) for r in frame_rows] for k in keys}


def pearson(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) < 2 or len(a) != len(b) or np.std(a) == 0.0 or np.std(b) == 0.0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def run_case(spec):
    name = spec["name"]
    case_dir = OUT_DIR / name
    edge_dir = case_dir / "edges"
    case_dir.mkdir(parents=True, exist_ok=True)
    edge_dir.mkdir(parents=True, exist_ok=True)

    phi = initial_substrate()
    previous_flow = {}
    old_phase = 0.0
    old_vortex = {}

    inputs = []
    outputs = []
    rows = []

    phase_period = spec["phase_period"]
    vortex_period = spec["vortex_period"]
    ratio = None
    if phase_period is not None and vortex_period is not None:
        ratio = float(phase_period) / float(vortex_period)  # omega_vortex / omega_phase

    for frame in range(FRAMES):
        phase, phase_theta = phase_value(frame, phase_period)
        phase_signed, phase_abs = apply_uniform_delta(phi, phase - old_phase)
        old_phase = phase

        if vortex_period is None:
            vortex_theta = 0.0
            new_vortex = {}
        else:
            vortex_theta = 2.0 * math.pi * frame / float(vortex_period)
            new_vortex = vortex_component(vortex_theta)
        vortex_signed, vortex_abs = apply_external_delta(phi, component_delta(old_vortex, new_vortex))
        old_vortex = new_vortex

        phi_in = dense_phi(phi)
        raw_edges = edge_fields(phi, previous_flow)
        total_before = float(sum(phi.values()))
        phi, next_flow, diag = operator_step(phi, previous_flow, dimension=DIMENSION)
        phi_out = dense_phi(phi)
        save_edge_frame(edge_dir / f"frame_{frame:02d}.npz", raw_edges, next_flow)

        aa = np.asarray(diag.alpha_samples, dtype=float)
        bb = np.asarray(diag.beta_samples, dtype=float)
        j_values = np.asarray(list(next_flow.values()), dtype=float)

        center = HALF_WIDTH
        lo = center - MEASURE_HALF_WIDTH
        hi = center + MEASURE_HALF_WIDTH + 1
        interior = phi_out[lo:hi, lo:hi, lo:hi, lo:hi]
        environment_deviation = interior - (BACKGROUND + phase)

        row = {
            "frame": frame,
            "phase_theta": phase_theta,
            "phase_value": phase,
            "phase_period": float(phase_period or 0),
            "vortex_theta": vortex_theta,
            "vortex_period": float(vortex_period or 0),
            "frequency_ratio_vortex_over_phase": float(ratio or 0.0),
            "phase_external_signed": phase_signed,
            "phase_external_abs": phase_abs,
            "vortex_external_signed": vortex_signed,
            "vortex_external_abs": vortex_abs,
            "operator_live_transfer": float(diag.live_transfer),
            "alpha_mean": float(aa.mean()) if aa.size else 0.0,
            "alpha_std": float(aa.std()) if aa.size else 0.0,
            "beta_mean": float(bb.mean()) if bb.size else 0.0,
            "beta_std": float(bb.std()) if bb.size else 0.0,
            "j_mean_nonzero": float(j_values.mean()) if j_values.size else 0.0,
            "j_std_nonzero": float(j_values.std()) if j_values.size else 0.0,
            "interior_deviation_mean": float(environment_deviation.mean()),
            "interior_deviation_std": float(environment_deviation.std()),
            "total_before_operator": total_before,
            "total_after_operator": float(sum(phi.values())),
            "operator_conservation_error": float(sum(phi.values()) - total_before),
            "births": float(diag.births),
        }
        rows.append(row)
        inputs.append(phi_in)
        outputs.append(phi_out)
        previous_flow = next_flow

    input_history = np.stack(inputs, axis=0)
    output_history = np.stack(outputs, axis=0)
    # State history for derivative reconstruction: first operator input then every output.
    state_history = np.concatenate([input_history[:1], output_history], axis=0)
    np.savez_compressed(
        case_dir / "matrix_history.npz",
        axis=coords_axis(),
        phi_input=input_history,
        phi_output=output_history,
        state_history=state_history,
    )

    table = frame_rows_to_table(rows)
    problem = Problem(
        title=f"Phase-memory vortex graph: {name}",
        description="Artificial phase-field / imposed rotating closed-potential-ring protocol; graph scan only.",
        domain="self_reflexive_operator",
        tags=["phase-memory", "vortex-template", "derivative-depth", name],
        payload={"table": table},
        constraints={
            "phase_field_is_artificial_input": True,
            "vortex_rotation_is_artificial_training_input": True,
            "no_physical_frequency_calibration": True,
            "no_mass_law": True,
            "no_time_law": True,
            "no_gravity_law": True,
            "no_stability_rule": True,
            "fixed_preexisting_grid": True,
        },
    )
    scan = direct_analysis(problem)
    reconstruction = derivative_reconstruction(state_history)

    result = {
        "case": spec,
        "frequency_ratio_vortex_over_phase": ratio,
        "frames": FRAMES,
        "rows": rows,
        "scanner_relation_scan": scan,
        "derivative_reconstruction_phi": reconstruction,
        "raw_files": {
            "matrix_history": "matrix_history.npz",
            "edge_frames": "edges/frame_XX.npz",
        },
        "checks": {
            "births_total": int(sum(r["births"] for r in rows)),
            "max_abs_operator_conservation_error": float(max(abs(r["operator_conservation_error"]) for r in rows)),
        },
    }
    (case_dir / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def relation_signature(case):
    rows = case["rows"]
    keys = ["operator_live_transfer", "alpha_mean", "beta_mean", "interior_deviation_std"]
    sig = []
    for k in keys:
        y = [r[k] for r in rows]
        phase_sin = [math.sin(r["phase_theta"]) for r in rows]
        phase_cos = [math.cos(r["phase_theta"]) for r in rows]
        vortex_sin = [math.sin(r["vortex_theta"]) for r in rows]
        vortex_cos = [math.cos(r["vortex_theta"]) for r in rows]
        for x in (phase_sin, phase_cos, vortex_sin, vortex_cos):
            v = pearson(x, y)
            sig.append(0.0 if v is None else v)
    return np.asarray(sig, dtype=float)


def cosine(a, b):
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        return None
    return float(np.dot(a, b) / (na * nb))


def write_manifest(results, comparisons):
    manifest = {
        "experiment": "phase_memory_vortex_graph",
        "purpose": [
            "Measure graph response of an imposed closed rotating 4D-lattice potential-ring inside an artificial homogeneous periodic scalar phase background.",
            "Test whether keeping omega_vortex/omega_phase fixed while changing absolute frame periods preserves the measured relation signature.",
            "Measure how much 0th/1st/2nd/3rd discrete temporal derivative depth helps reconstruct the next local scalar state.",
        ],
        "non_claims": [
            "The artificial phase field is not claimed to be emergent physical phase space.",
            "The rotating closed ring is not claimed to be an emergent particle.",
            "No measured derivative order is identified with mass or local time in this experiment.",
            "No GR, Compton, gravity, charge, inertia or physical clock relation is inserted.",
        ],
        "fixed_grid": {
            "dimension": DIMENSION,
            "shape": [2 * HALF_WIDTH + 1] * DIMENSION,
            "coordinate_axis": [-HALF_WIDTH, HALF_WIDTH],
            "background": BACKGROUND,
            "all_points_preexist": True,
            "periodic_boundary": False,
            "reflecting_boundary": False,
            "edge_damping": False,
            "frames": FRAMES,
            "vortex_template_coordinate_support_bound": 4,
            "distance_from_template_bound_to_edge": HALF_WIDTH - 4,
            "boundary_causality_check": "FRAMES < distance_from_template_bound_to_edge; nearest-neighbour operator propagates at most one edge per frame.",
            "boundary_causally_unreachable": FRAMES < (HALF_WIDTH - 4),
        },
        "artificial_inputs": {
            "phase": {
                "form": "uniform additive scalar component A*sin(theta) applied by frame-to-frame delta",
                "amplitude": PHASE_AMPLITUDE,
                "periods_tested_frames": sorted({c["phase_period"] for c in CASES if c["phase_period"] is not None}),
            },
            "vortex_template": {
                "form": "closed Gaussian potential ring in x-y with z,w thickness and a rotating cosine orientation marker",
                "peak_excess": VORTEX_PEAK_EXCESS,
                "radius": VORTEX_RADIUS,
                "sigma": VORTEX_SIGMA,
                "marker_fraction": VORTEX_MARKER,
                "periods_tested_frames": sorted({c["vortex_period"] for c in CASES if c["vortex_period"] is not None}),
                "forcing": "frame-to-frame template delta; no stability or force law added",
            },
        },
        "raw_data_definition": {
            "case/matrix_history.npz": {
                "axis": "integer coordinate labels",
                "phi_input": "complete fixed-grid scalar matrix immediately before each operator frame",
                "phi_output": "complete fixed-grid scalar matrix immediately after each operator frame",
                "state_history": "phi_input[0] followed by every phi_output; used for derivative-depth diagnostic",
                "dtype": "float64",
            },
            "case/edges/frame_XX.npz": {
                "coord": "source lattice coordinate for every positive-delta live edge before operator frame",
                "direction": "nearest-neighbour direction index from scanner.self_reflexive_operator.directions",
                "alpha": "raw Delta_ij / sum Delta_ik",
                "beta": "raw previous-flow fraction J_prev_ij / sum J_prev_ik",
                "j_out": "actual operator output flow on the same edge; absent edges are exactly zero",
            },
            "case/result.json": "framewise scalar readouts, Scanner relation scan, derivative-depth reconstruction diagnostics and checks",
        },
        "derivative_depth_definition": {
            "d1_phi": "phi[t]-phi[t-1]",
            "d2_phi": "d1[t]-d1[t-1]",
            "d3_phi": "d2[t]-d2[t-1]",
            "test": "affine least-squares next-phi reconstruction on a 9^4 interior volume; deterministic spatial train/test split",
            "interpretation_limit": "Lower reconstruction error at order k means that derivative depth contains predictive information in this artificial protocol only; it does not establish a physical k-th-order law.",
        },
        "cases": CASES,
        "comparisons": comparisons,
        "operator": "src/scanner/self_reflexive_operator.py unchanged",
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = [run_case(c) for c in CASES]
    by_name = {r["case"]["name"]: r for r in results}

    fast = relation_signature(by_name["coupled_ratio1_fast"])
    slow = relation_signature(by_name["coupled_ratio1_slow"])
    ratio2 = relation_signature(by_name["coupled_ratio2"])
    ratio_half = relation_signature(by_name["coupled_ratio_half"])
    comparisons = {
        "same_ratio_absolute_period_change": {
            "cases": ["coupled_ratio1_fast", "coupled_ratio1_slow"],
            "signature_cosine": cosine(fast, slow),
            "question": "Does the graph signature remain similar when both absolute periods are doubled while omega_vortex/omega_phase remains 1?",
        },
        "different_ratio_controls": {
            "ratio1_slow_vs_ratio2": cosine(slow, ratio2),
            "ratio1_fast_vs_ratio_half": cosine(fast, ratio_half),
        },
    }
    write_manifest(results, comparisons)

    summary = {
        "experiment": "phase_memory_vortex_graph",
        "cases": {
            r["case"]["name"]: {
                "frequency_ratio_vortex_over_phase": r["frequency_ratio_vortex_over_phase"],
                "births_total": r["checks"]["births_total"],
                "max_abs_operator_conservation_error": r["checks"]["max_abs_operator_conservation_error"],
                "derivative_reconstruction_phi": r["derivative_reconstruction_phi"],
            }
            for r in results
        },
        "comparisons": comparisons,
        "raw_output_dir": str(OUT_DIR.relative_to(ROOT)),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
