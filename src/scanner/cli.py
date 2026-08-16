from __future__ import annotations
import argparse
import json
from pathlib import Path
from .models import Problem
from .engine import ScannerEngine
from .web.server import serve


def load_problem(path: str) -> Problem:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return Problem(**data)


def main() -> None:
    parser = argparse.ArgumentParser(prog="scanner")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="Run baseline + learner layers")
    run.add_argument("problem")
    run.add_argument("--memory", default="memory/graph.json")
    run.add_argument("--scans", default="run-data/scans")

    web = sub.add_parser("web", help="Start local dashboard")
    web.add_argument("--memory", default="memory/graph.json")
    web.add_argument("--scans", default="run-data/scans")
    web.add_argument("--host", default="127.0.0.1")
    web.add_argument("--port", type=int, default=8765)

    args = parser.parse_args()
    if args.cmd == "run":
        record = ScannerEngine(args.memory, args.scans).scan(load_problem(args.problem))
        print(json.dumps(record.to_dict(), ensure_ascii=False, indent=2))
    else:
        serve(args.memory, args.scans, args.host, args.port)

if __name__ == "__main__":
    main()
