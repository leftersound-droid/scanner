# Kísérleti archívum

A kísérletek vizsgált terület szerint vannak rendezve. Egy kísérlet saját alkönyvtárat kap; benne legyen legalább a futtatható kód és egy rövid README a kérdésről, bemenetről, kontrollról és értelmezési korlátról.

```text
experiments/
├─ r4_projection/        R4→R3 projekció, komplementaritás, latens rendezés
├─ emergent_time/        belső órák, multi-clock, projekciós időjelöltek
├─ electromagnetism/     töltés, komplementer párok, E/B jelleg
├─ operator_dynamics/    önreflexív operátor, front, torlódás, visszaáramlás
├─ gravity_binding/      Eötvös-analóg, kötés, effektív gravitációs tesztek
└─ meta_strategy/        scanner, analógia, negatív memória, stratégiai tanulás
```

## Szabály

A tudományos operátort és a kísérleti feltételeket a scanner/learner nem módosíthatja. A mérési vagy numerikus segédeszközöket külön kell jelölni az elméleti operátortól.

## Eredmények

A futási eredmények alapból `run-data/<terület>/<kísérlet>/` alá kerülnek és nincsenek verziókezelésbe kényszerítve. GitHub Actions futásnál artifactként mentjük őket. A stabil, értelmezett eredmények később külön `results/` összefoglalóba kerülhetnek.

A gyökérben lévő `r4_complement_clock_probe.py` az első beta kontroll örökölt helye; az új kísérletek már a fenti struktúrát használják.
