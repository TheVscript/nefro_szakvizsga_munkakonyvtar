# -*- coding: utf-8 -*-
"""
Determinisztikus ellenorzes az Anki-kartyakra. NEM AI.

HAROM dolgot vizsgal, mindharmat gepi osszehasonlitassal:

  1. SZAMOK      — a Valasz minden szama szerepel-e az Idezet-ben
  2. IDEZET      — az Idezet szo szerint megvan-e a horgonyozott forrasban
  3. SZERKEZET   — megvan-e mind a 7 oszlop

Hasznalat:
    python _scriptek/ellenoriz_szamok.py _output/anki/051_kartyak.csv
    python _scriptek/ellenoriz_szamok.py          # az osszes CSV-re
    python _scriptek/ellenoriz_szamok.py --csak-szam   # idezet-ellenorzes nelkul

MIERT TOKENES A SZAMOSSZEHASONLITAS
-----------------------------------
A korabbi valtozat reszsztringet keresett: az "5" "megtalalhato" volt a
"45-59"-ben, tehat egy kitalalt 5-os ertek atment. Most mindket mezobol
szamTOKENEKET nyerunk ki, es halmazkent hasonlitunk. Egy szam vagy
onallo tokenkent ott van az idezetben, vagy nincs.

MIERT KELL AZ IDEZET-ELLENORZES IS
----------------------------------
A szam-ellenorzes csak azt nezi, hogy a Valasz es az Idezet osszhangban
van-e EGYMASSAL. Ha a modell az IDEZETET is elrontotta (atfogalmazta),
a ketto konzisztens marad, es a kartya atmegy — pedig a forrasban nem
az all. Ezert az Idezet mezot a forrashoz is hozzamerjuk.
"""
from __future__ import annotations   # a "str | None" jeloles 3.9-en is mukodjon

import csv, html, re, sys, unicodedata, pathlib

from _kozos import GYOKER, norm
from ellenoriz_idezet import forrasok_beolvas
SZAM = re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)?(?![\w.,]*\d)")

# Csak a horgony-alaku [ID | p.NNN] blokk: egy sima [30–300 mg/g] tartalmi adat, marad.
HORGONY_SZOVEGBEN = re.compile(r"\[[^\[\]]*\|\s*p\.\s*\d+[^\[\]]*\]")
HTML_CIMKE = re.compile(r"<[^>]+>")


def szam_tokenek(szoveg: str) -> set[str]:
    """Szamok halmaza, normalizalt alakban (tizedesvesszo -> pont)."""
    sz = unicodedata.normalize("NFKC", html.unescape(szoveg))
    sz = HORGONY_SZOVEGBEN.sub(" ", sz)
    sz = HTML_CIMKE.sub(" ", sz)
    return {m.group(0).replace(",", ".").rstrip(".")
            for m in SZAM.finditer(sz)}


def hianyzo_szamok(valasz: str, idezet: str) -> list[str]:
    """A Valasz azon szamai, amik az Idezet-ben NEM szerepelnek tokenkent."""
    return sorted(szam_tokenek(valasz) - szam_tokenek(idezet),
                  key=lambda x: (len(x), x))


def idezet_megvan(idezet: str, horgony: str, forrasok: dict) -> str | None:
    """None = rendben. Egyebkent a hiba szovege."""
    if not forrasok:
        return None
    m = re.match(r"\s*\[?([A-Za-z0-9_-]+)\s*\|\s*p\.(\d+)\]?", horgony.strip())
    if not m:
        return f"ERTELMEZHETETLEN HORGONY: {horgony[:40]}"
    fid, oldal = m.group(1), int(m.group(2))
    if fid not in forrasok:
        return f"ISMERETLEN FORRAS-ID: {fid}"
    n = norm(idezet.strip('"„”*-• '))
    if len(n) < 10:
        return None                       # tul rovid, nem ertelmezheto
    oldalak = forrasok[fid]
    if n in oldalak.get(oldal, ""):
        return None
    talalt = [o for o, szov in oldalak.items() if n in szov]
    if talalt:
        return f"ROSSZ OLDAL: horgony p.{oldal:03d}, valojaban p.{talalt[0]:03d}"
    return f"IDEZET NINCS A FORRASBAN ({fid} p.{oldal:03d})"


def ellenoriz(csv_ut: pathlib.Path, forrasok: dict) -> int:
    gond = 0
    # 1. Elválasztójel automatikus detektálása az Anki vezérlősorból
    delimiter = ";"
    with open(csv_ut, encoding="utf-8") as f:
        for _ in range(5):
            sor = f.readline()
            if sor.lower().startswith("#separator:tab"):
                delimiter = "\t"
                break
            elif sor.lower().startswith("#separator:semicolon"):
                delimiter = ";"
                break

    # 2. Beolvasás és szigorú mezőszám-ellenőrzés (pontosan 7 oszlop)
    with open(csv_ut, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, sor in enumerate(reader, start=1):
            if not sor or sor[0].startswith("#") or sor[0] == "Kerdes":
                continue

            # Se kevesebb (< 7), se több (> 7) nem lehet!
            if len(sor) != 7:
                print(f"  {i:4d}  HIBAS MEZOSZAM: {len(sor)} oszlop, pontosan 7 kellene!")
                print(f"        Valószínűleg idézőjel nélküli elválasztójel ({delimiter!r}) van a szövegben.")
                print(f"        Sor eleje: {sor[0][:60]}...")
                gond += 1
                continue

            kerdes, valasz, horgony, idezet = sor[0], sor[1], sor[2], sor[3]

            if (h := hianyzo_szamok(valasz, idezet)):
                print(f"  {i:4d}  SZAM NINCS AZ IDEZETBEN: {h}")
                print(f"        {kerdes[:66]}")
                gond += 1

            if forrasok and (hiba := idezet_megvan(idezet, horgony, forrasok)):
                print(f"  {i:4d}  {hiba}")
                print(f"        {kerdes[:66]}")
                gond += 1
    return gond


def main():
    csak_szam = "--csak-szam" in sys.argv
    argok = [a for a in sys.argv[1:] if not a.startswith("--")]
    fajlok = ([pathlib.Path(a) for a in argok] if argok
              else sorted((GYOKER / "_output" / "anki").glob("*.csv")))
    if not fajlok:
        sys.exit("Nem talaltam CSV-t az _output/anki/ mappaban.")

    forrasok = {}
    if not csak_szam:
        forrasok = forrasok_beolvas()
        if not forrasok:
            print("Figyelem: nem talaltam horgonyozott forrast a md/ mappakban.")
            print("Az idezet-ellenorzes kimarad. Futtasd eloszor:")
            print("  python _scriptek/pdf_horgonnyal.py\n")

    osszes = 0
    for f in fajlok:
        if not f.exists():
            print(f"\n== {f}  <-- NINCS ILYEN FAJL")
            continue
        print(f"\n== {f.name}")
        gond = ellenoriz(f, forrasok)
        osszes += gond
        if not gond:
            print("  rendben")

    print()
    if osszes:
        print(f"Osszesen {osszes} gyanus kartya.")
        print("Ezeket dobd, vagy kuldd vissza a generalo lepesbe.")
        print("NEM itelet kerdese: amit a szkript jelez, az szovegosszehasonlitas.")
        sys.exit(1)
    print("Minden kartya atment a gepi ellenorzesen.")
    print("(Ez NEM jelenti, hogy orvosilag helyes — a 🔢 ertekeket")
    print(" a forrasjegyzek A. szakasza alapjan kezzel is ellenorizd.)")


if __name__ == "__main__":
    main()
