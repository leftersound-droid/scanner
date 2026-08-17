from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import math

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('training_film_collision_core', HERE/'run.py')
core=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(core)

# scanner.self_reflexive_operator uses 4-component coordinate tuples also in dimension=3.
r=range(-core.DOMAIN_L1,core.DOMAIN_L1+1)
core.DOMAIN=[(int(x),int(y),int(z),0) for x,y,z in product(r,repeat=3)
             if abs(x)+abs(y)+abs(z)<=core.DOMAIN_L1]
core.DOMAIN_SET=set(core.DOMAIN)
core.INDEX={c:i for i,c in enumerate(core.DOMAIN)}

def component4(center_x: float, theta: float):
    comp={}; cx=float(center_x)
    for x,y,z in product(range(-12,13),repeat=3):
        dx=float(x)-cx; rho=math.hypot(dx,float(y))
        d2=(rho-core.RING_R)**2+float(z*z)
        env=math.exp(-0.5*d2/(core.SIGMA*core.SIGMA))
        ang=math.atan2(float(y),dx)
        val=env*(1.0+0.35*math.cos(3*(ang-theta)))
        c=(int(x),int(y),int(z),0)
        if val>1e-12 and c in core.DOMAIN_SET:
            comp[c]=val
    s=sum(comp.values()); k=core.OBJ_TOTAL/(s+1e-30)
    return {c:v*k for c,v in comp.items()}

core.component=component4
core.main()
