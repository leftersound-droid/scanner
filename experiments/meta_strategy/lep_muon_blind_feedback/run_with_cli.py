from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
from typing import Any

import yaml
from hepdata_cli.api import Client

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "run-data" / "meta_strategy" / "lep_muon_blind_feedback"
OUT.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("lep_muon_blind_feedback_core", HERE / "run.py")
core = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(core)

client = Client(verbose=True)
DOWNLOADS: dict[str, list[str]] = {}
for name, inspire_id in (("DELPHI", "699726"), ("OPAL", "628491")):
    ddir = OUT / "hepdata_cli" / name.lower()
    ddir.mkdir(parents=True, exist_ok=True)
    result = client.download([inspire_id], file_format="yaml", ids="inspire", download_dir=str(ddir))
    files: list[str] = []
    if isinstance(result, dict):
        for value in result.values():
            if isinstance(value, (list, tuple)):
                files.extend(str(x) for x in value)
            elif value:
                files.append(str(value))
    if not files:
        files = [str(p) for p in ddir.rglob("*.yaml")]
    DOWNLOADS[name] = files
    print(name, "downloaded yaml files:", len(files))


def cli_loader(name: str, _unused: str) -> tuple[dict[str, Any], str]:
    paths = [Path(p) for p in DOWNLOADS[name]]
    if not paths:
        paths = list((OUT / "hepdata_cli" / name.lower()).rglob("*.yaml"))
    docs: dict[str, Any] = {}
    h = hashlib.sha256()
    for p in sorted(paths, key=lambda q: str(q)):
        if not p.exists() or p.suffix.lower() not in (".yaml", ".yml"):
            continue
        blob = p.read_bytes(); h.update(blob)
        try:
            docs[p.name] = yaml.safe_load(blob.decode("utf-8"))
        except Exception:
            continue
    if not docs:
        raise RuntimeError(f"HEPData CLI returned no parseable YAML for {name}: {paths}")
    return docs, h.hexdigest()


core.download_yaml_archive = cli_loader
core.main()
