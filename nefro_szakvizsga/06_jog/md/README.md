# `md/` — oldalhorgonnyal ellátott markdown

Ide a `pdf_horgonnyal.py` írja a `_pdf/` mappából konvertált fájlokat:

```
===== [CKD-IRANYELV-BM-2025 | p.047] =====
```

> ## Ezt töltöd fel a NotebookLM-be — ne a PDF-et
>
> Két okból: a szövegkinyerés így determinisztikus (nem a Google
> parsere dönti el, mi lesz a táblázatból), és a horgonyok garantáltan
> bekerülnek az indexbe. **Horgony nélkül a modell az oldalszámot vagy
> elhagyja, vagy kitalálja.**

## Feltöltés előtt nézd át a táblázatokat

CKD-stádiumbeosztás, eGFR-kategóriák, albuminuria-besorolás,
dóziskorrekciós táblák. Ezek a legfontosabb adatok az egész anyagban,
és a szövegkinyerés szét tudja szedni őket. Ami szétesett, azt a néhány
oldalt kézzel vagy vision-OCR-rel pótold.

---

## A jogi anyag: KETTŐS hivatkozás

Jogszabálynál **mindkét azonosító kell**:

```
[NJT-EUTV-1997-CLIV-2026-10-08 | p.012 | 12. § (3)]
```

| | Mire való |
|---|---|
| **oldalszám** | ettől **géppel ellenőrizhető** — az `ellenoriz_idezet.py` látja |
| **szakaszszám** | ez a jogszabály stabil egysége, és ezt mondod a vizsgán |

> 🔴 **Ezért a jogszabályokat is PDF-be nyomtatod**, nem linkeled.
> Egy linkelt forrásban nincs `=====` horgony, tehát a hivatkozás nem
> ellenőrizhető — és a modell vagy elhagyja az oldalszámot, vagy kitalálja.

**Hogyan kerül ide fájl:** megnyitod az njt.hu-n a rendeletet, **kinyitod a
lenyíló részeket**, `Ctrl+P` → *Mentés PDF-ként*, **fejléc/lábléc KI**.
Dátumos néven mented a `_pdf\` mappába, és lefuttatod a `pdf_horgonnyal.py`-t.

Részletesen: `00_PARANCSOK_WINDOWS11.md` **7/b** lépés.
