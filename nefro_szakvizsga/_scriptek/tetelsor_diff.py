# -*- coding: utf-8 -*-
"""
Osszeveti egy uj tetelsor-PDF kerdeslistajat a jelenlegi tetelsor_*.md-vel.

HASZNALAT
    python _scriptek/tetelsor_diff.py
    python _scriptek/tetelsor_diff.py <uj.pdf>

A szkript MECHANIKUSAN hasonlit: megmondja, melyik sorszamnal valtozott a
szoveg, mi kerult hozza, mi tunt el.

Amit NEM csinal meg: a blokkbeosztas es a forras-hozzarendeles atvezeteset.
Az szerkesztoi dontes. A diff alapjan te (vagy az AI) vezeted at a
tetelek_forrasok/ lapokon.
"""
from __future__ import annotations

import pathlib, re, sys, difflib

from _kozos import GYOKER
TS = GYOKER / "00_tetelsor"

def kerdesek_pdfbol(pdf: pathlib.Path) -> dict[int, str]:
    from _kozos import pymupdf_betolt
    fitz = pymupdf_betolt()
    doc = fitz.open(pdf)
    teljes = "\n".join(o.get_text() for o in doc)
    # a "Vizsgakerdesek" utani szamozott lista
    i = teljes.lower().find("vizsgak")
    if i >= 0:
        teljes = teljes[i:]
    ki, elozo = {}, 0
    for m in re.finditer(r"^\s*(\d{1,3})\.\s+(.+)$", teljes, re.M):
        n, szoveg = int(m.group(1)), m.group(2).strip()
        if n == elozo + 1:          # csak folytonos sorszamozast fogadunk el
            ki[n] = szoveg
            elozo = n
    return ki

def kerdesek_mdbol(md: pathlib.Path) -> dict[int, str]:
    ki = {}
    for sor in md.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^\|\s*(\d{1,3})\s*\|\s*(.+?)\s*\|", sor)
        if m:
            ki[int(m.group(1))] = m.group(2).strip()
    return ki

def main():
    if len(sys.argv) > 1:
        uj_pdf = pathlib.Path(sys.argv[1])
    else:
        jeloltek = sorted((TS / "_pdf").glob("*.pdf"))
        if not jeloltek:
            sys.exit("Nincs PDF a 00_tetelsor/_pdf/ mappaban.")
        uj_pdf = jeloltek[-1]

    regi_md = sorted(TS.glob("tetelsor_*.md"))
    if not regi_md:
        sys.exit("Nincs tetelsor_*.md a 00_tetelsor/ mappaban.")
    regi_md = regi_md[-1]

    uj = kerdesek_pdfbol(uj_pdf)
    regi = kerdesek_mdbol(regi_md)

    print(f"regi: {regi_md.name}   ({len(regi)} kerdes)")
    print(f"uj:   {uj_pdf.name}   ({len(uj)} kerdes)\n")

    if not uj:
        sys.exit("Nem talaltam szamozott kerdeslistat az uj PDF-ben. "
                 "Nezd meg kezzel.")

    valtozott = uj_tetel = eltunt = 0
    for n in sorted(set(regi) | set(uj)):
        r, u = regi.get(n), uj.get(n)
        if r is None:
            print(f"  + {n:3d}  UJ TETEL:  {u}"); uj_tetel += 1
        elif u is None:
            print(f"  - {n:3d}  ELTUNT:    {r}"); eltunt += 1
        elif r.lower() != u.lower():
            arany = difflib.SequenceMatcher(None, r.lower(), u.lower()).ratio()
            cimke = "atfogalmazas" if arany > 0.6 else "MAS TETEL"
            print(f"  ~ {n:3d}  {cimke} ({arany:.0%}):")
            print(f"          regi: {r}")
            print(f"          uj:   {u}")
            valtozott += 1

    print(f"\n==== uj: {uj_tetel}  eltunt: {eltunt}  valtozott: {valtozott}")
    if uj_tetel or eltunt or valtozott:
        print("\nTeendo:")
        print("  1. tetelek_forrasok/ : az erintett NNN.md lapok atnezese")
        print("  2. 00_tetelsor/tetelsor_*.md : uj nevvel menteni, frissiteni")
        print("  3. a blokkbeosztas felulvizsgalata (szerkesztoi dontes)")
    else:
        print("Nincs valtozas a kerdeslistaban.")

if __name__ == "__main__":
    main()
