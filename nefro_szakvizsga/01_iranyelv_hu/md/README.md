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
