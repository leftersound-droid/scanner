from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from hepdata_cli.api import Client

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from scanner.engine import ScannerEngine
from scanner.models import Problem
from scanner.analyzers import direct_analysis

spec = importlib.util.spec_from_file_location("lep_core", HERE / "run.py")
core = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(core)

OUT = ROOT / "run-data" / "meta_strategy" / "lep_muon_parallel_original_vs_learner"
OUT.mkdir(parents=True, exist_ok=True)

# Download each official record once. Both branches consume the same parsed data.
client = Client(verbose=True)
docs_by_name: dict[str, dict[str, Any]] = {}
sha_by_name: dict[str, str] = {}
for name, inspire_id in (("DELPHI", "699726"), ("OPAL", "628491")):
    ddir = OUT / "hepdata_cli" / name.lower()
    ddir.mkdir(parents=True, exist_ok=True)
    client.download([inspire_id], file_format="yaml", ids="inspire", download_dir=str(ddir))
    paths = sorted(ddir.rglob("*.yaml")) + sorted(ddir.rglob("*.yml"))
    docs: dict[str, Any] = {}
    h = hashlib.sha256()
    for p in paths:
        blob = p.read_bytes(); h.update(blob)
        try:
            docs[str(p.relative_to(ddir))] = yaml.safe_load(blob.decode("utf-8"))
        except Exception:
            pass
    if not docs:
        raise RuntimeError(f"No parseable HEPData YAML for {name}")
    docs_by_name[name] = docs
    sha_by_name[name] = h.hexdigest()

D = core.extract_muon_angular_profiles(docs_by_name["DELPHI"], "DELPHI")
O = core.extract_muon_angular_profiles(docs_by_name["OPAL"], "OPAL")
common_e = sorted(set(D) & set(O) & set(int(x) for x in core.NOMINAL_E))
if len(common_e) < 4:
    raise RuntimeError(f"Need >=4 common muon angular energies, found {common_e}")

# ORIGINAL SCANNER: fixed direct analyzer, no strategy memory and no learner routing.
original_rounds = []
for ridx, drop in enumerate(core.JACKKNIFE_DROPS):
    energies = [e for e in common_e if e != drop]
    discovery_table = core.common_problem_table(D, energies)
    validation_table = core.common_problem_table(O, energies)
    problem = Problem(
        title=f"Original scanner DELPHI muon round {ridx}",
        description="Fixed direct relation scan; no learner and no strategy memory",
        domain="hep-ex real data",
        tags=["DELPHI", "muon", "angular", "original-scanner"],
        payload={"table": discovery_table},
        constraints={"validation_hidden_from_analyzer": True, "dropped_nominal_energy": drop},
    )
    output = direct_analysis(problem)
    pred = core.relation_map(output)
    truth = core.direct_validation_graph(validation_table)
    null_truth = core.direct_validation_graph(core.permuted_null(validation_table, 20260817 + ridx))
    score, details = core.blind_score(pred, truth)
    null_score, null_details = core.blind_score(pred, null_truth)
    original_rounds.append({
        "round": ridx, "drop": drop, "energies": energies,
        "score": score, "null_score": null_score,
        "matched_edges": details["matched_edges"], "rmse": details["rmse"], "cosine": details["cosine"]
    })

# LEARNER SCANNER: same DELPHI input and same OPAL validator.
memory = OUT / "learner_strategy_memory.json"
if memory.exists(): memory.unlink()
engine = ScannerEngine(memory, OUT / "learner_scans")
learner_rounds = []
for ridx, drop in enumerate(core.JACKKNIFE_DROPS):
    energies = [e for e in common_e if e != drop]
    discovery_table = core.common_problem_table(D, energies)
    validation_table = core.common_problem_table(O, energies)
    truth = core.direct_validation_graph(validation_table)
    null_truth = core.direct_validation_graph(core.permuted_null(validation_table, 20260817 + ridx))
    for strategy in ("direct", "analogy", "hybrid"):
        problem = Problem(
            title=f"Learner DELPHI muon round {ridx}",
            description="Parallel learner branch; OPAL hidden until external validation",
            domain="hep-ex real data",
            tags=["DELPHI", "muon", "angular", "learner"],
            payload={"table": discovery_table},
            constraints={"validation_hidden_from_analyzer": True, "dropped_nominal_energy": drop},
        )
        rec = engine.scan(problem, force_strategy=strategy)
        pred = core.relation_map(rec.learner.output)
        score, details = core.blind_score(pred, truth)
        null_score, null_details = core.blind_score(pred, null_truth)
        engine.validate_scan(rec, score, details={
            "validator": "OPAL muon angular relation graph",
            "main": details,
            "permuted_null": {"score": null_score, **null_details},
        })
        learner_rounds.append({
            "round": ridx, "drop": drop, "strategy": strategy,
            "score": score, "null_score": null_score,
            "matched_edges": details["matched_edges"], "rmse": details["rmse"], "cosine": details["cosine"]
        })

# Free routing after exactly 3 real blind validations per strategy.
full_table = core.common_problem_table(D, common_e)
final_problem = Problem(
    title="Learner final free routing on DELPHI muon data",
    description="Strategy chosen from accumulated OPAL blind-validation memory only",
    domain="hep-ex real data",
    tags=["DELPHI", "muon", "angular", "learner"],
    payload={"table": full_table},
    constraints={"validation_hidden_from_analyzer": True},
)
final_rec = engine.scan(final_problem)
final_pred = core.relation_map(final_rec.learner.output)
final_truth = core.direct_validation_graph(core.common_problem_table(O, common_e))
final_score, final_details = core.blind_score(final_pred, final_truth)

orig_scores = np.asarray([r["score"] for r in original_rounds], float)
orig_null = np.asarray([r["null_score"] for r in original_rounds], float)
summary = {
    "experiment": "lep_muon_parallel_original_vs_learner",
    "data": {
        "discovery": "DELPHI ins699726",
        "validation": "OPAL ins628491",
        "delphi_sha256": sha_by_name["DELPHI"],
        "opal_sha256": sha_by_name["OPAL"],
        "common_nominal_energies_GeV": common_e,
        "channel": "e+e- -> mu+mu- angular distributions only",
    },
    "original_scanner": {
        "definition": "direct_analysis only; no StrategyRouter; no GraphMemory feedback",
        "rounds": original_rounds,
        "mean_score": float(orig_scores.mean()),
        "mean_null_score": float(orig_null.mean()),
    },
    "learner_scanner": {
        "definition": "same direct/analogy/hybrid implementation with external OPAL validation feedback",
        "rounds": learner_rounds,
        "strategy_stats": {s: engine.memory.strategy_stats(s) for s in ("direct", "analogy", "hybrid")},
        "final_free_strategy": final_rec.learner.strategy,
        "final_blind_score": final_score,
        "final_matched_edges": final_details["matched_edges"],
    },
    "controls": {
        "same_downloaded_data_for_both_branches": True,
        "same_interpolation_grid": True,
        "same_jackknife_rounds": True,
        "same_OPAL_validator": True,
        "OPAL_hidden_from_analyzers": True,
        "operator_modified": False,
        "physics_formula_injected": False,
        "success_threshold": None,
    },
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
