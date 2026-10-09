# -*- coding: utf-8 -*-
"""
Vegigvezet a rendszerezesen: atnevezo.py -> pdf_horgonnyal.py -> riport.

Windowson es Linuxon/macOS-en egyarant fut. Nincs kulon .bat es .sh.

HASZNALAT
---------
    python _scriptek/futtat.py          # lepesenkent, megerositessel
    python _scriptek/futtat.py --gyors  # szaraz futas es szunetek nelkul

MIERT KELL
----------
A harom lepes sorrendje kotott, es a masodik INTERAKTIV (kerdez). Ha a
sorrendet elrontod, vagy a szaraz futast kihagyod, csendben rossz
fajlnevekkel dolgozol tovabb — es a forras_id a fajlnevbol jon, vagyis
az egesz hivatkozasi lanc rosszul all ossze.

Ez a szkript csak osszefogja a lepeseket. Semmi ujat nem csinal.
"""
from __future__ import annotations

import subprocess, sys, pathlib, shutil

SZK = pathlib.Path(__file__).resolve().parent
GYOKER = SZK.parent
GYORS = "--gyors" in sys.argv

# Windows-konzolon az emoji/unicode elszallhat -> ASCII keretek
VONAL = "=" * 66


def cim(n, szoveg):
    print(f"\n{VONAL}\n  {n}. LEPES — {szoveg}\n{VONAL}")


def varj(kerdes="Mehet tovabb? [Enter = igen, n = kilepes] "):
    if GYORS:
        return True
    try:
        return input(f"\n>>> {kerdes}").strip().lower() not in ("n", "nem", "q")
    except (EOFError, KeyboardInterrupt):
        print("\nMegszakitva.")
        return False


def futtat(nev, *argok, interaktiv=False):
    """A szkriptet UGYANAZZAL a Python-nal inditja, ami ezt futtatja."""
    ut = SZK / nev
    if not ut.exists():
        print(f"  HIANYZIK: {ut}")
        return False
    parancs = [sys.executable, str(ut), *argok]
    print(f"  $ {' '.join(parancs[1:])}\n")
    # stdio oroklodik -> az atnevezo.py tud kerdezni, te tudsz valaszolni
    kod = subprocess.call(parancs, cwd=str(GYOKER))
    if kod != 0:
        print(f"\n  !! A szkript {kod} hibakoddal allt le.")
        return False
    return True


def pymupdf_ellenorzes():
    try:
        import pymupdf  # noqa: F401
        return True
    except ImportError:
        try:
            import fitz  # noqa: F401
            return True
        except ImportError:
            pass
    print("  Hianyzik a pymupdf (ez az egyetlen fuggoseg).")
    if not varj("Telepitsem most? [Enter = igen, n = nem] "):
        return False
    return subprocess.call(
        [sys.executable, "-m", "pip", "install", "pymupdf"]) == 0


def main():
    print(f"\n{VONAL}")
    print("  NEFROLOGIAI SZAKVIZSGA — rendszerezes")
    print(f"  Munkakonyvtar: {GYOKER}")
    print(f"  Python:        {sys.version.split()[0]}  ({sys.executable})")
    print(VONAL)

    # --- 0. kornyezet ---
    if not pymupdf_ellenorzes():
        sys.exit("\nA pymupdf nelkul egyik szkript sem fut. Telepitsd:\n"
                 "  python -m pip install pymupdf")

    letoltve = GYOKER / "_letoltve"
    pdfek = list(letoltve.glob("*.pdf")) + list(letoltve.glob("*.PDF"))
    print(f"\n  _letoltve/ : {len(pdfek)} PDF")
    if not pdfek:
        print("\n  Nincs mit rendszerezni. Toltsd le a forrasokat a")
        print("  _letoltve/ mappaba (lasd 00_LETOLTESI_TERV.md), es futtasd ujra.")
        print("\n  Megjegyzes: a bongeszobol nyomtatott PDF-eket (jogszabaly,")
        print("  online cikk) NEM ide mented, hanem egybol a cel _pdf/ mappaba,")
        print("  kezzel elnevezve. Azokra csak a 3. lepes kell.")
        if not varj("Ugorjunk egybol a horgonyozasra? [Enter = igen, n = kilepes] "):
            return
    else:
        # --- 1. szaraz futas ---
        if not GYORS:
            cim(1, "atnevezo.py --szaraz  (nem nyul semmihez)")
            print("  Csak kiirja, melyik fajlt minek ismerte fel.")
            print("  Fusd at: ertelmesnek tunnek a tippek?\n")
            if not futtat("atnevezo.py", "--szaraz"):
                sys.exit(1)
            if not varj():
                return

        # --- 2. eles atnevezes (INTERAKTIV) ---
        cim(2, "atnevezo.py  (kerdezni fog)")
        print("  Enter = elfogadod a tippet | 1/2/3 = masik | s = kihagyas")
        print("  vagy beirod a sajat forras_id-t.\n")
        if not futtat("atnevezo.py", interaktiv=True):
            sys.exit(1)
        if not varj():
            return

    # --- 3. horgonyozas ---
    cim(3, "pdf_horgonnyal.py  (PDF -> markdown oldalhorgonnyal)")
    print("  Minden oldal ele beirja:  ===== [FORRAS-ID | p.NNN] =====")
    print("  A vegen kulon feldolgozza az _ARCHIV_LEJART/ mappat is.\n")
    if not futtat("pdf_horgonnyal.py"):
        sys.exit(1)

    # --- 4. elavulas-riport (opcionalis) ---
    if (SZK / "elavulas_riport.py").exists():
        if GYORS or varj("Lefussak az elavulas-riportot is? [Enter = igen, n = nem] "):
            cim(4, "elavulas_riport.py  (csak kiir, nem mozgat)")
            futtat("elavulas_riport.py")

    # --- zaras ---
    print(f"\n{VONAL}")
    print("  KESZ. Ami meg hatra van, azt gep nem tudja megcsinalni:")
    print(VONAL)
    print("""
  1. AMIT AZ ATNEVEZO KIHAGYOTT
     Nevezd at kezzel a 00_FORRAS_ID_LISTA.md alapjan, es futtasd ujra
     ezt a szkriptet.

  2. TABLAZAT-ELLENORZES  (~15 perc, NE hagyd ki)
     Nyiss meg 2-3 generalt .md-t, es nezd meg a tablazatokat:
     CKD-stadiumbeosztas, eGFR-kategoriak, albuminuria-besorolas,
     doziskorrekcios tablak. Ezek a legfontosabb adatok az egesz
     anyagban, es a szovegkinyeres szet tudja szedni oket.

  3. SZEPARACIO-ELLENORZES
     Nezd meg, hogy a lejart anyag tenyleg az _ARCHIV_LEJART/ mappaban
     van-e, es a munkakonyvtarban NINCS. Ez a rendszer egyetlen
     100%-os vedelme.

  4. FELTOLTES A NOTEBOOKLM-BE
     A md/ mappak .md fajljai mennek fel — NEM a PDF-ek.
     Melyik hova: 00_NOTEBOOK_FELTOLTES.md
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nMegszakitva.")
