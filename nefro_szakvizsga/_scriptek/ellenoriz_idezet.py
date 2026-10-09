# -*- coding: utf-8 -*-
"""
Ellenorzi, hogy a kinyert <forras> blokk idezetei SZO SZERINT megtalalhatok-e
a forrasfajlban, es hogy a horgony a HELYES oldalra mutat-e.

MIERT EZ A LEGFONTOSABB SZKRIPT A "CSAK CLAUDE" UTVONALON
----------------------------------------------------------
Ha nincs NotebookLM, akkor a kinyerest is a Claude vegzi a mappabol. A
kinyeres viszont pont az a lepes, ahol eldol minden: ha ott atfogalmaz vagy
kitalal, utana mar hiaba tokeletes a formatum.

A szerencse az, hogy a kinyeres helyesseget NEM kell AI-nak ellenoriznie:
egy idezet vagy ott van a forrasban, vagy nincs. Ez szovegosszehasonlitas.

HASZNALAT
---------
    python _scriptek/ellenoriz_idezet.py _output/forras/047_forras.md
    python _scriptek/ellenoriz_idezet.py            # az osszes

A bemeneti fajl formatuma (ezt allitja elo a kinyero lepes):

    ===== [CKD-IRANYELV-BM-2025 | p.047] =====
    "A stadiumbeosztas alapja a becsult GFR es az albuminuria."
    "Mersekelten csokkent GFR (G3a): 45-59 ml/min/1,73 m2"

    ===== [KDIGO-CKD | p.012] =====
    "..."
"""
from __future__ import annotations

import pathlib, re, sys

import _kozos
from _kozos import GYOKER, HORGONY, norm

FORRAS_MAPPAK = _kozos.MD_MAPPAK



# Idezojel-, kotojel- es szokoz-valtozatok egysegesitese.
#
# NEM sebessegi okbol translate (az valojaban kicsit lassabb, mint nehany
# replace) - hanem a LEFEDETTSEG miatt: a PDF-bol kinyert szovegben eloforcul
# a U+2010 kotojel, a nem-toro es a keskeny szokoz, a francia idezojel. Ezek
# a regi listaban nem szerepeltek, es hamis "NINCS A FORRASBAN" talalatot
# okoztak olyan idezeteknel, amik valojaban ott voltak.
EGYSEGESIT = str.maketrans({
    "„": '"', "”": '"', "“": '"', "»": '"', "«": '"',
    "’": "'", "‘": "'", "´": "'",
    "–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-",
    " ": " ", " ": " ", " ": " ", " ": " ",
})


def forrasok_beolvas() -> dict[str, dict[int, str]]:
    """forras_id -> {oldalszam: normalizalt szoveg}"""
    ki: dict[str, dict[int, str]] = {}
    for mappa in FORRAS_MAPPAK:
        d = GYOKER / mappa
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            if f.name == "README.md":
                continue
            akt_id, akt_oldal, puffer = None, None, []
            # darabok listaban gyulnek, a vegen egyszer joinolunk:
            # a korabbi "sztring += ..." minden horgonynal ujramasolta az
            # egesz oldalt, ami nagy iranyelveknel nagysagrendekkel lassabb
            darabok: dict[str, dict[int, list]] = {}
            def ment():
                if akt_id is not None and akt_oldal is not None:
                    darabok.setdefault(akt_id, {}).setdefault(akt_oldal, []).append(
                        norm("\n".join(puffer)))
            for sor in f.read_text(encoding="utf-8").split("\n"):
                m = HORGONY.match(sor.strip())
                if m:
                    ment(); puffer = []
                    akt_id, akt_oldal = m.group(1), int(m.group(2))
                else:
                    puffer.append(sor)
            ment()
            for fid, oldalak in darabok.items():
                cel = ki.setdefault(fid, {})
                for oldal, reszek in oldalak.items():
                    cel[oldal] = (cel.get(oldal, "") + " " + " ".join(reszek)).strip()
    return ki

def ellenoriz(be: pathlib.Path, forrasok: dict) -> tuple[int, int]:
    jo = rossz = 0
    rovid: list[tuple[int, str]] = []
    akt_id = akt_oldal = None
    print(f"\n== {be.name}")
    for szam, sor in enumerate(be.read_text(encoding="utf-8").split("\n"), start=1):
        t = sor.strip()
        m = HORGONY.match(t)
        if m:
            akt_id, akt_oldal = m.group(1), int(m.group(2))
            if akt_id not in forrasok:
                print(f"  {szam:4d}  ISMERETLEN FORRAS-ID: {akt_id}")
                print(f"        (ismert: {', '.join(sorted(forrasok)[:6])}…)")
            continue
        if not t or t.startswith("#") or norm(t).startswith("nincs tal"):
            continue
        idezet = t.strip('"„”*-• ').strip()
        if len(idezet) < 10:          # ennyi alatt nem ertelmezheto idezet
            if idezet:
                rovid.append((szam, idezet))
            continue
        if akt_id is None:
            print(f"  {szam:4d}  HORGONY NELKULI IDEZET: {idezet[:60]}…")
            rossz += 1
            continue
        n = norm(idezet)
        oldalak = forrasok.get(akt_id, {})
        # az oldalhataron atnyulo mondat miatt a kovetkezo oldalt is hozzafuzzuk
        atfedo = re.sub(r"\s+", " ",
                        oldalak.get(akt_oldal, "") + " " + oldalak.get((akt_oldal or 0) + 1, ""))
        if n in oldalak.get(akt_oldal, ""):
            jo += 1
        elif akt_oldal is not None and n in atfedo:
            print(f"  {szam:4d}  OLDALHATARON ATNYULO (p.{akt_oldal:03d}-{akt_oldal+1:03d}) - elfogadva")
            jo += 1
        else:
            talalt = [o for o, szov in oldalak.items() if n in szov]
            if talalt:
                print(f"  {szam:4d}  ROSSZ OLDAL: horgony p.{akt_oldal:03d}, "
                      f"valojaban p.{talalt[0]:03d}")
                print(f"        {idezet[:70]}…")
            else:
                print(f"  {szam:4d}  NINCS A FORRASBAN ({akt_id}):")
                print(f"        {idezet[:70]}…")
            rossz += 1
    if rovid:
        print(f"  {len(rovid)} tul rovid sor kihagyva (10 karakter alatt):")
        for szam, sz in rovid[:5]:
            print(f"        {szam:4d}  {sz}")
        if len(rovid) > 5:
            print(f"        ... es meg {len(rovid)-5} db")
        print("        Ha ezek kozott szamot tartalmazo mondat van, nezd at kezzel.")
    print(f"  --> {jo} rendben, {rossz} problemas")
    return jo, rossz

def main():
    forrasok = forrasok_beolvas()
    if not forrasok:
        sys.exit("Nem talaltam horgonyozott forrasfajlt. Futtasd eloszor:\n"
                 "  python _scriptek/pdf_horgonnyal.py")
    print(f"Forrasok betoltve: {len(forrasok)} dokumentum, "
          f"{sum(len(v) for v in forrasok.values())} oldal.")

    argok = [a for a in sys.argv[1:] if not a.startswith("--")]
    fajlok = ([pathlib.Path(a) for a in argok] if argok
              else sorted((GYOKER / "_output" / "forras").glob("*.md")))
    fajlok = [f for f in fajlok if f.exists()]
    if not fajlok:
        sys.exit("Nincs ellenorizendo fajl az _output/forras/ mappaban.")

    jo = rossz = 0
    for f in fajlok:
        a, b = ellenoriz(f, forrasok); jo += a; rossz += b

    print(f"\n==== OSSZESEN: {jo} rendben, {rossz} problemas")
    if rossz:
        print("\nA problemas idezetek NEM hasznalhatok. Ket lehetoseg:")
        print("  - a kinyero lepes atfogalmazott -> futtasd ujra, szigorubb prompttal")
        print("  - a horgony csuszott el -> javitsd kezzel")
        sys.exit(1)

if __name__ == "__main__":
    main()
