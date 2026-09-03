from __future__ import annotations

import math
import numpy as np

# Representation-calibration probe for the live-neighbour sector of the
# self-reflexive operator.  No physical law or stabilizer is added.
#
# The test domain is a periodic 4D reference manifold used only to remove
# boundary/birth contamination while comparing resolutions.  The local
# transfer algebra is the same alpha/beta/capacity rule as the scanner.

DIRS = [(0,-1),(0,1),(1,-1),(1,1),(2,-1),(2,1),(3,-1),(3,1)]


def step(P: np.ndarray, prev: np.ndarray | None = None):
    neigh = np.stack([np.roll(P, -s, axis=a) for a, s in DIRS], axis=-1)
    delta = np.maximum(P[..., None] - neigh, 0.0)
    live = delta > 0.0
    sum_delta = delta.sum(axis=-1)
    n_live = live.sum(axis=-1)
    capacity = np.divide(sum_delta, n_live, out=np.zeros_like(sum_delta), where=n_live > 0)
    alpha = np.divide(delta, sum_delta[..., None], out=np.zeros_like(delta), where=sum_delta[..., None] > 0)

    if prev is None:
        beta = np.zeros_like(delta)
    else:
        prev_live = np.where(live, np.maximum(prev, 0.0), 0.0)
        prev_sum = prev_live.sum(axis=-1)
        beta = np.divide(prev_live, prev_sum[..., None], out=np.zeros_like(prev_live), where=prev_sum[..., None] > 0)

    J = capacity[..., None] * alpha / (1.0 + beta)
    out = J.sum(axis=-1)
    scale = np.ones_like(out)
    mask = (out > P) & (out > 0.0)
    scale[mask] = P[mask] / out[mask]
    J *= scale[..., None]

    dP = -J.sum(axis=-1)
    for di, (axis, sign) in enumerate(DIRS):
        dP += np.roll(J[..., di], sign, axis=axis)
    return P + dP, J


def reference_field(n: int, permutation=None):
    x = np.linspace(-math.pi, math.pi, n, endpoint=False)
    X = list(np.meshgrid(x, x, x, x, indexing="ij"))
    if permutation is not None:
        X = [X[p] for p in permutation]
    a, b, c, d = X
    return (
        1.5
        + 0.20 * np.cos(a)
        + 0.15 * np.sin(b)
        + 0.10 * np.cos(c + d)
        + 0.05 * np.sin(a - b + d)
        + 0.04 * np.cos(2.0 * c - d)
    )


def metrics(P, J, h):
    total_J = J.sum(axis=-1)
    active = total_J > 1e-14
    probs = np.zeros_like(J)
    probs[active] = J[active] / total_J[active, None]

    lp = np.where(probs > 0.0, np.log(np.maximum(probs, 1e-300)), 0.0)
    H = np.zeros_like(total_J)
    H[active] = -np.sum(probs[active] * lp[active], axis=-1) / np.log(8.0)
    concentration = np.sum(probs * probs, axis=-1)
    pairdiff = np.stack(
        [
            np.abs(probs[...,0] - probs[...,1]),
            np.abs(probs[...,2] - probs[...,3]),
            np.abs(probs[...,4] - probs[...,5]),
            np.abs(probs[...,6] - probs[...,7]),
        ],
        axis=-1,
    )

    return {
        "sumP": float(P.sum()),
        "intP_control": float(P.sum() * h**4),
        "meanP": float(P.mean()),
        "stdP": float(P.std()),
        "meanJ": float(total_J.mean()),
        "J_over_h": float(total_J.mean() / h),
        "rmsJ_over_h": float(np.sqrt(np.mean(J * J)) / h),
        "direction_entropy": float(H[active].mean()),
        "direction_concentration": float(concentration[active].mean()),
        "antipodal_orientation": float(pairdiff[active].mean()),
        "active_fraction": float(active.mean()),
    }


def main():
    permutation = (3, 1, 2, 0)  # x <-> w; representation-only symmetry control
    resolutions = (8, 12, 16, 20, 24)

    rows = []
    for n in resolutions:
        h = 2.0 * math.pi / n
        steps = n // 4  # steps*h = pi/2, numerical evolution-scale control
        for label, perm in (("base", None), ("perm", permutation)):
            P = reference_field(n, perm)
            J = None
            for _ in range(steps):
                P, J = step(P, J)
            row = {"n": n, "h": h, "steps": steps, "steps_h": steps*h, "representation": label}
            row.update(metrics(P, J, h))
            rows.append(row)

    keys = list(rows[0])
    print(",".join(keys))
    for r in rows:
        print(",".join(str(r[k]) for k in keys))

    # Exact permutation-equivariance check at n=16.
    n = 16
    h = 2.0 * math.pi / n
    steps = n // 4
    Pb, Jb = reference_field(n), None
    Pp, Jp = reference_field(n, permutation), None
    for _ in range(steps):
        Pb, Jb = step(Pb, Jb)
        Pp, Jp = step(Pp, Jp)
    Pp = np.transpose(Pp, axes=permutation)
    Jp = np.transpose(Jp, axes=permutation + (4,))
    Jp = Jp[..., [6,7,2,3,4,5,0,1]]
    print("max_permutation_P_error", float(np.max(np.abs(Pb-Pp))))
    print("max_permutation_J_error", float(np.max(np.abs(Jb-Jp))))


if __name__ == "__main__":
    main()
