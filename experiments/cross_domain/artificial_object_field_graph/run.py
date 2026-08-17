from __future__ import annotations

import json
import math
import sys
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from scanner.self_reflexive_operator import operator_step

OUT_DIR = ROOT / "run-data" / "cross_domain" / "artificial_object_field_graph"
OUT = OUT_DIR / "result.json"

DIMENSION = 4
STEPS = 28
BACKGROUND = 1.0
INITIAL_HALF_WIDTH = 3          # initial active substrate: 7^4 points
TOTAL_OBJECT_EXCESS = 180.0
SUPPORT_R = 2.4
ASYM = 0.35

# Same imposed artificial-object path for every shape.  This is a probe input,
# not a force law.  Environmental points outside the prescribed object are
# created only by the operator's recovered birth branch.
PATH = [(1, 0, 0, 0), (-1, 0, 0, 0), (0, 1, 0, 0), (0, -1, 0, 0)]


def initial_substrate() -> dict[tuple[int, int, int, int], float]:
    rng = range(-INITIAL_HALF_WIDTH, INITIAL_HALF_WIDTH + 1)
    return {tuple(c): BACKGROUND for c in product(rng, repeat=4)}


def object_profile(kind: str, shift: tuple[int, int, int, int]):
    # Enumerate only integer sites inside the finite support around the imposed probe.
    lo = math.floor(-SUPPORT_R) - 1
    hi = math.ceil(SUPPORT_R) + 1
    rows = []
    for off in product(range(lo, hi + 1), repeat=4):
        r2 = sum(float(v * v) for v in off)
        r = math.sqrt(r2)
        if r > SUPPORT_R:
            continue
        base = math.exp(-0.5 * r2 / (1.15 ** 2))
        x, y, z, w = map(float, off)
        if kind == "symmetric":
            mod = 1.0
        elif kind == "dipole_x":
            mod = 1.0 + ASYM * x / SUPPORT_R
        elif kind == "quadrupole_xy":
            mod = 1.0 + ASYM * (x * x - y * y) / (SUPPORT_R ** 2)
        elif kind == "mixed_xyz":
            mod = 1.0 + ASYM * (x + y - z) / (math.sqrt(3.0) * SUPPORT_R)
        else:
            raise ValueError(kind)
        raw = max(base * mod, 0.0)
        if raw > 0.0:
            coord = tuple(int(off[i] + shift[i]) for i in range(4))
            rows.append((coord, raw))

    raw_sum = sum(v for _, v in rows)
    scale = TOTAL_OBJECT_EXCESS / raw_sum
    return {coord: v * scale for coord, v in rows}


def radial_environment_features(phi, object_cells):
    # No mean/HF decomposition is assumed.  The graph is built directly from
    # raw environmental potential and topology around the origin.
    shells = [(0, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8)]
    feats = []
    for lo, hi in shells:
        vals = []
        for c, value in phi.items():
            if c in object_cells:
                continue
            r = math.sqrt(sum(float(v * v) for v in c))
            if lo <= r < hi:
                vals.append(value)
        if vals:
            a = np.asarray(vals, dtype=float)
            feats.extend([float(a.mean()), float(a.std()), float(len(vals))])
        else:
            feats.extend([0.0, 0.0, 0.0])
    return feats


def max_radius(phi):
    return max((math.sqrt(sum(float(v * v) for v in c)) for c in phi), default=0.0)


def run_case(kind: str) -> dict:
    phi = initial_substrate()
    previous_flow = {}
    frame_features = []
    injections = []
    births = []
    live_transfer = []
    birth_transfer = []
    alpha_mean = []
    alpha_std = []
    beta_mean = []
    beta_std = []
    point_counts = []
    radii = []
    conservation_error = []

    for step in range(STEPS):
        obj = object_profile(kind, PATH[step % len(PATH)])
        object_cells = set(obj)

        # The probe itself is externally prescribed.  Its imposed reset/activation
        # is logged; it is not counted as environmental point birth.
        injection = 0.0
        for coord, excess in obj.items():
            target = BACKGROUND + excess
            injection += target - phi.get(coord, 0.0)
            phi[coord] = target
        injections.append(float(injection))

        phi, previous_flow, diag = operator_step(phi, previous_flow, dimension=DIMENSION)
        births.append(diag.births)
        live_transfer.append(diag.live_transfer)
        birth_transfer.append(diag.birth_transfer)
        conservation_error.append(diag.total_after - diag.total_before)

        aa = np.asarray(diag.alpha_samples, dtype=float)
        bb = np.asarray(diag.beta_samples, dtype=float)
        alpha_mean.append(float(aa.mean()) if aa.size else 0.0)
        alpha_std.append(float(aa.std()) if aa.size else 0.0)
        beta_mean.append(float(bb.mean()) if bb.size else 0.0)
        beta_std.append(float(bb.std()) if bb.size else 0.0)

        point_counts.append(len(phi))
        radii.append(max_radius(phi))
        frame_features.append(radial_environment_features(phi, object_cells))

    mat = np.asarray(frame_features, dtype=float)
    graph = np.concatenate([
        mat.mean(axis=0),
        mat.std(axis=0),
        np.asarray([
            np.mean(point_counts), np.std(point_counts),
            np.mean(radii), np.std(radii),
            np.mean(births), np.std(births),
            np.mean(live_transfer), np.mean(birth_transfer),
            np.mean(alpha_mean), np.mean(alpha_std),
            np.mean(beta_mean), np.mean(beta_std),
            np.mean(injections), np.std(injections),
        ], dtype=float),
    ])

    return {
        "graph": graph.tolist(),
        "final_active_points": int(point_counts[-1]),
        "final_max_radius": float(radii[-1]),
        "births_total": int(sum(births)),
        "birth_transfer_total": float(sum(birth_transfer)),
        "live_transfer_total": float(sum(live_transfer)),
        "alpha_mean_over_frames": float(np.mean(alpha_mean)),
        "beta_mean_over_frames": float(np.mean(beta_mean)),
        "injection_mean": float(np.mean(injections)),
        "max_abs_operator_conservation_error": float(np.max(np.abs(conservation_error))),
    }


def cosine(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    return None if na == 0 or nb == 0 else float(np.dot(a, b) / (na * nb))


def main():
    kinds = ["symmetric", "dipole_x", "quadrupole_xy", "mixed_xyz"]
    cases = {k: run_case(k) for k in kinds}
    g0 = np.asarray(cases["symmetric"]["graph"], dtype=float)

    similarities = {}
    residual_norms = {}
    residual_vectors = {}
    for k in kinds:
        g = np.asarray(cases[k]["graph"], dtype=float)
        similarities[k] = cosine(g, g0)
        residual = g - g0
        residual_norms[k] = float(np.linalg.norm(residual))
        residual_vectors[k] = residual

    pair_residual_cos = {}
    for i, a in enumerate(kinds[1:]):
        for j, b in enumerate(kinds[1:]):
            if j > i:
                pair_residual_cos[f"{a}__{b}"] = cosine(residual_vectors[a], residual_vectors[b])

    common = np.mean(np.vstack([np.asarray(cases[k]["graph"], float) for k in kinds]), axis=0)

    result = {
        "experiment": "artificial_object_field_graph",
        "status": "artificial-object probe on reconstructed framewise self-reflexive operator",
        "operator": {
            "alpha": "positive local potential difference / local positive-difference sum",
            "beta": "previous-frame local edge flow / previous-frame local outgoing-flow sum",
            "coupling": "J = C * alpha / (1 + beta)",
            "C": "mean positive local potential difference",
            "alpha_beta_fixed_parameters": False,
            "alpha_beta_internal_evolution_law": False,
            "point_birth": "recovered ratio-capacity rule from onreflexiv_cpu_gpu_dense_bundle",
            "birth_threshold": None,
            "external_braking_K": None,
        },
        "guardrails": {
            "gravity_law_inserted": False,
            "electric_law_inserted": False,
            "mass_or_charge_labels_used_in_analysis": False,
            "mean_hf_components_predefined": False,
            "object_total_excess_equal_across_shapes": True,
            "common_motion_path_equal_across_shapes": True,
            "object_is_externally_prescribed_probe": True,
            "environmental_point_birth_only_from_operator": True,
        },
        "numerics": {
            "initial_active_substrate": "7^4",
            "steps": STEPS,
            "background_initial_phi": BACKGROUND,
            "object_total_excess": TOTAL_OBJECT_EXCESS,
        },
        "cases": cases,
        "graph_comparison": {
            "cosine_to_symmetric": similarities,
            "residual_norm_from_symmetric": residual_norms,
            "asymmetric_residual_pair_cosines": pair_residual_cos,
            "common_graph": common.tolist(),
        },
        "interpretation_limits": {
            "positive_meaning": "A shared graph component plus reproducible asymmetry-dependent residual supports structural separation at this operator resolution.",
            "negative_meaning": "If the whole graph changes with shape or residual directions are inconsistent, this separation is not supported.",
            "not_evidence_for": "physical mass, gravity, electric charge or electric field; labels remain post-hoc hypotheses",
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
