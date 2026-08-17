from __future__ import annotations

import io
import json
import math
import sys
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import requests
import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from scanner.engine import ScannerEngine
from scanner.models import Problem

OUT = ROOT / "run-data" / "meta_strategy" / "lep_muon_blind_feedback"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "DELPHI": "https://www.hepdata.net/download/submission/ins699726/1/yaml",
    "OPAL": "https://www.hepdata.net/download/submission/ins628491/1/yaml",
}
NOMINAL_E = np.asarray([189.0, 192.0, 196.0, 200.0, 202.0, 205.0, 207.0])
GRID = np.linspace(-0.85, 0.85, 18)
JACKKNIFE_DROPS = [None, 192, 202]


def download_yaml_archive(name: str, url: str) -> tuple[dict[str, Any], str]:
    r = requests.get(url, timeout=120, headers={"User-Agent": "scanner-realdata-method-test/1.0"})
    r.raise_for_status()
    import hashlib
    digest = hashlib.sha256(r.content).hexdigest()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    docs: dict[str, Any] = {}
    rawdir = OUT / "raw" / name.lower()
    rawdir.mkdir(parents=True, exist_ok=True)
    (rawdir / "source.zip").write_bytes(r.content)
    for member in z.namelist():
        if not member.endswith((".yaml", ".yml")):
            continue
        try:
            doc = yaml.safe_load(z.read(member).decode("utf-8"))
        except Exception:
            continue
        docs[member] = doc
    return docs, digest


def text_blob(doc: Any) -> str:
    try:
        return json.dumps(doc, ensure_ascii=False).upper()
    except Exception:
        return str(doc).upper()


def fnum(x: Any) -> float | None:
    try:
        return float(x)
    except Exception:
        return None


def qualifier_energy(dep: dict[str, Any], fallback: str = "") -> float | None:
    candidates = []
    for q in dep.get("qualifiers") or []:
        qn = str(q.get("name", "")).upper()
        qv = q.get("value")
        if "SQRT" in qn or "ENERGY" in qn or "GEV" in str(qv).upper():
            candidates.append(qv)
    candidates.append(fallback)
    import re
    for c in candidates:
        s = str(c)
        nums = re.findall(r"(?<![\d.])(1(?:8[0-9]|9[0-9])|20[0-9])(?:\.\d+)?", s)
        if nums:
            return float(nums[0])
    return None


def nominal_energy(e: float | None) -> int | None:
    if e is None:
        return None
    i = int(np.argmin(np.abs(NOMINAL_E - e)))
    if abs(float(NOMINAL_E[i]) - e) > 2.5:
        return None
    return int(NOMINAL_E[i])


def extract_muon_angular_profiles(docs: dict[str, Any], experiment: str) -> dict[int, tuple[np.ndarray, np.ndarray]]:
    profiles: dict[int, list[tuple[np.ndarray, np.ndarray]]] = {}
    inventory = []
    for fname, doc in docs.items():
        if not isinstance(doc, dict) or fname.endswith("submission.yaml"):
            continue
        blob = text_blob(doc)
        is_muon = ("MU+ MU-" in blob or "MUON" in blob or "MU+MU-" in blob)
        if not is_muon:
            continue
        ivs = doc.get("independent_variables") or []
        dvs = doc.get("dependent_variables") or []
        if not ivs or not dvs:
            continue
        xvar = ivs[0]
        xname = str((xvar.get("header") or {}).get("name", "")).upper()
        # Angular profile only: the independent variable must be an angle/cos(theta)-like quantity.
        if not ("COS" in xname or "THETA" in xname or "ANGLE" in xname):
            continue
        xvals = xvar.get("values") or []
        x = []
        for xv in xvals:
            v = fnum(xv.get("value"))
            lo = fnum(xv.get("low")); hi = fnum(xv.get("high"))
            if v is None and lo is not None and hi is not None:
                v = 0.5 * (lo + hi)
            x.append(v)
        for dep in dvs:
            yname = str((dep.get("header") or {}).get("name", "")).upper()
            # Exclude asymmetry scalars; keep differential/cross-section-like angular series.
            if "ASYM" in yname or "A_FB" in yname or "AFB" in yname:
                continue
            vals = dep.get("values") or []
            y = [fnum(v.get("value")) for v in vals]
            if len(y) != len(x) or len(y) < 5:
                continue
            ok = np.asarray([a is not None and b is not None for a, b in zip(x, y)], dtype=bool)
            if int(ok.sum()) < 5:
                continue
            xa = np.asarray([float(v) if v is not None else np.nan for v in x])[ok]
            ya = np.asarray([float(v) if v is not None else np.nan for v in y])[ok]
            order = np.argsort(xa); xa = xa[order]; ya = ya[order]
            if xa.max() - xa.min() < 0.5:
                continue
            e = nominal_energy(qualifier_energy(dep, fallback=fname + " " + blob[:1000]))
            if e is None:
                continue
            profiles.setdefault(e, []).append((xa, ya))
            inventory.append({"file": fname, "energy": e, "x_name": xname, "y_name": yname, "n": len(xa)})
    (OUT / f"{experiment.lower()}_muon_inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    # If multiple candidate dependent variables exist at one energy, choose the longest series only.
    chosen = {}
    for e, arr in profiles.items():
        arr.sort(key=lambda p: len(p[0]), reverse=True)
        chosen[e] = arr[0]
    return chosen


def common_problem_table(profiles: dict[int, tuple[np.ndarray, np.ndarray]], energies: list[int]) -> dict[str, list[float]]:
    table: dict[str, list[float]] = {"angle": GRID.tolist()}
    for e in energies:
        x, y = profiles[e]
        lo = max(float(x.min()), float(GRID.min())); hi = min(float(x.max()), float(GRID.max()))
        if hi <= lo:
            continue
        # GRID is deliberately fixed before validation; interpolation is numerical alignment only.
        table[f"E{e}"] = np.interp(GRID, x, y).astype(float).tolist()
    return table


def relation_map(output: dict[str, Any]) -> dict[tuple[str, str], float]:
    if output.get("type") == "hybrid_scan":
        output = output.get("direct") or {}
    rels = output.get("relations") if isinstance(output, dict) else None
    if not isinstance(rels, list):
        return {}
    out = {}
    for r in rels:
        a = str(r.get("a")); b = str(r.get("b"))
        if a == "angle" or b == "angle":
            # Keep angle relations too: they are part of the raw measurement graph, not a physics formula.
            pass
        try:
            v = float(r.get("pearson"))
        except Exception:
            continue
        out[tuple(sorted((a, b)))] = v
    return out


def direct_validation_graph(table: dict[str, list[float]]) -> dict[tuple[str, str], float]:
    keys = list(table)
    vals = {k: np.asarray(table[k], float) for k in keys}
    out = {}
    for i, a in enumerate(keys):
        for b in keys[i+1:]:
            if np.std(vals[a]) <= 0 or np.std(vals[b]) <= 0:
                r = 0.0
            else:
                r = float(np.corrcoef(vals[a], vals[b])[0, 1])
            out[tuple(sorted((a, b)))] = r
    return out


def blind_score(pred: dict[tuple[str, str], float], truth: dict[tuple[str, str], float]) -> tuple[float, dict[str, Any]]:
    common = sorted(set(pred) & set(truth))
    if not common:
        return 0.0, {"matched_edges": 0, "cosine": None, "rmse": None}
    p = np.asarray([pred[k] for k in common], float)
    q = np.asarray([truth[k] for k in common], float)
    den = float(np.linalg.norm(p) * np.linalg.norm(q))
    cosine = float(np.dot(p, q) / den) if den > 0 else 0.0
    # map [-1,1] to [0,1]; no success threshold is introduced.
    score = 0.5 * (cosine + 1.0)
    rmse = float(np.sqrt(np.mean((p - q) ** 2)))
    return score, {"matched_edges": len(common), "cosine": cosine, "rmse": rmse,
                   "edges": [{"edge": list(k), "discovery": pred[k], "validation": truth[k]} for k in common]}


def permuted_null(table: dict[str, list[float]], seed: int) -> dict[str, list[float]]:
    rng = np.random.default_rng(seed)
    out = {"angle": list(table["angle"])}
    for k, v in table.items():
        if k == "angle":
            continue
        a = np.asarray(v, float).copy(); rng.shuffle(a); out[k] = a.tolist()
    return out


def main() -> None:
    delphi_docs, delphi_sha = download_yaml_archive("DELPHI", SOURCES["DELPHI"])
    opal_docs, opal_sha = download_yaml_archive("OPAL", SOURCES["OPAL"])
    D = extract_muon_angular_profiles(delphi_docs, "DELPHI")
    O = extract_muon_angular_profiles(opal_docs, "OPAL")
    common_e = sorted(set(D) & set(O) & set(int(x) for x in NOMINAL_E))
    if len(common_e) < 4:
        raise RuntimeError(f"Need >=4 common muon angular energies, found {common_e}")

    # Validation data are parsed here by the external experiment driver, but never placed in the Problem payload.
    # Strategy/analyzers see only DELPHI tables.
    memory = OUT / "strategy_memory.json"
    scans = OUT / "scans"
    if memory.exists(): memory.unlink()
    engine = ScannerEngine(memory, scans)

    rounds = []
    for ridx, drop in enumerate(JACKKNIFE_DROPS):
        energies = [e for e in common_e if e != drop]
        discovery_table = common_problem_table(D, energies)
        validation_table = common_problem_table(O, energies)
        truth = direct_validation_graph(validation_table)
        null_truth = direct_validation_graph(permuted_null(validation_table, 20260817 + ridx))

        for strategy in ("direct", "analogy", "hybrid"):
            problem = Problem(
                title=f"DELPHI muon angular relation graph round {ridx}",
                description="Blind cross-detector relation discovery from DELPHI muon angular distributions",
                domain="hep-ex real data",
                tags=["DELPHI", "muon", "angular", "blind-validation"],
                payload={"table": discovery_table},
                constraints={"validation_hidden_from_analyzer": True, "dropped_nominal_energy": drop},
            )
            rec = engine.scan(problem, force_strategy=strategy)
            pred = relation_map(rec.learner.output)
            score, details = blind_score(pred, truth)
            null_score, null_details = blind_score(pred, null_truth)
            engine.validate_scan(rec, score, details={
                "validator": "OPAL muon angular relation graph",
                "validation_record": "ins628491",
                "discovery_record": "ins699726",
                "nominal_energies": energies,
                "main": details,
                "permuted_null": {"score": null_score, **null_details},
            })
            rounds.append({"round": ridx, "drop": drop, "strategy": strategy, "score": score,
                           "null_score": null_score, "matched_edges": details["matched_edges"],
                           "rmse": details["rmse"], "cosine": details["cosine"]})

    # Final free routing after 3 externally validated runs per strategy.
    full_table = common_problem_table(D, common_e)
    final_problem = Problem(
        title="DELPHI muon angular relation graph final free routing",
        description="Choose analysis strategy using only accumulated external validation memory",
        domain="hep-ex real data",
        tags=["DELPHI", "muon", "angular", "blind-validation"],
        payload={"table": full_table},
        constraints={"validation_hidden_from_analyzer": True},
    )
    final = engine.scan(final_problem)

    # Independent fresh-memory negative routing control.
    fresh_memory = OUT / "fresh_memory.json"
    if fresh_memory.exists(): fresh_memory.unlink()
    fresh_engine = ScannerEngine(fresh_memory, OUT / "fresh_scans")
    fresh = fresh_engine.scan(final_problem)

    stats = {s: engine.memory.strategy_stats(s) for s in ("direct", "analogy", "hybrid")}
    summary = {
        "experiment": "lep_muon_blind_feedback",
        "status": "real HEPData cross-detector strategy-feedback test",
        "discovery": {"experiment": "DELPHI", "record": "ins699726", "sha256": delphi_sha},
        "validation": {"experiment": "OPAL", "record": "ins628491", "sha256": opal_sha},
        "common_nominal_energies_GeV": common_e,
        "measurement": "muon-pair angular distributions only; no hadron/atom channel",
        "analyzer_input": "DELPHI only",
        "external_validator": "OPAL relation-vector cosine similarity, mapped linearly from [-1,1] to [0,1]",
        "no_success_threshold": True,
        "rounds": rounds,
        "strategy_stats_after_real_validation": stats,
        "final_free_strategy": final.learner.strategy,
        "fresh_memory_control_strategy": fresh.learner.strategy,
        "baseline_strategy_all_scans": "direct",
        "operator_modified": False,
        "physics_formula_injected": False,
        "notes": [
            "The current analogy strategy emits memory matches rather than a numerical relation graph; if it makes no testable relation prediction its external score is 0 by construction.",
            "The current hybrid strategy contains the same direct relation scan plus memory retrieval; this test does not add a special hybrid advantage.",
            "The test measures whether the present learner can use real blind validation feedback; it does not claim new physics.",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
