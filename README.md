# Scanner v2 beta

Kétrétegű, párhuzamos kutatási scanner relációs és stratégiai memóriával.

## Lényeg

Ugyanaz a probléma egyszerre két úton fut:

1. **Baseline réteg** – direkt elemzés, stratégiai memória nélkül.
2. **Learner réteg** – ugyanaz a probléma és ugyanazok a korlátok, de a korábbi kutatási + stratégiai memóriából választ `direct`, `analogy` vagy `hybrid` elemzési utat.

A learner beta módban **nem módosíthatja a vizsgált fizikai operátort, paramétereket vagy kísérleti feltételeket**. Csak az elemzés módját és a memória-visszakeresést változtathatja.

A stratégiai gráf maga is a memória része: a rendszer minden futás után eltárolja, mit választott, mit keresett vissza, mennyibe került, és később domain-specifikus validátorral azt is, mennyire volt jó a tudományos eredmény.

## Gyors indítás

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -e .
scanner run examples/relation_problem.json
scanner web
```

Dashboard: `http://127.0.0.1:8765`

Részletesen: [docs/USAGE.md](docs/USAGE.md) · [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) · [experiments/README.md](experiments/README.md)

## Repo felépítése

```text
src/scanner/       motor, memória, router, web, latens relációs eszközök
memory/graph.json  bootstrap kutatási + stratégiai gráf
docs/              használat és architektúra
examples/          példa bemenet
experiments/       területenként rendezett kutatási kísérletek
tests/             minimális regressziós tesztek
run-data/          lokális/GitHub Actions futási eredmények (gitignore)
```

A `experiments/` jelenleg külön területet tart fenn az R4→R3 projekciónak, emergens időnek, elektromágneses jellegnek, operátordinamikának, gravitáció/kötés vizsgálatoknak és a scanner meta-stratégiájának.

## Jelenlegi beta-határ

A keretrendszer futtatható. A generikus relációs scanner mellett már van orientációfüggetlen latens közös-rendezés rekonstruktor és R4→R3 szintetikus kontroll. A konkrét korábbi R4/self-reflexive operator kísérleteket továbbra is külön domain adapterként kell bekötni úgy, hogy az eredeti operátor változatlan maradjon.
