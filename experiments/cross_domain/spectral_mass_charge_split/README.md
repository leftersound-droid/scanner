# Spectral mass-charge split control

## Cél

A jelenlegi felbontáson azt tesztelni, hogy ugyanannak a mező-válasznak két dinamikai komponense szeparálható-e:

- nagy amplitúdójú, időben elmosódott / átlagolt komponens (tömeg/tehetetlenség-jelölt),
- kisebb amplitúdójú magasfrekvenciás aszimmetria-komponens (töltés-jelölt).

## Hipotézis ezen a felbontáson

A részletes belső szerkezet nincs modellezve. Csak az szükséges, hogy legyen egy gyors belső dinamika és egy külön aszimmetria-csatorna. A kontrollparaméter dimenziótlan sebességarány: chi = v_internal / v_prop. A teszt nem állít fizikai tömeget vagy töltést, csak azt méri, hogy két eltérő spektrális komponens elválasztható-e.

## Kísérleti terv

Három esetet hasonlítunk össze ugyanazzal a mintavételi ablakkal:

1. symmetric: aszimmetria = 0, csak átlagolt komponens;
2. asymmetric: ugyanaz az átlagolt komponens + kis amplitúdójú HF moduláció;
3. coupled-negative-control: a HF amplitúdó mesterségesen együtt változik a mean komponenssel, hogy ellenőrizzük, észlelhető-e az összekapcsolás.

A scanner nem kap `mass`, `charge`, elektronfizikai törvényt vagy küszöböt. A kimenet nyers spektrális és relációs mérőszám.

## Guardrail

Ez szintetikus reprezentációs kontroll. Nem bizonyítja, hogy a primitív R4 operátor valóban létrehozza ezeket a komponenseket. A következő fizikai teszthez nyers véges objektum/örvény operátortrajektória szükséges.
