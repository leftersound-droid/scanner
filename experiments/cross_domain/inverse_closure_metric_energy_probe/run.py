from __future__ import annotations

import json, math, sys
from collections import defaultdict
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from scanner.self_reflexive_operator import operator_step, directions, add

OUT = ROOT / "run-data" / "cross_domain" / "inverse_closure_metric_energy_probe"
DIM = 4
BACKGROUND = 100.0
DOMAIN_L1 = 14
SUPPORT_L1 = 4
LOCAL_L1 = 7
SIGMA = 0.48
M = 3
DRIVE_FRAMES = 6
RELEASE_FRAMES = 3
DS = directions(DIM)

DOMAIN = [tuple(int(v) for v in c) for c in product(range(-DOMAIN_L1, DOMAIN_L1 + 1), repeat=4)
          if sum(abs(v) for v in c) <= DOMAIN_L1]
LOCAL = [c for c in DOMAIN if sum(abs(v) for v in c) <= LOCAL_L1]
LOCAL_SET = set(LOCAL)


def packet(radius: float, theta: float, total_excess: float):
    raw = {}
    for c in product(range(-SUPPORT_L1, SUPPORT_L1 + 1), repeat=4):
        if sum(abs(v) for v in c) > SUPPORT_L1:
            continue
        x, y, z, w = (float(v) for v in c)
        rr = math.hypot(x, y)
        d2 = (rr - radius) ** 2 + z*z + w*w
        env = math.exp(-0.5 * d2 / (SIGMA * SIGMA))
        if env < 1e-12:
            continue
        ang = math.atan2(y, x) if rr else 0.0
        val = env * (1.0 + 0.35 * math.cos(M * (ang - theta)))
        if val > 0.0:
            raw[tuple(int(v) for v in c)] = val
    scale = total_excess / sum(raw.values())
    return {c: v * scale for c, v in raw.items()}


def apply_component(phi, old, new):
    for c in set(old) | set(new):
        phi[c] += new.get(c, 0.0) - old.get(c, 0.0)


def projected_metrics(phi):
    proj = defaultdict(float)
    for (x, y, z, w), value in phi.items():
        if (x, y, z, w) in LOCAL_SET:
            proj[(x, y, z)] += value - BACKGROUND
    pos = {c: max(v, 0.0) for c, v in proj.items()}
    q = sum(pos.values())
    sq = sum(v*v for v in pos.values())
    veff = q*q / sq if sq > 0.0 else 0.0
    if q > 0.0:
        ctr = np.sum(np.asarray([np.asarray(c, float) * v for c, v in pos.items()]), axis=0) / q
        r2 = sum(v * float(np.sum((np.asarray(c, float) - ctr) ** 2)) for c, v in pos.items()) / q
    else:
        r2 = 0.0
    return float(q), float(veff), float(math.sqrt(max(r2, 0.0)))


def flow_metrics(flow):
    j3 = j4 = 0.0
    for (c, di), value in flow.items():
        if c not in LOCAL_SET or value <= 0.0:
            continue
        if di < 6:
            j3 += value
        else:
            j4 += value
    return float(j3), float(j4)


def recurrence_distance(phi, ref):
    a = np.asarray([phi[c] - BACKGROUND for c in LOCAL], float)
    b = np.asarray([ref[c] - BACKGROUND for c in LOCAL], float)
    return float(np.linalg.norm(a - b) / (np.linalg.norm(b) + 1e-30))


def initial_flow(kind, pkt):
    prev = {}
    if kind == "none":
        return prev
    for c, value in pkt.items():
        x, y, z, w = c
        if kind == "tangent":
            if abs(x) >= abs(y):
                di = 3 if x > 0 else 2
            else:
                di = 0 if y > 0 else 1
        elif kind == "radial_out":
            comps = [abs(x), abs(y), abs(z), abs(w)]
            axis = int(np.argmax(comps)); s = c[axis]
            di = 2 * axis + (1 if s >= 0 else 0)
        elif kind == "w_plus":
            di = 7
        else:
            raise ValueError(kind)
        prev[(c, di)] = value
    return prev


def run_driven(radius, period, total_excess):
    phi = {c: BACKGROUND for c in DOMAIN}; prev = {}; old = {}; rows = []
    for frame in range(DRIVE_FRAMES):
        theta = 2.0 * math.pi * frame / period / M
        new = packet(radius, theta, total_excess)
        apply_component(phi, old, new); old = new
        q, veff, rrms = projected_metrics(phi)
        phi, prev, diag = operator_step(phi, prev, dimension=DIM)
        j3, j4 = flow_metrics(prev)
        rows.append({"phase":"drive", "frame":frame, "Q":q, "Veff":veff, "Rrms":rrms,
                     "J3":j3, "J4":j4, "live_transfer":float(diag.live_transfer), "births":diag.births})
    release_ref = dict(phi)
    for frame in range(RELEASE_FRAMES):
        q, veff, rrms = projected_metrics(phi)
        rec = recurrence_distance(phi, release_ref)
        phi, prev, diag = operator_step(phi, prev, dimension=DIM)
        j3, j4 = flow_metrics(prev)
        rows.append({"phase":"release", "frame":frame, "Q":q, "Veff":veff, "Rrms":rrms,
                     "J3":j3, "J4":j4, "live_transfer":float(diag.live_transfer), "births":diag.births,
                     "recurrence_distance":rec})
    return summarize(radius, period, total_excess, rows)


def run_free_topology(kind, radius=1.5, total_excess=60.0, steps=9):
    phi = {c: BACKGROUND for c in DOMAIN}
    pkt = packet(radius, 0.0, total_excess)
    apply_component(phi, {}, pkt)
    ref = dict(phi); prev = initial_flow(kind, pkt); rows = []
    for frame in range(steps + 1):
        q, veff, rrms = projected_metrics(phi); j3, j4 = flow_metrics(prev)
        rows.append({"phase":"free", "frame":frame, "Q":q, "Veff":veff, "Rrms":rrms,
                     "J3":j3, "J4":j4, "recurrence_distance":recurrence_distance(phi, ref)})
        if frame < steps:
            phi, prev, _ = operator_step(phi, prev, dimension=DIM)
    first, last = rows[0], rows[-1]
    return {"kind":kind, "rows":rows, "summary":{
        "Q_ratio_last_first":last["Q"]/(first["Q"]+1e-30),
        "Veff_ratio_last_first":last["Veff"]/(first["Veff"]+1e-30),
        "Rrms_ratio_last_first":last["Rrms"]/(first["Rrms"]+1e-30),
        "recurrence_last":last["recurrence_distance"],
        "min_recurrence_after_initial":min(r["recurrence_distance"] for r in rows[1:])}}


def summarize(radius, period, total_excess, rows):
    drive = [r for r in rows if r["phase"] == "drive"]
    rel = [r for r in rows if r["phase"] == "release"]
    return {"radius":radius, "period":period, "total_excess":total_excess, "rows":rows, "summary":{
        "drive_Veff_mean":float(np.mean([r["Veff"] for r in drive])),
        "drive_live_transfer_mean":float(np.mean([r["live_transfer"] for r in drive])),
        "release_Veff_ratio_last_first":rel[-1]["Veff"]/(rel[0]["Veff"]+1e-30),
        "release_Q_ratio_last_first":rel[-1]["Q"]/(rel[0]["Q"]+1e-30),
        "release_recurrence_last":rel[-1]["recurrence_distance"],
        "births_total":int(sum(r.get("births", 0) for r in rows))}}


def fit_power(xs, ys):
    x = np.asarray(xs, float); y = np.asarray(ys, float); mask = (x > 0) & (y > 0)
    b, a = np.polyfit(np.log(x[mask]), np.log(y[mask]), 1)
    pred = a + b*np.log(x[mask]); obs = np.log(y[mask])
    den = float(np.sum((obs - obs.mean()) ** 2))
    return {"exponent":float(b), "prefactor":float(math.exp(a)),
            "log_r2":float(1.0 - np.sum((obs - pred) ** 2)/den) if den > 0 else None}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cases = [run_driven(r, p, 60.0) for r in (1.0, 1.5, 2.0) for p in (3.0, 4.0, 6.0)]
    amp_cases = [run_driven(1.5, 4.0, q) for q in (30.0, 60.0, 120.0)]
    p4 = [c for c in cases if c["period"] == 4.0]
    r15 = [c for c in cases if c["radius"] == 1.5]
    free = [run_free_topology(k) for k in ("none", "tangent", "radial_out", "w_plus")]
    result = {
        "experiment":"inverse_closure_metric_energy_probe_pilot",
        "status":"mixed analog/emergent pilot; no energy, Compton, metric or time law injected",
        "operator":"unchanged scanner.self_reflexive_operator.operator_step",
        "parameters":{"background":BACKGROUND, "domain_l1":DOMAIN_L1, "support_l1":SUPPORT_L1,
                      "drive_frames":DRIVE_FRAMES, "release_frames":RELEASE_FRAMES,
                      "boundary_unreachable":SUPPORT_L1 + DRIVE_FRAMES + RELEASE_FRAMES < DOMAIN_L1},
        "driven_cases":cases, "amplitude_cases":amp_cases, "free_topology_cases":free,
        "fits":{
            "Veff_vs_radius_at_period4":fit_power([c["radius"] for c in p4], [c["summary"]["drive_Veff_mean"] for c in p4]),
            "live_transfer_vs_radius_at_period4":fit_power([c["radius"] for c in p4], [c["summary"]["drive_live_transfer_mean"] for c in p4]),
            "live_transfer_vs_frequency_at_radius1p5":fit_power([1.0/c["period"] for c in r15], [c["summary"]["drive_live_transfer_mean"] for c in r15]),
            "live_transfer_vs_total_excess":fit_power([c["total_excess"] for c in amp_cases], [c["summary"]["drive_live_transfer_mean"] for c in amp_cases])},
        "guardrail":"Driven packet relations are calibration only. Free survival/dispersion is the closure test. Negative closure must not be repaired by new operator terms."
    }
    (OUT / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"parameters":result["parameters"], "fits":result["fits"],
                      "free_topology_summaries":{c["kind"]:c["summary"] for c in free}}, indent=2))


if __name__ == "__main__":
    main()
