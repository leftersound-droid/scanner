# Artificial object → field graph test

Cél: több mesterséges, véges 4D objektumot használni szondaként, és ugyanazzal a lokális tér-operátorral mérni a környezet válaszát. A scanner/elemzés nem kap előre `mass`, `charge`, `gravity`, `electric`, `mean` vagy `HF` címkéket.

Objektumcsalád: azonos teljes többletpotenciál, azonos támogatási méret és azonos előírt mozgási ciklus; különbség csak a szimmetria/profil. A család: `symmetric`, `dipole_x`, `quadrupole_xy`, `mixed_xyz`.

A mesterséges objektum merev, külsőleg előírt szonda: minden lépés elején az objektumcellák visszaállnak az adott profilra, majd a környezet egyetlen lokális potenciáláramlási lépést végez. A visszaállításból eredő potenciálinjekció külön mérve van, ezért ez nem zárt konzervatív fizikai rendszernek van beállítva.

A tér–objektum gráf a nyers környezeti válaszból készül: radiális átlagok és szórások több héjon, ezek időbeli átlagai/szórásai, valamint a globális külső válasz és az injekció statisztikái. A szimmetrikus gráfhoz képesti reziduális szerkezetet és gráf-koszinuszokat mérjük.

## Fontos operátor-korlát

A GitHubon jelenleg reprodukálhatóan elérhető 4D kód a `leftersound-droid/szoliton-elektron-modell/src/simulation.ts` fájlban van (blob `0c41e37f7f6020071acdde7f916b3ea44f4c0e01`). Ebben a fékezőfaktor `diffSum/(diffSum + K*n)`, amely nagyobb különbségnél növekvő átfolyást ad. Ez nem azonos a később tárgyalt erős negatív-visszacsatolású operátorral. Ezért a futás az **elérhető operator-candidate** tesztje, nem a legújabb operátor végső fizikai tesztje.

A jó eredmény ezen a szinten: erős közös térválasz-gráf minden objektumnál, plusz szimmetriafüggő reziduális gráfok. A rossz/negatív eredmény: az aszimmetria az egész válaszgráfot erősen összerántja vagy nincs stabil elkülöníthető reziduális szerkezet.
