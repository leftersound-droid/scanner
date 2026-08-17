from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

@dataclass
class Match:
    node_id: str
    score: float
    node: dict[str, Any]

class GraphMemory:
    """Persistent research + strategy graph stored as transparent JSON."""
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.data = {"nodes": [], "edges": [], "strategy_stats": {}}

    def save(self) -> None:
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def upsert_node(self, node: dict[str, Any]) -> None:
        node_id = node["id"]
        for i, old in enumerate(self.data["nodes"]):
            if old.get("id") == node_id:
                self.data["nodes"][i] = node
                return
        self.data["nodes"].append(node)

    def add_edge(self, source: str, relation: str, target: str, **meta: Any) -> None:
        edge = {"source": source, "relation": relation, "target": target, **meta}
        if edge not in self.data["edges"]:
            self.data["edges"].append(edge)

    def retrieve(self, tokens: set[str], limit: int = 5) -> list[Match]:
        matches: list[Match] = []
        for node in self.data["nodes"]:
            text = " ".join(str(node.get(k, "")) for k in ("label", "summary", "kind", "tags")).lower()
            nt = {t.strip(".,:;()[]{}!?") for t in text.split() if len(t) > 2}
            score = 0.0 if not nt or not tokens else len(tokens & nt) / len(tokens | nt)
            if score > 0:
                matches.append(Match(node["id"], score, node))
        matches.sort(key=lambda m: m.score, reverse=True)
        return matches[:limit]

    def strategy_stats(self, strategy: str) -> dict[str, float]:
        raw = self.data["strategy_stats"].get(strategy, {})
        return {
            "runs": int(raw.get("runs", 0)),
            "mean_score": float(raw.get("mean_score", 0.0)),
            "mean_ms": float(raw.get("mean_ms", 0.0)),
            "validated_runs": int(raw.get("validated_runs", 0)),
            "mean_validation_score": float(raw.get("mean_validation_score", 0.0)),
        }

    def record_strategy_run(self, strategy: str, elapsed_ms: float) -> None:
        old = self.strategy_stats(strategy)
        n = old["runs"] + 1
        self.data["strategy_stats"][strategy] = {
            **old,
            "runs": n,
            "mean_ms": old["mean_ms"] + (elapsed_ms - old["mean_ms"]) / n,
        }

    def record_validation(self, strategy: str, score: float) -> None:
        """Record an externally supplied scientific/domain validation score.

        The memory does not define the score.  A domain validator or blind
        validation experiment supplies it after the strategy has produced an
        output.  This keeps strategy learning outside the physical operator.
        """
        old = self.strategy_stats(strategy)
        n = old["validated_runs"] + 1
        self.data["strategy_stats"][strategy] = {
            **old,
            "validated_runs": n,
            "mean_validation_score": old["mean_validation_score"] + (float(score) - old["mean_validation_score"]) / n,
            # compatibility field for older dashboards; now mirrors real validation
            "mean_score": old["mean_validation_score"] + (float(score) - old["mean_validation_score"]) / n,
        }

    def record_strategy(self, strategy: str, score: float, elapsed_ms: float) -> None:
        """Backward-compatible helper for older callers.

        New code should record execution and external validation separately.
        """
        self.record_strategy_run(strategy, elapsed_ms)
        self.record_validation(strategy, score)
