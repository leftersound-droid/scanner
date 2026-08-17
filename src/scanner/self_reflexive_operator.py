from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

Coord = Tuple[int, int, int, int]
Edge = Tuple[Coord, int]


@dataclass
class StepDiagnostics:
    births: int
    live_transfer: float
    birth_transfer: float
    total_before: float
    total_after: float
    alpha_samples: list[float]
    beta_samples: list[float]


def directions(dimension: int = 4) -> tuple[Coord, ...]:
    if dimension not in (3, 4):
        raise ValueError("dimension must be 3 or 4")
    ds = [
        (-1, 0, 0, 0), (1, 0, 0, 0),
        (0, -1, 0, 0), (0, 1, 0, 0),
        (0, 0, -1, 0), (0, 0, 1, 0),
    ]
    if dimension == 4:
        ds += [(0, 0, 0, -1), (0, 0, 0, 1)]
    return tuple(ds)


def opposite_indices(dimension: int = 4) -> tuple[int, ...]:
    return (1, 0, 3, 2, 5, 4, 7, 6) if dimension == 4 else (1, 0, 3, 2, 5, 4)


def add(a: Coord, b: Coord) -> Coord:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])


def operator_step(
    phi: Dict[Coord, float],
    previous_flow: Dict[Edge, float] | None = None,
    *,
    dimension: int = 4,
) -> tuple[Dict[Coord, float], Dict[Edge, float], StepDiagnostics]:
    """One synchronous frame of the reconstructed self-reflexive operator.

    The two local parameters have no independent evolution law:

      alpha_ij = Delta_ij / sum_k Delta_ik
      beta_ij  = J_prev_ij / sum_k J_prev_ik

    They are measured afresh from the current potential distribution and the
    previous frame's actual local edge-flow distribution.  The operator only
    couples these raw ratios:

      C_i  = mean(positive Delta_ij)
      J_ij = C_i * alpha_ij / (1 + beta_ij)

    No fixed alpha, beta, braking K, threshold, damping, cooling, or physical
    force law is present.

    Missing-neighbour birth is the ratio-capacity rule recovered from the
    dense CPU/GPU bundle:

      q       = J_opp / J_other,              0 < q < 1
      C_free  = J_other - J_opp
      C_birth = C_free * q
      R_vac   = 1 + phi_i / C_i
      J_birth = C_birth / R_vac

    Birth transfers potential from the donor to the newly activated point.
    """
    prev = previous_flow or {}
    ds = directions(dimension)
    opp = opposite_indices(dimension)
    total_before = float(sum(phi.values()))

    donor_plans: list[tuple[Coord, list[tuple[Coord, int, float, bool]], float]] = []
    alpha_samples: list[float] = []
    beta_samples: list[float] = []

    for x, value in list(phi.items()):
        if value <= 0.0:
            continue

        live: list[tuple[int, Coord, float]] = []
        sum_delta = 0.0
        for di, d in enumerate(ds):
            y = add(x, d)
            if y not in phi:
                continue
            delta = value - phi[y]
            if delta > 0.0:
                live.append((di, y, delta))
                sum_delta += delta

        if not live or sum_delta <= 0.0:
            continue

        capacity = sum_delta / len(live)
        if capacity <= 0.0:
            continue

        prev_sum = sum(max(prev.get((x, di), 0.0), 0.0) for di, _, _ in live)
        live_j = [0.0] * len(ds)
        plans: list[tuple[Coord, int, float, bool]] = []

        for di, y, delta in live:
            alpha = delta / sum_delta
            beta = (max(prev.get((x, di), 0.0), 0.0) / prev_sum) if prev_sum > 0.0 else 0.0
            j = capacity * alpha / (1.0 + beta)
            alpha_samples.append(alpha)
            beta_samples.append(beta)
            live_j[di] = j
            if j > 0.0:
                plans.append((y, di, j, False))

        # Point birth: exactly the recovered local ratio-capacity construction.
        for di, d in enumerate(ds):
            y = add(x, d)
            if y in phi:
                continue

            odi = opp[di]
            opposite_coord = add(x, ds[odi])
            if opposite_coord not in phi:
                continue

            j_opp = live_j[odi]
            if j_opp <= 0.0:
                continue

            others = [live_j[j] for j in range(len(ds)) if j != odi and live_j[j] > 0.0]
            if not others:
                continue
            j_other = sum(others) / len(others)
            if j_other <= 0.0:
                continue

            q = j_opp / j_other
            if not (0.0 < q < 1.0):
                continue

            c_free = j_other - j_opp
            c_birth = c_free * q
            r_vac = 1.0 + value / capacity
            j_birth = c_birth / r_vac
            if j_birth > 0.0:
                plans.append((y, di, j_birth, True))

        out = sum(p[2] for p in plans)
        scale = value / out if out > value and out > 0.0 else 1.0
        donor_plans.append((x, plans, scale))

    delta_phi: dict[Coord, float] = {}
    births: dict[Coord, float] = {}
    next_flow: dict[Edge, float] = {}
    live_transfer = 0.0
    birth_transfer = 0.0

    # Synchronous application: every donor plan was computed from the same frame.
    for source, plans, scale in donor_plans:
        for target, di, amount, is_birth in plans:
            a = amount * scale
            if a <= 0.0:
                continue
            delta_phi[source] = delta_phi.get(source, 0.0) - a
            next_flow[(source, di)] = next_flow.get((source, di), 0.0) + a
            if target in phi:
                delta_phi[target] = delta_phi.get(target, 0.0) + a
                live_transfer += a
            else:
                births[target] = births.get(target, 0.0) + a
                birth_transfer += a

    out_phi = dict(phi)
    for x, dphi in delta_phi.items():
        value = out_phi.get(x, 0.0) + dphi
        out_phi[x] = 0.0 if abs(value) < 1e-15 else value
    for x, amount in births.items():
        if amount > 0.0:
            out_phi[x] = out_phi.get(x, 0.0) + amount

    total_after = float(sum(out_phi.values()))
    diag = StepDiagnostics(
        births=len(births),
        live_transfer=live_transfer,
        birth_transfer=birth_transfer,
        total_before=total_before,
        total_after=total_after,
        alpha_samples=alpha_samples,
        beta_samples=beta_samples,
    )
    return out_phi, next_flow, diag
