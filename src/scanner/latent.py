from __future__ import annotations

from math import sqrt
from statistics import mean
from typing import Mapping, Sequence


def _pearson(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    mx, my = mean(x), mean(y)
    dx = [float(v) - mx for v in x]
    dy = [float(v) - my for v in y]
    den = sqrt(sum(v * v for v in dx) * sum(v * v for v in dy))
    return 0.0 if den == 0 else sum(a * b for a, b in zip(dx, dy)) / den


def normalized_ranks(values: Sequence[float]) -> list[float]:
    """Return average-tie ranks on [0, 1]. No physical meaning is assigned."""
    n = len(values)
    if n == 0:
        return []
    if n == 1:
        return [0.0]

    order = sorted(range(n), key=lambda i: float(values[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i + 1
        while j < n and float(values[order[j]]) == float(values[order[i]]):
            j += 1
        avg_rank = 0.5 * (i + j - 1)
        for k in range(i, j):
            ranks[order[k]] = avg_rank / (n - 1)
        i = j
    return ranks


def spearman(x: Sequence[float], y: Sequence[float]) -> float:
    return _pearson(normalized_ranks(x), normalized_ranks(y))


def _aligned_ranks(table: Mapping[str, Sequence[float]], names: list[str]) -> tuple[dict[str, list[float]], dict[str, int]]:
    ranks = {name: normalized_ranks(table[name]) for name in names}
    reference = ranks[names[0]]
    aligned: dict[str, list[float]] = {}
    orientation: dict[str, int] = {}
    for name in names:
        current = ranks[name]
        sign = -1 if _pearson(reference, current) < 0 else 1
        orientation[name] = sign
        aligned[name] = [1.0 - r for r in current] if sign < 0 else list(current)
    return aligned, orientation


def infer_common_order(table: Mapping[str, Sequence[float]]) -> dict:
    """Infer an orientation-free common ordering from multiple observables.

    The result is a relational ordering candidate only. It is deliberately not
    called time and it does not assume a fourth coordinate, dynamics or a
    physical law. Overall reversal of the inferred order is equivalent.
    """
    names = [name for name, values in table.items() if isinstance(values, (list, tuple))]
    if len(names) < 3:
        raise ValueError("common-order inference requires at least three observables")

    lengths = {len(table[name]) for name in names}
    if len(lengths) != 1 or next(iter(lengths)) < 3:
        raise ValueError("all observables must have the same length >= 3")

    aligned, orientation = _aligned_ranks(table, names)
    n = len(table[names[0]])
    consensus = [mean(aligned[name][i] for name in names) for i in range(n)]

    # Leave-one-observable-out validation avoids scoring an observable against
    # a consensus that already contains itself.
    loo: dict[str, float] = {}
    for held_out in names:
        others = [name for name in names if name != held_out]
        other_aligned, _ = _aligned_ranks(table, others)
        other_consensus = [mean(other_aligned[name][i] for name in others) for i in range(n)]
        loo[held_out] = abs(spearman(table[held_out], other_consensus))

    pairwise_abs = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            pairwise_abs.append(abs(spearman(table[a], table[b])))

    return {
        "type": "latent_common_order",
        "observable_count": len(names),
        "sample_count": n,
        "orientation": orientation,
        "consensus_order": consensus,
        "mean_leave_one_out_abs_spearman": mean(loo.values()),
        "leave_one_out_abs_spearman": loo,
        "mean_pairwise_abs_spearman": mean(pairwise_abs) if pairwise_abs else 0.0,
        "note": "Orientation-free relational order only; no time interpretation is assigned.",
    }
