# -*- coding: utf-8 -*-
"""
Hol tartasz a 70 tetellel? Pipalas nelkul, a fajlokbol kiolvasva.

Hasznalat (Windowson is):
    python _scriptek/allapot.py            # attekinto tablazat, mind a 70
    python _scriptek/allapot.py 47 6 28    # reszletesen ezek a tetelek
    python _scriptek/allapot.py --hianyzo  # mely PDF-ek hianyoznak, es hany tetelhez kellenek

Mit nez:
  PDF     a tetellap forras_id-jai kozul hany PDF van meg a _pdf/ mappakban
  F T J A M   _output/forras, tetelek, ellenorzes/forrasjegyzek, anki, ellenorzes/minosites
  PIPA    a tetellapon a gyartasi ciklus (1-9.) pipai, amit kezzel jeloltel
  KOVETKEZO   az elso hianyzo lepes

A tetellapot NEM modositja, csak olvas.
"""
from __future__ import annotations

import csv, re, sys
from collections import defaultdict

from _kozos import GYOKER, PDF_MAPPAK, ARCHIV_PDF

# Windows-konzolon atiranyitasnal se alljon le ekezet miatt.
sys.stdout.reconfigure(errors="replace")

FORRASLAPOK = GYOKER / "tetelek_forrasok"
OUT = GYOKER / "_output"

SOR_ID = re.compile(r"^\|\s*(?:☐|☑|\[[ xX]\]).*\|\s*`([A-Z0-9][A-Z0-9-]+)`\s*\|\s*$")
CIKLUS_PIPA = re.compile(r"^- \[([ xX])\] \*\*(\d)\.\*\*")


def meglevo_pdfek() -> set[str]:
    nevek = set()
    for mappa in [*PDF_MAPPAK, ARCHIV_PDF]:
        d = (GYOKER / mappa).resolve()
        if d.is_dir():
            nevek |= {p.stem.upper() for p in d.glob("*.pdf")}
            nevek |= {p.stem.upper() for p in d.glob("*.PDF")}
    return nevek


def tetellap(ut):
    sorok = ut.read_text(encoding="utf-8").splitlines()
    cim = sorok[0].lstrip("# ").split("–", 1)[-1].strip() if sorok else ""
    idk, pipak = [], {}
    for s in sorok:
        if (m := SOR_ID.match(s)) and m.group(1) not in idk:
            idk.append(m.group(1))
        elif m := CIKLUS_PIPA.match(s):
            pipak[int(m.group(2))] = m.group(1) != " "
    return cim, idk, pipak


def anki_szamlalo(ut):
    """(kartyak szama, ebbol NYERS)"""
    ossz = nyers = 0
    with open(ut, encoding="utf-8", newline="") as f:
        for sor in csv.reader(f, delimiter=";"):
            if not sor or sor[0].startswith("#") or sor[0] == "Kerdes":
                continue
            ossz += 1
            if len(sor) > 5 and sor[5].strip().upper() == "NYERS":
                nyers += 1
    return ossz, nyers


def tetel_allapot(ut, pdfek):
    nnn = ut.stem
    cim, idk, pipak = tetellap(ut)
    fajl = {
        "F": OUT / "forras" / f"{nnn}_forras.md",
        "T": OUT / "tetelek" / f"{nnn}.md",
        "J": OUT / "ellenorzes" / f"{nnn}_forrasjegyzek.md",
        "A": OUT / "anki" / f"{nnn}_kartyak.csv",
        "M": OUT / "ellenorzes" / f"{nnn}_minosites.md",
    }
    van = {k: p.exists() for k, p in fajl.items()}
    hiany = [i for i in idk if i not in pdfek]

    if idk and len(hiany) == len(idk):
        kov = "letoltes (egy PDF sincs meg)"
    elif not van["F"]:
        kov = "1-3. kinyeres -> _output/forras"
    elif not (van["T"] and van["J"]):
        kov = "4. gyartas, kor 1 (tetel + jegyzek)"
    elif not van["A"]:
        kov = "4. gyartas, kor 2 (Anki)"
    elif not van["M"]:
        kov = "6. minosites"
    elif not all(pipak.get(n) for n in (7, 8, 9)):
        kov = "7-9. kezi ellenorzes, feltoltes, Anki"
    else:
        kov = "KESZ"

    return dict(nnn=nnn, cim=cim, idk=idk, hiany=hiany, van=van, fajl=fajl,
                pipak=pipak, kov=kov)


def attekintes(allapotok):
    print(f"{'TET':<4} {'CIM':<38} {'PDF':>5}  F T J A M  {'PIPA':>4}  KOVETKEZO")
    print("-" * 100)
    for a in allapotok:
        pdf = f"{len(a['idk']) - len(a['hiany'])}/{len(a['idk'])}"
        jelek = " ".join("x" if a["van"][k] else "." for k in "FTJAM")
        pipa = f"{sum(a['pipak'].values())}/9"
        cim = a["cim"][:37] + ("…" if len(a["cim"]) > 37 else "")
        print(f"{a['nnn']:<4} {cim:<38} {pdf:>5}  {jelek}  {pipa:>4}  {a['kov']}")

    kesz = sum(a["kov"] == "KESZ" for a in allapotok)
    print("-" * 100)
    print(f"Kesz: {kesz}/{len(allapotok)}    "
          "(x = megvan, . = hianyzik;  F forras, T tetel, J jegyzek, A anki, M minosites)")


def reszletes(a):
    print(f"\n== {a['nnn']}. {a['cim']}")
    print(f"   Kovetkezo lepes: {a['kov']}")
    print(f"   PDF: {len(a['idk']) - len(a['hiany'])}/{len(a['idk'])} megvan")
    for i in a["hiany"]:
        print(f"      hianyzik: {i}.pdf")
    for k, nev in zip("FTJAM", ["forras", "tetel", "forrasjegyzek", "anki", "minosites"]):
        p = a["fajl"][k]
        jel = "megvan " if a["van"][k] else "HIANYZIK"
        extra = ""
        if k == "A" and a["van"][k]:
            ossz, nyers = anki_szamlalo(p)
            extra = f"  ({ossz} kartya, ebbol NYERS: {nyers})"
        print(f"   {jel}  {nev:<14} {p.relative_to(GYOKER)}{extra}")
    if a["pipak"]:
        sor = " ".join(f"{n}:{'x' if a['pipak'].get(n) else '.'}" for n in range(1, 10))
        print(f"   Pipak a tetellapon: {sor}")


def hianyzo_pdfek(allapotok):
    kell = defaultdict(list)
    for a in allapotok:
        for i in a["hiany"]:
            kell[i].append(int(a["nnn"]))
    if not kell:
        print("Minden tetellapon szereplo PDF megvan.")
        return
    print(f"{len(kell)} PDF hianyzik. Elol azok, amik a legtobb tetelhez kellenek:\n")
    for i, tetelek in sorted(kell.items(), key=lambda x: (-len(x[1]), x[0])):
        print(f"  {len(tetelek):>3} tetel  {i:<34} {', '.join(map(str, tetelek))}")


def main():
    lapok = sorted(FORRASLAPOK.glob("*/[0-9][0-9][0-9].md"), key=lambda p: int(p.stem))
    if not lapok:
        sys.exit(f"Nem talaltam tetellapot itt: {FORRASLAPOK}")
    pdfek = meglevo_pdfek()
    allapotok = [tetel_allapot(p, pdfek) for p in lapok]

    if "--hianyzo" in sys.argv:
        hianyzo_pdfek(allapotok)
        return

    kert = {int(a) for a in sys.argv[1:] if a.isdigit()}
    if kert:
        for a in allapotok:
            if int(a["nnn"]) in kert:
                reszletes(a)
        return

    attekintes(allapotok)


if __name__ == "__main__":
    main()
