# Nefrológiai szakvizsga – AI-támogatott felkészülési munkakönyvtár

*Created using Anthropic Claude* — ez a megjegyzés maradjon a dokumentumon, amíg egy ember át nem nézte és nem validálta a tartalmát.

> **Ellenőrizetlen munkaanyag.** A linkek, dokumentumcímek és dátumok **2026-10-08-i** állapotot tükröznek. **Az irányelvek hatályosságát minden esetben az eredeti kibocsátói oldalon ellenőrizd, ne ebből a könyvtárból.**
>
> A rendszer kimenete minden esetben ellenőrizendő piszkozat — nem kész tananyag, és végképp nem klinikai döntéstámogatás.

---

## Mi ez

Munkakönyvtár a **magyar nefrológiai szakvizsgára** való felkészüléshez, felhőalapú AI-eszközökkel (NotebookLM + Claude).

**Egyetlen elvre épül: a modell soha nem a saját tudásából válaszol, hanem kizárólag abból, amit eléd teszel — és mindig megmondja, honnan.** Minden más ebből következik: az oldalhorgonyok, a kétlépcsős generálás, a forrásjegyzék-mellékletek.

**Mit épít:** forrásalapú tanulási rendszert. A hivatalos tételsort veszi vázként, a hatályos magyar irányelveket használja tartalomként, minden állításhoz ellenőrizhető hivatkozást ad (forrás + oldalszám), tételenként strukturált kidolgozást és Anki-kártyákat generál, és korlátlanul kikérdez.

**Mit nem épít:** orvosi tudásforrást. A nyelvi modell a saját emlékezetéből erre nem megbízható — és ami ennél fontosabb, **meggyőzően és összefüggően hibázik**, jellemzően egy másik ország protokollját adva vissza.

| | |
|---|---|
| Tételsor | OKFŐ ENK – „Nefrológia – egységes", **2024.07.25.**, **70 vizsgakérdés** |
| Fájl | `00_tetelsor/TETELSOR-NEFROLOGIA-2024-07-25.pdf` *(a ZIP-ben benne van)* |

> A vizsgán a honlapról aktuálisan letöltött verzió használható. **A pontos hitelesítési szabályokat a vizsgaszervezőtől kérdezd meg**, ne ebből a könyvtárból.

---

## Hol kezdd

**Ebben a sorrendben olvasd — mindegyik máshová való, nincs átfedés:**

| # | Fájl | Mire |
|---|---|---|
| **1** | **`00_ELSO_HETVEGE_CHECKLIST.md`** | **Innen indulj.** Pipálható lista az első hétvégére. Nyomtasd ki |
| **2** | **`00_PARANCSOK_WINDOWS11.md`** | A pontos parancsok sorrendben, `D:\Szakvizsga` gyökérrel. Mellé tartod a gép mellett |
| **3** | **`00_PROMPTOK.md`** | A tételenkénti promptok. **Ezt fogod a legtöbbet használni** |
| 4 | `00_LETOLTESI_TERV.md` | A ~45 dokumentum, forrásoldal szerint csoportosítva |
| 5 | `00_NOTEBOOK_FELTOLTES.md` | Mely `.md` fájl melyik NotebookLM-notebookba megy |
| 6 | `00_KIEGESZITO_KOVETELMENYEK.md` | Amit a tételsor kér, de nem önálló vizsgakérdés. **Olvasd el az első tétel előtt** |
| 7 | `00_INDEX.md` | Részletes térkép: mappaszerkezet, szkriptek, haladáskövető tábla |
| 8 | `00_FORRAS_ID_LISTA.md` | Átnevezési segédlet — ahhoz, amit az `atnevezo.py` nem ismert fel |
| — | `MODSZERTAN_v5.0.md` | A teljes módszertan. **A 7.2-es agent-definíció innen kell** |
| — | `tetelek_forrasok/<blokk>/NNN.md` | 70 forráslap — tételenként: mely forrásokból dolgozz, hol tartasz |

> **A lényeg három mondatban.** Letöltöd a forrásokat, két szkript horgonyozott markdownt csinál belőlük. Feltöltöd **egy** NotebookLM-notebookba, és végigviszel **egy** tételt a teljes körön. Ha az megy, a maradék **62 futószalag** — nyolc tételhez ugyanis nincs letölthető magyar forrás *(lásd lentebb)*.

---

## Három szabály, ami nem alku tárgya

Ez a három a rendszer gerince. Ha valamelyik sérül, a kimenet **nem lesz rosszabbul kinéző** — csak hamis lesz, hivatkozással és önellenőrzéssel együtt.

### 1. A `forras_id` a fájlnévből jön

```
CKD-IRANYELV-BM-2025.pdf
    ↓  pdf_horgonnyal.py
===== [CKD-IRANYELV-BM-2025 | p.047] =====
    ↓  NotebookLM + Claude
„…45–59 ml/min/1,73 m²  [CKD-IRANYELV-BM-2025 | p.047]"
    ↓  te, könyvvel
a 47. oldalon tényleg ez áll ✓
```

Ha a fájl `docread.pdf` néven marad, a hivatkozás is az lesz, és a 70 tétel ellenőrzése használhatatlanná válik. Ezért van az `atnevezo.py`.

**És ezért `.md`-t tölts fel a NotebookLM-be, ne PDF-et.** PDF-ből a modell az oldalszámot nem látja — vagy elhagyja, vagy **kitalálja.** Egy kitalált oldalszámú, egyébként *helyes* állítás ugyanannyi keresgélési időt éget el, mint egy hamis — csak soha nem találod meg a hibát.

### 2. A lejárt irányelv a munkakönyvtáron KÍVÜL van

```
D:\Szakvizsga\
├── nefro_szakvizsga\        ← EZT csatolod
└── _ARCHIV_LEJART\          ← EZT SOHA
```

**Testvérkönyvtár, nem almappa.** Ha a mappát csatolod egy AI-nak, minden benne lévő fájl egyetlen olvasásnyira van — egy `lejart/` almappa tehát nem véd semmitől.

Nem elég metaadatban jelölni, hogy lejárt: az arra épülne, hogy a modell engedelmeskedik, és mérések szerint a promptkövetés orvosi kontextusban a hibák mintegy felét bent hagyja. **Ami nincs a kontextusban, azt viszont nem tudja idézni.** Ez az egyetlen 100%-os védelem a rendszerben.

> **A konkrét eset:** a CKD-irányelv **2021-es EMMI-verzióját felülírta a 2025-ös BM-verzió.** Ha a régi elérhető marad, a rendszer hibátlanul, hivatkozva, önellenőrzötten fog elavult választ adni — pontosan az a kimenet, ami ellen az egész építmény védekezik.

### 3. Nyers Anki-kártyát soha nem tanulsz

A frissen generált kártyák **felfüggesztve** érkeznek a `00 Beérkező` pakliba, és csak a forrásjegyzék kipipálása után oldódnak fel.

**Egy bevésett hiba rosszabb, mint egy hiányzó tudás.** A hiányról tudod, hogy hiányzik. A rosszul megtanult eGFR-határról azt hiszed, hogy tudod — és magabiztosan mondod be a vizsgán.

---

## Mappaséma dióhéjban

Minden forrásmappa (`01_` … `06_`) egyformán épül fel:

| | |
|---|---|
| `_pdf/` | a letöltött mesterpéldány — **ne töröld**, az ellenőrzéskor ebben keresel |
| `md/` | horgonyozott markdown — **ezt töltöd fel a NotebookLM-be** |

Kivétel a `07_sajat_jegyzet/`: a saját jegyzeted nem hivatkozható forrás — nincs benne oldalszám, nem hitelesített, és már átment egy értelmezésen. **Ne töltsd fel generáló notebookba.** Ha bekerül, a modell idézni fogja, és onnantól a saját korábbi félreértésed szerepel forrásként, hivatkozással.

A teljes fa, a nyolc szkript (+ egy közös modul) leírásával: **`00_INDEX.md`**.

> **A rendszerezéshez elég egy parancs:** `python _scriptek\futtat.py` — végigvezet az átnevezésen, a horgonyozáson és az elavulás-riporton, a helyes sorrendben, megerősítéssel.

**Egyetlen függőség:** `pip install pymupdf`

---

## Amire számíts

**Összesen ~27 óra**, reálisan **4–5 hétvége** a napi rutin mellett elosztva. A részletes bontás és az ütemterv: **`MODSZERTAN_v5.0.md`, 12. fejezet.**

**Anki-terhelés:** 70 tétel × ~20 kártya ≈ 1400 kártya. Napi 20 új kártyával 70 nap, a csúcson napi 20–30 perc ismétlés.

> **Ha a vizsga 3 hónapon belül van:** hagyd ki a könyvszkennelést, dolgozz a letölthető irányelvekkel és az AJKD Core Curriculummal, és csinálj tételenként 8–10 kártyát 20 helyett — csak a 🔢 számokból és a leggyakrabban kérdezett definíciókból. A `tipus::szam` tag pont ezt a szűkítést teszi lehetővé.

Előfizetés és a „mikor mit vegyél meg": **`00_PARANCSOK_WINDOWS11.md`**, az utolsó szakasz.

---

## Ismert hiányosságok

- **A tételsor PDF fejezetszámozása I. → II. → V.** A III. és IV. fejezet nincs benne. Érdemes rákérdezned a vizsgaszervezőnél, hogy létezik-e teljesebb verzió.
- **A gyakorlati vizsgához nincs külön tétellista.** A legközelebbi a II. fejezet „Gyakorlati követelmények" szakasza — ezt a `00_KIEGESZITO_KOVETELMENYEK.md` dolgozza fel.
- **Több magyar MANET-dokumentum 2012–2016-os** (gyógyszerdózis, vesekő, RAS-gátlás, CKD-MBD). A forráslapokon ⚠️ jelöli őket. Mielőtt feltöltöd, nézd meg, van-e újabb azonos témájú — és ahol a magyar anyag öreg, ott a KDIGO és az AJKD egészíti ki.
- 🔴 **Nyolc tételhez nincs letölthető magyar forrás:** 6, 8, 28, 29, 30, 31, 32, 39. A forráslapjukon csak gyűjtőoldal-link van, `forras_id` nélkül — üres korpusszal a rendszer helyesen NINCS A FORRÁSOKBAN-t ad. A három lehetőség (AJKD-cikk, tankönyvszkennelés, hagyományos tanulás) mindegyik érintett forráslap alján ott van.
- **A CKD-irányelvnek két változata van:** `CKD-IRANYELV-BM-2025` (Magyar Közlöny) és `-SUPPL` (Hypertonia és Nephrologia Supplementum). **Ugyanaz a tartalom, más tördelés.** Egy notebookba csak az EGYIKET töltsd fel, különben minden találat duplán jön. **Javaslat: a `-SUPPL`** — olvashatóbb tördelés, jobb szövegkinyerés. A másik marad mesterpéldánynak a `_pdf/` mappában.
- **A közvetlen PDF-linkek nincsenek mind ellenőrizve.** Ahol „ELLENŐRIZD" szerepel, ott tényleg nézd meg.
- **A `06_jog/` is PDF-ből dolgozik.** A jogszabályokat böngészőből nyomtatod PDF-be, így oldalhorgonyt is kapnak — a hivatkozás kettős lesz: oldal **és** szakaszszám. Lásd `MODSZERTAN_v5.0.md`, 5.2.

---

> Ezt a könyvtárat csak olyanokkal oszd meg, akik a forrásanyagot is jogosultak látni. A beszkennelt, szerzői jogvédett tankönyvek kezelésére a szokásos magáncélú felhasználási szabályok vonatkoznak.
>
> *Created using Anthropic Claude*
