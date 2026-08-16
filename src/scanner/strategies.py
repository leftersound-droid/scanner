from __future__ import annotations
from typing import Any
from .models import Problem
from .memory import GraphMemory

STRATEGIES = ("direct", "analogy", "hybrid")

class StrategyRouter:
    """Learns which analysis strategy is efficient without altering the experiment itself."""
    def choose(self, problem: Problem, memory: GraphMemory) -> tuple[str, dict[str, Any]]:
        matches = memory.retrieve(problem.fingerprint_tokens())
        best_match = matches[0].score if matches else 0.0
        if best_match >= 0.22:
            candidate = "hybrid"
        elif best_match >= 0.10:
            candidate = "analogy"
        else:
            candidate = "direct"

        measured = []
        for strategy in STRATEGIES:
            s = memory.strategy_stats(strategy)
            if s["runs"] >= 3:
                utility = s["mean_score"] / max(s["mean_ms"], 0.1)
                measured.append((utility, strategy))
        if measured:
            measured.sort(reverse=True)
            learned = measured[0][1]
            if best_match < 0.22:
                candidate = learned

        return candidate, {
            "best_memory_match": best_match,
            "retrieved": [{"id": m.node_id, "score": m.score, "label": m.node.get("label")} for m in matches],
        }
