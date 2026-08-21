# Scanner v2 beta

Kétrétegű, párhuzamos kutatási scanner: egy direkt/baseline réteg és egy tanuló stratégiai réteg közös, verziózott memóriával.

> **Kutatási szabály:** a tanuló réteg nem módosíthatja a vizsgált fizikai operátort vagy kísérletet. Csak reprezentációt, visszakeresést és elemzési stratégiát választhat.

## Aktuális kutatási állapot

A projekt kanonikus állapotmentése: **[`PROJECT_STATE.md`](PROJECT_STATE.md)**.

Új kutatási lépés, kísérlet vagy kódmódosítás előtt ebből kell visszaolvasni:

- a nem tárgyalható alapdefiníciókat,
- az aktuális gráftérképet,
- az elfogadott és elutasított kísérleti eredményeket,
- az R4 -> R3 projekciós/skálázási elvet,
- a provenance-címkéket (`A`, `S`, `E`, `M`),
- a nyitott hipotéziseket és stopfeltételeket.

### Rövid állapot

A jelenlegi modellben egy fizikai effektív tulajdonság **nem egyetlen mezőváltozó**, hanem legalább komplementer gráfpár, általánosabban több gráfelem arányából/relációjából származó statisztikai kimenet.

A kutatási gráf két fő ága:

```text
                         G_R4
                        /    \
        belső R4 orbit         R3 projekció
              |                    |
      orbit-statisztikák     projekciós statisztikák
              |                    |
     kvantumtulajdonságok    tömegpont / klasszikus
```

A fő nyitott probléma az **R4 -> R3 karakterisztika-függő transzformáció** formalizálása. Kvantumos rezsimben az aktuális skálajelölt:

```text
Lambda4_eff ~ v_* T
chi = v_* T / D3
```

ahol `D3`, `T` és `v_*` emergenciatesztben mérendő karakterisztikák, nem előre beírt fizikai skálák.

## Kötelező provenance

Minden kísérleti elem címkézendő:

- `A` — analóg input
- `S` — strukturális következmény
- `E` — emergens output
- `M` — kevert analóg/emergens

## Fejlesztési szabály

A `PROJECT_STATE.md` a kutatás **source of truth** fájlja. Ha egy új eredmény megváltoztatja a gráftérképet vagy valamely alaphipotézist, először ezt a fájlt kell frissíteni, majd a kódot/README-t.

A teljes v2 beta implementáció az `agent/scanner-v2-beta` ágon készül.