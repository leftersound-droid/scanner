from __future__ import annotations
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json

HTML = r'''<!doctype html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Scanner v2 beta</title><style>
body{font-family:system-ui,sans-serif;margin:0;background:#0f1115;color:#e9edf2}header{padding:22px 5vw;border-bottom:1px solid #2b3039}main{padding:24px 5vw;display:grid;gap:18px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.card{background:#171b22;border:1px solid #2b3039;border-radius:14px;padding:16px}h1,h2{margin:.2em 0}.muted{color:#aab4c0}.scan{margin:10px 0;padding:12px;border-left:3px solid #8994a3;background:#141820}code{white-space:pre-wrap}.badge{display:inline-block;padding:3px 8px;border-radius:999px;background:#252c36;margin-right:6px}</style></head><body>
<header><h1>Scanner v2 beta</h1><div class="muted">Baseline + párhuzamos tanuló réteg · közös rekurzív memória</div></header><main><section class="cards" id="stats"></section><section class="card"><h2>Stratégiai memória</h2><div id="strategies"></div></section><section class="card"><h2>Legutóbbi scannek</h2><div id="scans"></div></section><section class="card"><h2>Memóriagráf</h2><div id="graph"></div></section></main>
<script>
async function load(){let s=await (await fetch('/api/state')).json();
let st=document.getElementById('stats'); st.innerHTML=`<div class=card><b>${s.nodes}</b><div class=muted>gráfcsomópont</div></div><div class=card><b>${s.edges}</b><div class=muted>kapcsolat</div></div><div class=card><b>${s.scans.length}</b><div class=muted>scan</div></div>`;
let q=document.getElementById('strategies'); q.innerHTML=Object.entries(s.strategy_stats).map(([k,v])=>`<div class=scan><span class=badge>${k}</span> runs=${v.runs} · mean=${v.mean_ms.toFixed(3)} ms · score=${v.mean_score.toFixed(3)}</div>`).join('')||'<div class=muted>Még nincs tanult stratégia.</div>';
let sc=document.getElementById('scans'); sc.innerHTML=s.scans.slice().reverse().map(x=>`<div class=scan><b>${x.problem.title}</b><div><span class=badge>baseline: ${x.baseline.strategy}</span><span class=badge>learner: ${x.learner.strategy}</span></div><div class=muted>${new Date(x.created_at*1000).toLocaleString()} · ${x.scan_id}</div></div>`).join('')||'<div class=muted>Még nincs scan.</div>';
let g=document.getElementById('graph'); g.innerHTML=`<div class=muted>Utolsó 20 él</div>`+s.recent_edges.map(e=>`<div class=scan><code>${e.source} → ${e.relation} → ${e.target}</code></div>`).join('');}
load();setInterval(load,5000);
</script></body></html>'''


def serve(memory_path: str, scans_dir: str, host: str, port: int) -> None:
    mp, sd = Path(memory_path), Path(scans_dir)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                body, typ = HTML.encode(), "text/html; charset=utf-8"
            elif self.path == "/api/state":
                memory = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {"nodes":[],"edges":[],"strategy_stats":{}}
                scans=[]
                if sd.exists():
                    for p in sorted(sd.glob("*.json"))[-50:]:
                        try: scans.append(json.loads(p.read_text(encoding="utf-8")))
                        except Exception: pass
                payload={"nodes":len(memory.get("nodes",[])),"edges":len(memory.get("edges",[])),"strategy_stats":memory.get("strategy_stats",{}),"recent_edges":memory.get("edges",[])[-20:],"scans":scans}
                body, typ = json.dumps(payload, ensure_ascii=False).encode(), "application/json; charset=utf-8"
            else:
                self.send_response(404); self.end_headers(); return
            self.send_response(200); self.send_header("Content-Type",typ); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
        def log_message(self, fmt, *args): pass
    print(f"Scanner dashboard: http://{host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
