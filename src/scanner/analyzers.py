from __future__ import annotations
from math import sqrt
from statistics import mean
from typing import Any
from .models import Problem
from .memory import GraphMemory


def _pearson(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    mx, my = mean(x), mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    den = sqrt(sum(v*v for v in dx) * sum(v*v for v in dy))
    return 0.0 if den == 0 else sum(a*b for a,b in zip(dx,dy)) / den


def direct_analysis(problem: Problem) -> dict[str, Any]:
    table = problem.payload.get("table")
    if isinstance(table, dict) and table:
        numeric = {k: [float(v) for v in vals] for k, vals in table.items() if isinstance(vals, list)}
        keys = list(numeric)
        pairs = []
        for i, a in enumerate(keys):
            for b in keys[i+1:]:
                r = _pearson(numeric[a], numeric[b])
                pairs.append({"a": a, "b": b, "pearson": r, "abs": abs(r)})
        pairs.sort(key=lambda p: p["abs"], reverse=True)
        return {"type": "relation_scan", "relations": pairs, "count": len(pairs)}
    return {
        "type": "structural_scan",
        "fingerprint": sorted(problem.fingerprint_tokens()),
        "payload_keys": sorted(problem.payload.keys()),
        "constraint_keys": sorted(problem.constraints.keys()),
    }


def analogy_analysis(problem: Problem, memory: GraphMemory) -> dict[str, Any]:
    matches = memory.retrieve(problem.fingerprint_tokens(), limit=8)
    return {
        "type": "analogy_scan",
        "matches": [
            {"id": m.node_id, "score": m.score, "label": m.node.get("label"), "kind": m.node.get("kind")}
            for m in matches
        ],
    }


def hybrid_analysis(problem: Problem, memory: GraphMemory) -> dict[str, Any]:
    direct = direct_analysis(problem)
    analogy = analogy_analysis(problem, memory)
    return {
        "type": "hybrid_scan",
        "analogy": analogy,
        "direct": direct,
        "search_space_hint": [m["id"] for m in analogy.get("matches", [])[:3]],
    }
