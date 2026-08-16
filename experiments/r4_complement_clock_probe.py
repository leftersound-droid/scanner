from __future__ import annotations

import json
import math
import random
from pathlib import Path

from scanner.engine import ScannerEngine
from scanner.models import Problem


ROOT = Path(__file__).resolve().parents[1]
RUN_ROOT = ROOT / "run-data" / "r4-complement-probe"
MEMORY = RUN_ROOT / "memory.json"
SCANS = RUN_ROOT / "scans"
RESULT = RUN_ROOT / "result.json"


def build_table(shuffle: bool = False) -> dict[str, list[float]]:
    """Create projected observables from a hidden 4D complementary trajectory.

    The hidden ordering variable and x4 values are NOT given to ScannerEngine.
    Only three projected observable series are supplied.  In the negative
    control one observable is deterministically shuffled, preserving its
    marginal values while destroying the shared ordering relation.
    """
    n = 41
    hidden = [i / (n - 1) for i in range(n)]

    # Complementary hidden fourth-coordinate pair: +u and -u.
    x4_a = [2.0 * u - 1.0 for u in hidden]
    x4_b = [-v for v in x4_a]

    # Neutral projected observables.  Their names intentionally carry no time
    # or electromagnetic semantics.  They depend on the same hidden state but
    # the hidden state itself is omitted from the scan input.
    p = [0.70 * u + 0.30 * math.sin(0.8 * u) for u in hidden]
    q = [0.55 * u + 0.45 * (1.0 - math.cos(0.9 * u)) for u in hidden]
    r = [0.50 * (a - b) + 0.50 * u for a, b, u in zip(x4_a, x4_b, hidden)]

    if shuffle:
        rng = random.Random(7319)
        rng.shuffle(r)

    return {"obs_a": p, "obs_b": q, "obs_c": r}


def run_case(engine: ScannerEngine, name: str, table: dict[str, list[float]]) -> dict:
    problem = Problem(
        title=f"R4 complement projection {name}",
        description=(
            "Blind relation scan of projected observables from a hidden "
            "complementary 4D construction. No physical-time label is supplied."
        ),
        domain="r4_projection_control",
        tags=["r4", "projection", "complement", "blind-control", name],
        payload={"table": table},
        constraints={
            "no_extra_rules": True,
            "hidden_order_not_supplied": True,
            "no_time_label": True,
        },
    )
    record = engine.scan(problem)
    direct = record.baseline.output
    rels = direct.get("relations", [])
    abs_rs = [float(item["abs"]) for item in rels]
    return {
        "scan_id": record.scan_id,
        "learner_strategy": record.learner.strategy,
        "relations": rels,
        "mean_abs_pearson": sum(abs_rs) / len(abs_rs) if abs_rs else 0.0,
        "min_abs_pearson": min(abs_rs) if abs_rs else 0.0,
        "max_abs_pearson": max(abs_rs) if abs_rs else 0.0,
    }


def main() -> None:
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    # Start this benchmark from its own empty memory so the first measurement
    # is not contaminated by previous project-memory retrieval.
    MEMORY.write_text('{"meta": {"name": "isolated benchmark memory"}, "nodes": [], "edges": [], "strategy_stats": {}}', encoding="utf-8")
    engine = ScannerEngine(MEMORY, SCANS)

    positive = run_case(engine, "positive", build_table(shuffle=False))
    negative = run_case(engine, "negative", build_table(shuffle=True))

    result = {
        "experiment": "r4_complement_projection_common_order_probe",
        "status": "synthetic control; not evidence for physical emergent time",
        "question": (
            "Can the current Scanner v2 relation layer distinguish projected "
            "observables sharing one hidden ordering from a control where that "
            "ordering is broken, without receiving a time variable?"
        ),
        "positive": positive,
        "negative": negative,
        "contrast": {
            "mean_abs_pearson_delta": positive["mean_abs_pearson"] - negative["mean_abs_pearson"],
            "min_abs_pearson_delta": positive["min_abs_pearson"] - negative["min_abs_pearson"],
        },
        "interpretation_guardrail": (
            "A positive contrast only validates sensitivity to this simple shared "
            "ordering pattern. The current generic analyzer uses pairwise Pearson "
            "relations and does not yet reconstruct a latent emergent clock."
        ),
    }
    RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
