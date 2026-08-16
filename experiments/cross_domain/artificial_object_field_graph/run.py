from __future__ import annotations

import json
from pathlib import Path
import numpy as np

# Reproducible probe test using the currently accessible 4D local-flow candidate
# from leftersound-droid/szoliton-elektron-modell/src/simulation.ts.
# IMPORTANT: this is the legacy/candidate operator currently visible on GitHub;
# its braking factor increases with diff and therefore is NOT claimed to be the
# later negative-feedback operator discussed in the research thread.

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "run-data" / "cross_domain" / "artificial_object_field_graph"
OUT = OUT_DIR / "result.json"

N = 15
M = N ** 4
STEPS = 28
FLOW_RATE = 0.25
BRAKING_K = 50.0
BACKGROUND = 1.0
TOTAL_OBJECT_EXCESS = 180.0
SUPPORT_R = 2.4
ASYM = 0.35


def build_neighbors(n: int) -> np.ndarray:
    idx = np.arange(n**4, dtype=np.int64).reshape((n, n, n, n))
    out = np.full((n**4, 8), -1, dtype=np.int64)
    dirs = [(-1,0,0,0),(1,0,0,0),(0,-1,0,0),(0,1,0,0),(0,0,-1,0),(0,0,1,0),(0,0,0,-1),(0,0,0,1)]
    for k,(dx,dy,dz,dw) in enumerate(dirs):
        xs = slice(max(0,-dx), min(n,n-dx)); xt = slice(max(0,dx), min(n,n+dx))
        ys = slice(max(0,-dy), min(n,n-dy)); yt = slice(max(0,dy), min(n,n+dy))
        zs = slice(max(0,-dz), min(n,n-dz)); zt = slice(max(0,dz), min(n,n+dz))
        ws = slice(max(0,-dw), min(n,n-dw)); wt = slice(max(0,dw), min(n,n+dw))
        src = idx[xs,ys,zs,ws].ravel(); dst = idx[xt,yt,zt,wt].ravel()
        out[src,k] = dst
    return out

NEIGH = build_neighbors(N)
VALID = NEIGH >= 0
NEIGH_SAFE = np.where(VALID, NEIGH, 0)


def apply_flow(grid: np.ndarray) -> np.ndarray:
    vals = grid[:, None]
    nvals = grid[NEIGH_SAFE]
    diff = np.where(VALID, vals - nvals, 0.0)
    diff = np.where(diff > 0.0, diff, 0.0)
    diff_sum = diff.sum(axis=1)
    count = (diff > 0.0).sum(axis=1)
    braking = np.zeros_like(diff_sum)
    active = diff_sum > 1e-12
    braking[active] = diff_sum[active] / (diff_sum[active] + BRAKING_K * count[active])
    total_out = grid * FLOW_RATE * braking
    portions = np.zeros_like(diff)
    portions[active] = total_out[active, None] * diff[active] / diff_sum[active, None]
    outgoing = portions.sum(axis=1)
    flat_dst = NEIGH_SAFE[VALID]
    flat_w = portions[VALID]
    incoming = np.bincount(flat_dst, weights=flat_w, minlength=M)
    return grid - outgoing + incoming

coords = np.indices((N,N,N,N), dtype=float)
center = (N-1)/2.0
rel0 = [coords[i]-center for i in range(4)]
r2_0 = sum(r*r for r in rel0)

# Common imposed rigid-body path. Successive centers are Manhattan distance 2,
# while the local operator propagates one neighbor per update. This is an imposed
# dimensionless probe ratio, not an inferred physical constant.
path = [(1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,-1,0,0)]


def profile(kind: str, shift: tuple[int,int,int,int]) -> np.ndarray:
    rel = [coords[i] - (center + shift[i]) for i in range(4)]
    r2 = sum(r*r for r in rel)
    r = np.sqrt(r2)
    base = np.exp(-0.5*r2/(1.15**2)) * (r <= SUPPORT_R)
    eps = 1e-9
    if kind == "symmetric":
        mod = np.ones_like(base)
    elif kind == "dipole_x":
        mod = 1.0 + ASYM * rel[0] / SUPPORT_R
    elif kind == "quadrupole_xy":
        mod = 1.0 + ASYM * (rel[0]**2 - rel[1]**2) / (SUPPORT_R**2)
    elif kind == "mixed_xyz":
        mod = 1.0 + ASYM * (rel[0] + rel[1] - rel[2]) / (np.sqrt(3.0)*SUPPORT_R)
    else:
        raise ValueError(kind)
    raw = np.clip(base * mod, 0.0, None)
    raw_sum = raw.sum()
    raw *= TOTAL_OBJECT_EXCESS / raw_sum
    return raw.ravel()


def radial_features(field: np.ndarray) -> list[float]:
    arr = field.reshape((N,N,N,N)) - BACKGROUND
    r = np.sqrt(r2_0)
    feats = []
    for lo,hi in [(0,2),(2,3),(3,4),(4,5),(5,6)]:
        mask = (r >= lo) & (r < hi)
        feats.append(float(arr[mask].mean()))
        feats.append(float(arr[mask].std()))
    return feats


def run_case(kind: str) -> dict:
    grid = np.full(M, BACKGROUND, dtype=float)
    trace = []
    injections = []
    fields = []
    for step in range(STEPS):
        obj = profile(kind, path[step % len(path)])
        target = BACKGROUND + obj
        mask = obj > 0.0
        # Prescribed rigid artificial object: reset only object cells to the same
        # object profile before each environmental flow step. Injection is logged.
        before = grid.copy()
        injection = float(np.sum(target[mask] - grid[mask]))
        grid[mask] = target[mask]
        grid = apply_flow(grid)
        injections.append(injection)
        outside = ~mask
        excess = grid[outside] - BACKGROUND
        trace.append(float(excess.mean()))
        fields.append(radial_features(grid))
    field_mat = np.array(fields)
    graph = np.concatenate([
        field_mat.mean(axis=0),
        field_mat.std(axis=0),
        np.array([np.mean(trace), np.std(trace), np.mean(injections), np.std(injections)])
    ])
    return {
        "graph": graph.tolist(),
        "trace_mean": float(np.mean(trace)),
        "trace_std": float(np.std(trace)),
        "injection_mean": float(np.mean(injections)),
        "final_total_excess": float(np.sum(grid - BACKGROUND)),
    }


def cosine(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=np.linalg.norm(a); nb=np.linalg.norm(b)
    return None if na==0 or nb==0 else float(np.dot(a,b)/(na*nb))


def main():
    kinds = ["symmetric","dipole_x","quadrupole_xy","mixed_xyz"]
    cases = {k: run_case(k) for k in kinds}
    g0 = np.array(cases["symmetric"]["graph"])
    residuals = {}
    similarities = {}
    for k in kinds:
        g = np.array(cases[k]["graph"])
        residuals[k] = float(np.linalg.norm(g-g0))
        similarities[k] = cosine(g,g0)
    asym_graphs = [np.array(cases[k]["graph"]) for k in kinds[1:]]
    common = np.mean(np.vstack([np.array(cases[k]["graph"]) for k in kinds]), axis=0)
    asym_residuals = [g-g0 for g in asym_graphs]
    pair_residual_cos = {}
    for i,a in enumerate(kinds[1:]):
        for j,b in enumerate(kinds[1:]):
            if j>i:
                pair_residual_cos[f"{a}__{b}"] = cosine(asym_residuals[i], asym_residuals[j])

    result = {
        "experiment":"artificial_object_field_graph",
        "status":"driven artificial-object probe on accessible 4D local-flow operator candidate",
        "operator_source":{
            "repo":"leftersound-droid/szoliton-elektron-modell",
            "file":"src/simulation.ts",
            "source_blob_sha":"0c41e37f7f6020071acdde7f916b3ea44f4c0e01",
            "warning":"Accessible GitHub operator uses brakingFactor=diffSum/(diffSum+K*n), so this run is not claimed to represent the later negative-feedback operator."
        },
        "guardrails":{
            "gravity_law_inserted":False,
            "electric_law_inserted":False,
            "mass_or_charge_labels_used_in_analysis":False,
            "mean_hf_components_predefined":False,
            "object_total_excess_equal_across_shapes":True,
            "common_motion_path_equal_across_shapes":True,
            "object_is_externally_prescribed_rigid_probe":True,
            "object_reset_injection_logged":True
        },
        "numerics":{
            "grid":"15^4",
            "steps":STEPS,
            "flow_rate":FLOW_RATE,
            "braking_k":BRAKING_K,
            "background":BACKGROUND,
            "object_total_excess":TOTAL_OBJECT_EXCESS,
            "path_manhattan_jump":2,
            "local_neighbor_propagation_per_step":1
        },
        "cases":cases,
        "graph_comparison":{
            "cosine_to_symmetric":similarities,
            "residual_norm_from_symmetric":residuals,
            "asymmetric_residual_pair_cosines":pair_residual_cos,
            "common_graph":common.tolist()
        },
        "interpretation_limits":{
            "positive_meaning":"If all object graphs share a strong common component while asymmetric probes add reproducible residual structure, the operator/environment can separate common object-field response from symmetry-dependent response at this resolution.",
            "negative_meaning":"If asymmetry strongly changes the whole graph or residuals have no reproducible structure, the proposed separation is not supported in this operator candidate/probe design.",
            "not_evidence_for":"physical mass, gravity, electric charge, electric field, or the latest operator until rerun with the correct current operator"
        }
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    main()
