# Field / emergent-inertia / complement separation benchmark

## Cél

A Scanner v2 jelenlegi felbontásán megvizsgálni, hogy egy 2×2 kontrollmátrixban különválasztható-e a **térváltozásra adott objektumválasz** és a **komplementer állapot változására adott válasz**.

A kísérlet nem próbál előre tömeg- vagy töltéstörvényt illeszteni. Nem használ Coulomb-, Lorentz-, Newton- vagy kvantumképletet.

## 2×2 szerkezet

Ugyanaz az objektumgeometria és térfogat minden esetben azonos. Két tengely változik:

- `field_1`, `field_2` — két eltérő térállapot;
- `comp_a`, `comp_b` — két komplementer belső állapot.

A scanner négy semleges feature-vektort kap:

- `field_1 / comp_a`
- `field_1 / comp_b`
- `field_2 / comp_a`
- `field_2 / comp_b`

A feature-nevek semlegesek (`f0..fn`), tehát a scanner nem kap előre `mass`, `charge`, `inertia` címkét.

## Mit mérünk?

A négy állapotból három tisztán relációs kontraszt készül:

1. **field contrast** — a tértengely főhatása;
2. **complement contrast** — a komplementtengely főhatása;
3. **interaction residual** — mennyire változik az egyik tengely hatása a másik függvényében.

A field- és complement-kontraszt közötti abszolút koszinusz hasonlóság nyers összekapcsolódási mérőszám. Nem alkalmazunk tudományos küszöböt vagy előre definiált „jó/rossz” határt.

## Kontrollok

- `separated_control`: a két kontraszt külön feature-alterekben él; ez pozitív módszertani kontroll.
- `coupled_control`: a két kontraszt ugyanazon feature-iránnyal van összekötve; ez negatív kontroll.

Ezek **szintetikus kontrollok**, nem fizikai elektron- vagy tömegmodell. Céljuk annak ellenőrzése, hogy a scanner egy későbbi valódi két-részecskés operátortrajektórián képes-e egyáltalán detektálni a szeparációt vagy az összecsatoltságot.

## Következő fizikai lépés

A valódi teszthez nyers, véges kiterjedésű két-részecske/örvény trajektória kell a primitív operátorból, kontrollált térállapotokkal és komplementer belső állapotokkal. Az ellenállási/tehetetlenségi törvényt nem szabad előre beépíteni.
