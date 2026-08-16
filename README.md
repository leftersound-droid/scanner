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

Részletesen: [docs/USAGE.md](docs/USAGE.md) · [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Repo felépítése

```text
src/scanner/       motor, memória, router, web
memory/graph.json  bootstrap kutatási + stratégiai gráf
docs/              használat és architektúra
examples/          példa bemenet
tests/             minimális teszt
run-data/scans/    lokális futási naplók (gitignore)
```

## Jelenlegi beta-határ

A keretrendszer futtatható, de a konkrét korábbi R4/operator scannerek még nincsenek automatikusan beágyazva mint domain adapterek. A bootstrap gráf az eddigi kutatási tanulságokat tárolja; új fizikai scanhez a tényleges, változtatás nélküli operátor adapterét külön kell bekötni.
