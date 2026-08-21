# Scanner / Önreflexív operátor — aktuális állapot

**Dátum:** 2026-08-21

Ez a fájl a projekt kanonikus kutatási állapotmentése. Új kísérlet előtt ezt kell referenciának tekinteni.

## Alapdefiníciók

- Az operátorhoz nem adunk ad hoc stabilizáló vagy fizikai tagot.
- Az operátor külső memória nélküli; a memória a mező/gráf aktuális állapotában él.
- Fizikai effektív tulajdonság nem egyetlen nyers változó, hanem legalább komplementer gráfpár, általánosabban több gráfelem arányából/relációjából származik.
- Tilos közvetlen azonosítás: `J = sebesség`, `phi = töltés`, `Gamma = spin`, stb.
- A fizikai idő emergens; a nyers iteráció nem automatikusan fizikai idő.
- Az R4->R3 projekció karakterisztika-függő transzformáció, nem egyszerű geometriai vetítés.
- Analóg kísérletben reprezentációs skálázás megengedett; emergenciatesztben a skálát a modellből kell mérni.

## Nyers operátor

```text
Delta_ij = (phi_i - phi_j)_+
alpha_ij = Delta_ij / sum_k Delta_ik
beta_ij  = Jprev_ij / sum_k Jprev_ik
C_i      = (sum_j Delta_ij) / N_live
J_ij     = C_i * alpha_ij / (1 + beta_ij)
```

A minimális lokális állapot jelenleg `(phi, J)`.

## Aktuális gráftérkép

```text
                         G_R4
                        /    \
        belső R4 orbit         R3 projekció
              |                    |
      orbit-statisztikák     projekciós statisztikák
              |                    |
     kvantumtulajdonságok    tömegpont / klasszikus
```

Gráfelem-típusok: `L` = lokális, `I` = belső/kiterjedt, `R` = relációs.

Aktuális komplementer jelöltek:
- hely/lokalizáció <-> impulzus-/áramstruktúra,
- lokális részecskeprojekció <-> kiterjedt R4 orbit/fázis,
- spin-szerű analyzer-output <-> globális orientáció/topológiai orbit,
- lokális töltésjelleg <-> fluxus-/topológiai előjel vagy reláció,
- két lokális kimenet <-> közös többobjektumos R4 invariáns.

Általános elv: `Q_eff = F(G1/G2, G3/G4, ...)`, nem `Q_eff = G1`.

## R4->R3 skálázási elv

Ha a jelenség négy koordináta menti karakterisztikus skálái hasonlóak, a kis rács kvázi-euklideszi reprezentáció lehet. Ha valamelyik irány karakterisztikája eltér, a reprezentációt kell skálázni, nem az operátort módosítani.

Aktuális kvantumos skálajelölt:

```text
Lambda4_eff ~ v_* T
chi = v_* T / D3
```

`D3` = projektált R3 méret, `T` = mért belső/emergens periódus, `v_*` = mért kauzális karakterisztika. `chi` emergenciatesztben mérendő; analóg kísérletben reprezentációs arányként használható.

## Tér mint memória

A véges hatásterjedés miatt az aktuális mező korábbi lokális állapotok késleltetett szerkezetét hordozza. Munkahipotézis: véges hatássebesség + periodikus R4 dinamika + térben tárolt állapot -> skálafüggő statisztikai projekció. Makroszkopikusan sok fázis átlagolódhat, mikroszkopikusan kevés orbit-/fázisosztály maradhat elkülönülten. Ez még hipotézis.

## Kvantumág állapota

A jelenlegi tesztobjektum helikális `(phi,J)` lokalizált reprezentáció; nem fizikai elektron.

- coarse lokalizáció: használható,
- környezet- és objektumreláció: jelen van,
- stabil sajátfrekvencia: nincs igazolva,
- felbontásfüggetlen kvantált ág: nincs igazolva,
- kétút-interferencia: nem reprodukált,
- SG-szerű analyzer-érzékenység: részleges, stabil kétállapotúság nincs,
- tunneling exponenciális törvénye: nem reprodukált.

Aktuális hipotézis: kvantumtulajdonságok R4-beli periodikus/közös orbitok statisztikai invariánsai lehetnek.

## Tömegpont / klasszikus ág

A klasszikus tulajdonságok az R4 objektum R3 vetületének statisztikai invariánsai lehetnek. A coarse R3 lokalizáció több R4 skálareprezentáció mellett stabilnak bizonyult, miközben a rejtett R4 szerkezet jelentősen változott. Ez projekciós invariancia-jelölt.

Korrekció: a `J`-bias közvetlen sebességproxyként való használata érvénytelen fizikai azonosítás.

## Koncepcionális részhipotézis — emergens tömeg/idő gráf

**Státusz:** munkahipotézis / rész-eredmény, nem igazolt törvény.

A jelenlegi irány szerint fundamentális tömegpont nincs. A tömeg-/inerciajelleg a nem nulla tárolt potenciál, a potenciál-impulzus és a környező tér potenciál-/áramkarakterisztikájának komplementer relációjából származhat. A tér így nem passzív háttér: a tér–objektum reláció egyszerre vehet részt a lokalizáció és az inerciális válasz kialakulásában.

Natív readout-jelölt tengelyenként:

```text
Sigma_a = < |alpha_a - beta_a| >
```

ahol `alpha` a lokális potenciáleloszlási, `beta` a korábbi árameloszlási komplementer tag. Az R3 irányokra:

```text
Sigma_parallel = Sigma_x
Sigma_perp     = (Sigma_y + Sigma_z)/2
Sigma_iso      = (Sigma_x + Sigma_y + Sigma_z)/3
Sigma_aniso    = Sigma_parallel - Sigma_perp
```

Projekciósan hangolt inerciális tesztben `beta = 0 -> 0.85` mellett a mért `Sigma_iso` kb. 11.7%-kal nőtt, és nem csak a mozgásirányú, hanem a transzverzális komponens is nőtt. Ez az egész tér–anyag komplementer feszültség növekedésének jelöltje, nem puszta hosszanti geometriai torzulás bizonyítéka.

Aktuális tömeg-/inerciajelölt:

```text
M_G(beta) = Sigma_iso(beta) / Sigma_iso(0)
```

Az időgráf-jelölt a natív `alpha/beta` eloszlás magasabb rendű dinamikai karakterisztikájából származik; önmagában egyik elsőrendű tag sem adott reprezentációfüggetlen Lorentz-viselkedést. A jobb jelöltek változási arányok arányai voltak.

A tömeg- és időjelölt közös inverse tesztjében az egyszerű család

```text
K = M_G^a * T_G^b
```

legjobb tesztpontja hozzávetőleg

```text
a ~ +0.4
b ~ -0.4
```

lett, vagyis szerkezetileg:

```text
K ~ (M_G / T_G)^0.4
```

A konkrét `0.4` kitevő **nem** tekintendő fundamentálisnak; a fontosabb részhipotézis a komplementer arány:

```text
R_MT = M_G / T_G
```

mint magasabb rendű gráfkapcsolat. A joint holdout RMSE kb. `0.119` volt a kb. `0.242` konstansóra-baseline-nal szemben, de a reprezentációs szórás és a nagy-sebességű telítődés miatt a szigorú invarianciagate **nem teljesült**.

Koncepcionális gráf:

```text
(phi, J)
   |
   +--> natív komplementer tér–anyag reláció --> M_G
   |
   +--> natív alpha/beta dinamikai reláció  --> T_G
                                                |
                         M_G <--------------> T_G
                                   |
                              R_MT = M_G/T_G
                                   |
                     emergens idő / Lorentz-jelölt
```

Módszertani feltétel: tér- és időskálázást az analóg mérésnél együtt kell kezelni. Kis sebességnél a Lorentz-eltérés könnyen a projekciós/numerikus háttér alatt marad; nagyobb sebességnél a teljes R4 reprezentáció hangolása szükséges. A skálázás analóg input, az abból fennmaradó gráfinvariáns lehet csak emergens jelölt.

## Kauzalitás

Nearest-neighbor nullkontrollban `R_graph(n)=n`. Ez strukturális felső korlát, nem automatikusan a fizikai fénysebesség. A megfigyelhető `c` munkahipotézise R4 kauzális karakterisztika R3-tér/emergens-idő projekciós invariánsa.

## Provenance

Minden kísérleti elem címkézendő:
- `A` — analóg input,
- `S` — strukturális következmény,
- `E` — emergens output,
- `M` — kevert.

Csak az nevezhető emergensnek, ami nem következik közvetlenül az analóg inputból és ekvivalens reprezentációkban is fennmarad.

## Aktuális cél

1. komplementer gráfpárok és magasabb rendű relációk azonosítása,
2. R3 projekció statisztikai invariánsainak feltárása,
3. R4 belső orbitok statisztikai invariánsainak feltárása,
4. nyers karakterisztikus skálák mérése (`D3`, `T`, `v_*`, korrelációs hosszak),
5. az R4->R3 transzformáció formalizálása úgy, hogy az analóg skálázás és az emergens output elkülönüljön,
6. az `M_G`, `T_G` és `R_MT = M_G/T_G` jelöltek reprezentációfüggetlen kontrollja nagyobb rácson és új skálatartományban.

## Stopfeltételek

- Új fizikai tulajdonságonként új kézi paraméter -> sikertelen ág.
- Rácsfelbontással/update-paritással eltűnő kvantálás -> nem fizikai kvantálás.
- Analóg inputból közvetlenül következő output -> nem emergens.
- Ekvivalens R4 reprezentációban elvesző invariáns -> még nem fizikai invariáns.

> **Röviden:** a fizikai tulajdonságok komplementer gráfrelációk effektív statisztikai kimenetei. A klasszikus ág az R3 projekció robusztus statisztikáit, a kvantumos ág az R4 periodikus/orbit- és relációs invariánsokat vizsgálja. A jelenlegi részhipotézis szerint a tömeg/inercia-jelleg és az emergens idő két magasabb rendű, egymással komplementer gráfkarakterisztika lehet; közös arányuk `R_MT = M_G/T_G` Lorentz-szerű inverse jelölt, de még nem reprezentációfüggetlen invariáns.