# -*- coding: utf-8 -*-
"""
PDF -> markdown, oldalhorgonyokkal.

Használat:
    pip install pymupdf
    python _scriptek/pdf_horgonnyal.py

Végigmegy a forrásmappák _pdf/ almappáin, és minden PDF-bol .md-t keszit:

    ===== [CKD-IRANYELV-BM-2025 | p.047] =====

A p.NNN a PDF FIZIKAI oldalszama (1-tol, boritoval egyutt) — NEM a
dokumentum sajat, nyomtatott lapszama. A ketto gyakran elter! Ezert a
visszakeresesnel a PDF-nezegeto oldalszam-mezojet hasznald, ne a lapon
nyomtatott szamot. Minden generalt .md elejere ez a megjegyzes bekerul.

A forras_id a FAJLNEVBOL jon, kiterjesztes nelkul. Ezert fontos, hogy a
letoltes utan atnevezd a fajlokat a tervezett forras_id-ra.

A .md megy a NotebookLM-be. A PDF a mesterpeldany, azt ne dobd el.
"""
from __future__ import annotations

import pathlib, sys

from _kozos import GYOKER, PAROK, ARCHIV_PDF, ARCHIV_MD, pymupdf_betolt

fitz = pymupdf_betolt()


# A lejart anyag a munkakonyvtaron KIVUL van (testverkonyvtar), ezert kulon par.
# A belole keszulo .md KIZAROLAG a "99 - ARCHIV" notebookba mehet, generalo
# notebookba SOHA. Ezert kulon fut, es kulon figyelmeztetest is ir.

def pdf_horgonnyal(pdf_ut: pathlib.Path) -> tuple[str, int, int]:
    forras_id = pdf_ut.stem
    doc = fitz.open(pdf_ut)
    reszek, ures = [], 0
    # FEJLEC: a NotebookLM-be is bekerul, igy a modell is latja, mit jelent a p.NNN
    reszek.append(
        f"> **Forras:** {forras_id}\n"
        f"> **A horgonyokban szereplo p.NNN a PDF FIZIKAI oldalszama** "
        f"(1-tol szamozva, borito is beleertve), nem a dokumentum sajat, "
        f"nyomtatott lapszama. Visszakeresesnel a PDF-nezegeto oldalszamat hasznald.\n\n"
    )
    for i, oldal in enumerate(doc, start=1):
        reszek.append(f"\n\n===== [{forras_id} | p.{i:03d}] =====\n\n")
        szoveg = oldal.get_text()
        if len(szoveg.strip()) < 20:
            ures += 1
        reszek.append(szoveg)
    return "".join(reszek), len(doc), ures

def main():
    osszes = 0
    for pdf_mappa, md_mappa in PAROK:
        be, ki = GYOKER / pdf_mappa, GYOKER / md_mappa
        if not be.exists():
            continue
        ki.mkdir(parents=True, exist_ok=True)
        for pdf in sorted(be.glob("*.pdf")):
            szoveg, oldalak, ures = pdf_horgonnyal(pdf)
            cel = ki / (pdf.stem + ".md")
            cel.write_text(szoveg, encoding="utf-8")
            jel = ""
            if ures:
                jel = f"  <-- FIGYELEM: {ures} ures oldal, lehet szkennelt -> OCR kell"
            print(f"{pdf.name}  ->  {cel.relative_to(GYOKER)}  ({oldalak} oldal){jel}")
            osszes += 1
    # --- archivum: csak akkor, ha letezik, es hangos figyelmeztetessel ---
    arc_be, arc_ki = GYOKER / ARCHIV_PDF, GYOKER / ARCHIV_MD
    arc_db = 0
    if arc_be.exists() and list(arc_be.glob("*.pdf")):
        arc_ki.mkdir(parents=True, exist_ok=True)
        print("\n--- _ARCHIV_LEJART (lejart anyag) ---")
        for pdf in sorted(arc_be.glob("*.pdf")):
            szoveg, oldalak, _ = pdf_horgonnyal(pdf)
            cel = arc_ki / (pdf.stem + ".md")
            cel.write_text(szoveg, encoding="utf-8")
            print(f"{pdf.name}  ->  _ARCHIV_LEJART/md/{cel.name}  ({oldalak} oldal)")
            arc_db += 1
        print("\n*** FIGYELEM ***")
        print(f"{arc_db} LEJART dokumentum .md-je elkeszult az _ARCHIV_LEJART/md/ alatt.")
        print("Ezek KIZAROLAG a '99 - ARCHIV' notebookba mehetnek, verzio-osszevetesre.")
        print("Generalo notebookba SOHA ne toltsd fel oket, es a mappat ne csatold.")

    if not osszes and not arc_db:
        print("Nem talaltam PDF-et a _pdf/ mappakban. Eloszor tolts le valamit.")
    else:
        print(f"\nKesz: {osszes} fajl.")
        print("Ellenorizd a tablazatokat a .md-ben (CKD-stadiumok, eGFR-kategoriak,")
        print("dosziskorrekcios tablak) - a szovegkinyeres ezeket szet tudja szedni.")

if __name__ == "__main__":
    main()
