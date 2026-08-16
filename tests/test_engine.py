import json
from pathlib import Path
from tempfile import TemporaryDirectory
from scanner.models import Problem
from scanner.engine import ScannerEngine

def test_parallel_layers_and_recursive_memory():
    with TemporaryDirectory() as td:
        root=Path(td)
        e=ScannerEngine(root/'graph.json', root/'scans')
        p=Problem(title='test relation',description='relation scan',tags=['relation'],payload={'table':{'a':[1,2,3],'b':[2,4,6]}})
        r=e.scan(p)
        assert r.baseline.layer == 'baseline'
        assert r.learner.layer == 'learner'
        assert r.comparison['same_problem'] is True
        data=json.loads((root/'graph.json').read_text())
        assert any(n['kind']=='strategy' for n in data['nodes'])
        assert any(e['relation']=='used_strategy' for e in data['edges'])
