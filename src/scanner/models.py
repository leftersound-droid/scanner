from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any
import time
import uuid

@dataclass
class Problem:
    title: str
    description: str
    domain: str = "generic"
    tags: list[str] = field(default_factory=list)
    payload: dict[str, Any] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)
    problem_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def fingerprint_tokens(self) -> set[str]:
        text = " ".join([self.title, self.description, self.domain, *self.tags]).lower()
        return {t.strip(".,:;()[]{}!?\n\t") for t in text.split() if len(t) > 2}

@dataclass
class LayerResult:
    layer: str
    strategy: str
    output: dict[str, Any]
    elapsed_ms: float
    evidence: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

@dataclass
class ScanRecord:
    problem: Problem
    baseline: LayerResult
    learner: LayerResult
    comparison: dict[str, Any]
    created_at: float = field(default_factory=time.time)
    scan_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
