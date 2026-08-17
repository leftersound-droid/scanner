from __future__ import annotations

import json
import math
import random
from pathlib import Path

from scanner.latent import infer_common_order, spearman

ROOT = Path(__file__).resolve().parents[3]
RUN_ROOT = ROOT / "run-data" / "r4_projection" / "latent_common_order"
RESULT = RUN_ROOT / "result.json"


def hidden_construction() -> tuple[list[float], dict[str, list[float]]]:
    """Synthetic hidden ordering with several nonlinear projections.

    The hidden variable is kept inside the benchmark harness only and is not
    passed to infer_common_order(). One observable is reversed to test that
    absolute orientation is not required.
    """
    n = 61
    u = [i / (n - 1) for i in range(n)]
    table = {
        "obs_a": [x**3 for x in u],
        "obs_b": [math.log1p(5.0 * x) for x in u],
        "obs_c": [math.sqrt(x) + 0.10 * x for x in u],
        "obs_d": [1.0 / (1.0 + math.exp(-8.0 * (x - 0.5))) for x in u],
        "obs_e": [1.0 - x * x for x in u],
    }
    return u, table


def negative_control(table: dict[str, list[float]]) -> dict[str, list[float]]:
    """Preserve every marginal value set but independently destroy row order."""
    out = {name: list(values) for name, values in table.items()}
    for index, name in enumerate(sorted(out)):
        rng = random.Random(8101 + index * 97)
        rng.shuffle(out[name])
    return out


def evaluate(hidden: list[float], table: dict[str, list[float]]) -> dict:
    inferred = infer_common_order(table)
    # The hidden ordering is used only here, after inference, as a synthetic
    # validator. Overall sign/reversal is physically uninterpreted.
    recovered = abs(spearman(hidden, inferred["consensus_order"]))
    return {
        "inference": inferred,
        "validator_abs_spearman_to_hidden": recovered,
    }


def main() -> None:
    hidden, positive_table = hidden_construction()
    negative_table = negative_control(positive_table)

    positive = evaluate(hidden, positive_table)
    negative = evaluate(hidden, negative_table)

    result = {
        "experiment": "nonlinear_r4_projection_latent_common_order",
        "status": "synthetic blind-control benchmark; not evidence for physical emergent time",
        "question": (
            "Can the scanner reconstruct one orientation-free latent ordering from several "
            "nonlinear projected observables without receiving the hidden coordinate or a time label?"
        ),
        "input_guardrails": {
            "hidden_coordinate_passed_to_scanner": False,
            "time_label_passed_to_scanner": False,
            "physical_law_inserted": False,
            "positive_and_negative_memory_shared": False,
        },
        "positive": positive,
        "negative": negative,
        "contrast": {
            "loo_common_order_delta": (
                positive["inference"]["mean_leave_one_out_abs_spearman"]
                - negative["inference"]["mean_leave_one_out_abs_spearman"]
            ),
            "hidden_recovery_delta": (
                positive["validator_abs_spearman_to_hidden"]
                - negative["validator_abs_spearman_to_hidden"]
            ),
        },
        "interpretation_guardrail": (
            "Success means only that a common monotonic relational ordering can be recovered "
            "from this synthetic family. Calling that ordering emergent physical time would "
            "require independent dynamical, causal and multi-clock tests."
        ),
    }

    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
