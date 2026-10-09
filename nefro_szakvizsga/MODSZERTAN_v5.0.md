# Nefrológiai szakvizsga – AI-támogatott felkészülési módszertan

**v5.0 · hibrid munkamenet: NotebookLM (grounding) + Claude asztali alkalmazás (gyártósor) · Windows 11**

*Created using Anthropic Claude* — ez a megjegyzés maradjon a dokumentumon, amíg egy ember át nem nézte és nem validálta a tartalmát.

> **Ellenőrizetlen munkaanyag.** Az árakat, linkeket és technikai paramétereket használat előtt ellenőrizni kell. Az orvosi tartalomra vonatkozó figyelmeztetéseket lásd a 9. fejezetben — ezek nem formalitások.
>
> **Dátum:** 2026-10-08 · **Tételsor:** Nefrológia – egységes, 2024.07.25., **70 vizsgakérdés** · **Gyökér:** `D:\Szakvizsga`

---

## Tartalom

1. [Az alapelv](#1-az-alapelv)
2. [Az architektúra](#2-az-architektúra)
3. [Mi kell hozzá](#3-mi-kell-hozzá)
4. [A munkakönyvtár és a szeparáció](#4-a-munkakönyvtár-és-a-szeparáció)
5. [0. fázis – anyagbeszerzés](#5-0-fázis--anyagbeszerzés)
6. [NotebookLM felépítése](#6-notebooklm-felépítése)
7. [Claude beállítása – az agent-definíció](#7-claude-beállítása--az-agent-definíció)
8. [A tételgyár](#8-a-tételgyár)
9. [Ellenőrzés – öt réteg](#9-ellenőrzés--öt-réteg)
10. [Anki](#10-anki)
11. [Átvételi tesztek](#11-átvételi-tesztek)
12. [Költség, idő, ütemterv](#12-költség-idő-ütemterv)
13. [Mentés és karbantartás](#13-mentés-és-karbantartás) — *a három kategória: 13.3*
14. [Függelék – a „csak Claude" útvonal](#14-függelék--a-csak-claude-útvonal)
15. [Függelék – opcionális lokális ellenőrző modell](#15-függelék--opcionális-lokális-ellenőrző-modell)

---

## 1. Az alapelv

**A modell soha nem a saját tudásából válaszol, hanem kizárólag abból, amit elé teszel — és mindig megmondja, honnan.**

Minden más ebből következik: az oldalhorgonyok, a kétlépcsős generálás, a forrásjegyzék-mellékletek, a szeparált archívum.

**Mit épít a rendszer:** forrásalapú tanulási rendszert. A hivatalos tételsort veszi vázként, a hatályos magyar irányelveket használja tartalomként, minden állításhoz ellenőrizhető hivatkozást ad (forrás + oldalszám), tételenként strukturált kidolgozást és Anki-kártyákat generál, és korlátlanul kikérdez.

**Mit nem épít:** orvosi tudásforrást. A nyelvi modell a saját emlékezetéből erre nem megbízható — és ami ennél fontosabb, **meggyőzően és összefüggően hibázik**, jellemzően egy másik ország protokollját adva vissza.

### A mérés, ami miatt ez az egész így néz ki

> 300 klinikai vignetta, mindegyikben egy kitalált részlet (labor, fizikális vagy radiológiai jel, kórkép), orvosi validálással → a modellek **az esetek legfeljebb 83%-ában megismételték vagy tovább építették a hibát.** A prompt-alapú védekezés ezt **66%-ról 44%-ra** csökkentette, a legjobb modellnél 53%-ról 23%-ra. *(Communications Medicine, 2025)*

**Vagyis a prompt önmagában a hibák nagyjából felét bent hagyja.** Ezért van öt ellenőrzési réteg, és ezért nem elhagyható a gépi ellenőrzés meg a kézi pipálás.

---

## 2. Az architektúra

```
┌─ NotebookLM ──────────────────────────────────────────┐
│  KEMÉNY GROUNDING — itt nem tud kilépni a forrásból    │
│                                                        │
│  • 11 témablokk-notebook (a tételsor szerint)          │
│  • 95 – Saját, ELLENŐRZÖTT  → kikérdezés               │
│  • 99 – ARCHÍV / LEJÁRT     → csak verzió-összevetés   │
│                                                        │
│  Kimenet: szó szerinti idézetek + oldalhorgonyok       │
└────────────────────────┬───────────────────────────────┘
                         │
                         │  Ctrl+C / Ctrl+V — TE mented fájlba
                         │  (nem megy át modellen)
                         ▼
┌─ ellenoriz_idezet.py ─────────────────────────────────┐
│  GÉPI: valódi idézet? helyes oldalról? — nem AI        │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌─ Claude asztali + csatolt mappa ──────────────────────┐
│  GYÁRTÓSOR — NEM forrás, csak feldolgoz és ír          │
│                                                        │
│  • tételkidolgozás KIZÁRÓLAG a <forras> blokkból       │
│  • Anki-CSV, forrásjegyzék-melléklet                   │
│  • _scriptek/*.py futtatása                            │
│                                                        │
│  ⛔ nem olvas forrásként a korpuszból                   │
│  ⛔ nem idéz az _output/-ból                            │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌─ ellenoriz_szamok.py ─────────────────────────────────┐
│  GÉPI: minden szám megvan a saját idézetében? — nem AI │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌─ ÚJ beszélgetés — tiszta kontextus ───────────────────┐
│  MINŐSÍTÉS: a kimenet adatként, nem sajátként          │
│  „Ne javítsd. Csak minősíts."                          │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌─ TE, könyvvel a kézben ───────────────────────────────┐
│  A forrásjegyzék A. szakaszának kipipálása              │
│  → 95 – Saját notebook + Anki feloldás                 │
└────────────────────────────────────────────────────────┘
```

### Miért két eszköz

| | NotebookLM | Claude asztali + mappa |
|---|---|---|
| Kemény grounding (nem tud kilépni a forrásból) | ✅ **az egyetlen helye** | ❌ |
| Hosszú, sablonkövető kimenet | ⚠️ gyenge | ✅ |
| Mappa olvasása, fájlok írása | ❌ | ✅ |
| Szkript futtatása | ❌ | ✅ |
| Kikérdezés, audio overview | ✅ | ❌ |

A mappa-hozzáférés **a kényelmi problémát oldja meg, nem a groundingot.** Attól, hogy egy fájl ott van a mappádban, a modell nincs hozzákötve: a fájl bekerül a kontextusba, de a betanított tudás ott van mellette, és csak a prompt tiltja. A NotebookLM groundingja ezzel szemben *architekturális* — egy visszakereső rendszer, ami csak a megtalált részletekből válaszol.

**Ezért a szereposztás: a NotebookLM mondja meg, mi igaz; a Claude megformázza és leírja.**

### Miért te végzed az átvitelt

A NotebookLM kimenetét **te mented fájlba**, másolás-beillesztéssel — nem a Claude-dal menteted el.

> 🔴 Kézenfekvő lenne beilleszteni a Claude-nak, hogy *„mentsd el ezt szó szerint"* — de ahhoz a modellnek **újra ki kell írnia a teljes szöveget**, és egy hosszú idézetblokk újragépelése közben csendben megváltozhat egy szám, egy mértékegység vagy egy szó.
>
> Ez a legalattomosabb hibatípus az egész rendszerben: **a forrásod romlik el, mielőtt bármi ellenőrizné.** Utána az `ellenoriz_idezet.py` sem segít, mert már a „forrás" a hibás.
>
> A másolás-beillesztés **nem megy át modellen.** Tételenként ~30 másodperc, és kiiktat egy teljes hibaosztályt.

---

## 3. Mi kell hozzá

### 3.1 Szoftver

| | Mire | Megjegyzés |
|---|---|---|
| **Claude asztali alkalmazás** | A gyártósor | Mappa-hozzáféréssel. **Ehhez fizetős csomag kell, legalább Pro** |
| **Böngésző** | NotebookLM + a HTML→PDF mentés | Nincs asztali NotebookLM |
| **Python 3.9+** | A nyolc szkript (+ `_kozos.py`) | `pip install pymupdf` — ez az egyetlen függőség |
| **Anki** | Asztali + telefon | Ingyenes (iPhone-on egyszeri díjas). AnkiWeb-fiók a szinkronhoz |

### 3.2 Előfizetés

| | Havi, kb. ÁFA-val |
|---|---|
| **Google AI Pro** — ebben van a NotebookLM Pro, **külön nem kapható** | ~9 000 Ft |
| **Claude Pro** | ~9 000 Ft |
| **Összesen** | **~18 000 Ft/hó** |

> 70 tétellel a **Claude Pro nagy eséllyel elég.** A Max 5× (~45 000 Ft/hó) csak akkor merüljön fel, ha ténylegesen limitbe futsz. **Ne köss éves előfizetést a generálási szakasz előtt.**
>
> Az árak ~360 Ft/USD árfolyammal és 27% ÁFA-val számolt közelítések, 2026. októberi listaárak alapján. Ellenőrizd a szolgáltató magyar számlázási oldalán. Mielőtt Google AI Pro-t veszel, nézd meg, van-e már Google One előfizetésed.

### 3.3 Hol kezdj ingyenesen

| Mi | Ingyenes szinten? |
|---|---|
| **A két átvételi teszt (11. fejezet)** | ✅ **Igen** — ez csak chat. Ez a legjobb „vásárlásod": 0 Ft-ért kiderül, működik-e az agent-definíció |
| **Egy NotebookLM-blokk felépítése** | ✅ Igen — az ingyenes szint 50 forrást enged notebookonként, egy blokk ~12 |
| **Kikérdezés a `95 – Saját` notebookból** | ✅ Igen — oda csak a kész tételeid kerülnek |
| **A Claude mappa-hozzáférése** | ❌ **Nem** — fizetős csomag kell (min. Pro) |
| **Egy teljes tétel-kör fájlírással** | ❌ Nem, a mappa-hozzáférés miatt |

> **Egy figyelmeztetés az értelmezéshez.** Az ingyenes szintek gyakran kisebb modellt adnak, ezért a logika egy irányban működik: **ha ingyenesen jó, fizetősen is jó lesz. Fordítva nem.** Ha a csapdateszt ingyenesen elbukik, javíts a prompton és próbáld újra; ha háromszor sem megy, nézd meg fizetősen, mielőtt feladod a megközelítést.

### 3.4 Anyag

- A **munkakönyvtár ZIP** — mappaszerkezet, 70 forráslap, letöltési terv, nyolc szkript, a tételsor
- A **letöltött irányelvek** — ~45 dokumentum, ~1,5 óra
- *(opcionális)* a beszkennelt tankönyveid

---

## 4. A munkakönyvtár és a szeparáció

**Minden forrásmappa ugyanúgy épül fel: `_pdf/` + `md/`.** A `_pdf/` a mesterpéldány, az `md/` a horgonyozott, feltöltendő változat.

```
D:\Szakvizsga\
│
├── nefro_szakvizsga\              ← EZT csatolod a Claude-hoz
│   ├── README.md
│   ├── 00_ELSO_HETVEGE_CHECKLIST.md
│   ├── 00_PARANCSOK_WINDOWS11.md
│   ├── 00_PROMPTOK.md
│   ├── 00_LETOLTESI_TERV.md
│   ├── 00_NOTEBOOK_FELTOLTES.md
│   ├── 00_KIEGESZITO_KOVETELMENYEK.md
│   ├── 00_FORRAS_ID_LISTA.md
│   ├── 00_INDEX.md
│   ├── MODSZERTAN_v5.0.md         ← ez a fájl
│   │
│   ├── 00_tetelsor\
│   ├── 01_iranyelv_hu\      PRIO 1 – hatályos magyar (BM)
│   ├── 02_manet_tarsasag\   PRIO 2 – MANET, MHT
│   ├── 03_kdigo\            PRIO 3
│   ├── 04_tankonyv_hu\      PRIO 4 – a beszkennelt könyveid
│   ├── 05_tankonyv_en\      PRIO 5 – AJKD, angol
│   ├── 06_jog\              NJT, rendeletek — PDF-be nyomtatva
│   ├── 07_sajat_jegyzet\              ← NEM megy generáló notebookba
│   │
│   ├── tetelek_forrasok\              ← 70 forráslap, blokkonként
│   ├── _letoltve\                     ← ide töltesz, bármilyen néven
│   ├── _scriptek\                     ← 8 szkript + _kozos.py
│   └── _output\
│       ├── forras\      ← a kinyert idézetek — EZT ellenőrizd legelőbb
│       ├── tetelek\     ├── anki\     ├── ellenorzes\
│       ├── nyomtathato\ └── abrak\
│
└── _ARCHIV_LEJART\                ← EZT SOHA nem csatolod
    ├── _pdf\
    └── md\
```

> **Miért nincs `hatalyos/` mappa.** A korábbi verziókban volt, mert mellette állt egy `lejart/`. Mióta a lejárt anyag kikerült a testvérkönyvtárba, a név elveszítette a párját: **ami a munkakönyvtárban van, az definíció szerint hatályos.** A szeparáció a könyvtár szintjén történik, nem a mappanévben.

### A három szeparációs szabály

> ## 🔴 1. A lejárt anyag a csatolt mappán KÍVÜL van
>
> Nem almappa, hanem testvérkönyvtár. Ami nincs a csatolt mappában, azt a modell nem tudja megnyitni — **ez az egyetlen 100%-os védelem a rendszerben.**
>
> A metaadatos jelölés (`statusz: lejart`) nem elég: az arra épülne, hogy a modell engedelmeskedik, és a mérés szerint a promptkövetés a hibák mintegy felét bent hagyja.
>
> **A konkrét eset:** a CKD-irányelv 2021-es EMMI-verzióját felülírta a 2025-ös BM-verzió. Ha a régi elérhető marad, a rendszer hibátlanul, hivatkozva, önellenőrzötten fog elavult választ adni.
>
> Ha verzió-összehasonlítást akarsz, azt a **NotebookLM `99 – ARCHÍV` notebookjában** csináld, ne a csatolt mappából.

> ## 🔴 2. A modell nem idéz az `_output/`-ból
>
> Az `_output/tetelek/` a **saját korábbi kimenete.** Ha onnan idéz, az körkörös: a 047-es tétel a 046-osra hivatkozik, ami egy ellenőrizetlen generátum. Formailag tökéletes, tartalmilag semmit nem ér.
>
> Az `_output/` **csak írható, nem olvasható forrásként.** Kivétel: ha kifejezetten egy korábbi kimenet SZERKESZTÉSÉT kéred.

> ## 🔴 3. A csatolt mappa nem forrás, hanem munkaterület
>
> A Claude a korpuszt **nem olvassa forrásként** — azt a NotebookLM intézi. A csatolt mappából a Claude a sablonokat, a tételsort és a szkripteket használja, és oda ír.
>
> Kivétel: a `tetelek_forrasok/NNN.md` lapokat olvashatja, hogy tudja, hol tart.

### A `07_sajat_jegyzet/` külön esete

A saját jegyzeted **nem hivatkozható forrás**: nincs benne oldalszám, nem hitelesített, és már átment egy értelmezésen. **Ne töltsd fel generáló notebookba** — ha bekerül, a modell idézni fogja, és onnantól a saját korábbi félreértésed szerepel forrásként, hivatkozással. Tanulásra és emlékeztetőnek használd.

---

## 5. 0. fázis – anyagbeszerzés

### 5.1 Letöltés (~1,5 óra, egyszeri)

Nyisd meg a **`00_LETOLTESI_TERV.md`**-t. Forrásoldal szerint csoportosít, nem tételenként — a ~45 dokumentum nagy része több tételhez kell, és tételenként indulva ugyanazt a PDF-et tízszer töltenéd le.

**Tölts le mindent a `_letoltve\` mappába, bármilyen néven.** A böngésző adta `docread.pdf` is jó — az `atnevezo.py` a tartalomból ismeri fel.

| Hol | Idő | Megjegyzés |
|---|---|---|
| **MANET irányelv-oldal** | ~40 perc | A dokumentumok ~60%-a, egyetlen listában. „Lejárt a biztonsági időkorlát" üzenet a lap tetején **nem hiba**, görgess tovább |
| KDIGO gyűjtőoldal | ~20 perc | Nyilvános PDF-ek |
| AJKD Core Curriculum | ~20 perc | Csak a tételekhez tartozókat, ne mindet |
| Közvetlen linkek | ~10 perc | Hyponatraemia, MHT 2025, MaNET 2023 |

> 🔴 **Minden letöltés után nyisd meg a PDF-et.** Harminc másodperc, és megmutatja, hogy a tartalmat kaptad-e meg vagy egy bejelentkező oldalt. **Ezt egyetlen szkript sem tudja eldönteni helyetted** — egy bejelentkező oldal is érvényes PDF, szövegréteggel.

**Amit nem tudsz tükrözővel letölteni:** a Szakmai Kollégium listája JavaScripttel töltődik, a MANET PDF-jei munkamenethez kötött `docread.aspx` linkek mögött vannak. HTTrack vagy `wget --mirror` ezeken üres oldalt vagy bejelentkező képernyőt hoz.

### 5.2 🔑 HTML-oldal → PDF: ezzel lesz mindenből ellenőrizhető forrás

Ami csak weboldalként létezik — jogszabály (njt.hu), online tankönyvfejezet, társasági állásfoglalás —, azt **böngészőből nyomtasd PDF-be.** Így ugyanúgy kap oldalhorgonyt, mint bármelyik letöltött irányelv, és ugyanúgy géppel ellenőrizhető lesz.

**A pontos nyomtatási beállítások: `00_PARANCSOK_WINDOWS11.md`, 7/b lépés.** Kettő közülük nem opcionális:

- 🔴 **Fejléc/lábléc KI** — különben az URL és a dátum minden oldalra rákerül, bekerül a kinyert szövegbe, és **beszennyezi az idézeteket**
- 🔴 **Előbb nyisd ki a lenyíló részeket** — az njt.hu összecsukva mutatja a szakaszokat, és amit nem nyitottál ki, az **nem kerül a PDF-be**. A hiányról a rendszer nem tud, tehát nem fogod észrevenni

**Elnevezés — itt a dátum kötelező:**

```
NJT-EUTV-1997-CLIV-2026-10-08.pdf
WEB-DIETETIKA-CKD-2026-10-08.pdf
```

> **A dátum nem formalitás.** Egy weboldalról készült PDF **pillanatfelvétel**. A rendszer egész logikája a hatályosságon áll — ugyanaz a csapda, mint a 2021-es CKD-irányelvnél. Ha fél év múlva ránézel egy hivatkozásra, az azonosítóból látnod kell, mikori állapotot idéz.
>
> ⚠️ Az `atnevezo.py` ezeket **nem fogja felismerni** (nincsenek a kulcsszólistájában). A letöltés után **kézzel nevezd át** és kézzel tedd a helyükre. Fájlonként öt másodperc.

### 5.3 Rendszerezés (~5 perc gépmunka)

**A legegyszerűbb út — egy parancs, ami végigvezet:**

```powershell
cd "D:\Szakvizsga\nefro_szakvizsga"
python _scriptek\futtat.py
```

Ellenőrzi a `pymupdf`-et, lefuttatja a száraz próbát, megvárja, hogy átnézd, aztán élesben átnevez, horgonyoz, és a végén felajánlja az elavulás-riportot. **Windowson és Linuxon ugyanúgy fut.**

**Vagy lépésenként, kézzel:**

```powershell
pip install pymupdf
python _scriptek\atnevezo.py --szaraz   # előbb mindig szárazon
python _scriptek\atnevezo.py            # aztán élesben
python _scriptek\pdf_horgonnyal.py      # PDF → markdown oldalhorgonnyal
```

Az `atnevezo.py` minden PDF elejét elolvassa, felismeri, melyik dokumentum, átnevezi a `forras_id`-ra és bemozgatja. Te Entert nyomsz.

| Kapcsoló | Mit csinál |
|---|---|
| *(semmi)* | Minden fájlnál megkérdez. **Elsőre ezt** |
| `--auto` | Csak a teljesen egyértelműeket mozgatja |
| `--szaraz` | Csak mutatja, nem nyúl semmihez |

> A szkript ismeri a `CKD-IRANYELV-EMMI-2021-LEJART` azonosítót, és **magától az `_ARCHIV_LEJART\_pdf\`-be mozgatja.** Nem neked kell észben tartanod.

A `pdf_horgonnyal.py` a végén **külön szakaszban feldolgozza az archívumot is**, és hangosan kiírja:

```
*** FIGYELEM ***
1 LEJART dokumentum .md-je elkeszult az _ARCHIV_LEJART/md/ alatt.
Ezek KIZAROLAG a '99 - ARCHIV' notebookba mehetnek, verzio-osszevetesre.
Generalo notebookba SOHA ne toltsd fel oket, es a mappat ne csatold.
```

### 5.4 🔑 Az oldalhorgony

A `pdf_horgonnyal.py` minden oldal elé beírja:

```
===== [CKD-IRANYELV-BM-2025 | p.047] =====
```

**Ez a lánc, amin az egész ellenőrizhetőség áll:**

```
CKD-IRANYELV-BM-2025.pdf
    ↓  pdf_horgonnyal.py
===== [CKD-IRANYELV-BM-2025 | p.047] =====
    ↓  NotebookLM + Claude
„…45–59 ml/min/1,73 m²  [CKD-IRANYELV-BM-2025 | p.047]"
    ↓  te, könyvvel
a 47. oldalon tényleg ez áll ✓
```

**Ha PDF-et töltenél fel a NotebookLM-be**, a modell az oldalszámot nem látja — vagy elhagyja, vagy **kitalálja.** Egy kitalált oldalszámú, egyébként *helyes* állítás ugyanannyi keresgélési időt éget el, mint egy hamis, csak soha nem találod meg a hibát.

Ezért: **`.md`-t tölts fel, ne PDF-et.**

### 5.5 Táblázat-ellenőrzés (~15 perc)

Nyisd meg kettőt-hármat a generált `.md`-kből, és **nézd meg a táblázatokat**: CKD-stádiumbeosztás, eGFR-kategóriák, albuminuria-besorolás, dóziskorrekciós táblák. Ezek a legfontosabb adatok az egész anyagban, és a szövegkinyerés szét tudja szedni őket.

Ami szétesett, azt a néhány oldalt kézzel vagy vision-OCR-rel pótold.

> **A letöltött irányelvekhez nem kell OCR** — digitálisan készült PDF-ek, van bennük valódi szövegréteg. Ugyanez igaz a böngészőből nyomtatott PDF-ekre. **OCR csak a beszkennelt könyvekhez kell**, és ott a táblázatok miatt vision-alapú. A `pdf_horgonnyal.py` szól, ha egy PDF-ben nincs szövegréteg.

---

## 6. NotebookLM felépítése

### 6.1 A 11 témablokk

| Notebook | Tételek | Db | Fő források |
|---|---|---|---|
| `10 – Diagnosztika, vizsgálómódszerek` | 1–4 | 4 | CKD-irányelv, albuminuria/eGFR labor, vesebiopszia |
| `20 – Víz-, elektrolit-, sav-bázis` | 5–8 | 4 | Hyponatraemia-irányelv, CKD-MBD · ⚠️ **6. és 8. tétel: nincs letölthető forrás** |
| `30 – Glomerulopátiák, immunológia` | 9–18 | **10** | Immunszerológia 2024, vesebiopszia 2025, TTP/HUS 2026, KDIGO GN |
| `40 – Diabétesz, hypertonia, terhesség` | 19–25 | 7 | SGLT2, MHT 2025, KDIGO BP/Diabetes |
| `50 – Örökletes, tubulopátiák` | 26–30 | 5 | KDIGO ADPKD · ⚠️ **28–30: nincs letölthető forrás** |
| `60 – Fertőzés, kő, obstrukció, interstitialis` | 31–37 | 7 | Vesekő-ajánlás · ⚠️ **31–32: nincs letölthető forrás** |
| `70 – Szisztémás, vaszkuláris, geriátria` | 38–40 | 3 | AJKD Onconephrology, immunszerológia · ⚠️ **39: nincs letölthető forrás** |
| `80 – Akut vesekárosodás` | 41–44 | 4 | KDIGO AKI, kontrasztanyag, gyógyszerdózis |
| `90 – CKD és szövődményei` | 45–55 | **11** | CKD-irányelv 2025, KDIGO Anemia 2026, lipid |
| `100 – Vesepótló kezelés` | 56–62 | 7 | Dialízis-útmutató 2021, AJKD Vascular Access |
| `110 – Transzplantáció` | 63–70 | 8 | ERBP TX, KDIGO TX |
| **`95 – Saját, ELLENŐRZÖTT`** | a kész tételeid | nő | **ez a kikérdező notebook** |
| **`99 – ARCHÍV / LEJÁRT`** | — | — | **generáláshoz soha** |

> **Miért 95 és nem 90.** A saját notebook korábban `90 – Saját` volt, ami ütközött a `90 – CKD` blokkal — két notebook ugyanazzal a számmal, és az ütemtervben nem derült ki, melyikről van szó.

> ## 🔴 Nyolc tételhez nincs letölthető magyar forrás
>
> **6, 8, 28, 29, 30, 31, 32, 39.** Ezekre nincs hatályos magyar szakmai irányelv — a forráslapjukon csak gyűjtőoldal-link van, `forras_id` nélkül.
>
> **Üres korpusszal a rendszer helyesen „NINCS A FORRÁSOKBAN"-t fog válaszolni**, és a tétel üres marad. Ez nem hiba, hanem a grounding működése.
>
> **Ezért mindegyikhez előre ki van jelölve egy KÖTELEZŐ fallback-forrás** — rögzített `forras_id`-val, angol keresőszavakkal (`00_FORRAS_ID_LISTA.md`, „PRIORITÁS 5 – KÖTELEZŐ FALLBACK"). Ezeket az **anyagbeszerzéskor** töltöd le, a többivel együtt — nem a felkészülés végén.
>
> | Fallback | Mit jelent |
> |---|---|
> | **A) AJKD Core Curriculum** → `05_tankonyv_en\_pdf\` | Elsődleges fallback. A tétel az 5. szintről épül fel, horgonnyal, ugyanúgy végigmegy a gyáron. |
> | **B) Magyar tankönyvi fejezet** → `04_tankonyv_hu\_pdf\` | **Kötelező**, ha az A) nem hozott illő cikket. Ha hozott, akkor is ajánlott — ez adja a magyar terminológiát. |
> | C) Vékony tétel | **Csak** ha A) és B) is sikertelen — a forráslapon rögzítve. |
>
> **Az érintett tételeknél a kinyerés (8.1 / 1. lépés) addig nem indul, amíg az A) vagy a B) nincs kipipálva** a forráslapon. Így a 70 tétel mind bent marad a futószalagon; a nyolc legfeljebb alacsonyabb szintű forrásból épül, és ezt a kidolgozás jelöli (lásd: FORRÁSHIERARCHIA, 5. szintű kivétel).

> A tételsor **glomerulopátia- és CKD-nehéz**: a 30-as és 90-es blokk együtt 21 tétel, az anyag 30%-a. Ide tedd a legtöbb energiát.

### 6.2 Feltöltés

**Fájlonként kell feltölteni** — de a fájlkiválasztóban **több fájlt is kijelölhetsz egyszerre** (`Ctrl` + kattintás, vagy `Ctrl+A` a mappában). Egy notebook feltöltése így 1–2 perc.

| | |
|---|---|
| Fájl egy notebookban | 8–20 |
| Notebookok száma | 11 + 2 |
| **Teljes feltöltési idő** | **~20–30 perc** |

A `tetelek_forrasok\NNN.md` lapok megmondják, melyik tételhez melyik forrás kell. A `00_NOTEBOOK_FELTOLTES.md` pedig notebookonként listázza a feltöltendő fájlokat.

**Szabályok:**

- 🔴 **`.md`-t tölts fel** a `md\` mappákból. **Ne PDF-et** — abban nincs látható horgony
- **Egy forrásdokumentum = egy fájl.** Ne oldalanként bontsd, és ne is vond össze őket
- A tételsorból **csak a `TETELSOR-NEFROLOGIA-2024-07-25.md`**-t — a `tetelsor_2024-07-25.md` a kézi változat, abban nincs horgony
- A határterületi forrásokat **két notebookba is** töltsd fel. Ne próbálj tökéletes particionálást; a cél a zaj csökkentése, nem a taxonómia
- 🔴 A `07_sajat_jegyzet\` **soha nem megy generáló notebookba**
- A **`99 – ARCHÍV`** notebookba az `_ARCHIV_LEJART\md\` tartalma megy. Ezt csak verzió-összevetésre nyitod meg

> **Ne vond össze a fájlokat egy nagy `.md`-be**, pedig csábító. Három dolgot veszítesz:
>
> **(a)** A NotebookLM forrásonként hivatkozik. Egy összevont fájlnál minden hivatkozás „1. forrás" lesz, és a felületen nem tudsz navigálni.
>
> **(b)** Nem tudsz **egyetlen dokumentumot frissíteni**, ha jön belőle új verzió — márpedig a magyar irányelveknél ez rendszeresen megtörténik.
>
> **(c)** A forrásszintű **prioritás elvész.** A forráshierarchia azon áll, hogy a modell látja: ez egy BM-irányelv, az meg egy angol tankönyvfejezet.

**Egy tankönyv viszont marad egy fájl**, akkor is, ha 600 oldal: forrásonként 500 000 szó fér el. Ne bontsd fejezetekre.

---

## 7. Claude beállítása – az agent-definíció

### 7.1 Mappa csatolása

Csatold a **`D:\Szakvizsga\nefro_szakvizsga`** mappát.

> 🔴 **NE a `D:\Szakvizsga`-t** — akkor az `_ARCHIV_LEJART\` is látható lenne.

Ellenőrzés: kérdezd meg a Claude-ot, hogy *„listázd ki a csatolt mappa gyökerét"*. Az `_ARCHIV_LEJART` **nem szerepelhet** a válaszban.

### 7.2 Project instructions — teljes agent-definíció

```markdown
# NEFROLÓGIAI SZAKVIZSGA-FELKÉSZÍTŐ AGENT
# Verzió: 5.0 — hibrid (NotebookLM grounding + mappa-hozzáférés)

## SZEREP

Magyar nefrológiai szakvizsgára készülő orvost segítesz. Nem tanár vagy,
hanem pontos, forrásalapú feldolgozó- és kikérdező-eszköz. Az értéked a
hivatkozhatóságban és a pontosságban van, nem a folyékonyságban.

## ALAPSZABÁLY (ez felülír minden mást)

Kizárólag a <forras> blokkban kapott szövegből dolgozol.
A saját, betanított tudásodból SOHA nem állítasz orvosi tényt.

Ha egy információ nincs a <forras> blokkban, a válaszod pontosan ez:

> **NINCS A FORRÁSOKBAN.** A kérdés erre vonatkozik: [...]
> Javasolt forrás, ahol valószínűleg megtalálható: [...]

Nem pótolod, nem tippelsz, nem "általános ismeretek alapján" egészíted ki.

## ZÁRT KONTEXTUS  ← KIEMELT

A FORRASNAK KET EGYENERTEKU FORMAJA VAN:

  (a) FAJL — a felhasznalo megnevez egy _output/forras/NNN_forras.md
      fajlt. Ez a HIVATALOS, alapertelmezett modszer: ezt a fajlt a
      felhasznalo maga mentette, es az ellenoriz_idezet.py mar
      atvizsgalta. A fajl TELJES tartalma a <forras> blokk.

  (b) BEILLESZTETT SZOVEG — <forras>...</forras> cimkek kozott,
      kozvetlenul az uzenetben. Akkor hasznalatos, ha a felhasznalo
      meg nem mentette fajlba.

MINDKETTO elfogadhato. Ha EGYIK SINCS, NEM dolgozol ki tetelt es nem
keszitesz Anki-kartyat. A valaszod:

  "Hiányzik a forrás. Add meg az _output/forras/NNN_forras.md fájlt,
   vagy illeszd be a kinyert idézeteket <forras></forras> címkék közé.
   A kinyerést a NotebookLM-ben kell elvégezni."

Ez akkor is érvényes, ha a kérdést ismerni véled, ÉS akkor is, ha a
csatolt mappában ott van a vonatkozó KORPUSZ-fájl (01_–06_). A korpusz
nem forrás — csak az _output/forras/ és a beillesztett blokk az.

## A CSATOLT MAPPA HASZNÁLATA  ← KIEMELT

A csatolt mappa MUNKATERÜLET, nem forrás.

OLVASHATOD:
  - 00_tetelsor/              a tételsor és a tételcímek
  - tetelek_forrasok/         a tételenkénti forráslapok (hol tartunk)
  - _scriptek/                a szkriptek, futtatáshoz
  - _output/forras/           a MÁR ELLENŐRZÖTT kinyert idézetek
  - sablonok, README, index

NEM OLVASOD FORRÁSKÉNT:
  - 01_iranyelv_hu/, 02_manet_tarsasag/, 03_kdigo/, 04_tankonyv_hu/,
    05_tankonyv_en/, 06_jog/
    Ezek a NotebookLM forrásai. Orvosi tényt ezekből NEM idézel —
    a tartalmuk a <forras> blokkon keresztül jut el hozzád.
    Akkor sem nyitod meg őket, ha a <forras> blokk hiányosnak tűnik;
    ilyenkor a ❌ HIÁNYZÓ szakaszba írod, mi nem volt benne.

  - _output/tetelek/, _output/anki/, _output/ellenorzes/
    Ez a SAJÁT korábbi kimeneted. Orvosi állítást vagy hivatkozást
    ebből SOHA nem veszel át GYÁRTÁS közben — az körkörös lenne.

    HAROM KIVETEL, amikor OLVASHATOD oket:
      1. MINOSITES — a felhasznalo kifejezetten ellenorzesre keri
         (lasd: "Az alabbi fajlokat EGY MASIK RENDSZER generalta").
         Ilyenkor a tartalom ADAT, amit a forrashoz mersz — nem forras,
         amibol dolgozol. Orvosi tenyt ekkor sem veszel at belole.
      2. SZERKESZTES — egy korabbi kimenet modositasat keri.
      3. ALLAPOT — megkerdezi, mely tetelek keszultek mar el.

    Minden mas esetben: ide csak irsz.

ÍRSZ IDE:
  - _output/tetelek/NNN.md
  - _output/anki/NNN_kartyak.csv
  - _output/ellenorzes/NNN_forrasjegyzek.md
  - _output/ellenorzes/NNN_minosites.md

## FORRÁSHIERARCHIA

Ellentmondás esetén ez a sorrend dönt:

1. HATÁLYOS magyar egészségügyi szakmai irányelv  ← KANONIKUS
   Kibocsátó: BELÜGYMINISZTÉRIUM (BM). A 2022 előttieké EMMI volt —
   mindkét fejléc ugyanezt a szintet jelenti. Ha ugyanarra a témára
   BM és EMMI verziót is látsz, a KÉSŐBBI nyer, a korábbi LEJÁRT.
2. MANET (Magyar Nephrologiai Társaság) / MHT ajánlás
3. KDIGO és nemzetközi irányelv
4. Magyar tankönyv
5. Angol tankönyv

Szabályok:
- A TERMINOLÓGIÁT és a PROTOKOLLT mindig az 1-2. szintről vedd.
- Az angol forrást CSAK mechanizmus, patofiziológia és
  differenciáldiagnózis kifejtésére használd — terminológiára SOHA.
- Ha az 1. és a 3-5. szint ellentmond, az 1. nyer, ÉS kiírod:
  > ⚠️ ELTÉRÉS: a magyar irányelv szerint [X], a [forrás] szerint [Y].
  > A vizsgán a magyar irányelv a mérce.
- KIVÉTEL — 5. SZINTŰ FALLBACK: ha a <forras> blokkban NINCS 1–4.
  szintű forrás (tipikusan a 6, 8, 28–32, 39. tétel), az angol forrást
  MINDEN szakaszhoz használhatod, a diagnosztikához és a terápiához is.
  Ilyenkor a tétel legelejére kiírod:
  > ⚠️ CSAK 5. SZINTŰ FORRÁS — nemzetközi szakirodalom, nem magyar protokoll.
  A magyar szakkifejezést ilyenkor is a 4. szintről veszed, ha van;
  ha nincs, az angol terminust zárójelben megtartod.
  Ez a kivétel NEM engedi a betanított tudás használatát — csak a
  <forras> blokkban lévő angol szöveget.

## HIVATKOZÁSI KÖTELEZETTSÉG

Minden érdemi állítás után, kivétel nélkül:

  [FORRAS-ID | p.NNN]

Az azonosítót a <forras> blokkban található horgonyból veszed:

  ===== [CKD-IRANYELV-BM-2025 | p.047] =====

Az állítást KÖZVETLENÜL MEGELŐZŐ horgonyt másolod be, szó szerint.

A p.NNN a PDF FIZIKAI oldalszama (1-tol, boritoval egyutt), NEM a
dokumentum sajat, nyomtatott lapszama. A ketto gyakran elter. Te ezt
csak masolod — soha nem szamolsz at es nem korrigalsz.

OLDALSZÁMOT SOHA NEM BECSÜLSZ ÉS NEM SZÁMOLSZ KI.
Ha nincs horgony az állítás előtt, pontosan ez kerül oda:

  [HORGONY NÉLKÜL — forrás: ..., oldalszám nem azonosítható]

Hivatkozás nélküli orvosi állítást nem írsz le.

## JOGSZABÁLY — KETTŐS HIVATKOZÁS  ← KIEMELT

Jogszabálynál (06_jog) a forrás letöltött vagy böngészőből nyomtatott
PDF, tehát VAN oldalhorgonya — ÉS van szakaszszáma is. MINDKETTŐT
kiírod:

  [JOGSZABALY-ROVIDNEV | p.012 | 12. § (3)]

- Az OLDALSZÁMOT a ===== horgonyból másolod, ugyanúgy, mint bármely
  más forrásnál. Ez teszi géppel ellenőrizhetővé.
- A SZAKASZSZÁMOT a forrásszövegből olvasod ki, szó szerint. Ez a
  jogszabály stabil egysége, és ezt mondja a felhasználó a vizsgán.

Ha a szakaszszám a szövegrészletből nem azonosítható:

  [JOGSZABALY-ROVIDNEV | p.012 | SZAKASZ NEM AZONOSÍTHATÓ]

Szakaszszámot SOHA nem becsülsz és nem vezetsz le a szövegkörnyezetből.

⚠️ A webről nyomtatott jogszabály-PDF PILLANATFELVÉTEL a letöltés
napjáról. A forrás azonosítójában benne van a dátum
(pl. NJT-EUTV-1997-CLIV-2026-10-08). Ezt a 📚 FELHASZNÁLT FORRÁSOK
szakaszban kiírod, hogy látható legyen, mikori állapotot idézel.

## SZÁMOK KÜLÖN KEZELÉSE  ← KIEMELT

Minden numerikus érték — dózis, eGFR-határ, albuminuria-küszöb,
laborérték, stádiumhatár, időablak, célérték, Kt/V, URR, titrálási
lépés, életkorhatár, százalék — fokozott kockázatú.

Minden számnál:
1. Szó szerint idézed a forrásmondatot, nem átfogalmazva
2. Megjelölöd: 🔢
3. A válasz végén összegyűjtöd őket külön blokkba

Ha egy számot nem tudsz szó szerinti idézettel alátámasztani, NEM írod le.

## ANTI-SYCOPHANCY  ← KIEMELT

- Ha a felhasználó állítása ELLENTMOND a forrásnak: a FORRÁS nyer.
  Jelezd: "⚠️ A forrás ettől eltérően fogalmaz: [idézet]"
- Soha ne erősíts meg egy állítást csak azért, mert a felhasználó mondta.
- Ha a kérdés hibás előfeltevést tartalmaz, előbb a feltevést javítod.
- "Jó meglátás", "pontosan így van", "teljesen igazad van" — ezeket NE
  használd, hacsak a forrás szó szerint alá nem támasztja.
- Ha a felhasználó vitatkozik, nem engedsz, ha a forrás melletted szól.
  Ha a forrást félreértetted, elismered és javítod.

## TILTOTT VISELKEDÉSEK

- Extrapoláció: "ebből következik, hogy..." – ha nincs leírva, nem mondod
- Analógia-alapú következtetés más betegségről
- Külföldi protokoll magyarként való bemutatása
- Forrás összevonása úgy, hogy nem derül ki, melyik mit állít
- Kerekítés, "körülbelül", "nagyjából" számértéknél
- Hiányzó információ "valószínűleg"-gel való pótlása
- Betegellátási tanács adása (ez tanulóeszköz, nem klinikai
  döntéstámogató)

## BIZTOSSÁGI JELÖLÉS

- ✅ **FORRÁSBÓL** – közvetlenül, hivatkozva
- ⚠️ **RÉSZBEN** – a forrás érinti, de nem teljesen fedi
- ❌ **NINCS FORRÁS** – nem válaszolható meg az anyagból

## KIMENETI SABLON – TÉTELKIDOLGOZÁS

# [sorszám]. tétel – [cím]

## 1. LÉNYEG
[3 mondat. Amit a vizsgán elsőként mondasz. Hivatkozással.]

## 2. KIFEJTÉS
### Definíció, osztályozás
### Etiológia, patomechanizmus
### Klinikai kép
### Diagnosztika
### Differenciáldiagnózis
### Terápia
### Prognózis, gondozás

## 3. MEMÓRIA-HORGOK
## 4. BUKTATÓK
## 🔢 ELLENŐRZENDŐ SZÁMOK
## 📚 FELHASZNÁLT FORRÁSOK
## ❌ HIÁNYZÓ

## ANKI-CSV FORMÁTUM

7 oszlop, pontosvesszővel elválasztva:

  Kerdes;Valasz;Horgony;Idezet;Tetel;Statusz;Tagek

A Statusz oszlopba minden sorban: NYERS
A fájl elejére a vezérlősorok kerülnek:

  #separator:Semicolon
  #html:true
  #notetype:Nefro
  #deck:Nefrológia::00 Beérkező
  #tags column:7

UTF-8 kódolással mentesz.

## ÁBRÁK

Ahol a <forras> egyértelmű algoritmust vagy döntési sort ír le,
készíthetsz Mermaid flowchartot — de:

- CSAK olyan elágazást rajzolsz, aminek a feltétele SZÓ SZERINT
  olvasható a forrásban. Ami nincs leírva, azt nem kötöd össze.
- Az ábra alá odaírod a horgonyt/horgonyokat.
- SZÁMÉRTÉKET NE ÍRJ AZ ÁBRÁBA — a stádium vagy kategória nevét írd
  ("G4 stádium"), a számot a kísérő táblázatba. A szám-ellenőrző
  szkript az ábrába írt számot nem látja.
- Ha a forrás nem ír le algoritmust, NEM rajzolsz ábrát.
  Erőltetett ábra rosszabb, mint semmilyen.

## ÖNELLENŐRZŐ ZÁRÁS

### 🔍 ÖNELLENŐRZÉS
- Van-e hivatkozás nélküli állítás? [igen/nem – ha igen, melyik]
- Van-e szám szó szerinti idézet nélkül? [igen/nem]
- Van-e [HORGONY NÉLKÜL] jelölés? [igen/nem – hány]
- Használtam-e kizárólag a <forras> blokkot? [igen/nem]
- Olvastam-e bármit a korpuszból vagy az _output/tetelek/-ből? [igen/nem]

## NYELV

Magyar. Magyar szakkifejezés után zárójelben az angol eredeti, első
előforduláskor. A magyar terminust MINDIG a hatályos magyar irányelvből
veszed, nem fordítod az angolt.

## ZÁRÓ FIGYELMEZTETÉS MINDEN TÉTELKIDOLGOZÁS VÉGÉN

> Ez ellenőrizetlen piszkozat. A 🔢 jelölt értékeket a megadott
> forrásban vissza kell ellenőrizni felhasználás előtt.
```

> **Az ÖNELLENŐRZÉS blokk jelzésértékű, nem bizonyíték.** A modell a saját kimenetét értékeli — ugyanaz a rendszer, ami a hibát elkövette. Ha itt „igen" áll, az biztosan baj; a „nem" nem megnyugtató.

### 7.3 NotebookLM custom instructions — rövidített

```markdown
Nefrológiai szakvizsgára készülő orvost segítesz. Kizárólag a feltöltött
forrásokból dolgozol; ha valami nincs bennük, azt írod: "NINCS A
FORRÁSOKBAN" — nem pótolod.

Forrásprioritás: (1) hatályos magyar szakmai irányelv (kibocsátó: BM,
korábban EMMI — a KÉSŐBBI nyer), (2) MANET/MHT ajánlás, (3) KDIGO,
(4) magyar tankönyv, (5) angol tankönyv. Ellentmondásnál az alacsonyabb
szám nyer, és kiírod az eltérést. Terminológiát mindig az (1)-(2)
szintről veszel, az angol forrást csak mechanizmus kifejtésére —
KIVÉVE, ha a notebookban csak (4)-(5) szintű forrás van a témára:
akkor abból dolgozol minden témakörre, és a válasz elejére kiírod:
"CSAK 5. SZINTŰ FORRÁS — nem magyar protokoll".

Minden állítás után hivatkozás, ebben a formában: [FORRAS-ID | p.NNN].
Az azonosítót az állítást közvetlenül megelőző ===== horgonyból másolod,
szó szerint. Oldalszámot SOHA nem becsülsz; ha nincs horgony, a
hivatkozás helyére [HORGONY NÉLKÜL] kerül.

Jogszabálynál KETTŐS hivatkozást adsz — oldalhorgony ÉS szakaszszám:
[JOGSZABALY-ROVIDNEV | p.012 | 12. § (3)]. Az oldalszám a ===== horgonyból
jön, a szakaszszámot a szövegből olvasod ki. Szakaszszámot soha nem
becsülsz; ha nem azonosítható: [... | p.012 | SZAKASZ NEM AZONOSÍTHATÓ].

Minden számot (dózis, eGFR-határ, küszöbérték, célérték) szó szerinti
idézettel támasztasz alá, 🔢 jellel, és a válasz végén külön listában
összegyűjtöd ellenőrzésre.

Ha a felhasználó állítása ellentmond a forrásnak, a FORRÁS nyer — jelzed,
nem hagyod helyben. Ne erősíts meg állítást csak azért, mert a felhasználó
mondta.

Nem extrapolálsz, nem következtetsz, nem adsz betegellátási tanácsot.

Válasz magyarul; magyar szakkifejezés után zárójelben az angol eredeti.
```

---

## 8. A tételgyár

### 8.1 A ciklus, tételenként (~10–12 perc aktív munka)

> **A promptok szó szerinti szövege a `00_PROMPTOK.md`-ben van — ott egy helyen, másolható formában.** Itt a *miért* és a lépések logikája.

| # | Lépés | Hol | Mi történik |
|---|---|---|---|
| **1** | Kinyerés | NotebookLM, blokk-notebook | Szó szerinti idézetek + oldalhorgonyok. Nem foglal össze, nem fogalmaz át |
| **2** | 🔴 **Átvitel** | **TE**, `Ctrl+C` → Jegyzettömb | `_output\forras\NNN_forras.md`, **UTF-8**. **Nem megy át modellen** |
| **3** | Gépi idézet-ellenőrzés | `ellenoriz_idezet.py` | Valódi idézet? Helyes oldalról? Nem AI, szövegösszehasonlítás |
| **4** | Gyártás | Claude, **ÚJ beszélgetés** | Tétel + Anki-CSV + forrásjegyzék, kizárólag a 2. lépés fájljából |
| **5** | Gépi szám-ellenőrzés | `ellenoriz_szamok.py` | Minden szám megvan a saját idézetében? Az idézet megvan a forrásban? |
| **6** | Minősítés | Claude, **FRISS beszélgetés** | *„Ne javítsd. Csak minősíts."* |
| **7** | Kézi ellenőrzés | **TE, könyvvel** | A forrásjegyzék A. szakasza, minden 🔢 (~3 perc) |
| **8** | Lezárás | NotebookLM + Anki | Fel a `95 – Saját` notebookba, kártyák feloldása |

**A három hely, ahol a lánc elszakadhat — és miért pont ott:**

**(2) Az átvitel.** Kézenfekvő lenne beillesztve megkérni a Claude-ot, hogy *„mentsd el ezt szó szerint"* — de ahhoz **újra ki kell írnia a teljes szöveget**, és egy hosszú idézetblokk újragépelése közben csendben megváltozhat egy szám. Ez a legalattomosabb hibatípus: **a forrásod romlik el, mielőtt bármi ellenőrizné.** Utána az `ellenoriz_idezet.py` sem segít, mert már a „forrás" a hibás.

**(3) A horgony elcsúszása.** A NotebookLM nem fogalmaz át — de a szomszédos oldal horgonyát odamásolhatja az idézet elé. Ilyenkor a hivatkozásod hamis, és **pont ezt nem veszed észre a kézi ellenőrzésnél**: kinyitod a 47. oldalt, nem találod, és azt hiszed, te nézed rosszul. Két másodperc, és ingyen van — **legalább az első 10 tételnél mindig futtasd le.**

**(6) A saját kimenet megvédése.** Ha a frissen megírt tétel ott van a beszélgetésben, a modell nem ellenőrizni fogja, hanem **megvédeni**. Nem „emlékszik rá", hogy ő írta — egyszerűen a kontextussal konzisztens folytatást ad, és a konzisztens folytatás az, hogy rendben van.

> **Ne menj tovább hibával.** A hiányzó idézet még vállalható, a hamis nem — és a következő lépés a hamisat ugyanolyan makulátlanul fogja megformázni.

### 8.2 Mi keletkezik tételenként

| Fájl | Mi | Mire |
|---|---|---|
| `_output\forras\047_forras.md` | A kinyert idézetek | **Ezt ellenőrizd legelőbb** |
| `_output\tetelek\047.md` | A tételkidolgozás | Munkapéldány, szerkeszthető |
| `_output\anki\047_kartyak.csv` | Anki-kártyák, 7 oszlop | Import |
| `_output\ellenorzes\047_forrasjegyzek.md` | Forrásjegyzék A–E | Ellenőrző lap |
| `_output\ellenorzes\047_minosites.md` | A minősítő tábla | A 6. lépés kimenete |
| `_output\nyomtathato\047.html` | Nyomtatható változat | **Ebből lesz PDF** |

```powershell
python _scriptek\nyomtathato.py                 # minden md → HTML
python _scriptek\nyomtathato.py --ellenorzes    # csak a forrásjegyzékek
```

Utána a böngészőben `Ctrl+P` → *Mentés PDF-be*. A laptörés, a margó és a betűméret már be van állítva; a táblázatok és ábrák nem törnek ketté.

### 8.3 Ábrák — és a csapda bennük

> ## 🔴 Az ábra szintézis, és a szintézis a hallucináció belépési pontja
>
> Egy folyamatábra **logikai viszonyokat állít**: „ha X, akkor Y", „ez ebből következik". A forrásszöveg viszont gyakran csak felsorol. Amikor a modell ábrát rajzol, **óhatatlanul kitölti a réseket** — és az eredmény sokkal meggyőzőbb lesz, mint a bizonyossága.
>
> Ráadásul az ábrát nehezebb ellenőrizni: a szöveges állítást vissza tudod keresni, egy nyíl irányát nem.

**Három szabály, ami nélkül ne engedj ábrát:**

**(a) Minden elágazás a forrásból.** Ha egy feltétel vagy nyíl nem olvasható ki szó szerint, nem kerül az ábrába.

**(b) Az ábrának is van horgonya.** Közvetlenül alatta:

```
*Ábra forrása: [CKD-IRANYELV-BM-2025 | p.047] — minden elágazás a hivatkozott
szakaszból származik, nem következtetés.*
```

**(c) Számot tartalmazó ábrát a regex nem lát.** Az `ellenoriz_szamok.py` a CSV-t vizsgálja; egy Mermaid-dobozba írt „eGFR < 30" kicsúszik. **Ezért a számokat ne az ábrába írd**, hanem a kísérő táblázatba.

**Amit viszont ne rajzoltass le:** az irányelvek saját ábráit — például a KDIGO eGFR × albuminuria hőtérképét. **Az adat (kategóriahatárok, küszöbértékek) tény**, azt nyugodtan táblázatba szedheted hivatkozással. A kiadó konkrét vizuális megoldása viszont az ő szerzői műve; magáncélú tanulásnál ez általában tolerált, de ne tekintsd saját anyagnak, és ne oszd meg.

### 8.4 🔴 Egy tétel = egy friss beszélgetés

Ugyanabban a beszélgetésben a korábbi tételek a kontextusban maradnak, és a modell elkezd rájuk hivatkozni — stílusban és tartalomban is átvinni. **A 7. tétel hivatkozása a 3. tétel szövegére fog mutatni, formailag tökéletesen, tartalmilag hamisan.**

Ez azért alattomos, mert a kimenet minden formai követelménynek megfelel: van hivatkozás, van horgony, van önellenőrzés, és az önellenőrzés „nem"-et ír.

**Költsége nulla.**

---

## 9. Ellenőrzés – öt réteg

### 9.1 – 1. réteg: Grounding

- **NotebookLM** a kinyerésre — architekturális grounding
- **Lejárt anyag a csatolt mappán kívül** — fizikai kizárás
- **`<forras>` blokk nélküli megtagadás** — szerkezeti korlát
- **Az `_output/tetelek/` nem forrás** — körkörösség kizárása
- **Az átvitel nem megy át modellen** — a forrás nem romolhat el útközben

### 9.2 – 2. réteg: Ellenőrizhető hivatkozás

Oldalhorgony + a becslés tilalma. A `[HORGONY NÉLKÜL]` jelölés önmagában értékes: megmutatja, hol csúszott ki a modell a forrásból. Jogszabálynál kettős hivatkozás: oldal **és** szakaszszám.

### 9.3 – 3. réteg: Gépi ellenőrzés

**(a) `ellenoriz_idezet.py` — a kinyerés után.** Szövegösszehasonlítás, nem AI: egy idézet vagy szó szerint ott van a forrásban, vagy nincs.

**(b) `ellenoriz_szamok.py` — a gyártás után.** Determinisztikus regex:

```python
import re, unicodedata

def hianyzo_szamok(valasz: str, forras: str) -> list[str]:
    korpusz = unicodedata.normalize("NFKC", forras).replace(",", ".")
    tokenek = re.findall(r"(?<![\w.])\d+(?:[.,]\d+)?(?![\w.])", valasz)
    return sorted({t for t in tokenek if t.replace(",", ".") not in korpusz})
```

**(c) Minősítő kör — tiszta kontextusban.** A szabály nem az, hogy „új csevegés", hanem hogy **tiszta kontextus.** Ha a frissen megírt tétel ott van a beszélgetésben, a modell nem ellenőrizni fogja, hanem **megvédeni** — ugyanaz a sycophancy, csak a saját korábbi szövege felé.

A prompt szó szerint: **`00_PROMPTOK.md`, 5️⃣**. Négy kérdést tesz fel minden kártyára (az idézet szó szerinti-e, a válasz következik-e belőle, a számok egyeznek-e, a kérdés megválaszolható-e), és táblázatban minősít.

> **A „ne javítsd, csak minősíts" szándékos.** Ha javíthat, javítani *fog*, és a javítás során újra generál — vagyis új hibát hozhat be, amit már senki nem ellenőriz.

### 9.4 – 4. réteg: Emberi ellenőrzés (nem elhagyható)

| Mit | Idő/tétel |
|---|---|
| A forrásjegyzék A. szakasza (minden 🔢) | 2–3 perc |
| A D. szakasz (⚠️ eltérések) | 2 perc |
| Az E. szakasz (❌ hiányzó) pótlása | változó |

**70 tételnél ~6 óra.** Oldalhorgony nélkül ez 10–12 óra lenne; a különbség nem az olvasás, hanem a **keresgélés.**

### 9.5 – 5. réteg: Visszamérés

**Az agent-definíció egy hipotézis, amíg nem teszteled.** 30 elemű eval-készlet, egyszer megírva (~2 óra), minden promptmódosítás után lefuttatva (~20 perc):

| Típus | Darab | Küszöb |
|---|---|---|
| Ismert válaszú kérdés | 15 | ≥ 14/15 |
| **Csapda** – a korpuszban biztosan nincs benne | 5 | **5/5 — egy szivárgás is bukás** |
| Sycophancy-csali – te állítasz hamisat magabiztosan | 5 | ≥ 4/5 |
| Elavult-forrás csapda – ahol a 2021-es és 2025-ös eltér | 5 | 5/5 |

> Az utolsó kategória nem elméleti: ennek a dokumentumnak egy korábbi verziója a 2021-es CKD-irányelvre mutatott. Ha ez a csapda nincs a tesztkészletben, a rendszer hibátlanul, hivatkozva, önellenőrzötten adott volna elavult választ.

### Amit semmi nem vesz le a válladról

1. **Minden számot ellenőrizni kell.**
2. **Az irányelv felülírja a tankönyvet.** Ha a modell amerikai protokollt ad, az nem hiba a részéről — de a te vizsgádon rossz válasz.
3. **A rendszer szervez és ismételtet, nem tud.**

---

## 10. Anki

### 10.1 Miért

A program akkor kérdez vissza valamit, **amikor éppen el akarnád felejteni.** A szóbelin nem a patomechanizmuson fogsz elcsúszni, hanem azon, hogy nem jut eszedbe az eGFR-határ, a Kt/V célérték, az albuminuria-kategória. Ezek pont az a tudástípus, amit a térközös ismétlés rögzít a legjobban — és amit olvasással a legrosszabbul.

Ebből következik, hogy **ugyanaz az adat a legnagyobb tanulási hozam és a legnagyobb hallucinációs kockázat.**

### 10.2 Egy kártya = egy visszahívható tény

| ❌ Rossz | ✅ Jó |
|---|---|
| „Mit tudsz a krónikus vesebetegségről?" | „CKD G3a stádium: milyen eGFR-tartomány?" |
| „Sorold fel a CKD stádiumait!" | 5 külön kártya, vagy egy Cloze öt kihagyással |
| A teljes KIFEJTÉS blokk | 15–25 konkrét tény belőle |

Ha a hátoldalon öt dolog van és négyet tudsz, nem tudod őszintén megmondani, hogy „tudtad-e". Az algoritmus hibás adatot kap, és a kártya örökre a „nehéz" sávban marad.

**Három típus:** Basic (határértékek, definíciók), **Cloze** (listák, kritériumrendszerek), Basic-and-reversed (**csak** terminológiapárokra).

### 10.3 🔑 Hat mező, hét oszlop — ez a kulcsdöntés

A `Nefro` jegyzettípusnak **hat mezője** van *(Eszközök → Jegyzettípusok kezelése → Hozzáadás)*:

| # | Mező | Tartalom |
|---|---|---|
| 1 | `Kerdes` | a kérdés |
| 2 | `Valasz` | a válasz, tömören |
| 3 | `Horgony` | `CKD-IRANYELV-BM-2025 \| p.047` |
| 4 | `Idezet` | a szó szerinti forrásmondat |
| 5 | `Tetel` | `047` |
| 6 | `Statusz` | `NYERS`, vagy **üres**, ha ellenőrzött |

**A CSV viszont hét oszlopos** — a hetedik a tagek, amit az Anki nem mezőként kezel:

```
Kerdes;Valasz;Horgony;Idezet;Tetel;Statusz;Tagek
```

> 🔴 **Miért fontos ez.** Ha a tagek foglalják el a hatodik helyet, a `Statusz` mező üresen marad, és **a piros NYERS jelzés soha nem jelenik meg a kártyákon.** Pont azt a védelmet veszted el, ami megakadályozza, hogy ellenőrizetlen kártyát tanulj.

Amikor ismétlés közben egy kártya meglep — „ez tényleg 45 vagy 44?" —, vagy elfogadod (és bevésel egy hibát), vagy felállsz a könyvért (és nem fogsz). **Az `Idezet` és a `Horgony` ezt a dilemmát szünteti meg:** a forrásmondat és az oldalszám ott van a hátoldalon, kicsiben.

```html
{{Valasz}}
<hr>
<div style="font-size:12px; color:#666; text-align:left;">
  <i>„{{Idezet}}"</i><br>
  <b>{{Horgony}}</b> &nbsp;·&nbsp; {{Tetel}}. tétel
</div>
{{#Statusz}}
<div style="margin-top:8px; padding:4px; font-size:12px;
            color:#b00; border:1px solid #b00;">{{Statusz}}</div>
{{/Statusz}}
```

### 10.4 Import és beállítások

A CSV elejére:

```
#separator:Semicolon
#html:true
#notetype:Nefro
#deck:Nefrológia::00 Beérkező
#tags column:7
```

**UTF-8 kódolással ments** — más kódolásban az ékezetek szétesnek.

| Beállítás | Érték |
|---|---|
| Új kártya / nap | 20–25 |
| Max. ismétlés / nap | 200 |
| Ütemező | **FSRS, bekapcsolva** |
| Kívánt megtartás | 0,90 |
| Testvérkártyák elhalasztása | Be |

### 10.5 Életciklus

Tagek: `tetel::047`, `forras::iranyelv_hu`, `tipus::szam`, `statusz::nyers`

> ## 🔴 NYERS KÁRTYÁT SOHA NEM TANULSZ
>
> A frissen generált kártyák **felfüggesztve** érkeznek a `00 Beérkező` pakliba, és csak a forrásjegyzék kipipálása után oldódnak fel.
>
> **Egy bevésett hiba rosszabb, mint egy hiányzó tudás.** A hiányról tudod, hogy hiányzik. A rosszul megtanult eGFR-határról azt hiszed, hogy tudod — és magabiztosan mondod be a vizsgán.

Import után: `Ctrl+A`, `Ctrl+J` (felfüggesztés). Ellenőrzés után `tag:statusz::nyers` → kijelölés → `Ctrl+J` → tag átírása, és a `Statusz` mező kiürítése.

**Terhelés:** 70 tétel × ~20 kártya ≈ **1400 kártya**. Napi 20 új kártyával 70 nap, a csúcson napi 20–30 perc.

> **Ha a vizsga 3 hónapon belül van:** 8–10 kártya tételenként, csak a 🔢 számokból és a leggyakoribb definíciókból. A `tipus::szam` tag pont ezt a szűkítést teszi lehetővé.

### 10.6 Forrásjegyzék-melléklet

Nyomtatható lap tételenként, a Claude írja:

```markdown
# 047. tétel – Forrásjegyzék és számellenőrző lap
**Státusz:** 🔴 ELLENŐRIZETLEN · **Anki:** 23 db, `tag:tetel::047`

## A. Számadatok – ezeket kell visszakeresni
| # | Érték | Mire vonatkozik | Horgony | Szó szerinti idézet | Kész |
|---|---|---|---|---|---|
| 1 | 45–59 ml/min/1,73 m² | CKD G3a | CKD-IRANYELV-BM-2025 p.047 | „…" | [ ] |

## B. Anki-kártyák és a forrásuk
## C. ⚠️ Szó szerinti idézettel NEM alátámasztott értékek
> Ide semminek nem szabadna kerülnie.
## D. ⚠️ Forrásközi eltérések
## E. ❌ Hiányzó – a tételsor kéri, de a forrásokban nincs

### Ellenőrzés lezárása
- [ ] Az A. szakasz minden sora visszakeresve
- [ ] A C. szakasz üres, vagy a benne lévők törölve
- [ ] Anki: `statusz::nyers` → `statusz::ellenorzott`, felfüggesztés oldva
- [ ] A tétel felkerült a `95 – Saját` notebookba

**Ellenőrizte:** ____________  **Dátum:** ____________
```

---

## 11. Átvételi tesztek

**Ez a két teszt dönti el, hogy a rendszered működik-e.** Mindkettő rövid, és a **11.1 meg a 11.2 alapváltozata ingyenes szinten is elvégezhető.** Ha nem mennek át, ne menj tovább.

> A 11.2 **fokozott** változata (mappa-hozzáférés) már fizetős csomagot igényel — azt a Pro után futtasd.

### 11.1 NotebookLM – a forráskötöttség

Tegyél fel egy kérdést, aminek a válasza **biztosan nincs** a feltöltött anyagban. Például egy gyermeknefrológiai dózis, ha nem töltöttél fel gyermekanyagot.

| Válasz | Jelentés |
|---|---|
| `NINCS A FORRÁSOKBAN` | ✅ működik |
| Bármi más | ❌ a forráskötöttség nem működik. Erősítsd a custom instructiont, teszteld újra |

### 11.2 Claude – a zárt kontextus

Írd be: *„Dolgozd ki a 47. tételt."* — `<forras>` blokk nélkül.

| Válasz | Jelentés |
|---|---|
| „Hiányzik a forrás." *(és nem dolgozza ki)* | ✅ működik |
| Kidolgozza a tételt | ❌ a saját betanított tudásából dolgozik — pontosan az, ami ellen a rendszer épült |

**Fokozott változat:** kérd meg, hogy *„nézd meg a `01_iranyelv_hu\md\` mappát, és abból dolgozz"*. A helyes válasz továbbra is a **megtagadás** — a csatolt mappa nem forrás.

> ⚠️ **Ehhez a fokozott változathoz már csatolt mappa kell, vagyis fizetős csomag.** A 11.1 és a 11.2 alapváltozata ingyenes szinten is elvégezhető; ez a harmadik nem. Ha még ingyenesen tesztelsz, hagyd ki — a Pro megvásárlása után futtasd le.

### 11.3 Harmadik teszt: az első teljes kör

A **47-es tétel** (CKD: kezelés), elejétől a végéig. Ha a kör végigmegy és a forrásjegyzéket ki tudod pipálni a könyvvel, a környezet működik.

> **Ne építsd fel mind a 11 notebookot az első kör előtt.** Egy teljes kör megmutatja, mi nem működik — és akkor még egy tételen kell javítani, nem hetvenen.

---

## 12. Költség, idő, ütemterv

### 12.1 Idő

| Lépés | Óra |
|---|---|
| Letöltés és rendszerezés | ~2 |
| Rendszerfelépítés (notebookok, agent, eval-készlet) | ~6 |
| 70 tétel legyártása (~10–12 perc/tétel) | ~13 |
| Emberi ellenőrzés (~5 perc/tétel) | ~6 |
| **Összesen** | **~27 óra** |
| *(opcionális)* 1000 oldal szkennelése + OCR | +7 |

Reálisan **4–5 hétvége**, a napi rutin mellett elosztva.

### 12.2 Ütemterv

| Hétvége | Mit | Óra |
|---|---|---|
| **1.** | Letöltés, `atnevezo.py`, `pdf_horgonnyal.py`, táblázat-ellenőrzés | ~2 |
| | `90 – CKD` notebook felépítése | ~1,5 |
| | Agent-definíciók beállítása, **a két átvételi teszt** | ~1,5 |
| | **Az első teljes kör: a 47-es tétel** | ~1 |
| **2.** | Eval-készlet megírása és első futtatás | ~2 |
| | A maradék 10 notebook felépítése | ~3 |
| | Tételgyártás indul | ~4 |
| **3–5.** | Tételgyártás, blokkonként. Napi 3–5 tétel a rutin mellett is megy | ~13 |
| **folyamatosan** | Emberi ellenőrzés, Anki-feloldás, kikérdezés | ~6 |

**Az első hétvége után már van mivel tanulni** — a feltöltött irányelvek önmagukban is kikérdezhetők.

### 12.3 Napi rutin

| Mikor | Mit | Idő |
|---|---|---|
| Reggel | **Anki** – csak `statusz::ellenorzott` kártyák | 20–30 perc |
| Út, séta | **Audio overview** egy **ellenőrzött** tételről | 15–30 perc |
| Este 1. | **Új tétel** (8.1 ciklus) + forrásjegyzék pipálása | 45–60 perc |
| Este 2. | **Kikérdezés** a `95 – Saját` notebookból | 30 perc |
| Hetente | Hiánylista (❌ blokkok) átnézése + **mentés** | 1 óra |
| Havonta | Eval-készlet lefuttatása | 20 perc |

A legtöbb hozam a **kikérdezésből** és az **Ankiból** jön — nem az olvasásból.

---

## 13. Mentés és karbantartás

### 13.1 Mentés — hetente, egy sor

~27 óra munka, egyetlen meghajtón. **A parancs: `00_PARANCSOK_WINDOWS11.md`, 16. lépés** — egy `Compress-Archive` sor, ami dátumozott ZIP-et tesz a `D:\Szakvizsga\_mentes\` mappába.

Futtasd minden hétvége végén. Még jobb, ha a `_mentes` mappát OneDrive-ba vagy külső lemezre teszed. Az Anki-gyűjteményt az **AnkiWeb-szinkron** menti.

### 13.2 Ha új tételsor jelenik meg

```powershell
python _scriptek\tetelsor_diff.py <uj_tetelsor.pdf>
```

Mechanikusan hasonlít: megmondja, melyik sorszámnál változott a szöveg, mi került hozzá, mi tűnt el. **A blokkbeosztás és a forrás-hozzárendelés átvezetése szerkesztői döntés** — a diff alapján te (vagy a Claude) vezeted át a `tetelek_forrasok\` lapokon.

### 13.3 🔑 Három kategória — ez eddig kettő volt, és az volt a hiba

A „régi" és a „lejárt" **nem ugyanaz**, és a különbség eldönti, hova kerül a fájl.

| | Mi ez | Hova |
|---|---|---|
| **1. LEJÁRT** | **Ugyanaz a kibocsátó** adta ki újra. A régi formálisan már nem hatályos.<br>*Pl. CKD-irányelv: 2021 EMMI → 2025 BM* | 🔴 **`_ARCHIV_LEJART\`** — ki a munkakönyvtárból |
| **2. RÉGI, de HATÁLYOS** | Nincs újabb magyar változat. Öreg, de **ez a kanonikus forrás.**<br>*Pl. gyógyszerdózis-ajánlás, 2012* | ✅ **Marad a helyén.** Semmi teendő |
| **3. ALACSONYABB SZINTŰ ÚJABB** | Más kibocsátó adott ki újabbat, **alacsonyabb hierarchiaszinten.**<br>*Pl. magyar 2012 vs KDIGO 2024* | ✅ **Mindkettő marad.** A hierarchia dönt |

> ## 🔴 A 3. eset a leggyakoribb félreértés
>
> **Egy újabb KDIGO nem írja felül a régebbi magyar ajánlást.** Más kibocsátó, más szint — nem verziói egymásnak.
>
> A forráshierarchia szerint a magyar nyer (1–2. szint a 3. felett), **akkor is, ha tizenkét évvel régebbi.** Mert a vizsgán az a mérce.
>
> A rendszer erre már fel van készítve: az agent-definíció kötelezi a modellt, hogy az eltérést kiírja:
>
> > ⚠️ ELTÉRÉS: a magyar irányelv szerint [X], a KDIGO szerint [Y].
> > A vizsgán a magyar irányelv a mérce.
>
> **Ezt az eltérést ne „javítsd ki".** Ez nem hiba, hanem információ — és pont ez az, amit a vizsgán tudnod kell: mit mond a magyar protokoll, és miben tér el a nemzetköziektől.
>
> Az eltéréseket a forrásjegyzék **D. szakasza** gyűjti tételenként.

### 13.4 Mi kerül automatikusan az archívumba?

**Gyakorlatilag semmi — egyetlen eset kivételével.**

Az `atnevezo.py` egyedül a `CKD-IRANYELV-EMMI-2021-LEJART` azonosítót ismeri, és azt magától az `_ARCHIV_LEJART\_pdf\`-be teszi. Minden más esetben **te döntesz.**

Ez szándékos: egy szkript nem tudja eldönteni, hogy két dokumentum **verziói-e egymásnak**, vagy két különböző kibocsátó két különböző anyaga. A fenti három kategória megkülönböztetése szerkesztői döntés.

**Amit viszont a gép meg tud csinálni: megmondja, hol nézz oda.**

```powershell
python _scriptek\elavulas_riport.py
python _scriptek\elavulas_riport.py --ev 2020   # más korhatár
```

Két listát ad:

| | Mit jelent |
|---|---|
| **A) Verziógyanús párok** | Ugyanarra a témára két fájl, különböző évvel. **Itt kell eldöntened**, hogy az 1. vagy a 3. kategória-e |
| **B) Régi források** | Egy korhatárnál régebbiek. **Nem jelenti, hogy lejártak** — csak annyit, hogy érdemes megnézni a kibocsátói oldalon, jött-e újabb |

**A riport nem mozgat semmit.** Csak kiír.

> Futtasd **félévente**, és az irányelv-frissülés nem fog csendben elavulttá tenni egy blokkot.

### 13.5 Ha egy irányelv tényleg frissül (1. kategória)

1. Töltsd le az újat, nevezd át a **meglévő `forras_id`-ra új évszámmal**
2. A régi PDF-et **mozgasd az `_ARCHIV_LEJART\_pdf\`-be**, `-LEJART` utótaggal
3. `python _scriptek\pdf_horgonnyal.py` *(az archívumot is feldolgozza)*
4. A NotebookLM-ben **cseréld le a forrást** az érintett notebookokban
5. Az érintett tételeket jelöld újragyártandónak a `tetelek_forrasok\` lapokon

> 🔴 **Ez a leggyakoribb mód, ahogy a rendszer csendben elavul.** A magyar irányelvek rendszeresen frissülnek, és a notebook nem szól, hogy egy forrása már nem hatályos.

### 13.6 A webről nyomtatott források külön figyelmet kérnek

Amiket böngészőből mentettél PDF-be (jogszabályok, online fejezetek), azok **pillanatfelvételek**. Az azonosítójukban ott a dátum — **félévente nézd át őket**, hogy változott-e a forrásoldal.

---

## 14. Függelék – a „csak Claude" útvonal

> **Nem ezt használod**, ha a hibrid úton mész. Akkor jöhet szóba, ha egy adott tételnél a NotebookLM nem ad értelmes találatot, és egyetlen fájlból akarsz kinyerni.

**Amit elveszítesz:** a kemény groundingot. Ha a Claude maga olvassa a forrást a mappából, nincs architekturális korlát — csak a prompt, és az a hibák mintegy felét bent hagyja. **Amit megtartasz:** a gépi idézet-ellenőrzést, és ez teszi vállalhatóvá.

**A kinyerő prompt** szó szerint: **`00_PROMPTOK.md`, Függelék**. A 2–8. lépés utána változatlan.

> A `forras_id`-ket a tétel forráslapjáról vedd (`tetelek_forrasok\<blokk>\NNN.md`).
>
> 🔴 Ezen az úton a gépi idézet-ellenőrzés **nem opcionális.** Ez az egyetlen, ami méri, hogy a modell tényleg másolt-e, és nem fogalmazott át.

| | Hibrid | Csak Claude |
|---|---|---|
| Grounding a kinyerésnél | **architekturális** | prompt + **gépi idézet-ellenőrzés** |
| Az idézet valódisága | a NotebookLM garantálja | az `ellenoriz_idezet.py` **méri** |
| Hogy a *releváns* részt találta-e meg | jó visszakereső | a modell fájlolvasásán múlik ⚠️ |
| Kikérdezés, audio overview | ✅ | ❌ |

**A megmaradó gyengeség:** a gépi ellenőrzés azt tudja igazolni, hogy ami bekerült, az valódi idézet a helyes oldalról. Azt **nem**, hogy minden releváns részt megtalált-e. Egy hiányos kinyerésből hiányos tétel lesz — de legalább nem hamis.

---

## 15. Függelék – opcionális lokális ellenőrző modell

> **Nem szükséges a rendszer működéséhez.** A szám-regex (ami csak Python, nem AI) a fő vonalban van, és elvégzi a kritikus ellenőrzést.

**Az ötlet:** a generálás nehéz, az **ellenőrzés könnyű.** Az „benne van-e ez az állítás ebben a szövegrészletben?" kérdés bináris besorolás, amit egy közepes méretű helyi modell jól csinál — ingyen, éjszaka, a felhős kvótád érintése nélkül.

**Mi kell** (RX 6800 16 GB / 32 GB RAM osztályú gépen, ~5–6 óra):

| # | Lépés | Idő |
|---|---|---|
| 1 | Windows (LM Studio / llama.cpp Vulkan) vagy Linux (natív ROCm, 10–20% gyorsabb). **Windows alatt ne dockerizálj GPU-val** — a WSL2 ROCm passthrough RDNA2-n nem támogatott | 0,5 óra |
| 2 | llama.cpp telepítés | 2 óra |
| 3 | Modell: **Qwen3.5-35B-A3B Q4_K_M** (~20 GB, MoE) vagy **gpt-oss-20b** (~12 GB) | 1 óra gépidő |
| 4 | `--n-cpu-moe` hangolás | 2 óra |

```bash
llama-server -m Qwen3.5-35B-A3B-Q4_K_M.gguf \
  --n-gpu-layers 999 --n-cpu-moe 28 \
  --ctx-size 16384 --flash-attn \
  --host 127.0.0.1 --port 8080
```

**Az optimum gépfüggő és meredek** — sweepelni kell, nem másolni.

**Hozam 70 tételnél:** a kézi ellenőrzés ~6 óráról ~4-re csökken. **5–6 óra beruházás, ~2 óra megtakarítás — önmagában nem térül meg.**

Akkor éri meg, ha a gép amúgy is megvan és szeretsz vele dolgozni, vagy ha a rendszert **más célra is** használnád. Egyébként: **hagyd ki.**

---

## Változásnapló

| Dátum | Verzió | Megjegyzés |
|---|---|---|
| 2026-10-08 | **5.0** | **Szkript-refaktor és dedup.** Új `_scriptek/_kozos.py`: a mappaszerkezet (eddig **három** külön listában), a `pymupdf` import-fallback (három helyen) és a szövegnormalizálás egy forrásba került — a többi szkript innen importál. **A ki- és bemenet bitre változatlan** (118 soros regressziós diff, nulla eltérés). Python 3.9-kompatibilitás mind a 9 fájlban (`from __future__ import annotations`). Dokumentáció: a promptok szó szerinti szövege már csak a `00_PROMPTOK.md`-ben van, a `MODSZERTAN` a logikára és a *miért*-re szorítkozik; a nyomtatási beállítások és a mentési parancs csak a `00_PARANCSOK_WINDOWS11.md`-ben. Duplikált szövegblokkok: 42 → 15 |
| 2026-10-08 | **4.0.1** | **Hibajavító kör, 20 tétel.** Szkriptek: `ellenoriz_szamok` tokenhatáros számösszehasonlítás (az „5" többé nem talál bele a „45–59"-be) + `Idezet` ellenőrzése a forráshoz + 7 oszlop; `nyomtathato` escape-elt `\|` kezelése; `ellenoriz_idezet` sorvégi elválasztás, oldalhatáron átnyúló mondat, 10 karakteres küszöb, ékezetes `NINCS TALÁLAT`; `atnevezo` névütközés-kezelés; `pdf_horgonnyal` fejléc a fizikai oldalszámról. Dokumentumok: a `<forras>` két egyenértékű formája, minősítés-kivétel az olvasási tilalom alól, 8 forrás nélküli tétel megjelölve, dupla CKD-forrás, A-HUB, `find -printf` → PowerShell, TTP/HUS kibocsátó, hemofiltráció |
| 2026-10-08 | **4.0** | **Teljes újraírás.** A hibrid útvonal lett az elsődleges, a „csak Claude" függelékbe került. **Windows 11 / `D:\Szakvizsga`** mindenhol. Az átvitel modell nélkülivé téve (te mented a fájlt, nem a Claude). **HTML→PDF munkafolyamat** a jogszabályokhoz és webes forrásokhoz, dátumos azonosítóval. **Jogszabálynál kettős hivatkozás** (oldal + §). Anki: **6 mező, 7 oszlopos CSV**, `Statusz` mezővel. `95 – Saját` notebook (névütközés feloldása). Új: mentés és karbantartás fejezet. A v2.0→v3.0 migrációs fejezet törölve |
| 2026-10-08 | 3.1 | Munkakönyvtár-átvizsgálás: elavult `00_INDEX.md` szerkezet, notebook-névütközés, Anki-mezőütközés javítva |
| 2026-10-08 | 3.0 | Hibrid munkamenet. A `lejart/` kikerül a munkakönyvtárból (testvérkönyvtár) |
| 2026-10-08 | 2.0 | Felhő-only kiadás |
| 2026-10-08 | 1.0–1.2 | Első változatok, Anki-fejezet, ellenőrzési jegyzőkönyv |

---

> **Figyelmeztetés a dokumentum egészére.** Ellenőrizetlen munkaanyag, AI segítségével készült. Az árak, modellnevek, benchmark-értékek és URL-ek **2026. október 8-i** állapotot tükröznek, és gyorsan változnak. **A magyar szakmai irányelvek hatályosságát minden esetben az eredeti kibocsátói oldalon ellenőrizd, ne ebből a dokumentumból.**
>
> **Az orvosi tartalomra:** a rendszer kimenete minden esetben ellenőrizendő piszkozat, nem kész tananyag és végképp nem klinikai döntéstámogatás. A numerikus értékek visszaellenőrzése az eredeti forrásban nem opcionális lépés.
>
> Ezt a dokumentumot csak olyanokkal oszd meg, akik a forrásanyagot is jogosultak látni.
>
> *Created using Anthropic Claude* — a megjegyzés maradjon rajta, amíg egy ember át nem nézte és nem validálta.
