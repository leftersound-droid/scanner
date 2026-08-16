# Two identical particle recursive map

## Cél

Két teljesen azonos részecske segítségével a jelenlegi Scanner v2 felbontásán feltérképezni, hogy az emergens idő, tömeg- és töltésjellegű struktúrából mi azonosítható, mi csak relatív/gauge jellegű, és hol érjük el az elméleti információs határt.

## Szigorú korlát

- nincs beépített Coulomb-, Lorentz-, Newton- vagy kvantumképlet;
- nincs előre adott tömeg- vagy töltésérték;
- nincs külső óra vagy abszolút időskála;
- nincs új fizikai szabály;
- csak a repo jelenlegi mérési képességei és a memóriában ténylegesen jelen lévő korábbi elektron/óra eredmények használhatók;
- a rekurzió akkor áll meg, amikor új, megkülönböztethető invariáns már nem vezethető le a rendelkezésre álló információból.

## Jelenlegi scanner-felbontás

A scanner jelenleg képes több megfigyelhetőből orientációfüggetlen közös monoton sorrendet rekonstruálni, páronkénti relációkat mérni és memóriagráfból korábbi eredményeket visszakeresni. Nincs még nyers két-elektronos R4 operátortrajektória vagy olyan domain adapter, amelyből abszolút tömeg/töltés skála mérhető lenne.

## Értelmezés

A futás egy identifikációs/episztemikus térképet készít, nem elektronfizikai bizonyítást. A „határ” itt azt jelenti, hogy a jelenlegi reprezentációból több, fizikailag különböző mély állapot ugyanazt a megfigyelhető relációs struktúrát adhatja.

GitHub Actions benchmark: `Two identical particle recursive map`.
