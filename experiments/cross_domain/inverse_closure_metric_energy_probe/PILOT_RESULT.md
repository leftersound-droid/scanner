# Pilot result — inverse closure / metric–energy probe

**Státusz:** első negatív záródási eredmény + kalibrációs skálázási kontroll.

A futás az `agent/scanner-v2-beta` ág aktuális `self_reflexive_operator.operator_step` implementációjával készült. Az operátorhoz nem került új tag.

## Kalibrációs ág

Kontrollált periodikus R4 csomag:

- háttér `phi = 100`,
- teljes csomagtöbblet alapból `Q = 60`,
- sugár: `1.0, 1.5, 2.0`,
- periódus: `3, 4, 6` scanner-frame,
- külön amplitúdósor: `Q = 30, 60, 120` azonos geometrián és perióduson.

Mért pilot-fit:

```text
V_eff ~ radius^0.834      (csak 3 durva skálapont; nem fizikai térfogattörvény)
live_transfer ~ radius^-0.042   R²_log ~ 0.114 -> nincs érdemi sugárskálázás ebben a pilotban
live_transfer ~ frequency^0.376 R²_log ~ 0.699 -> gyenge/közepes jelölt, még nem invariáns
live_transfer ~ Q^1.000          R²_log = 1.000
```

Az utolsó linearitás ebben a kontrollban az operátor/homogén amplitúdóskálázás szerkezeti tulajdonsága lehet; nem energia-törvény.

## Kényszer megszüntetése

A periodikusan előírt csomag elengedése után 3 szabad readout alatt:

- `V_eff(last)/V_eff(first)` ≈ **1.28–1.88**,
- `Q(last)/Q(first)` ≈ **0.87–0.92**,
- normalizált recurrence distance ≈ **0.54–0.85**.

A csomag tehát azonnal terül; ezen a konfigurációosztályon nem jelent meg önfenntartó zárt objektum.

## Szabad kezdeti áramtopológia kontroll

Azonos kezdeti kompakt csomagot 9 lépésig futtattunk négy kezdeti `previous_flow` állapottal:

| kezdeti flow | Q arány | V_eff arány | RMS-sugár arány | végső recurrence distance |
|---|---:|---:|---:|---:|
| none | 0.747 | 9.739 | 1.632 | 0.963 |
| tangent | 0.751 | 9.707 | 1.630 | 0.962 |
| radial_out | 0.755 | 9.596 | 1.623 | 0.961 |
| w_plus | 0.753 | 9.773 | 1.633 | 0.962 |

A kezdeti tangenciális, radiális vagy `+w` flow nem stabilizálta a csomagot. A különbségek kicsik, a hosszabb távú viselkedés mindegyik esetben szétterülő.

## Következtetés

1. A mostani egyszerű ring/packet mag **nem használható még fizikai részecskereferenciának**.
2. A Compton-frekvencia–térfogat–energia inverz megfeleltetést csak akkor szabad komolyabban illeszteni, ha előbb van önfenntartó periodikus zárt konfiguráció.
3. A következő kísérletnek a korábbi valódi részecske-/orbit-jelölteket kell ugyanilyen `V_eff`, recurrence és skálafüggetlenségi readouttal újramérnie, nem új stabilizáló szabályt hozzáadnia.
4. A `Q -> live_transfer` pontos linearitás hasznos normalizációs kontroll, de önmagában nem fizikai energiaazonosítás.
