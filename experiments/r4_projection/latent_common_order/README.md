# Nonlineáris latens közös rendezés

Kérdés: több, egymástól eltérő nemlineáris R3-projekcióból visszanyerhető-e egy közös rendezési paraméter úgy, hogy a scanner nem kapja meg a rejtett koordinátát és nem kap `time` címkét?

A pozitív kontroll öt monoton, de eltérő alakú projekciót használ; az egyik fordított orientációjú. A scanner rangalapú, orientációfüggetlen közös sorrendet rekonstruál. A negatív kontroll minden megfigyelhető értékkészletét változatlanul hagyja, de a sorok sorrendjét egymástól függetlenül összekeveri.

A belső rejtett rendezést csak a kísérleti harness látja a végső validálásnál. A scanner bemenetében nincs idő, R4-koordináta vagy fizikai törvény.

Futtatás:

```bash
PYTHONPATH=src python experiments/r4_projection/latent_common_order/run.py
```

Kimenet:

```text
run-data/r4_projection/latent_common_order/result.json
```

Értelmezési korlát: siker esetén csak egy közös monoton relációs rendezés rekonstruálhatóságát igazoljuk ezen a szintetikus adaton. Fizikai emergens időhöz külön dinamikai, kauzális és több-órás teszt szükséges.
