from __future__ import annotations
from typing import Any
from .models import Problem
from .memory import GraphMemory

STRATEGIES = ("direct", "analogy", "hybrid")

class StrategyRouter:
    """Learns analysis routing from memory and external validation feedback.

    The router never changes the physical experiment/operator.  Scientific
    quality comes only from externally recorded validation scores.
    """
    def choose(self, problem: Problem, memory: GraphMemory) -> tuple[str, dict[str, Any]]:
        matches = memory.retrieve(problem.fingerprint_tokens())
        best_match = matches[0].score if matches else 0.0
        if best_match >= 0.22:
            candidate = "hybrid"
        elif best_match >= 0.10:
            candidate = "analogy"
        else:
            candidate = "direct"

        validated = []
        for strategy in STRATEGIES:
            s = memory.strategy_stats(strategy)
            if s["validated_runs"] > 0:
                # Validation quality is primary. Runtime only breaks near-ties;
                # no physical success threshold is introduced.
                validated.append((s["mean_validation_score"], -s["mean_ms"], strategy))
        if validated:
            validated.sort(reverse=True)
            candidate = validated[0][2]

        return candidate, {
            "best_memory_match": best_match,
            "retrieved": [{"id": m.node_id, "score": m.score, "label": m.node.get("label")} for m in matches],
            "validation_stats": {s: memory.strategy_stats(s) for s in STRATEGIES},
        }
