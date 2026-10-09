# Nefrológiai szakvizsga – munkakönyvtár

*Created using Anthropic Claude* — ellenőrizetlen munkaanyag, 2026-10-08.

> **Figyelem:** a benne szereplő linkek, dátumok és dokumentumcímek 2026-10-08-i állapotot tükröznek. A magyar állami és társasági oldalak átszerveződhetnek. Az irányelvek hatályosságát **minden esetben az eredeti kibocsátói oldalon** ellenőrizd.

---

> **Ez a lap a részletes térkép.** Ha most nyitottad ki először, a
> **`README.md`** mondja meg, mit olvass milyen sorrendben; az első hétvége
> lépéseit pedig a **`00_ELSO_HETVEGE_CHECKLIST.md`** vezeti végig.
>
> Itt a mappaszerkezet, a szkriptek és a haladáskövető tábla van.

---

## Mappaszerkezet

> 🔴 **A legfontosabb szerkezeti tény:** a lejárt anyag **nem almappa, hanem
> testvérkönyvtár** — a `nefro_szakvizsga/` MELLETT, nem benne. Amit nem
> csatolsz, azt a modell nem tudja megnyitni, és **ez az egyetlen 100%-os
> védelem a rendszerben.**

```
D:\Szakvizsga\                        (a gyökér — EZT NE csatold)
│
├── nefro_szakvizsga\                  ← EZT csatolod a Claude-hoz
│   ├── README.md                      ← INNEN INDULJ
│   ├── 00_INDEX.md                    ← ez a fájl (részletes térkép)
│   ├── 00_ELSO_HETVEGE_CHECKLIST.md   ← pipálható indulólista
│   ├── 00_PARANCSOK_WINDOWS11.md      ← pontos parancsok, sorrendben
│   ├── 00_LETOLTESI_TERV.md           ← a letöltés forrásoldalanként
│   ├── 00_NOTEBOOK_FELTOLTES.md       ← mi megy melyik notebookba
│   ├── 00_PROMPTOK.md                 ← a tételenkénti promptok (5 lépés)
│   ├── 00_KIEGESZITO_KOVETELMENYEK.md
│   ├── 00_FORRAS_ID_LISTA.md          ← átnevezési segédlet
│   ├── MODSZERTAN_v5.0.md       ← a teljes módszertan (agent-definíció: 7.2)
│   │
│   ├── 00_tetelsor\
│   │   ├── TETELSOR-NEFROLOGIA-2024-07-25.md   ← horgonyozott, EZ megy a notebookba
│   │   ├── tetelsor_2024-07-25.md              ← kézi, a tetelsor_diff.py-nak
│   │   └── _pdf\
│   │
│   ├── 01_iranyelv_hu\        PRIORITÁS 1 – hatályos magyar (BM)
│   │   ├── _pdf\              ← mesterpéldány, ne töröld
│   │   └── md\                ← horgonyozott → EZ megy a notebookba
│   ├── 02_manet_tarsasag\     PRIORITÁS 2 – MANET, MHT      (_pdf\ + md\)
│   ├── 03_kdigo\              PRIORITÁS 3                    (_pdf\ + md\)
│   ├── 04_tankonyv_hu\        PRIORITÁS 4 – beszkennelt      (_pdf\ + md\)
│   ├── 05_tankonyv_en\        PRIORITÁS 5 – AJKD, angol      (_pdf\ + md\)
│   ├── 06_jog\                NJT, rendeletek                (_pdf\ + md\)
│   ├── 07_sajat_jegyzet\      ← NEM megy generáló notebookba
│   │
│   ├── tetelek_forrasok\      ← 70 forráslap, blokkonként
│   ├── _letoltve\             ← ide töltesz, bármilyen néven
│   ├── _scriptek\
│   │   ├── _kozos.py               ⭐ közös rész: mappaszerkezet, pymupdf, norm()
│   │   ├── atnevezo.py             felismerés + átnevezés + bemozgatás
│   │   ├── pdf_horgonnyal.py       PDF → markdown oldalhorgonnyal
│   │   ├── ellenoriz_idezet.py     szó szerinti idézet + horgony ellenőrzése
│   │   ├── ellenoriz_szamok.py     determinisztikus szám-ellenőrzés (nem AI)
│   │   ├── nyomtathato.py          markdown → nyomtatható HTML
│   │   ├── tetelsor_diff.py        új tételsor összevetése a jelenlegivel
│   │   ├── elavulas_riport.py      melyik forrásnál nézz utána, van-e újabb
│   │   └── futtat.py               ⭐ végigvezet: átnevezés → horgonyozás → riport
│   └── _output\
│       ├── forras\            ← a kinyert idézetek — EZT ellenőrizd legelőbb
│       ├── tetelek\           ← 001.md … 070.md
│       ├── anki\              ← NNN_kartyak.csv
│       ├── ellenorzes\        ← NNN_forrasjegyzek.md + NNN_minosites.md
│       ├── nyomtathato\       ← HTML, ebből nyomtatsz PDF-et
│       └── abrak\             ← Mermaid-források
│
└── _ARCHIV_LEJART\                    ← EZT SOHA nem csatolod
    ├── _pdf\                          a felülírt, lejárt irányelvek
    └── md\                            csak a `99 – ARCHÍV` notebookba
```

> **Miért nincs `hatalyos/` mappa.** A korábbi verziókban volt, mert mellette
> állt egy `lejart/`. Mióta a lejárt anyag kikerült a testvérkönyvtárba, a név
> elveszítette a párját: **ami a munkakönyvtárban van, az definíció szerint
> hatályos.** A szeparáció a könyvtár szintjén történik, nem a mappanévben.

---

## A 11 blokk = 11 NotebookLM notebook

| Mappa | Notebook neve | Tételek | Db |
|---|---|---|---|
| `10_diagnosztika` | `10 – Diagnosztika, vizsgálómódszerek` | 1–4 | 4 |
| `20_viz_elektrolit_savbazis` | `20 – Víz-, elektrolit- és sav-bázis háztartás` | 5–8 | 4 |
| `30_glomerulopatiak` | `30 – Glomerulopátiák, immunológia` | 9–18 | 10 |
| `40_diabetesz_ht_terhesseg` | `40 – Diabétesz, hypertonia, terhesség` | 19–25 | 7 |
| `50_oroklott_tubulopatiak` | `50 – Örökletes betegségek, tubulopátiák` | 26–30 | 5 |
| `60_fertozes_ko_obstrukcio` | `60 – Fertőzés, kő, obstrukció, interstitialis` | 31–37 | 7 |
| `70_szisztemas_vaszkularis` | `70 – Szisztémás, vaszkuláris, geriátria` | 38–40 | 3 |
| `80_akut_vesekarosodas` | `80 – Akut vesekárosodás` | 41–44 | 4 |
| `90_ckd` | `90 – CKD és szövődményei` | 45–55 | 11 |
| `100_vesepotlo_kezeles` | `100 – Vesepótló kezelés (HD, PD, plazmaferezis)` | 56–62 | 7 |
| `110_transzplantacio` | `110 – Transzplantáció` | 63–70 | 8 |
| — | `95 – Saját, ELLENŐRZÖTT` | a kész tételeid | nő |
| — | `99 – ARCHÍV / LEJÁRT` | **generáláshoz soha** | — |

> A notebookonkénti forráskeret bőven elbírja ezt a bontást. **A pontos limiteket a szolgáltató oldalán ellenőrizd** — gyakran változnak, és előfizetési szintenként eltérnek. Az ingyenes szint notebookonként kevesebbet enged, de egy blokkhoz (~12 forrás) az is elég.

### Az átfedésről

Néhány tétel átível a blokkokon (a diabéteszes nephropathia a 40-esbe és a
90-esbe is tartozik). A megoldás, hogy a **határterületi forrásokat két
notebookba is feltöltöd** — a forráskeret ezt elbírja. Ne próbálj tökéletes
particionálást; a cél a zaj csökkentése, nem a taxonómia.


---

## Haladás

| Blokk | Letöltve | Feltöltve | Kidolgozva | Ellenőrizve |
|---|---|---|---|---|
| 10 – Diagnosztika, vizsgálómódszerek | [ ] | [ ] | [ ] | [ ] |
| 20 – Víz-, elektrolit- és sav-bázis háztartás | [ ] | [ ] | [ ] | [ ] |
| 30 – Glomerulopátiák, immunológia | [ ] | [ ] | [ ] | [ ] |
| 40 – Diabétesz, hypertonia, terhesség | [ ] | [ ] | [ ] | [ ] |
| 50 – Örökletes betegségek, tubulopátiák | [ ] | [ ] | [ ] | [ ] |
| 60 – Fertőzés, kő, obstrukció, interstitialis | [ ] | [ ] | [ ] | [ ] |
| 70 – Szisztémás, vaszkuláris, geriátria | [ ] | [ ] | [ ] | [ ] |
| 80 – Akut vesekárosodás | [ ] | [ ] | [ ] | [ ] |
| 90 – CKD és szövődményei | [ ] | [ ] | [ ] | [ ] |
| 100 – Vesepótló kezelés (HD, PD, plazmaferezis) | [ ] | [ ] | [ ] | [ ] |
| 110 – Transzplantáció | [ ] | [ ] | [ ] | [ ] |

*Created using Anthropic Claude*
