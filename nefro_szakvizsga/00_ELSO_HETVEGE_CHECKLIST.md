# Nefrológiai szakvizsga — ELSŐ HÉTVÉGE checklist

**Útvonal:** hibrid (NotebookLM = kinyerés · Claude = gyártósor) · **Gyökér:** `D:\Szakvizsga`
**Cél:** a hétvége végére **egy** kész, ellenőrzött tétel (a 47-es) és egy bizonyítottan működő rendszer.

*Created using Anthropic Claude* — a megjegyzés maradjon rajta, amíg egy ember át nem nézte és nem validálta.

> **Ne a 70 tételt akard meg a hétvégén.** Egy teljes kör megmutatja, mi nem működik — és akkor még egy tételen kell javítani, nem hetvenen.

---

## Mi változott ebben a ZIP-ben (v5.0)

A módszertani dokumentum **teljesen újraírva** `MODSZERTAN_v5.0.md` néven — minden módosítás a helyére beépítve, nem külön szekcióban.

**A v5.0 ezen felül:** a szkriptek közös része egy fájlba került (`_scriptek/_kozos.py`), és a promptok szó szerinti szövege már csak a `00_PROMPTOK.md`-ben van. **A szkriptek ki- és bemenete változatlan** — 118 soros regressziós diffel ellenőrizve, nulla eltérés.

### ✅ Amivel nincs dolgod — már át van vezetve

| | Mi volt a baj |
|---|---|
| 🔴 **Az `00_INDEX.md` a RÉGI szerkezetet dokumentálta** | `lejart/` almappaként a csatolt mappán **belül** — pontosan az, ami ellen az egész rendszer épült. Ha eszerint építed fel, a lejárt irányelv egy fájlolvasásnyira van. Újraírva |
| **Notebook-névütközés** | `90 – CKD` és `90 – Saját` ugyanazzal a számmal → **`95 – Saját, ELLENŐRZÖTT`**, mind a 70 forráslapon |
| **Anki-mezőütközés** | A CSV most **7 oszlopos** (`…;Tetel;Statusz;Tagek`), `#tags column:7`. Enélkül a piros **NYERS** jelzés soha nem jelent volna meg |
| **`pdf_horgonnyal.py` kihagyta az archívumot** | Javítva: külön szakaszban feldolgozza, és hangos figyelmeztetést ír |
| **Az átvitel modellen ment át** | Most **te** mented a NotebookLM kimenetét fájlba. Így a forrás nem romolhat el, mielőtt bármi ellenőrizné |
| **Jogszabály-hivatkozás** | **Kettős lett:** `[NJT-EUTV-... \| p.012 \| 12. § (3)]` — az oldalszám teszi géppel ellenőrizhetővé, a § az, amit a vizsgán mondasz |
| **Elavult hivatkozások** | `python3` → `python` (Windows), rossz tételsor-fájlnév, megszűnt `hatalyos/` mappa a tesztleírásban |

### 🔧 Hibajavító kör — 20 javított hiba

A szkriptekben **négy olyan hiba volt, ami csendben átengedett volna rossz kártyát**:

| | |
|---|---|
| 🔴 **Részsztringes számellenőrzés** | Az „5" „megtalálható" volt a „45–59"-ben, tehát egy kitalált érték **átment**. Most tokenhatáros |
| 🔴 **Az `Idezet` mezőt senki nem nézte** | Ha a modell az idézetet IS elrontotta, a válasz és az idézet konzisztens maradt, és a kártya átment. Most a forráshoz is hozzámérjük |
| **A `\|` szétesett a táblázatokban** | A `[FORRAS-ID \| p.047]` két cellára tört, és stray `\` maradt a nyomtatott lapon |
| **Hamis „NINCS A FORRÁSBAN"** | A sorvégi elválasztás („kezelé-\nse") és az oldalhatáron átnyúló mondat buktatta az ellenőrzést |

**És egy fogalmi tisztázás:** a horgony `p.NNN` a **PDF fizikai oldalszáma** (1-től, borítóval együtt), nem a lapon nyomtatott szám. A kettő gyakran eltér. Visszakereséskor a PDF-nézegető oldalszám-mezőjét használd. Ez most minden generált `.md` fejlécében ott van.

### 🆕 Új, mert te döntöttél így

**Minden HTML-forrást PDF-be nyomtatsz** — jogszabály, online fejezet. Ezzel az egész lánc egységes lesz: mindennek lesz oldalhorgonya, és minden géppel ellenőrizhető.

A parancsfájl **7/b lépése** megadja a pontos nyomtatási beállításokat. **Kettő közülük nem opcionális:**

| | |
|---|---|
| 🔴 **Fejléc/lábléc KI** | Különben minden oldalra rákerül az URL és a dátum, ami bekerül a kinyert szövegbe és **beszennyezi az idézeteket** |
| 🔴 **Előbb nyisd ki a lenyíló részeket** | Az njt.hu összecsukva mutatja a szakaszokat. Amit nem nyitottál ki, az **nem kerül bele a PDF-be** — és nem fogod észrevenni |

A webes PDF-ek neve **dátumos**: `NJT-EUTV-1997-CLIV-2026-10-08`. Ezek pillanatfelvételek, és fél év múlva látnod kell, mikori állapotot idézel.

### ⚠️ Egy dolog marad, amit program nem tud megakadályozni

**Két tételsor-fájl van** a `00_tetelsor\`-ban, és összekeverhetők. A kézi változatba beírtam egy ⛔ figyelmeztető fejlécet, de **a feltöltés a te kezedben van**: csak a `TETELSOR-NEFROLOGIA-2024-07-25.md` megy a notebookba.

**És a mentés:** ~27 óra munka, egyetlen meghajtón. A parancsfájl **16. lépése** egy soros — futtasd minden hétvége végén.

---

## 0. Előkészítés (~20 perc)

- [ ] **Python 3.9+ telepítve**, `python --version` válaszol *(nem a Microsoft Store-t nyitja meg)*
- [ ] `D:\Szakvizsga` létezik, van rajta **~10 GB** szabad hely
- [ ] A munkakönyvtár ZIP bemásolva `D:\Szakvizsga`-ba
- [ ] ZIP kicsomagolva → **`nefro_szakvizsga\` és `_ARCHIV_LEJART\` EGYMÁS MELLETT**
- [ ] Az ellenőrző parancs **9 fájlt a `_scriptek\`-ben és a tételsort** találta
- [ ] `pip install pymupdf` lefutott

> 🔴 Ha az `_ARCHIV_LEJART\` a `nefro_szakvizsga\`-n **belülre** kerül, a rendszer egyetlen 100%-os védelme elveszik. A ZIP jól csomagolja — **csak ne told be kézzel.**

---

## 1. Anyagbeszerzés (~1,5 óra — a hétvége leghosszabb, legunalmasabb része)

> A tételsor **már a ZIP-ben van**, ezt nem kell beszerezned.

- [ ] `00_LETOLTESI_TERV.md` megnyitva — **forrásoldal szerint haladj, ne tételenként**
- [ ] MANET irányelv-oldal (~40 perc) — *a „Lejárt a biztonsági időkorlát" üzenet a lap tetején **nem hiba**, görgess tovább*
- [ ] KDIGO gyűjtőoldal (~20 perc)
- [ ] AJKD Core Curriculum (~20 perc) — csak a tételekhez tartozókat
- [ ] 🔴 **A 8 vakfolt-tétel fallback-forrásai** *(6, 8, 28–32, 39)* — `00_FORRAS_ID_LISTA.md` → „KÖTELEZŐ FALLBACK". **Most, nem a végén.** Ahol nincs illő AJKD-cikk, oda a tankönyvi fejezet kerül a listára.
- [ ] Közvetlen linkek (~10 perc): hyponatraemia, MHT 2025, MaNET 2023
- [ ] **HTML-oldalak PDF-be nyomtatva** *(jogszabály, online fejezet)* — `Ctrl+P` → Mentés PDF-ként, **fejléc/lábléc KI**, 100%, és előbb **nyisd ki a lenyíló részeket**
- [ ] A webes PDF-ek **dátumos néven** mentve *(`NJT-EUTV-1997-CLIV-2026-10-08`)*, egyből a cél `_pdf\` mappába

> **Minden letöltés után nyisd meg a PDF-et.** Harminc másodperc. Egy bejelentkező oldal is érvényes PDF, szövegréteggel — **ezt egyetlen szkript sem tudja eldönteni helyetted.**

---

## 2. Rendszerezés (~20 perc, ebből 5 gépmunka)

- [ ] **`python _scriptek\futtat.py`** lefutott *(végigvezet: száraz próba → átnevezés → horgonyozás → riport)*
- [ ] A száraz próba tippjei értelmesnek tűntek
- [ ] A fel nem ismert fájlok kézzel átnevezve a `00_FORRAS_ID_LISTA.md` alapján, majd újra lefuttatva
- [ ] `pdf_horgonnyal.py` nem jelzett hiányzó szövegréteget
- [ ] Ha volt `*** FIGYELEM ***` blokk: az archív `.md`-k **csak a `99 – ARCHÍV` notebookba** mennek
- [ ] **Táblázat-ellenőrzés (~15 perc):** 2-3 generált `.md` megnyitva, benne a CKD-stádiumbeosztás, eGFR-kategóriák, albuminuria-besorolás **ép**

> Ami szétesett, azt a néhány oldalt pótold kézzel. Ezek a legfontosabb adatok az egész anyagban.

- [ ] **Ellenőrizve: a `nefro_szakvizsga\` alatt NINCS lejárt anyag** *(az `atnevezo.py` a 2021-es EMMI CKD-irányelvet magától az `_ARCHIV_LEJART\_pdf\`-be mozgatja — ellenőrizd, hogy tényleg ott van)*

---

## 3. NotebookLM — EGY notebook (~1 óra)

- [ ] NotebookLM megnyitva, **`90 – CKD és szövődményei`** notebook létrehozva
- [ ] A 45–55. tételhez tartozó `.md` fájlok feltöltve a `md\` mappákból — **`.md`-t, NE PDF-et**
- [ ] A tételsorból **csak a `TETELSOR-NEFROLOGIA-2024-07-25.md`** töltve fel → **H2**
- [ ] A CKD-irányelvből **csak az EGYIK** változat *(javaslat: `-SUPPL`)* — ne mindkettő
- [ ] A 7.3-as rövidített custom instruction bemásolva
- [ ] **`95 – Saját, ELLENŐRZÖTT` notebook létrehozva, üresen**

> **Ne vond össze a fájlokat egy nagy `.md`-be.** Elveszted a forrásszintű hivatkozást, a frissíthetőséget és a forráshierarchiát.
> **Egy tankönyv viszont marad egy fájl**, akkor is, ha 600 oldal.

---

## 4. Claude beállítása (~30 perc)

- [ ] A **`D:\Szakvizsga\nefro_szakvizsga`** mappa csatolva — **NEM a `D:\Szakvizsga`!**
- [ ] Ellenőrizve: az `_ARCHIV_LEJART\` **nem látszik** a csatolt mappából
- [ ] A 7.2-es teljes agent-definíció bemásolva a projekt-utasításokba

---

## 5. 🔴 A két átvételi teszt — INNEN NEM MÉSZ TOVÁBB, AMÍG NEM ZÖLD

### 5.1 NotebookLM — forráskötöttség

- [ ] Kérdezz valamit, ami **biztosan nincs** a feltöltött anyagban *(pl. egy gyermeknefrológiai dózis)*

| Válasz | |
|---|---|
| `NINCS A FORRÁSOKBAN` | ✅ mehetsz tovább |
| bármi más | ❌ erősítsd a custom instructiont, teszteld újra |

### 5.2 Claude — zárt kontextus

- [ ] Írd be: **„Dolgozd ki a 47. tételt."** — `<forras>` blokk **nélkül**

| Válasz | |
|---|---|
| „Hiányzik a forrás." *(és nem dolgozza ki)* | ✅ mehetsz tovább |
| kidolgozza a tételt | ❌ a betanított tudásából dolgozik — pontosan az, ami ellen a rendszer épült |

- [ ] **Fokozott változat:** *„nézd meg a `01_iranyelv_hu\md\` mappát, és abból dolgozz"* → a helyes válasz továbbra is a **megtagadás**

---

## 6. Az első teljes kör — 47. tétel (~1 óra)

- [ ] **1.** NotebookLM: kinyerő prompt (8.1) → szó szerinti idézetek + horgonyok
- [ ] **2.** **TE** mented a választ `_output\forras\047_forras.md`-be, **UTF-8**-ban *(Ctrl+C → Jegyzettömb)*
- [ ] **3.** `python _scriptek\ellenoriz_idezet.py _output\forras\047_forras.md` → **0 problémás**
- [ ] **4.** Claude, **ÚJ beszélgetés**: gyártás **két körben** *(`00_PROMPTOK.md` 4️⃣)*
  - [ ] Kör 1: `_output\tetelek\047.md` + `_output\ellenorzes\047_forrasjegyzek.md`
  - [ ] Kör 2 *(ugyanott)*: `_output\anki\047_kartyak.csv`
- [ ] **5.** `python _scriptek\ellenoriz_szamok.py _output\anki\047_kartyak.csv` → **nem jelzett eltérést**
- [ ] **6.** Claude, **HARMADIK, FRISS beszélgetés**: minősítés (9.3) — *„Ne javítsd. Csak minősíts."*
- [ ] **7.** **TE, könyvvel:** a forrásjegyzék **A. szakasza** kipipálva, minden 🔢 visszakeresve (~3 perc)
- [ ] **8.** A kész tétel feltöltve a `95 – Saját` notebookba
- [ ] **9.** Anki-import, **felfüggesztve** (`Ctrl+A`, `Ctrl+J`), majd a pipálás után feloldva

> 🔴 **Egy tétel = egy friss beszélgetés.** Ugyanabban a beszélgetésben a 7. tétel hivatkozása a 3. tétel szövegére fog mutatni — formailag tökéletesen, tartalmilag hamisan. **Költsége nulla.**
>
> 🔴 **Nyers kártyát soha nem tanulsz.** Egy bevésett hiba rosszabb, mint egy hiányzó tudás.

---

## 7. Zárás (~10 perc)

- [ ] `_output\` **lementve ZIP-be** *(a parancsfájl 16. lépése)*
- [ ] Ha bármi nem működött: **a prompton javíts, ne a tételen**

---

## A hétvége sikerkritériuma

**Nem** az, hogy sok tételed van. Hanem ez a három:

1. Mindkét átvételi teszt **zöld**
2. A 047-es forrásjegyzék **C. szakasza üres** *(ide semminek nem szabadna kerülnie)*
3. A könyvvel kipipálás **tényleg ment** — megtaláltad az oldalt a horgony alapján

Ha mindhárom megvan, a maradék 69 tétel már futószalag: ~10-12 perc darabja.

---

> **Ellenőrizetlen munkaanyag.** A rendszer kimenete minden esetben ellenőrizendő piszkozat — nem kész tananyag, és végképp nem klinikai döntéstámogatás. A numerikus értékek visszaellenőrzése az eredeti forrásban **nem opcionális lépés.** A magyar szakmai irányelvek hatályosságát mindig az eredeti kibocsátói oldalon ellenőrizd.
>
> Csak olyanokkal oszd meg, akik a forrásanyagot is jogosultak látni.
