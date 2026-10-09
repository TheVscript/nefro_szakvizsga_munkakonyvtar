# Letöltési terv

*Created using Anthropic Claude* — ellenőrizetlen munkaanyag, 2026-10-08-i állapot.

> ## Fontos: NE tételenként tölts le
>
> A 70 tétel összesen **~45 dokumentumra** támaszkodik, és ezek nagy része több
> tételhez is kell. Ha tételenként indulsz, ugyanazt a PDF-et tízszer töltöd le.
>
> **Forrásonként tölts le, egyszer.** Ez a lap forrásoldal szerint csoportosít.
> A `tetelek_forrasok/` alatti lapok csak megmondják, melyik tételhez melyik kell.

## Becsült idő

| Lépés | Idő |
|---|---|
| MANET-oldal végigtöltése (a dokumentumok ~60%-a egyetlen listában) | ~40 perc |
| KDIGO gyűjtőoldal | ~20 perc |
| AJKD Core Curriculum (a tételhez illő cikkek) | ~20 perc |
| Egyéb közvetlen linkek | ~10 perc |
| **Összesen** | **~1,5 óra** |

## Mielőtt elkezded

1. Hozz létre egy `_pdf/` almappát mindegyik forrásmappában (a ZIP-ben már megvan).
2. **Nevezd át a fájlokat a `forras_id` szerint**, amint letöltötted. Ez lesz a
   hivatkozás gyökere a teljes rendszerben — ha most elhanyagolod, a 70 tétel
   hivatkozásai használhatatlanok lesznek.
   Példa: `CKD-IRANYELV-BM-2025.pdf`, nem `docread.pdf` vagy `irányelv(3).pdf`.
3. **Honnan mi jön** — ez a négy eset, és mindegyik PDF-ben végződik:

| Szakasz | Mi van a link mögött | Mit csinálsz |
|---|---|---|
| **1. MANET** | PDF | Letöltöd → `_letoltve/` |
| **2. KDIGO** | PDF | Letöltöd → `_letoltve/` |
| **3. AJKD** | ⚠️ **HTML-cikkoldal** | PDF-gomb, vagy `Ctrl+P` → `05_tankonyv_en/_pdf/` |
| **4. Közvetlen linkek** | PDF | Letöltöd → `_letoltve/` |
| **5. njt.hu, Digitális Tankönyvtár** | ⚠️ **HTML-oldal** | `Ctrl+P` → `06_jog/_pdf/` vagy `04_tankonyv_hu/_pdf/` |

4. **Minden letöltés után nyisd meg a PDF-et.** Harminc másodperc, és megmutatja,
   hogy a tartalmat kaptad-e meg, vagy egy bejelentkező oldalt.

---

## 1. ⭐⭐ MANET irányelv-oldal – ezzel kezdd

**http://www.nephrologia.hu/info.aspx?sp=17** → a bal menüben **IRÁNYELVEK**

A lap tetején megjelenhet egy „Lejárt a biztonsági időkorlát" üzenet — **nem hiba**, görgess tovább. A publikus dokumentumok listája bejelentkezés nélkül is látszik, a lap alján.

A lista **nagyjából** dátum szerint csökkenő — de nem mindenhol (néhány 2014-es sor a 2016-osok elé került). Ne a sorrendre hagyatkozz: **a dokumentum címe alapján keress.** Ezeket töltsd le:

| Kész | Publikálva | Dokumentum | Mentsd ide | `forras_id` |
|---|---|---|---|---|
| [ ] | 2026.04.16. | BM egészségügyi szakmai irányelv – TTP és HUS kezelése | `01_iranyelv_hu/_pdf/` | `TTP-HUS-IRANYELV-BM-2026` |
| [ ] | 2026.03.09. | Ellenőrző lista háziorvosoknak – SGLT-2-gátló terápia T2DM-ben, 2026 | `02_manet_tarsasag/_pdf/` | `SGLT2-T2DM-CHECKLIST-2026` |
| [ ] | 2025.08.22. | Ugyanez, Hypertonia és Nephrologia Supplementum verzió | `01_iranyelv_hu/_pdf/` | `CKD-IRANYELV-BM-2025-SUPPL` |
| [ ] | 2025.05.06. | BM egészségügyi szakmai irányelv – felnőttkori idült vesebetegség diagnózisa és kezelése | `01_iranyelv_hu/_pdf/` | `CKD-IRANYELV-BM-2025` |
| [ ] | 2025.03.17. | Állásfoglalás orvosi laboratóriumok számára – albuminuria és eGFR vizsgálatok, 2025 | `02_manet_tarsasag/_pdf/` | `ALBUMINURIA-EGFR-LABOR-2025` |
| [ ] | 2025.01.15. | Percutan natív vesebiopszia végzése felnőttkori nephrologiai kórképekben, 2025 | `02_manet_tarsasag/_pdf/` | `VESEBIOPSZIA-MANET-2025` |
| [ ] | 2024.07.11. | SGLT2-gátlók alkalmazása idült vesebetegségben, 2024 | `02_manet_tarsasag/_pdf/` | `SGLT2-CKD-MANET-2024` |
| [ ] | 2024.07.11. | Ajánlás háziorvosoknak – mikor gondoljunk vesebetegségre, mikor küldjük nefrológushoz, 2024 | `02_manet_tarsasag/_pdf/` | `BEUTALAS-HAZIORVOS-2024` |
| [ ] | 2024.07.11. | Immunserologiai vizsgálatok vesebetegségekben, 2024 | `02_manet_tarsasag/_pdf/` | `IMMUNSZEROLOGIA-MANET-2024` |
| [ ] | 2024.02.27. | Javaslat az idült vesebetegségben alkalmazott lipidcsökkentő kezelésre, 2024 | `02_manet_tarsasag/_pdf/` | `LIPID-CKD-MANET-2024` |
| [ ] | 2022.01.18. | Kontrasztanyagok által okozott vesekárosodás és megelőzése | `02_manet_tarsasag/_pdf/` | `KONTRASZT-NEPHROPATHIA-2022` |
| [ ] | 2021.09.24. | A korszerű dialíziskezelés gyakorlata – szakmai útmutató, 2021 | `02_manet_tarsasag/_pdf/` | `DIALIZIS-UTMUTATO-MANET-2021` |
| [ ] | 2021.02.25. | KDIGO 2021 – Blood Pressure Management in CKD | `03_kdigo/_pdf/` | `KDIGO-BP-2021` |
| [ ] | 2020.12.09. | MANET javaslatai a 2020-as Kardiovaszkuláris Konszenzus Konferenciára | `02_manet_tarsasag/_pdf/` | `MANET-KV-KONSZENZUS-2020` |
| [ ] | 2014.10.06. | ERBP – Szakmai irányelv a vesetranszplantáció donorának és recipiensének vizsgálatáról, perioperatív ellátás | `02_manet_tarsasag/_pdf/` | `ERBP-TX-2013` |
| [ ] | 2016.05.31. ⚠️ | Gyakorlati útmutató – cukorbetegek kezelése CKD 3b vagy előrehaladottabb stádiumban | `02_manet_tarsasag/_pdf/` | `DM-CKD3B-2016` |
| [ ] | 2014.11.23. | MANET állásfoglalás – MR kontrasztanyagok nephrogen szisztémás fibrosist okozó mellékhatása | `02_manet_tarsasag/_pdf/` | `MR-KONTRASZT-NSF-2014` |
| [ ] | 2014.11.23. ⚠️ | A felnőttkori idült vesebetegség felismerése és beosztása a számított GFR és a fehérjevizelés vizsgálatával | `02_manet_tarsasag/_pdf/` | `EGFR-BEOSZTAS-2014` |
| [ ] | 2013.06.14. ⚠️ | A krónikus vesebetegségben kialakuló csont- és ásványianyagcsere-zavar vizsgálata és kezelése | `02_manet_tarsasag/_pdf/` | `CKD-MBD-MANET-2012` |
| [ ] | 2012.08.23. ⚠️ | Összefoglaló a metformin vesebetegségben történő alkalmazásáról | `02_manet_tarsasag/_pdf/` | `METFORMIN-CKD-2012` |
| [ ] | 2012.07.31. ⚠️ | A gyógyszerek vesefunkciót figyelembe vevő adagolásáról | `02_manet_tarsasag/_pdf/` | `GYOGYSZERDOZIS-CKD-2012` |
| [ ] | 2012.02.14. ⚠️ | Állásfoglalás az ACE-gátlók és ARB-k idült vesebetegségben történő alkalmazásáról | `02_manet_tarsasag/_pdf/` | `RAS-GATLAS-CKD-2012` |
| [ ] | 2012.02.14. ⚠️ | Ajánlás a vesekőbetegség belgyógyászati kivizsgálására és kezelésére | `02_manet_tarsasag/_pdf/` | `VESEKO-MANET-2012` |
| [ ] | 2012.02.14. ⚠️ | Állásfoglalás a kontrasztanyagok vesekárosító hatásának megelőzésére | `02_manet_tarsasag/_pdf/` | `KONTRASZT-ALLASFOGLALAS-2012` |
| [ ] | 2012.02.14. ⚠️ | Ajánlás az albuminuria, proteinuria, haematuria szűrésére és vizsgálatára | `02_manet_tarsasag/_pdf/` | `ALBUMINURIA-SZURES-2012` |
| [ ] | 2009.02.11. ⚠️ | Nephrológiai beutalás módja, javallatai, szükséges kísérő információi | `02_manet_tarsasag/_pdf/` | `NEPHRO-BEUTALAS-2009` |

> **A ⚠️ jelöltek 2012–2016-osak.** Ne töröld őket, de **mielőtt feltöltöd őket a
> generáló notebookokba, nézd meg, van-e újabb azonos témájú.** Amelyiket felülírta
> egy frissebb, az az `_ARCHIV_LEJART/` testvérkönyvtárba és a `99 – ARCHÍV` notebookba megy.
>
> A legfontosabb eset: a **2021-es EMMI CKD-irányelvet** felülírta a 2025-ös BM-verzió.
> Ha valahonnan a 2021-est töltöd le, az `_ARCHIV_LEJART/_pdf/`-be kerül (az `atnevezo.py` magától odateszi).


---

## 2. KDIGO

**https://kdigo.org/guidelines/**

| Kész | Dokumentum | Megjegyzés | `forras_id` |
|---|---|---|---|
| [ ] | KDIGO 2026 Clinical Practice Guideline – Anemia in CKD | Közvetlen PDF (ELLENŐRIZD). 2026.01.02-án jelent meg, az első teljes frissítés 2012 óta | `KDIGO-ANEMIA-2026` |
| [ ] | KDIGO – CKD Evaluation and Management (legfrissebb kiadás) | A KDIGO gyűjtőoldalon keresd a 'CKD Evaluation and Management' címet, és a LEGFRISSEBB évszámút töltsd le | `KDIGO-CKD` |
| [ ] | KDIGO – Glomerular Diseases | Gyűjtőoldal → 'Glomerular Diseases', legfrissebb | `KDIGO-GN` |
| [ ] | KDIGO – Diabetes Management in CKD | Gyűjtőoldal → 'Diabetes', legfrissebb | `KDIGO-DIABETES` |
| [ ] | KDIGO – Acute Kidney Injury | Gyűjtőoldal → 'Acute Kidney Injury', legfrissebb | `KDIGO-AKI` |
| [ ] | KDIGO – CKD-MBD (ásványi anyagcsere és csontbetegség) | Gyűjtőoldal → 'CKD-MBD', legfrissebb | `KDIGO-CKD-MBD` |
| [ ] | KDIGO – Care of Kidney Transplant Recipients / Living Donor | Gyűjtőoldal → transzplantációs irányelvek | `KDIGO-TX` |
| [ ] | KDIGO – ADPKD (Autosomal Dominant Polycystic Kidney Disease) | Gyűjtőoldal → 'ADPKD' | `KDIGO-ADPKD` |
| [ ] | KDIGO – Lipid Management in CKD | Gyűjtőoldal → 'Lipid' | `KDIGO-LIPID` |

> A KDIGO irányelvek nyilvános PDF-ek, **közvetlen linkkel letölthetők**, tehát itt egy `wget -i linkek.txt` is működik, ha összegyűjtöd a linkeket.


---

## 3. AJKD Core Curriculum (open access)

**https://www.ajkd.org/content/corecurriculum**

| Kész | Cikk | `forras_id` |
|---|---|---|
| [ ] | [Hemodialysis Vascular Access: Core Curriculum 2025](https://www.ajkd.org/article/S0272-6386(24)00976-4/fulltext) | `AJKD-CC-VASCULAR-ACCESS-2025` |
| [ ] | [Kidney Dysfunction in Heart Failure: Core Curriculum 2025](https://www.ajkd.org/article/S0272-6386(25)00691-2/fulltext) | `AJKD-CC-HEART-FAILURE-2025` |
| [ ] | [Onconephrology: Core Curriculum 2023](https://www.ajkd.org/article/S0272-6386(23)00739-4/fulltext) | `AJKD-CC-ONCONEPHROLOGY-2023` |
| [ ] | [Nutrition in Kidney Disease: Core Curriculum 2022](https://www.ajkd.org/article/S0272-6386(21)00764-2/fulltext) | `AJKD-CC-NUTRITION-2022` |

### 3b. 🔴 KÖTELEZŐ fallback a 8 vakfolt-tételhez (6, 8, 28–32, 39)

Ezekhez nincs magyar irányelv. **Ne halaszd a végére** — most keresd ki őket a gyűjtőoldalon, a keresőszavakkal és a rögzített `forras_id`-kkal: `00_FORRAS_ID_LISTA.md` → **„PRIORITÁS 5 – KÖTELEZŐ FALLBACK"**. Ahol nincs illő cikk, oda a magyar tankönyv megfelelő fejezete kerül (`04_tankonyv_hu/_pdf/`).

> ## ⚠️ Figyelem: ezek a linkek HTML-oldalra visznek, nem PDF-re
>
> Az AJKD `/fulltext` címe a cikk **weboldala.** Két lehetőséged van:
>
> 1. **Keresd a „PDF" gombot a cikk oldalán** — ha van, az a legjobb, mert a kiadó saját tördelése
> 2. **Ha nincs, `Ctrl+P` → Mentés PDF-ként** — a beállításokat lásd az 5. szakaszban (🔴 **fejléc/lábléc KI**)
>
> Mindkét esetben a `05_tankonyv_en\_pdf\` mappába mentsd, a megadott `forras_id` néven. Az `atnevezo.py` ezeket **nem ismeri fel** — kézzel nevezd át.

> A gyűjtőoldalon sokkal több cikk van. **Ne töltsd le mindet** — nézd végig a tételsort, és csak azokat szedd le, amelyekhez tartozik tétel. A `tetelek_forrasok/` lapokon a **PRIORITÁS 5 – angol mélység** szakasz sorolja fel, melyik tételhez melyik AJKD-cikk kell.


---

## 4. Közvetlen linkek (ellenőrizd mindegyiket)

> ✅ **Ezek a linkek közvetlenül `.pdf`-re mutatnak** — a „Link" oszlop azt mondja meg, **honnan töltöd le**, nem azt, hogy linkként használnád. Rákattintasz, lejön a PDF, kész.
>
> Mindhármat felismeri az `atnevezo.py`, tehát elég a `_letoltve\` mappába menteni — a helyükre teszi őket.

| Kész | Dokumentum | Honnan töltöd le | Mentsd ide | `forras_id` |
|---|---|---|---|---|
| [ ] | Egészségügyi szakmai irányelv – a hyponatraemia diagnosztikájáról és kezeléséről | [pharmindex.hu](https://static.pharmindex.hu/Pharmindex/additional/guideline/document/A%20hyponatraemia%20diagnosztik%C3%A1j%C3%A1r%C3%B3l%20%C3%A9s%20kezel%C3%A9s%C3%A9r%C5%91l.pdf) | `_letoltve/` | `HYPONATRAEMIA-IRANYELV` |
| [ ] | MHT – Gyakorlati irányelv a magasvérnyomás-betegség ellátásáról, 2025 | [doki.net](https://doki.net/tarsasag/hypertension/upload/hypertension/document/hn_mht_iranyelv_2025_megj_szept_15_j_20251022.pdf) | `_letoltve/` | `MHT-HT-IRANYELV-2025` |
| [ ] | MaNET / MHT – Hypertonia irányelv, 2023 (H&N Suppl.) | [nephrologia.hu](http://www.nephrologia.hu/upload/nephrologia/document/hn_2023_suppl_2_manet_nyomda.pdf) | `_letoltve/` | `MANET-MHT-HT-2023` |


---

## 5. HTML-oldalak — ezeket PDF-be nyomtatod

Ezek weboldalként léteznek, nem PDF-ként. **Böngészőből nyomtatod PDF-be**, és onnantól ugyanolyan teljes értékű forrás lesz belőlük, mint bármelyik letöltött irányelvből: kap oldalhorgonyt, és géppel ellenőrizhető.

| Hol | Mit | Hova |
|---|---|---|
| **Nemzeti Jogszabálytár** — https://njt.hu/ | Csak a tételekhez tartozó rendeleteket (TX-jogszabályok, 65. tétel) | `06_jog\_pdf\` |
| **Digitális Tankönyvtár** — https://dtk.tankonyvtar.hu/ | Csak a szükséges fejezeteket, ne az egész könyvet | `04_tankonyv_hu\_pdf\` |

**A nyomtatás beállításai** — részletesen a `00_PARANCSOK_WINDOWS11.md` **7/b** lépésében:

| | |
|---|---|
| 🔴 Fejléc/lábléc | **KI** — különben az URL és a dátum minden oldalra rákerül, és beszennyezi az idézeteket |
| 🔴 Lenyíló részek | **Előbb nyisd ki mindet** — amit nem nyitottál ki, az nem kerül a PDF-be, és nem veszed észre |
| Méretezés | 100%, A4 |

**Elnevezés — dátummal:** `NJT-TX-RENDELET-2026-10-08.pdf`

> A dátum azért kell, mert ez **pillanatfelvétel**. A jogszabály módosulhat, az oldal átszerveződhet — fél év múlva az azonosítóból látnod kell, mikori állapotot idézel.

### Amit viszont tényleg nem töltesz le

- **NephSIM** — https://nephsim.com/
- **Renal Fellow Network** — https://www.renalfellow.org/foamed/

Ezek magyarázó, oktató anyagok (FOAMed), **nem idézendő protokollforrások.** Olvasd őket, ha egy mechanizmust nem értesz — de ne töltsd fel generáló notebookba, és ne hivatkozz rájuk.

---

## 6. Letöltés után: PDF → markdown oldalhorgonnyal

> ### Hogyan működik — nincs benne varázslat
>
> A `pdf_horgonnyal.py` **kizárólag helyi fájlokat lát.** Linket soha nem nyit meg, nem tölt le semmit, és nem tud róla, hogy egy forrás honnan származik.
>
> Amit csinál: végigmegy a `_pdf\` mappákon, és minden ott talált `*.pdf`-ből készít egy `.md`-t, azonos néven. **Ennyi.**
>
> ```
> 01_iranyelv_hu\_pdf\*.pdf   →   01_iranyelv_hu\md\*.md
> 02_manet_tarsasag\_pdf\*.pdf →   02_manet_tarsasag\md\*.md
> 03_kdigo\_pdf\*.pdf          →   03_kdigo\md\*.md
> 04_tankonyv_hu\_pdf\*.pdf    →   04_tankonyv_hu\md\*.md
> 05_tankonyv_en\_pdf\*.pdf    →   05_tankonyv_en\md\*.md
> 06_jog\_pdf\*.pdf            →   06_jog\md\*.md
> 00_tetelsor\_pdf\*.pdf       →   00_tetelsor\*.md
> _ARCHIV_LEJART\_pdf\*.pdf    →   _ARCHIV_LEJART\md\*.md   (külön, figyelmeztetéssel)
> ```
>
> **Ezért nincs „link" a rendszerben.** Egy weboldal két állapot egyikében lehet:
>
> | | |
> |---|---|
> | **Kinyomtattad PDF-be** → ott van a `_pdf\` mappában | Innentől **semmiben nem különbözik** egy letöltött irányelvtől. A szkript ugyanúgy megtalálja, ugyanúgy horgonyoz, és a `forras_id` ugyanúgy a fájlnév lesz |
> | **Nem nyomtattad ki** | A szkript számára **nem létezik.** Nem forrás, nem lesz belőle `.md`, nem kerül a notebookba, és nem lehet rá hivatkozni |
>
> Nincs köztes állapot. Ezért jó döntés, hogy mindent PDF-be mentesz: így a lánc egységes, és nincs olyan forrásod, ami „valahol ott van, de nem ellenőrizhető".



```powershell
pip install pymupdf
python _scriptek\pdf_horgonnyal.py
```

A szkript végigmegy a `_pdf/` mappákon, és minden PDF-ből `.md`-t készít
oldalhorgonnyal. **Ezt a `.md`-t töltöd fel a NotebookLM-be, nem a PDF-et.**

A PDF-et **ne dobd el**: az a mesterpéldány, abban keresel vissza az
ellenőrzéskor.

> **A letöltött irányelvekhez nem kell OCR** — digitálisan készült PDF-ek,
> van bennük valódi szövegréteg. OCR csak a beszkennelt könyvekhez kell.
> A kinyerés után viszont **nézd át a táblázatokat** (CKD-stádiumok,
> eGFR-kategóriák, dóziskorrekciós táblák) — ha szétestek, azt a néhány
> oldalt kézzel vagy vision-OCR-rel pótold.


---

## 7. 🔑 Új forrás felvétele — mit kell „generálni"?

**Semmit.** A `forras_id` **maga a fájlnév**, kiterjesztés nélkül:

```
06_jog\_pdf\NJT-TX-RENDELET-2026-10-08.pdf
    ↓  pdf_horgonnyal.py  (a fájlnévből veszi az azonosítót)
===== [NJT-TX-RENDELET-2026-10-08 | p.003] =====
```

Nincs regiszter, adatbázis vagy konfigurációs fájl, amit frissítened kellene a működéshez. **Elnevezed, a helyére teszed, lefuttatod a szkriptet — kész.**

### Amit viszont érdemes bejegyezned — a saját eligazodásod miatt

| Hol | Mit írj bele | Muszáj? |
|---|---|---|
| **`tetelek_forrasok\<blokk>\NNN.md`** | Melyik tételhez kell ez a forrás | **Ez a legfontosabb.** Ebből tudod majd, mit kell feltölteni, amikor arra a tételre kerül a sor |
| `00_NOTEBOOK_FELTOLTES.md` | Melyik notebookba megy | Ajánlott |
| `00_FORRAS_ID_LISTA.md` | Egy sor a listába | Ajánlott |
| `_scriptek\atnevezo.py` *(a `K` szótár)* | Felismerési kulcsszavak | **Nem.** Csak akkor, ha újra le fogod tölteni. Egy fájlt gyorsabb kézzel átnevezni |

> **Ezt a hármat megkérheted a Claude-ot is**, hogy vezesse át — a `tetelek_forrasok\` és a `00_*` fájlok a csatolt mappa olvasható részében vannak:
>
> ```
> Felvettem egy új forrást: 06_jog/_pdf/NJT-TX-RENDELET-2026-10-08.pdf
> (vesetranszplantációs rendelet, a 65. tételhez).
>
> Vezesd át a nyilvántartásban:
> - tetelek_forrasok/110_transzplantacio/065.md → a forrástáblába
> - 00_NOTEBOOK_FELTOLTES.md → a `110 – Transzplantáció` notebook listájába
> - 00_FORRAS_ID_LISTA.md → a listába
>
> Orvosi tartalmat NE írj, csak a nyilvántartási sorokat.
> ```

*Created using Anthropic Claude* — ellenőrizetlen munkaanyag.
