# `forras_id` lista – átnevezési segédlet

*Created using Anthropic Claude* — ellenőrizetlen munkaanyag, 2026-10-08.

> ## Nem kell kézzel átnevezned
>
> Tölts le mindent a `_letoltve/` mappába bármilyen néven, aztán:
>
> ```powershell
> python _scriptek\atnevezo.py
> ```
>
> A szkript felismeri és a helyére teszi őket. **Ez a lap arra kell, amit nem
> ismert fel**, illetve hogy lásd, melyik dokumentum hány tételhez kell.

> ## Mire való ez a lap
>
> Letöltés után **nevezd át a PDF-et a `forras_id`-ra**, és tedd a megadott
> mappába. A `pdf_horgonnyal.py` a **fájlnévből** veszi az azonosítót, és abból
> lesz a hivatkozás a teljes rendszerben:
>
> ```
> CKD-IRANYELV-BM-2025.pdf
>     ↓  pdf_horgonnyal.py
> ===== [CKD-IRANYELV-BM-2025 | p.047] =====
>     ↓  NotebookLM + Claude
> „A CKD G3a stádium eGFR-tartománya 45–59 ml/min/1,73 m²
>   [CKD-IRANYELV-BM-2025 | p.047]"
> ```
>
> **Ezért nem kozmetika.** Ha a fájl neve `docread.pdf` vagy `irányelv(3).pdf`,
> akkor a 70 tétel összes hivatkozása használhatatlan lesz.

### Elnevezési szabályok

- Csak **nagybetű, szám, kötőjel**. Ékezet, szóköz, zárójel, pont nem.
- A kiterjesztés `.pdf`, azt ne írd bele az azonosítóba.
- Ha olyat töltesz le, ami nincs a listán, a mintát kövesd:
  `TÉMA-KIBOCSÁTÓ-ÉV`, pl. `AKUT-DIALIZIS-MANET-2027`.
- **Lejárt dokumentumnál tedd a végére a `-LEJART` jelzést**, és a
  `_ARCHIV_LEJART/_pdf/` testvérkönyvtárba. Pl. `CKD-IRANYELV-EMMI-2021-LEJART`.

---

## PRIORITÁS 1 – hatályos magyar irányelv (BM)

**Mentsd ide:** `01_iranyelv_hu/_pdf/`

| Kész | `forras_id` → ez legyen a fájlnév | Dokumentum | Hány tétel | Tételek |
|---|---|---|---|---|
| [ ] | **`CKD-IRANYELV-BM-2025`** | BM egészségügyi szakmai irányelv – felnőttkori idült vesebetegség diag… | 18 | 1–2, 19–20, 40, 45–56, 67 |
| [ ] | **`CKD-IRANYELV-BM-2025-SUPPL`** | Ugyanez, Hypertonia és Nephrologia Supplementum verzió | 18 | 1–2, 19–20, 40, 45–56, 67 |
| [ ] | **`TTP-HUS-IRANYELV-BM-2026`** | BM egészségügyi szakmai irányelv – TTP és HUS kezelése | 2 | 18, 62 |
| [ ] | **`HYPONATRAEMIA-IRANYELV`** | Egészségügyi szakmai irányelv – a hyponatraemia diagnosztikájáról és k… | 1 | 5 |

## PRIORITÁS 2 – MANET / MHT

**Mentsd ide:** `02_manet_tarsasag/_pdf/`

| Kész | `forras_id` → ez legyen a fájlnév | Dokumentum | Hány tétel | Tételek |
|---|---|---|---|---|
| [ ] | **`IMMUNSZEROLOGIA-MANET-2024`** | Immunserologiai vizsgálatok vesebetegségekben, 2024 | 13 | 4, 9–18, 38, 62 |
| [ ] | **`VESEBIOPSZIA-MANET-2025`** | Percutan natív vesebiopszia végzése felnőttkori nephrologiai kórképekb… | 10 | 4, 9–17 |
| [ ] | **`ERBP-TX-2013`** | ERBP – Szakmai irányelv a vesetranszplantáció donorának és recipiensén… | 8 | 63–70 |
| [ ] | **`SGLT2-CKD-MANET-2024`** | SGLT2-gátlók alkalmazása idült vesebetegségben, 2024 | 6 | 19–20, 45–48 |
| [ ] | **`ALBUMINURIA-EGFR-LABOR-2025`** | Állásfoglalás orvosi laboratóriumok számára – albuminuria és eGFR vizs… | 6 | 1–2, 45–48 |
| [ ] | **`DIALIZIS-UTMUTATO-MANET-2021`** | A korszerű dialíziskezelés gyakorlata – szakmai útmutató, 2021 | 6 | 56–61 |
| [ ] | **`GYOGYSZERDOZIS-CKD-2012`** ⚠️ | A gyógyszerek vesefunkciót figyelembe vevő adagolásáról | 6 | 35, 40–43, 47 |
| [ ] | **`RAS-GATLAS-CKD-2012`** ⚠️ | Állásfoglalás az ACE-gátlók és ARB-k idült vesebetegségben történő alk… | 6 | 21–22, 45–48 |
| [ ] | **`MHT-HT-IRANYELV-2025`** | MHT – Gyakorlati irányelv a magasvérnyomás-betegség ellátásáról, 2025 | 5 | 21–25 |
| [ ] | **`BEUTALAS-HAZIORVOS-2024`** | Ajánlás háziorvosoknak – mikor gondoljunk vesebetegségre, mikor küldjü… | 4 | 45–48 |
| [ ] | **`KONTRASZT-NEPHROPATHIA-2022`** | Kontrasztanyagok által okozott vesekárosodás és megelőzése | 4 | 3, 41–43 |
| [ ] | **`NEPHRO-BEUTALAS-2009`** ⚠️ | Nephrológiai beutalás módja, javallatai, szükséges kísérő információi | 4 | 45–48 |
| [ ] | **`CKD-MBD-MANET-2012`** ⚠️ | A krónikus vesebetegségben kialakuló csont- és ásványianyagcsere-zavar… | 3 | 7, 33, 53 |
| [ ] | **`MANET-MHT-HT-2023`** | MaNET / MHT – Hypertonia irányelv, 2023 | 2 | 21–22 |
| [ ] | **`SGLT2-T2DM-CHECKLIST-2026`** | Ellenőrző lista háziorvosoknak – SGLT-2-gátló terápia T2DM-ben, 2026 | 2 | 19–20 |
| [ ] | **`LIPID-CKD-MANET-2024`** | Javaslat az idült vesebetegségben alkalmazott lipidcsökkentő kezelésre… | 2 | 47, 49 |
| [ ] | **`DM-CKD3B-2016`** ⚠️ | Gyakorlati útmutató – cukorbetegek kezelése CKD 3b vagy előrehaladotta… | 2 | 19–20 |
| [ ] | **`METFORMIN-CKD-2012`** ⚠️ | Összefoglaló a metformin vesebetegségben történő alkalmazásáról | 2 | 19–20 |
| [ ] | **`ALBUMINURIA-SZURES-2012`** ⚠️ | Ajánlás az albuminuria, proteinuria, haematuria szűrésére és vizsgálat… | 1 | 2 |
| [ ] | **`KONTRASZT-ALLASFOGLALAS-2012`** ⚠️ | Állásfoglalás a kontrasztanyagok vesekárosító hatásának megelőzésére | 1 | 3 |
| [ ] | **`MR-KONTRASZT-NSF-2014`** | MANET állásfoglalás – MR kontrasztanyagok nephrogen szisztémás fibrosi… | 1 | 3 |
| [ ] | **`VESEKO-MANET-2012`** ⚠️ | Ajánlás a vesekőbetegség belgyógyászati kivizsgálására és kezelésére | 1 | 33 |
| [ ] | **`EGFR-BEOSZTAS-2014`** ⚠️ | A felnőttkori idült vesebetegség felismerése és beosztása a számított … | 1 | 1 |
| [ ] | **`MANET-KV-KONSZENZUS-2020`** | MANET javaslatai a 2020-as Kardiovaszkuláris Konszenzus Konferenciára | 1 | 49 |

## PRIORITÁS 3 – KDIGO

**Mentsd ide:** `03_kdigo/_pdf/`

| Kész | `forras_id` → ez legyen a fájlnév | Dokumentum | Hány tétel | Tételek |
|---|---|---|---|---|
| [ ] | **`KDIGO-CKD`** | KDIGO – CKD Evaluation and Management | 13 | 1–3, 24–25, 34–37, 45–48 |
| [ ] | **`KDIGO-GN`** | KDIGO – Glomerular Diseases | 13 | 4, 9–18, 27, 38 |
| [ ] | **`KDIGO-TX`** | KDIGO – Care of Kidney Transplant Recipients / Living Donor | 8 | 63–70 |
| [ ] | **`KDIGO-AKI`** | KDIGO – Acute Kidney Injury | 4 | 41–44 |
| [ ] | **`KDIGO-BP-2021`** | KDIGO 2021 – Blood Pressure Management in CKD | 3 | 21–23 |
| [ ] | **`KDIGO-ANEMIA-2026`** | KDIGO 2026 Clinical Practice Guideline – Anemia in CKD | 2 | 50–51 |
| [ ] | **`KDIGO-DIABETES`** | KDIGO – Diabetes Management in CKD | 2 | 19–20 |
| [ ] | **`KDIGO-CKD-MBD`** | KDIGO – CKD-MBD | 2 | 7, 53 |
| [ ] | **`KDIGO-ADPKD`** | KDIGO – ADPKD | 1 | 26 |
| [ ] | **`KDIGO-LIPID`** | KDIGO – Lipid Management in CKD | 1 | 49 |

## PRIORITÁS 5 – AJKD Core Curriculum

**Mentsd ide:** `05_tankonyv_en/_pdf/`

| Kész | `forras_id` → ez legyen a fájlnév | Dokumentum | Hány tétel | Tételek |
|---|---|---|---|---|
| [ ] | **`AJKD-CC-VASCULAR-ACCESS-2025`** | Hemodialysis Vascular Access: Core Curriculum 2025 | 1 | 57 |
| [ ] | **`AJKD-CC-HEART-FAILURE-2025`** | Kidney Dysfunction in Heart Failure: Core Curriculum 2025 | 1 | 49 |
| [ ] | **`AJKD-CC-ONCONEPHROLOGY-2023`** | Onconephrology: Core Curriculum 2023 | 1 | 38 |
| [ ] | **`AJKD-CC-NUTRITION-2022`** | Nutrition in Kidney Disease: Core Curriculum 2022 | 1 | 56 |

## PRIORITÁS 5 – KÖTELEZŐ FALLBACK a vakfolt-tételekhez

**Mentsd ide:** `05_tankonyv_en/_pdf/` · **Az anyagbeszerzéskor, a többivel együtt.**

Ezekhez a tételekhez nincs magyar irányelv. A `forras_id` **előre rögzített, évszám nélkül** — a cikket te választod ki az AJKD gyűjtőoldalán a keresőszavakkal, de a fájlnév ez lesz, így a tétellapok és az `atnevezo.py` már most hivatkozhat rá.

| Kész | `forras_id` | Tétel | AJKD-keresőszó (angolul) | Ha nincs illő cikk |
|---|---|---|---|---|
| [ ] | **`AJKD-CC-KALIUM`** | 6 | potassium, hyperkalemia, hypokalemia | tankönyv → `04_tankonyv_hu/_pdf/` |
| [ ] | **`AJKD-CC-SAV-BAZIS`** | 8 | acid-base, metabolic acidosis, metabolic alkalosis | tankönyv |
| [ ] | **`AJKD-CC-TUBULOPATIA`** | 28 | inherited tubulopathies, Gitelman, Bartter | tankönyv |
| [ ] | **`AJKD-CC-RTA`** | 29 | renal tubular acidosis | előbb nézd meg, a `AJKD-CC-SAV-BAZIS` tárgyalja-e; ha nem: tankönyv |
| [ ] | **`AJKD-CC-CAKUT`** | 30 | congenital anomalies of the kidney and urinary tract, CAKUT | tankönyv |
| [ ] | **`AJKD-CC-UTI`** | 31, 32 | urinary tract infection, pyelonephritis | tankönyv |
| [ ] | — (közös a 31.-kel) | 32 | fungal, candiduria, Candida | ha az `AJKD-CC-UTI` nem tárgyalja: **tankönyv kötelező** |
| [ ] | **`AJKD-CC-RENOVASZKULARIS`** | 39 | renal artery thrombosis, renal vein thrombosis, atheroembolic, renovascular | tankönyv |

> **Tankönyvi fejezetnél** a mintát kövesd: `TANKONYV-HU-<TEMA>`, pl. `TANKONYV-HU-KALIUM`. Ha egy tételhez sem AJKD-cikk, sem tankönyvi fejezet nincs, azt a tétel forráslapján rögzítsd — csak akkor maradhat vékony.

---

## Gyors ellenőrzés letöltés után

```powershell
# 1. Mit töltöttél le eddig, és jó-e a nevük?
Get-ChildItem -Recurse -Filter *.pdf |
  Where-Object DirectoryName -like '*_pdf*' |
  Select-Object @{n='Nev';e={$_.Name}}, @{n='MB';e={[math]::Round($_.Length/1MB,2)}} |
  Sort-Object Nev | Format-Table -AutoSize

# 2. Melyik fájlnév NEM felel meg a forras_id szabálynak?
#    (csak NAGYBETŰ, szám, kötőjel — se kisbetű, se ékezet, se szóköz)
$rossz = Get-ChildItem -Recurse -Filter *.pdf |
  Where-Object { $_.DirectoryName -like '*_pdf*' -and
                 $_.Name -cnotmatch '^[A-Z0-9-]+\.pdf$' }
if ($rossz) { $rossz.Name } else { "mind rendben" }
```

A második parancs kiírja azokat, amikben kisbetű, ékezet, szóköz vagy zárójel
maradt. **Ha nem ír semmit, kész vagy.**


## Nem kell `forras_id`

Ezekhez nincs azonosító, mert nem töltöd le őket — linkeled vagy csak olvasod:

- NephSIM, Renal Fellow Network (FOAMed, magyarázó anyag)
- Nemzeti Jogszabálytár, net.jogtar.hu (ott a szakaszszám a hivatkozás)
- Digitális Tankönyvtár (böngészd, és csak a szükséges fejezeteket mentsd)

A **saját beszkennelt könyveidnek** viszont kell: azok a
`04_tankonyv_hu/_pdf/` mappába mennek, és te adsz nekik azonosítót.
Pl. `TANKONYV-KAKUK-NEPHROLOGIA`.


*Created using Anthropic Claude* — ellenőrizetlen munkaanyag.
