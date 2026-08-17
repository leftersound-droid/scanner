from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "run-data" / "cross_domain" / "field_inertia_charge_separation"
OUT = OUT_DIR / "result.json"


def mean_vec(a, b):
    return [(x + y) / 2.0 for x, y in zip(a, b)]


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def scale(a, s):
    return [x * s for x in a]


def norm(a):
    return math.sqrt(sum(x * x for x in a))


def cosine_abs(a, b):
    na, nb = norm(a), norm(b)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return abs(sum(x * y for x, y in zip(a, b)) / (na * nb))


def analyze(matrix: dict[str, list[float]]) -> dict:
    e1a = matrix["field_1/comp_a"]
    e1b = matrix["field_1/comp_b"]
    e2a = matrix["field_2/comp_a"]
    e2b = matrix["field_2/comp_b"]

    # Main contrasts only; no physical semantics or force law is inserted.
    field_1_mean = mean_vec(e1a, e1b)
    field_2_mean = mean_vec(e2a, e2b)
    field_contrast = sub(field_2_mean, field_1_mean)

    comp_a_mean = mean_vec(e1a, e2a)
    comp_b_mean = mean_vec(e1b, e2b)
    complement_contrast = sub(comp_b_mean, comp_a_mean)

    # Difference-in-differences: pure factor interaction in feature space.
    interaction = sub(sub(e2b, e2a), sub(e1b, e1a))

    total_scale = sum(norm(v) for v in matrix.values()) / 4.0
    return {
        "field_contrast": field_contrast,
        "complement_contrast": complement_contrast,
        "interaction_residual": interaction,
        "field_contrast_norm": norm(field_contrast),
        "complement_contrast_norm": norm(complement_contrast),
        "interaction_norm": norm(interaction),
        "interaction_relative_to_mean_state_norm": norm(interaction) / total_scale if total_scale else None,
        "field_complement_abs_cosine": cosine_abs(field_contrast, complement_contrast),
        "note": "Raw relational geometry only; no threshold is used to classify separation or coupling.",
    }


def controls() -> dict[str, dict[str, list[float]]]:
    base = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # Positive methodological control: two independent factor directions.
    f = [0.70, -0.35, 0.45, 0.0, 0.0, 0.0]
    c = [0.0, 0.0, 0.0, 0.60, -0.50, 0.30]
    separated = {
        "field_1/comp_a": base,
        "field_1/comp_b": add(base, c),
        "field_2/comp_a": add(base, f),
        "field_2/comp_b": add(add(base, f), c),
    }

    # Negative methodological control: the two factors point in the same direction.
    shared = [0.50, -0.25, 0.40, 0.20, -0.10, 0.15]
    coupled = {
        "field_1/comp_a": base,
        "field_1/comp_b": add(base, scale(shared, 0.8)),
        "field_2/comp_a": add(base, shared),
        "field_2/comp_b": add(base, scale(shared, 1.8)),
    }

    return {"separated_control": separated, "coupled_control": coupled}


def main() -> None:
    cases = controls()
    result = {
        "experiment": "field_inertia_charge_separation_2x2",
        "status": "synthetic scanner identifiability control; not a physical particle simulation",
        "guardrails": {
            "physical_force_law_inserted": False,
            "mass_value_inserted": False,
            "charge_value_inserted": False,
            "particle_geometry_changed_between_cells": False,
            "scientific_threshold_used": False,
        },
        "cases": {name: {"matrix": matrix, "analysis": analyze(matrix)} for name, matrix in cases.items()},
        "interpretation": {
            "goal": "Verify that the scanner representation can distinguish a field-associated response direction from a complement-associated response direction, and can also expose deliberate coupling.",
            "physical_limit": "A real field/emergent-inertia graph requires raw finite-particle operator trajectories. This control cannot establish that such a graph exists physically.",
        },
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
