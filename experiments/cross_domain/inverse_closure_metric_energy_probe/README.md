# Inverse closure / metric–energy probe

## Cél

Az új metrika–idő–részecske munkahipotézis első numerikus tesztje. A kísérlet nem azonosítja közvetlenül a `phi` vagy `J` változót energiával, távolsággal, idővel vagy sebességgel.

Két egymásra épülő kérdést választ szét:

1. **Kalibrációs/inverz ág (`A/M`)** — egy kontrollált, kompakt, periodikus R4 potenciálcsomag R3-projekcióján mérjük, hogyan függnek a natív operátorválaszok a csomag tartalmától, periódusától és projektált effektív térfogatától.
2. **Szabad záródási ág (`E`)** — a kényszert megszüntetjük, illetve külön futásokban csak kezdeti lokális áramtopológiát adunk. Azt mérjük, hogy a csomag külső stabilizáló szabály nélkül kompakt/rekurrens marad-e.

## Guardrail

- Az operátor változatlan: `scanner.self_reflexive_operator.operator_step`.
- Nincs Compton-, Klein–Gordon-, Newton-, Lorentz-, GR- vagy energiaformula az operátorban.
- Nincs damping, threshold, confinement, cooling vagy kézi stabilizálás.
- A periodikus csomag geometriája, periódusa és teljes többletpotenciálja **analóg input**, ezért ezekből közvetlenül következő összefüggés nem nevezhető emergensnek.
- A szabad elengedés utáni fennmaradás/szétesés valódi operátorkimenet.

## Mért mennyiségek

A projektált R3-csomag küszöbfüggetlen effektív térfogata inverse-participation formában:

```text
V_eff = (sum q_i)^2 / sum(q_i^2)
q_i   = max(projected_phi_i - projected_background_i, 0)
```

Továbbá:

- pozitív projektált csomagtartalom `Q`,
- projektált RMS-sugár,
- R3 és negyedik irányú natív éláram-összegek (`J3`, `J4`),
- teljes live transfer,
- normalizált állapottérbeli recurrence-distance.

A `V_eff` csak elemzési readout; nem kerül vissza az operátorba, és nem tekintendő eleve fizikai térfogatnak.

## Pilot eredmény

A helyi pilot futás összefoglalója a `PILOT_RESULT.md` fájlban található. A jelenlegi tesztmag a szabad elengedés után gyorsan terül; ezért ezen a konfigurációosztályon **nem igazolt önfenntartó zárt részecske**.
