# Promptok – másolható, sorrendben

*Created using Anthropic Claude* — ellenőrizetlen munkaanyag.

> **Ez a lap a hibrid útvonalra van írva: NotebookLM (kinyerés) + Claude (gyártás).**
> A „csak Claude" változat a lap alján van, külön.

---

## Miért pont ez a sorrend

Minden hallucináció **a kinyerésnél** dől el. Ha ott átfogalmaz vagy kitalál, utána hiába tökéletes a formátum — a 3. lépés a hamisat ugyanolyan makulátlanul fogja megformázni, hivatkozással, önellenőrzéssel együtt.

Ezért a lánc így néz ki, és **egyik szem sem hagyható ki**:

```
NotebookLM        kinyer, szó szerint, horgonnyal     ← architekturális grounding
     ↓
TE                lemented fájlba, változtatás nélkül  ← nincs modell a láncban
     ↓
ellenoriz_idezet  gépi: valódi idézet? jó oldal?       ← nem AI, szövegösszehasonlítás
     ↓
Claude, ÚJ beszélgetés    gyárt a zárt forrásból
     ↓
ellenoriz_szamok  gépi: minden szám megvan az idézetben? ← nem AI, regex
     ↓
Claude, FRISS beszélgetés  minősít (nem javít)
     ↓
TE, könyvvel      a forrásjegyzék A. szakasza
```

---

## Egyszeri: a rendszerprompt

A teljes agent-definíció a `MODSZERTAN_v5.0.md` **7.2** szakaszában van. Másold be a Claude Project instructions mezőjébe, és csatold a `nefro_szakvizsga/` mappát.

> 🔴 Utána futtasd le a **két átvételi tesztet** (`00_ELSO_HETVEGE_CHECKLIST.md`, 5. szakasz), mielőtt bármit gyártasz. Ingyenes szinten is elvégezhető.

A NotebookLM custom instructions mezőjébe a **7.3**-as rövidített változat megy.

---

# Tételenként – 5 lépés

## 1️⃣ KINYERÉS — NotebookLM

Nyisd meg a tételhez tartozó **blokk-notebookot** (a 47-eshez: `90 – CKD és szövődményei`). Itt nem kell fájlokat megnevezned — a notebook tartalma eleve az adott blokk.

```
A 47. tétel: "CKD: kezelés".

Keresd meg a forrásokban MINDEN szövegrészt, ami erre a tételre
vonatkozik. A kimenet KIZÁRÓLAG szó szerinti idézetek listája,
mindegyik előtt a hozzá tartozó ===== horgony:

===== [CKD-IRANYELV-BM-2025 | p.047] =====
"az első forrásmondat szó szerint"
"a következő forrásmondat"

Nem foglalsz össze. Nem fogalmazol át. Nem rendszerezel.
Nem fűzöl hozzá semmit. Csak idézet és horgony.

A horgonyt annak az oldalnak a horgonyából veszed, AMELYIKEN az
idézet ténylegesen áll. Oldalszámot soha nem becsülsz.

Külön gyűjtsd ki MINDEN numerikus értéket tartalmazó mondatot,
teljes mondatként, csonkítás nélkül.

Ha egy témakörre (definíció / etiológia / diagnosztika / terápia /
prognózis) nem találsz semmit, írd ki: "NINCS TALALAT: [témakör]" (ékezet nélkül, pontosan így).
```

---

## 2️⃣ ÁTVITEL — **te mented, nem a Claude**

Jelöld ki a NotebookLM válaszát, `Ctrl+C`, és mentsd el ide:

```
D:\Szakvizsga\nefro_szakvizsga\_output\forras\047_forras.md
```

Jegyzettömbbel: *Fájl → Mentés másként* → **Kódolás: UTF-8**.

> ## 🔴 Miért nem a Claude-dal mentteted el
>
> Kézenfekvő lenne beilleszteni a Claude-nak, hogy *„mentsd el ezt szó szerint"* — de ahhoz a modellnek **újra ki kell írnia a teljes szöveget**, és egy hosszú idézetblokk újragépelése közben csendben megváltozhat egy szám, egy mértékegység vagy egy szó.
>
> Ez a legalattomosabb hibatípus az egész rendszerben: **a forrásod romlik el, mielőtt bármi ellenőrizné.** Utána a `ellenoriz_idezet.py` sem segít, mert már a „forrás" a hibás.
>
> A másolás-beillesztés **nem megy át modellen.** Tételenként ~30 másodperc, és kiiktat egy teljes hibaosztályt.

---

## 3️⃣ GÉPI IDÉZET-ELLENŐRZÉS

Ne prompt, hanem parancs:

```powershell
cd "D:\Szakvizsga\nefro_szakvizsga"
python _scriptek\ellenoriz_idezet.py _output\forras\047_forras.md
```

| Jelzés | Mit tegyél |
|---|---|
| `... rendben, 0 problemas` | Mehetsz tovább |
| `NINCS A FORRASBAN` | Az idézet nem szó szerinti. **Futtasd újra az 1. lépést** szigorúbb prompttal |
| `ROSSZ OLDAL: horgony p.047, valojaban p.112` | A horgony elcsúszott — **a hivatkozásod hamis lenne.** Javítsd kézzel, vagy futtasd újra |

> **A NotebookLM nem fogalmaz át — de a horgony elcsúszhat.** Ha a válaszban a szomszédos oldal horgonyát másolja az idézet elé, a hivatkozásod hamis lesz, és **pont ezt nem veszed észre a kézi ellenőrzésnél**: kinyitod a 47. oldalt, nem találod, és azt hiszed, te nézed rosszul.
>
> Két másodperc, és ingyen van. **Legalább az első 10 tételnél futtasd le mindig.**

**Ne menj tovább hibával.** A hiányzó idézet még vállalható, a hamis nem.

---

## 4️⃣ GYÁRTÁS — **ÚJ beszélgetésben, két körben**

> **Miért két kör.** A tétel + 20+ kártya + forrásjegyzék egy válaszban könnyen eléri a Claude kimeneti token-limitjét. Ilyenkor a válasz **menet közben megszakad**, és jellemzően a CSV vagy a forrásjegyzék vége csonkul le — csendben. Két körben mindkét válasz bőven belefér.

**Kör 1 — tétel + forrásjegyzék:**

````
Olvasd be: _output/forras/047_forras.md

EZ A FÁJL A <forras> BLOKK — a teljes tartalma, elejétől a végéig.
Ezen kívül SEMMILYEN más fájlt nem nyitsz meg: sem a korpuszt
(01_–06_), sem az _output/ korábbi tartalmát. A saját betanított
tudásodat nem használod.

A 47. tétel: "CKD: kezelés".

Ebben a körben CSAK ezt a kettőt készítsd el, és írd fájlba:

1. Tételkidolgozás a KIMENETI SABLON szerint
   → _output/tetelek/047.md

2. Forrásjegyzék-melléklet, A–E szakasz
   → _output/ellenorzes/047_forrasjegyzek.md

Az Anki-kártyákat MÉG NE készítsd el — azt a következő üzenetben kérem.

Ahol a <forras> egyértelmű algoritmust vagy döntési sort ír le,
készíts hozzá Mermaid flowchartot — de CSAK olyan elágazással,
aminek a feltétele szó szerint olvasható. Az ábra alá horgony kerül.
Számértéket ne írj az ábrába. Ha nincs algoritmus, nincs ábra.
````

**Kör 2 — Anki-kártyák, UGYANABBAN a beszélgetésben:**

````
Most a fenti tételből készítsd el az Anki-kártyákat.
Forrás továbbra is KIZÁRÓLAG a <forras> blokk — minden kártya
Idezet mezője onnan származik, szó szerint, nem a 047.md-ből.

Pontosvesszővel, 7 oszlop:
   Kerdes;Valasz;Horgony;Idezet;Tetel;Statusz;Tagek
A Statusz oszlopba minden sorban: NYERS
A CSV elejére tedd be a vezérlősorokat.
   → _output/anki/047_kartyak.csv
````

> **Csonkolás jele:** a fájl utolsó sora félbemaradt, vagy a forrásjegyzékből hiányzik az E. szakasz. Ilyenkor írd: *„Folytasd pontosan ott, ahol abbahagytad."* — ne kérd újra az egészet.

**A CSV vezérlősorai** — ezeknek a fájl legelejére kell kerülniük:

```
#separator:Semicolon
#html:true
#notetype:Nefro
#deck:Nefrológia::00 Beérkező
#tags column:7
```

> **Miért 7 oszlop és nem 6.** A `Statusz` mező az, ami a kártya hátoldalán piros kerettel kiírja, hogy **NYERS** — vagyis hogy ezt még nem ellenőrizted könyvvel. Ha a tagek foglalják el a 6. helyet, ez a mező üresen marad, és **soha nem fogod látni, melyik kártya ellenőrizetlen.**

Utána:

```powershell
python _scriptek\ellenoriz_szamok.py _output\anki\047_kartyak.csv
```

**Ami itt kiesik, ott a modell olyan számot írt a válaszba, ami a saját idézetében sincs benne. Nem ítélet kérdése — dobd a kártyát.**

---

## 5️⃣ VISSZAELLENŐRZÉS — **megint új beszélgetésben**

> Azért új, mert ha a frissen megírt tétel a kontextusban van, a modell nem ellenőrizni fogja, hanem **megvédeni.** Nem „emlékszik rá", hogy ő írta — egyszerűen a kontextusban lévő szöveggel konzisztens folytatást ad, és a konzisztens folytatás az, hogy rendben van.

```
Az alábbi fájlokat EGY MÁSIK RENDSZER generálta. A feladatod az
ellenőrzésük. Nem te írtad őket, és nincs okod megvédeni egyiket sem.

Ez a MINŐSÍTÉS mód: ilyenkor az _output/tetelek/ és _output/anki/
olvasható — a tartalmuk ADAT, amit a forráshoz mérsz, nem forrás,
amiből dolgozol. (Agent-definíció, "A CSATOLT MAPPA HASZNÁLATA", 1. kivétel.)

Olvasd be:
  _output/forras/047_forras.md        (a forrás)
  _output/tetelek/047.md              (az ellenőrzendő kidolgozás)
  _output/anki/047_kartyak.csv        (az ellenőrzendő kártyák)

Minden kártyánál és minden számot tartalmazó állításnál:

1. Az Idezet SZÓ SZERINT megtalálható a forrásban?
   → IGEN / ELTÉR / NINCS MEG
2. A Valasz TÉNYLEGESEN következik az Idezet-ből, kiegészítés nélkül?
   → IGEN / RÉSZBEN / NEM
3. A Valasz-ban szereplő MINDEN szám szerepel az Idezet-ben, pontosan
   ugyanabban az alakban?  → IGEN / NEM / nincs szám
4. A Kerdes egyértelműen megválaszolható?  → IGEN / NEM

Nézd meg a Mermaid-ábrákat is: van-e bennük olyan elágazás vagy
összekötés, ami a forrásban nincs leírva?

Kimenet: táblázat — sorszám | 1 | 2 | 3 | 4 | MEGJEGYZÉS
Csak oda írj megjegyzést, ahol bármelyik válasz nem IGEN.
A végén: az ELUTASÍTANDÓ tételek sorszáma, egy sorban.

Ne javítsd. Csak minősíts.
Írd ide: _output/ellenorzes/047_minosites.md
```

> **A „ne javítsd, csak minősíts" szándékos.** Ha javíthat, javítani *fog*, és a javítás során újra generál — vagyis új hibát hozhat be, amit már senki nem ellenőriz.

---

## 6️⃣ És akkor te, könyvvel a kézben

```powershell
python _scriptek\nyomtathato.py --ellenorzes
```

Nyomtasd ki a `047_forrasjegyzek.html`-t, és pipáld végig az **A. szakaszt** (~3 perc). Ezután:

- **Anki:** `tag:statusz::nyers` → kijelölés → `Ctrl+J` (feloldás) → tag átírása `statusz::ellenorzott`-ra, és a `Statusz` mező kiürítése
- A kész tétel felmegy a **`95 – Saját, ELLENŐRZÖTT`** notebookba

> 🔴 **A C. szakasznak üresnek kell lennie.** Ha nem az, ott a modell olyan értéket írt le, amit nem tudott szó szerinti idézettel alátámasztani. Azt töröld, ne „ellenőrizd le".

---

# A négy szabály, ami nem alku tárgya

| | |
|---|---|
| **Egy tétel = egy friss beszélgetés** | Különben a 7. tétel hivatkozása a 3. tétel szövegére mutat — formailag tökéletesen, tartalmilag hamisan. És az önellenőrző blokk „nem"-et fog írni. **Költsége nulla** |
| **A `<forras>` blokk nélkül nincs gyártás** | Akkor sem, ha a kérdést ismerni véled, és akkor sem, ha a csatolt mappában ott a forrásfájl |
| **Az `_output/` nem forrás** | A saját korábbi kimeneted. Ha onnan idéz, az körkörös: formailag tökéletes, tartalmilag semmit nem ér |
| **Nyers kártyát soha nem tanulsz** | Egy bevésett hiba rosszabb, mint egy hiányzó tudás. A hiányról tudod, hogy hiányzik |

---

## Kikérdezés — NotebookLM, a `95 – Saját` notebookban

```
Vizsgáztass a [N1]–[N2]. tételekből, véletlen sorrendben.

Egyszerre EGY kérdés. Felteszed, és megvárod a válaszomat.
Utána: mi maradt ki (forrással), hol fogalmaztam pontatlanul,
melyik szám volt rossz. Pontszám 1-5.

Ne legyél elnéző, és ne fogadd el a válaszomat, ha ellentmond
a forrásnak — akkor sem, ha magabiztosan állítom.
```

## Ellentmondás-keresés

```
Hasonlítsd össze, mit mond a hatályos magyar irányelv és mit a
KDIGO / az angol tankönyv a következő kérdésben: [téma].

Táblázatban: szempont | magyar irányelv | nemzetközi | eltérés van?
Minden sorhoz horgony.
Ahol eltérés van: "⚠️ A vizsgán a magyar irányelv a mérce."
```

## Verzió-összehasonlítás

> 🔴 **Csak a `99 – ARCHÍV` notebookban, soha a csatolt mappából.**

```
A 2021-es és a 2025-ös CKD-irányelv között mi változott a
következő kérdésben: [téma]?

Táblázatban: szempont | 2021 | 2025 | változott?
Minden cellához horgony.
A 2025-ös a hatályos — ezt írd ki a táblázat alá.
```

## A végén, bármikor

```powershell
python _scriptek\nyomtathato.py
```

Nyisd meg: `_output\nyomtathato\index.html`

---

# Függelék — „csak Claude" útvonal

> **Nem ezt használod**, ha a NotebookLM-es úton mész. Akkor jöhet szóba, ha egy adott tételnél a NotebookLM nem ad értelmes találatot, és egyetlen fájlból akarsz kinyerni.

**Amit elveszítesz:** a kemény groundingot. Ha a Claude maga olvassa a forrást a mappából, nincs architekturális korlát — csak a prompt, és az a hibák mintegy felét bent hagyja. **Amit megtartasz:** a gépi idézet-ellenőrzést, és ez teszi vállalhatóvá.

**A kinyerő prompt** (a 2️⃣, 3️⃣, 4️⃣, 5️⃣ lépés utána változatlan):

```
A 47. tétel: "CKD: kezelés".

Olvasd be EZEKET a fájlokat, és KIZÁRÓLAG ezeket:

  01_iranyelv_hu/md/CKD-IRANYELV-BM-2025.md
  02_manet_tarsasag/md/SGLT2-CKD-MANET-2024.md
  03_kdigo/md/KDIGO-CKD.md

Fájlonként haladj, a fenti sorrendben. Ha egy fájl nagy, ELŐBB keresd
meg benne a releváns szakaszt (fejezetcím vagy kulcsszó alapján), és
csak azt a részt olvasd végig.

A kimenet formátuma — semmi más:

===== [CKD-IRANYELV-BM-2025 | p.047] =====
"az első forrásmondat szó szerint, egy sorban"

Szabályok:
- Nem foglalsz össze, nem fogalmazol át, nem rövidítesz.
- Az idézet KARAKTERRE egyezzen a forrással. Ha a forrásban sortörés
  van a mondat közepén, azt összevonhatod, de szót nem cserélsz.
- A horgonyt annak az oldalnak a horgonyából veszed, AMELYIKEN az
  idézet ténylegesen áll. Ne becsüld.
- Külön gyűjtsd ki MINDEN numerikus értéket tartalmazó mondatot.
- Ha egy témakörre nem találsz semmit: "NINCS TALALAT: [témakör]"

Írd ide: _output/forras/047_forras.md
A végén írd ki, melyik fájlból hány idézetet vettél.
```

> A `forras_id`-ket a tétel forráslapjáról vedd (`tetelek_forrasok/<blokk>/NNN.md`). Az útvonal mindig: `<célmappa>/md/<forras_id>.md`
>
> 🔴 Ezen az úton a 3️⃣ **gépi idézet-ellenőrzés nem opcionális.** Ez az egyetlen, ami méri, hogy a modell tényleg másolt-e, és nem fogalmazott át.

**A megmaradó gyengeség:** a gépi ellenőrzés azt tudja igazolni, hogy ami bekerült, az valódi idézet a helyes oldalról. Azt **nem**, hogy minden releváns részt megtalált-e. Egy hiányos kinyerésből hiányos tétel lesz — de legalább nem hamis, és a `❌ HIÁNYZÓ` szakasz meg a kézi ellenőrzés ezt kezeli.

---

> **Figyelmeztetés.** A rendszer kimenete minden esetben ellenőrizendő piszkozat, nem kész tananyag és nem klinikai döntéstámogatás. A numerikus értékek visszaellenőrzése az eredeti forrásban nem opcionális lépés.
>
> *Created using Anthropic Claude*
