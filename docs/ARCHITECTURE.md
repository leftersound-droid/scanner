# Architecture

```text
                    ┌─> Layer A: BASELINE ──> direct analysis ─┐
Problem + constraints                                      compare ─> record
                    └─> Layer B: LEARNER ──> memory/router ────┘
                                                  │
                                                  v
                                         recursive graph memory
```

A learner beta módban shadow-only: nem módosíthatja a kísérleti operátort, adatot vagy korlátokat; csak elemzési/visszakeresési stratégiát választhat.

A közös JSON-gráf egyszerre tart kutatási és stratégiai memóriát. Csomóponttípusok: `research`, `experiment`, `result`, `method`, `problem`, `scan`, `strategy`.

Fontos: a gyorsabb stratégia nem automatikusan jobb tudományosan. Futási költséget már a beta mér; tudományos minőséget domain-specifikus validatornak kell adnia (vak teszt, predikciós hiba, invariancia, reziduum, falszifikáció stb.).
