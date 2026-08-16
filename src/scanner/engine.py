from __future__ import annotations
from pathlib import Path
import json
import time
from .models import Problem, LayerResult, ScanRecord
from .memory import GraphMemory
from .strategies import StrategyRouter
from .analyzers import direct_analysis, analogy_analysis, hybrid_analysis

class ScannerEngine:
    def __init__(self, memory_path: str | Path, scans_dir: str | Path):
        self.memory = GraphMemory(memory_path)
        self.scans_dir = Path(scans_dir)
        self.scans_dir.mkdir(parents=True, exist_ok=True)
        self.router = StrategyRouter()

    def _run(self, strategy: str, problem: Problem) -> tuple[dict, float]:
        start = time.perf_counter()
        if strategy == "direct":
            output = direct_analysis(problem)
        elif strategy == "analogy":
            output = analogy_analysis(problem, self.memory)
        elif strategy == "hybrid":
            output = hybrid_analysis(problem, self.memory)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        return output, (time.perf_counter() - start) * 1000

    def scan(self, problem: Problem) -> ScanRecord:
        base_out, base_ms = self._run("direct", problem)
        baseline = LayerResult("baseline", "direct", base_out, base_ms)

        strategy, routing = self.router.choose(problem, self.memory)
        learn_out, learn_ms = self._run(strategy, problem)
        learner = LayerResult("learner", strategy, learn_out, learn_ms, evidence=routing)

        comparison = {
            "same_problem": True,
            "baseline_ms": base_ms,
            "learner_ms": learn_ms,
            "speed_ratio_baseline_over_learner": base_ms / learn_ms if learn_ms > 0 else None,
            "strategy_changed": strategy != "direct",
            "note": "Beta compares execution cost and traceability; scientific quality scoring must be supplied by a domain validator.",
        }
        record = ScanRecord(problem, baseline, learner, comparison)
        (self.scans_dir / f"{record.scan_id}.json").write_text(
            json.dumps(record.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )

        neutral_score = 1.0 if strategy == "direct" else max(routing.get("best_memory_match", 0.0), 0.01)
        self.memory.record_strategy(strategy, neutral_score, learn_ms)
        pnode = f"problem:{problem.problem_id}"
        snode = f"scan:{record.scan_id}"
        stnode = f"strategy:{strategy}"
        self.memory.upsert_node({"id": pnode, "kind": "problem", "label": problem.title, "summary": problem.description, "tags": problem.tags})
        self.memory.upsert_node({"id": snode, "kind": "scan", "label": record.scan_id, "summary": f"baseline=direct learner={strategy}"})
        self.memory.upsert_node({"id": stnode, "kind": "strategy", "label": strategy, "summary": "learned analysis strategy"})
        self.memory.add_edge(pnode, "evaluated_by", snode)
        self.memory.add_edge(snode, "used_strategy", stnode, elapsed_ms=learn_ms)
        for item in routing.get("retrieved", []):
            self.memory.add_edge(snode, "retrieved_memory", item["id"], similarity=item["score"])
        self.memory.save()
        return record
