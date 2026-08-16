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
OUT = OUT_DIR / "result.json"

DIMENSION = 4
HALF_WIDTH = 5
BACKGROUND = 1.0
TOTAL_OBJECT_EXCESS = 120.0
SUPPORT_R = 1.8
ASYM = 0.35
FRAMES_PER_STATE = 4

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


def initial_substrate():
    r = range(-HALF_WIDTH, HALF_WIDTH + 1)
    return {tuple(c): BACKGROUND for c in product(r, repeat=4)}


def object_profile(kind, center):
    lo = math.floor(-SUPPORT_R) - 1
    hi = math.ceil(SUPPORT_R) + 1
    raw = []
    for off in product(range(lo, hi + 1), repeat=4):
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
            coord = tuple(int(off[i] + center[i]) for i in range(4))
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
        rel = tuple(float(c[i] - center[i]) for i in range(4))
        r = math.sqrt(sum(v * v for v in rel))
        if r <= SUPPORT_R or r > 4.5:
            continue
        excess = value - BACKGROUND
        vals.append(excess)
        odd_x_num += excess * rel[0]
        odd_x_den += abs(excess) * (abs(rel[0]) + 1e-15)
        if motion_norm > 0.0:
            proj = sum(rel[i] * float(motion[i]) for i in range(4)) / motion_norm
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


def run_case(kind):
    phi = initial_substrate()
    previous_flow = {}

    # Only these columns are supplied to Scanner. Point birth and external
    # probe reset remain diagnostics, so they cannot become m-map edges.
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

    previous_center = CENTER_PROTOCOL[0]
    frame = 0
    for state_center in CENTER_PROTOCOL:
        for _ in range(FRAMES_PER_STATE):
            center = state_center
            motion = tuple(center[i] - previous_center[i] for i in range(4))
            obj = object_profile(kind, center)
            object_cells = set(obj)

            reset = 0.0
            for coord, excess in obj.items():
                target = BACKGROUND + excess
                reset += target - phi.get(coord, 0.0)
                phi[coord] = target

            phi, previous_flow, diag = operator_step(phi, previous_flow, dimension=DIMENSION)
            aa = np.asarray(diag.alpha_samples, dtype=float)
            bb = np.asarray(diag.beta_samples, dtype=float)
            substrate, env_mean, env_std, odd, motion_resp = environmental_moments(
                phi, object_cells, center, motion
            )

            rows["frame"].append(float(frame))
            rows["probe_center_x"].append(float(center[0]))
            rows["probe_motion_x"].append(float(motion[0]))
            rows["substrate_response"].append(substrate)
            rows["environment_mean"].append(env_mean)
            rows["environment_std"].append(env_std)
            rows["motion_response"].append(motion_resp)
            rows["odd_response"].append(odd)
            rows["live_transfer"].append(float(diag.live_transfer))
            rows["alpha_mean"].append(float(aa.mean()) if aa.size else 0.0)
            rows["alpha_std"].append(float(aa.std()) if aa.size else 0.0)
            rows["beta_mean"].append(float(bb.mean()) if bb.size else 0.0)
            rows["beta_std"].append(float(bb.std()) if bb.size else 0.0)
            diagnostics["probe_reset"].append(float(reset))
            diagnostics["birth_transfer"].append(float(diag.birth_transfer))
            diagnostics["births"].append(float(diag.births))

            previous_center = center
            frame += 1

    problem = Problem(
        title=f"Probe particle m binding map: {kind}",
        description="Map raw framewise relations among substrate, motion, symmetry-sensitive response and operator observables.",
        domain="self_reflexive_operator",
        tags=["probe", "m-binding", kind, "neutral-measurement"],
        payload={"table": rows},
        constraints={
            "no_mass_formula": True,
            "no_charge_formula": True,
            "no_gravity_law": True,
            "no_electric_law": True,
            "no_relation_threshold": True,
            "birth_not_scanner_input": True,
            "probe_reset_not_scanner_input": True,
        },
    )
    scan = direct_analysis(problem)

    return {
        "kind": kind,
        "frames": frame,
        "table": rows,
        "diagnostics_not_scanner_input": diagnostics,
        "scanner_relation_scan_top12": scan,
        "m_binding_focus_all_pairs": all_focus_relations(rows),
        "summary": {
            "substrate_response_mean": float(np.mean(rows["substrate_response"])),
            "motion_response_rms": float(np.sqrt(np.mean(np.square(rows["motion_response"])))),
            "odd_response_rms": float(np.sqrt(np.mean(np.square(rows["odd_response"])))),
            "alpha_mean": float(np.mean(rows["alpha_mean"])),
            "beta_mean": float(np.mean(rows["beta_mean"])),
            "births_total_diagnostic_only": int(sum(diagnostics["births"])),
            "birth_transfer_total_diagnostic_only": float(sum(diagnostics["birth_transfer"])),
            "probe_reset_mean_diagnostic_only": float(np.mean(diagnostics["probe_reset"])),
        },
    }


def focus_lookup(case, a, b):
    for r in case["m_binding_focus_all_pairs"]:
        if {r["a"], r["b"]} == {a, b}:
            return r["pearson"]
    return None


def main():
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
        "experiment": "probe_particle_m_binding",
        "goal": "binding topology only; no exact mass/charge/field characteristic",
        "probe_pair": {
            "same_total_excess": True,
            "same_center_protocol": True,
            "difference": "symmetric versus x-asymmetric internal potential profile",
        },
        "operator": "framewise self-reflexive alpha/beta coupling from src/scanner/self_reflexive_operator.py",
        "representation": {
            "initial_substrate": "11^4 active points",
            "scanner_feature_dimension_fixed": True,
            "point_birth_not_scanner_input": True,
            "probe_reset_not_scanner_input": True,
            "births_logged_only_as diagnostic": True,
        },
        "neutral_to_candidate_reading": {
            "substrate_response": "space/background-response candidate only",
            "motion_response": "inertia/mass-response candidate only",
            "odd_response": "symmetry/charge-response candidate only",
            "warning": "candidate labels are post-hoc interpretation, not inserted physical laws",
        },
        "symmetric": symmetric,
        "asymmetric": asymmetric,
        "m_binding_candidate_map": candidate_map,
        "interpretation_limit": "The map establishes only which measured channels co-vary at this resolution. It does not establish physical mass, charge, gravity, electric field, or a unique higher-order m law.",
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
