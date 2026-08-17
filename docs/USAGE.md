# Scanner v2 beta – rövid használat

## 1. Telepítés

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\\Scripts\\activate
pip install -e .
```

## 2. Egy scan futtatása

```bash
scanner run examples/relation_problem.json
```

Ugyanaz a probléma két rétegen fut:

- **baseline**: mindig direkt elemzés, nem használ tanult stratégiai memóriát;
- **learner**: ugyanazt a bemenetet kapja, de a memóriagráf alapján `direct`, `analogy` vagy `hybrid` elemzési stratégiát választhat.

A learner nem változtathatja meg a probléma fizikai operátorát, paramétereit vagy kísérleti feltételeit.

## 3. Webes dashboard

```bash
scanner web
```

Böngészőben:

```text
http://127.0.0.1:8765
```

A dashboard mutatja a memória méretét, a stratégiai statisztikákat, a legutóbbi scanneket, a két réteg választását és a gráf legutóbbi kapcsolatait.

## 4. Új probléma

```json
{
  "title": "kísérlet neve",
  "description": "mit vizsgálunk",
  "domain": "physics",
  "tags": ["r4", "shell"],
  "payload": {},
  "constraints": {"no_extra_rules": true}
}
```

A `payload` domainfüggő. A beta jelenleg általános strukturális scant és numerikus táblán páronkénti korrelációs scant tartalmaz. A konkrét R4/operator kísérletekhez külön adaptert kell bekötni úgy, hogy az eredeti operátor változatlan maradjon.

## 5. Mit tanul a rendszer?

A stratégiai memória maga is ugyanabban a gráfban él. Minden futás után rögzíti a problémát, a választott stratégiát, a visszakeresett korábbi mintákat és a futási költséget. Később domain-validatorral ugyanide kerülhet a predikciós/falszifikációs minőségi pontszám is.
