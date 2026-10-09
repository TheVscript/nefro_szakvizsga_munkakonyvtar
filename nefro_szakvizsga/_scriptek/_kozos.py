# -*- coding: utf-8 -*-
"""
Kozos resz a tobbi szkriptnek. ONMAGABAN NEM FUTTATHATO.

MIERT VAN EZ A FAJL
-------------------
Harom dolog korabban tobb szkriptben is szerepelt, egymastol fuggetlenul:

  1. A mappaszerkezet — HAROM kulonbozo listaban (pdf-mappak, md-mappak,
     pdf->md parok). Ha felvettel volna egy uj forrasmappat, harom helyen
     kellett volna atvezetni, es az egyik biztosan kimarad.
  2. A pymupdf import-fallback (pymupdf / fitz) — harom szkriptben.
  3. A szovegnormalizalas (norm) — ket szkript hasznalja.

Itt mindegyik EGYSZER szerepel. Ha a mappaszerkezet valtozik, a BLOKKOK
listat kell modositani, es minden szkript egyszerre kovet.

A szkriptek `import _kozos`-szal erik el. Ez mukodik, mert a Python a
futtatott szkript konyvtarat automatikusan a sys.path ele teszi.
"""
from __future__ import annotations

import pathlib
import re
import sys
import unicodedata

GYOKER = pathlib.Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# A MAPPASZERKEZET — EGYETLEN forras minden szkriptnek
#
#   (blokk-mappa, pdf-almappa, md-almappa)
#
# A 00_tetelsor kivetel: ott a .md kozvetlenul a blokk-mappaba kerul, nem
# egy md/ almappaba. Ezt az ures string jelzi.
# ---------------------------------------------------------------------------
BLOKKOK: list[tuple[str, str, str]] = [
    ("00_tetelsor",       "_pdf", ""),
    ("01_iranyelv_hu",    "_pdf", "md"),
    ("02_manet_tarsasag", "_pdf", "md"),
    ("03_kdigo",          "_pdf", "md"),
    ("04_tankonyv_hu",    "_pdf", "md"),
    ("05_tankonyv_en",    "_pdf", "md"),
    ("06_jog",            "_pdf", "md"),
]

# A lejart anyag a munkakonyvtaron KIVUL van (testverkonyvtar).
# Kulon kezeljuk, mert a belole keszult .md CSAK a "99 - ARCHIV"
# notebookba mehet, generalo notebookba soha.
ARCHIV_PDF = "../_ARCHIV_LEJART/_pdf"
ARCHIV_MD = "../_ARCHIV_LEJART/md"

# KDIGO és AJKD CC dokumentumok — PRIORITÁS 3 – Nemzetközi irányelv
KDIGO_PDF = "03_kdigo/_pdf"
KDIGO_FORRASOK = {
    "EULAR-ERA-LN-2023": (KDIGO_PDF, "EULAR-ERA-LN-2023.pdf"),
    "ISPD-PERITONITIS-2022": (KDIGO_PDF, "ISPD-PERITONITIS-2022.pdf"),
    "ISPD-PRESCRIBING-2020": (KDIGO_PDF, "ISPD-PRESCRIBING-2020.pdf"),
    "KDIGO-CKD-2024": (KDIGO_PDF, "KDIGO-CKD-2024.pdf"),
    "KDIGO-DIABETES-2023": (KDIGO_PDF, "KDIGO-DIABETES-2023.pdf"),
}


def _ut(blokk: str, al: str) -> str:
    return f"{blokk}/{al}" if al else blokk


#: PDF-mappa -> md-mappa parok (pdf_horgonnyal.py)
PAROK: list[tuple[str, str]] = [(_ut(b, p), _ut(b, m)) for b, p, m in BLOKKOK]

#: Csak a PDF-mappak (elavulas_riport.py)
PDF_MAPPAK: list[str] = [_ut(b, p) for b, p, _ in BLOKKOK]

#: Csak az md-mappak (ellenoriz_idezet.py).
#: A 00_tetelsor a vegen all, mert a korpusz-keresesben az a legkevesbe
#: valoszinu talalat — igy a gyakori forrasok elobb jonnek.
MD_MAPPAK: list[str] = ([_ut(b, m) for b, _, m in BLOKKOK if b != "00_tetelsor"]
                        + ["00_tetelsor"])


# ---------------------------------------------------------------------------
# pymupdf betoltes — a csomag ket neven is elerheto lehet
# ---------------------------------------------------------------------------
def pymupdf_betolt():
    """A pymupdf modult adja vissza, vagy ertheto hibaval kilep."""
    try:
        import pymupdf
        return pymupdf
    except ImportError:
        pass
    try:
        import fitz
        return fitz
    except ImportError:
        sys.exit("Hianyzik a pymupdf (ez az egyetlen fuggoseg). Telepitsd:\n"
                 "  python -m pip install pymupdf")


# ---------------------------------------------------------------------------
# Szovegnormalizalas — az idezet-osszehasonlitas alapja
# ---------------------------------------------------------------------------

#: A horgony formatuma:  ===== [FORRAS-ID | p.047] =====
HORGONY = re.compile(r"^=====\s*\[([A-Za-z0-9_-]+)\s*\|\s*p\.(\d+)\]\s*=====\s*$")

#: Sorvegi elvalasztas: "kezele-\nse" -> "kezelese"
ELVALASZTAS = re.compile(r"(\w)[-‐‑\xad]\s*\n\s*(\w)")

TOBB_SZOKOZ = re.compile(r"\s+")

# Idezojel-, kotojel- es szokoz-valtozatok egysegesitese.
#
# NEM sebessegi okbol translate (az valojaban kicsit lassabb, mint nehany
# replace) — hanem a LEFEDETTSEG miatt: a PDF-bol kinyert szovegben eloforul
# a U+2010 kotojel, a nem-toro es a keskeny szokoz, a francia idezojel. Ezek
# nelkul hamis "NINCS A FORRASBAN" talalatot kapnank olyan idezeteknel,
# amik valojaban ott vannak a forrasban.
EGYSEGESIT = str.maketrans({
    "„": '"', "”": '"', "“": '"', "»": '"', "«": '"',
    "’": "'", "‘": "'", "´": "'",
    "–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-",
    " ": " ", " ": " ", " ": " ", " ": " ",
    "\xad": None,  # lagy elvalasztojel: NFKC nem tavolitja el
})


def norm(s: str) -> str:
    """Osszehasonlithato alak: elvalasztas feloldva, jelek egysegesitve,
    szokozok osszevonva, kisbetus."""
    s = ELVALASZTAS.sub(r"\1\2", s)
    s = unicodedata.normalize("NFKC", s)
    s = s.translate(EGYSEGESIT)
    return TOBB_SZOKOZ.sub(" ", s).strip().lower()


if __name__ == "__main__":
    sys.exit("Ez a fajl a tobbi szkript kozos resze, onmagaban nem futtathato.\n"
             "Hasznald pl. ezt:  python _scriptek/futtat.py")
