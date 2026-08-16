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
from scanner.self_reflexive_operator import operator_step

OUT_DIR = ROOT / "run-data" / "cross_domain" / "probe_particle_m_binding"
RESULT_OUT = OUT_DIR / "result.json"
MANIFEST_OUT = OUT_DIR / "manifest.json"

DIMENSION = 4
HALF_WIDTH = 12                  # fixed 25^4 lattice, all points exist from frame 0
BACKGROUND = 1.0
TOTAL_OBJECT_EXCESS = 120.0
SUPPORT_R = 1.8
ASYM = 0.35
FRAMES_PER_STATE = 1            # 8 total frames: deliberately shorter than guard distance
MEASUREMENT_RADIUS = 4.5

CENTER_PROTOCOL = [
    (0, 0, 0, 0),
    (0, 0, 0, 0),
    (1, 0, 0, 0),
    (1, 0, 0, 0),
    (0, 0, 0, 0),
    (0, 0, 0, 0),
    (-1, 0, 0, 0),
    (-1, 0, 0, 0),
]

FOCUS = [
    "substrate_response",
    "motion_response",
    "odd_response",
    "alpha_mean",
    "beta_mean",
    "live_transfer",
]

AXIS = np.arange(-HALF_WIDTH, HALF_WIDTH + 1, dtype=np.int16)
SHAPE = (len(AXIS),) * DIMENSION
MAX_CENTER_ABS = max(max(abs(v) for v in c) for c in CENTER_PROTOCOL)
# Conservative integer support bound. A synchronous nearest-neighbour operator
# propagates information by at most one lattice edge per frame.
OBJECT_BOUND = MAX_CENTER_ABS + math.ceil(SUPPORT_R)
GUARD_DISTANCE = HALF_WIDTH - OBJECT_BOUND
TOTAL_FRAMES = len(CENTER_PROTOCOL) * FRAMES_PER_STATE


def initial_substrate():
    r = range(-HALF_WIDTH, HALF_WIDTH + 1)
    return {tuple(c): BACKGROUND for c in product(r, repeat=DIMENSION)}


def object_profile(kind, center):
    lo = math.floor(-SUPPORT_R) - 1
    hi = math.ceil(SUPPORT_R) + 1
    raw = []
    for off in product(range(lo, hi + 1), repeat=DIMENSION):
        r2 = sum(float(v * v) for v in off)
        if math.sqrt(r2) > SUPPORT_R:
            continue
        base = math.exp(-0.5 * r2 / (0.95 ** 2))
        x = float(off[0])
        if kind == "symmetric":
            mod = 1.0
        elif kind == "asymmetric":
            mod = 1.0 + ASYM * x / SUPPORT_R
        else:
            raise ValueError(kind)
        val = max(base * mod, 0.0)
        if val > 0.0:
            coord = tuple(int(off[i] + center[i]) for i in range(DIMENSION))
            raw.append((coord, val))
    scale = TOTAL_OBJECT_EXCESS / sum(v for _, v in raw)
    return {c: v * scale for c, v in raw}


def environmental_moments(phi, object_cells, center, motion):
    vals = []
    odd_x_num = 0.0
    odd_x_den = 0.0
    motion_num = 0.0
    motion_den = 0.0
    motion_norm = math.sqrt(sum(float(v * v) for v in motion))

    for c, value in phi.items():
        if c in object_cells:
            continue
        rel = tuple(float(c[i] - center[i]) for i in range(DIMENSION))
        r = math.sqrt(sum(v * v for v in rel))
        if r <= SUPPORT_R or r > MEASUREMENT_RADIUS:
            continue
        excess = value - BACKGROUND
        vals.append(excess)
        odd_x_num += excess * rel[0]
        odd_x_den += abs(excess) * (abs(rel[0]) + 1e-15)
        if motion_norm > 0.0:
            proj = sum(rel[i] * float(motion[i]) for i in range(DIMENSION)) / motion_norm
            motion_num += excess * proj
            motion_den += abs(excess) * (abs(proj) + 1e-15)

    a = np.asarray(vals, dtype=float)
    substrate_response = float(np.mean(np.abs(a))) if a.size else 0.0
    environment_mean = float(np.mean(a)) if a.size else 0.0
    environment_std = float(np.std(a)) if a.size else 0.0
    odd_response = float(odd_x_num / odd_x_den) if odd_x_den > 0.0 else 0.0
    motion_response = float(motion_num / motion_den) if motion_den > 0.0 else 0.0
    return substrate_response, environment_mean, environment_std, odd_response, motion_response


def pearson(x, y):
    a = np.asarray(x, dtype=float)
    b = np.asarray(y, dtype=float)
    if a.size < 2 or b.size != a.size or np.std(a) == 0.0 or np.std(b) == 0.0:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def all_focus_relations(rows):
    out = []
    for i, a in enumerate(FOCUS):
        for b in FOCUS[i + 1:]:
            out.append({"a": a, "b": b, "pearson": pearson(rows[a], rows[b])})
    return out


def phi_to_dense(phi):
    arr = np.empty(SHAPE, dtype=np.float64)
    arr.fill(BACKGROUND)
    shift = HALF_WIDTH
    for c, value in phi.items():
        if all(-HALF_WIDTH <= c[i] <= HALF_WIDTH for i in range(DIMENSION)):
            arr[tuple(c[i] + shift for i in range(DIMENSION))] = value
    return arr


def save_matrix(path, phi):
    arr = phi_to_dense(phi)
    np.savez_compressed(path, phi=arr, axis=AXIS)


def write_jsonl(path, records):
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, sort_keys=True) + "\n")


def run_case(kind):
    case_dir = OUT_DIR / kind
    case_dir.mkdir(parents=True, exist_ok=True)

    phi = initial_substrate()
    previous_flow = {}
    initial_phi = dict(phi)

    rows = {
        "frame": [],
        "probe_center_x": [],
        "probe_motion_x": [],
        "substrate_response": [],
        "environment_mean": [],
        "environment_std": [],
        "motion_response": [],
        "odd_response": [],
        "live_transfer": [],
        "alpha_mean": [],
        "alpha_std": [],
        "beta_mean": [],
        "beta_std": [],
    }
    diagnostics = {"probe_reset": [], "birth_transfer": [], "births": []}
    raw_records = []

    previous_center = CENTER_PROTOCOL[0]
    frame = 0
    for state_center in CENTER_PROTOCOL:
        for _ in range(FRAMES_PER_STATE):
            center = state_center
            motion = tuple(center[i] - previous_center[i] for i in range(DIMENSION))
            obj = object_profile(kind, center)
            object_cells = set(obj)

            reset = 0.0
            for coord, excess in obj.items():
                target = BACKGROUND + excess
                reset += target - phi[coord]
                phi[coord] = target

            total_before_step = float(sum(phi.values()))
            phi, previous_flow, diag = operator_step(phi, previous_flow, dimension=DIMENSION)
            aa = np.asarray(diag.alpha_samples, dtype=float)
            bb = np.asarray(diag.beta_samples, dtype=float)
            substrate, env_mean, env_std, odd, motion_resp = environmental_moments(
                phi, object_cells, center, motion
            )

            values = {
                "frame": float(frame),
                "probe_center_x": float(center[0]),
                "probe_motion_x": float(motion[0]),
                "substrate_response": substrate,
                "environment_mean": env_mean,
                "environment_std": env_std,
                "motion_response": motion_resp,
                "odd_response": odd,
                "live_transfer": float(diag.live_transfer),
                "alpha_mean": float(aa.mean()) if aa.size else 0.0,
                "alpha_std": float(aa.std()) if aa.size else 0.0,
                "beta_mean": float(bb.mean()) if bb.size else 0.0,
                "beta_std": float(bb.std()) if bb.size else 0.0,
            }
            for key, value in values.items():
                rows[key].append(value)

            diagnostics["probe_reset"].append(float(reset))
            diagnostics["birth_transfer"].append(float(diag.birth_transfer))
            diagnostics["births"].append(float(diag.births))

            raw_records.append({
                "frame": frame,
                "center": list(center),
                "motion": list(motion),
                "probe_reset": float(reset),
                "total_before_step": total_before_step,
                "total_after_step": float(sum(phi.values())),
                "births": int(diag.births),
                "birth_transfer": float(diag.birth_transfer),
                "live_transfer": float(diag.live_transfer),
                "alpha_samples": [float(v) for v in diag.alpha_samples],
                "beta_samples": [float(v) for v in diag.beta_samples],
                "measurements": values,
            })

            previous_center = center
            frame += 1

    save_matrix(case_dir / "input_phi.npz", initial_phi)
    save_matrix(case_dir / "output_phi.npz", phi)
    write_jsonl(case_dir / "frames.jsonl", raw_records)

    problem = Problem(
        title=f"Probe particle m binding map: {kind}",
        description="Map raw framewise relations among substrate, motion, symmetry-sensitive response and operator observables.",
        domain="self_reflexive_operator",
        tags=["probe", "m-binding", kind, "fixed-grid", "neutral-measurement"],
        payload={"table": rows},
        constraints={
            "no_mass_formula": True,
            "no_charge_formula": True,
            "no_gravity_law": True,
            "no_electric_law": True,
            "no_relation_threshold": True,
            "fixed_grid": True,
            "boundary_must_be_causally_unreachable": True,
        },
    )
    scan = direct_analysis(problem)

    return {
        "kind": kind,
        "frames": frame,
        "table": rows,
        "diagnostics_not_scanner_input": diagnostics,
        "scanner_relation_scan": scan,
        "m_binding_focus_all_pairs": all_focus_relations(rows),
        "raw_files": {
            "input_matrix": f"{kind}/input_phi.npz",
            "output_matrix": f"{kind}/output_phi.npz",
            "frame_log": f"{kind}/frames.jsonl",
        },
        "summary": {
            "substrate_response_mean": float(np.mean(rows["substrate_response"])),
            "motion_response_rms": float(np.sqrt(np.mean(np.square(rows["motion_response"])))),
            "odd_response_rms": float(np.sqrt(np.mean(np.square(rows["odd_response"])))),
            "alpha_mean": float(np.mean(rows["alpha_mean"])),
            "beta_mean": float(np.mean(rows["beta_mean"])),
            "births_total": int(sum(diagnostics["births"])),
            "birth_transfer_total": float(sum(diagnostics["birth_transfer"])),
            "probe_reset_mean_diagnostic_only": float(np.mean(diagnostics["probe_reset"])),
        },
    }


def focus_lookup(case, a, b):
    for r in case["m_binding_focus_all_pairs"]:
        if {r["a"], r["b"]} == {a, b}:
            return r["pearson"]
    return None


def parameter_manifest():
    return {
        "schema_version": 1,
        "experiment": "probe_particle_m_binding_fixed_grid",
        "coordinate_convention": {
            "dimension": DIMENSION,
            "axis_values": [int(v) for v in AXIS],
            "matrix_shape": list(SHAPE),
            "matrix_index_rule": "matrix index k on every axis corresponds to coordinate axis_values[k]",
            "matrix_dtype": "float64",
            "stored_field": "phi scalar potential at every fixed R4 lattice point",
        },
        "parameters": {
            "HALF_WIDTH": {"value": HALF_WIDTH, "meaning": "coordinate extent is [-HALF_WIDTH,+HALF_WIDTH] on every R4 axis"},
            "BACKGROUND": {"value": BACKGROUND, "meaning": "initial phi of every fixed lattice point"},
            "TOTAL_OBJECT_EXCESS": {"value": TOTAL_OBJECT_EXCESS, "meaning": "sum of prescribed probe excess potential above background"},
            "SUPPORT_R": {"value": SUPPORT_R, "meaning": "Euclidean R4 radius of prescribed artificial probe support"},
            "ASYM": {"value": ASYM, "meaning": "x-directed internal profile asymmetry coefficient; used only in asymmetric probe"},
            "FRAMES_PER_STATE": {"value": FRAMES_PER_STATE, "meaning": "operator frames executed at each center-protocol state"},
            "MEASUREMENT_RADIUS": {"value": MEASUREMENT_RADIUS, "meaning": "outer radius of neutral environmental readout region"},
            "CENTER_PROTOCOL": {"value": [list(c) for c in CENTER_PROTOCOL], "meaning": "externally prescribed probe-center sequence, identical for both probe shapes"},
        },
        "field_columns": {
            "substrate_response": "mean absolute phi excess in measured environment outside probe",
            "environment_mean": "signed mean phi excess in measured environment outside probe",
            "environment_std": "standard deviation of phi excess in measured environment outside probe",
            "motion_response": "signed first moment projected on imposed center displacement; neutral motion-sensitive observable",
            "odd_response": "signed x-odd first moment; neutral symmetry-sensitive observable",
            "live_transfer": "total transfer between already-existing lattice points during operator frame",
            "alpha_mean/std": "mean/std of raw local alpha samples emitted by operator",
            "beta_mean/std": "mean/std of raw local beta samples emitted by operator",
            "probe_reset": "external potential required to restore prescribed artificial probe profile; diagnostic only",
            "births/birth_transfer": "point-birth diagnostics; expected to remain exactly zero on causally isolated fixed grid",
        },
        "boundary_guarantee": {
            "operator_locality": "nearest-neighbour synchronous; maximum propagation is one lattice edge per frame",
            "object_coordinate_bound": OBJECT_BOUND,
            "distance_from_object_bound_to_grid_edge": GUARD_DISTANCE,
            "executed_frames": TOTAL_FRAMES,
            "causally_unreachable": TOTAL_FRAMES < GUARD_DISTANCE,
            "condition": "executed_frames < distance_from_object_bound_to_grid_edge",
            "periodic_boundary": False,
            "reflecting_boundary": False,
            "edge_clipping_or_damping": False,
            "note": "No boundary rule is used. The experiment ends before any disturbance can reach the finite grid edge.",
        },
        "raw_file_format": {
            "input_phi.npz/output_phi.npz": "compressed NumPy archive containing phi[25,25,25,25] and axis[25]",
            "frames.jsonl": "one JSON record per operator frame containing raw alpha/beta samples, transfers, totals and measurements",
            "result.json": "Scanner relations plus summaries; derived data, not a replacement for raw files",
        },
        "interpretation_limit": "Neutral instrumentation only. No mass, charge, gravity, electric-field or higher-order m law is inserted by the measurement code.",
    }


def main():
    if not TOTAL_FRAMES < GUARD_DISTANCE:
        raise RuntimeError(
            f"Boundary isolation violated: frames={TOTAL_FRAMES}, guard_distance={GUARD_DISTANCE}. "
            "Increase fixed lattice or shorten protocol; do not run an edge-contaminated measurement."
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = parameter_manifest()
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    symmetric = run_case("symmetric")
    asymmetric = run_case("asymmetric")

    candidate_map = {}
    pairs = [
        ("substrate_response", "alpha_mean"),
        ("substrate_response", "beta_mean"),
        ("substrate_response", "live_transfer"),
        ("motion_response", "alpha_mean"),
        ("motion_response", "beta_mean"),
        ("motion_response", "live_transfer"),
        ("odd_response", "alpha_mean"),
        ("odd_response", "beta_mean"),
        ("odd_response", "live_transfer"),
        ("substrate_response", "motion_response"),
        ("substrate_response", "odd_response"),
        ("motion_response", "odd_response"),
    ]
    for a, b in pairs:
        candidate_map[f"{a}__{b}"] = {
            "symmetric": focus_lookup(symmetric, a, b),
            "asymmetric": focus_lookup(asymmetric, a, b),
        }

    result = {
        "experiment": "probe_particle_m_binding_fixed_grid",
        "manifest": "manifest.json",
        "probe_pair": {
            "same_total_excess": True,
            "same_center_protocol": True,
            "difference": "symmetric versus x-asymmetric internal potential profile",
        },
        "fixed_grid_validation": manifest["boundary_guarantee"],
        "symmetric": symmetric,
        "asymmetric": asymmetric,
        "m_binding_candidate_map": candidate_map,
        "interpretation_limit": manifest["interpretation_limit"],
    }

    RESULT_OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "experiment": result["experiment"],
        "fixed_grid_validation": result["fixed_grid_validation"],
        "symmetric_summary": symmetric["summary"],
        "asymmetric_summary": asymmetric["summary"],
        "m_binding_candidate_map": candidate_map,
        "raw_output_dir": str(OUT_DIR.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
