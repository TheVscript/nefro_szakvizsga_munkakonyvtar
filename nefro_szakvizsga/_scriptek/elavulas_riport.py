# -*- coding: utf-8 -*-
"""
Elavulas-riport: megmondja, MELYIK forrasnal erdemes megnezni, van-e ujabb.

NEM dont el semmit. Nem mozgat fajlt. Csak kiir egy listat, amin vegigmesz.

HASZNALAT
---------
    python _scriptek/elavulas_riport.py
    python _scriptek/elavulas_riport.py --ev 2020    # mas korhatar

MIT CSINAL
----------
1. Osszegyujti az osszes forrast a _pdf/ mappakbol
2. Kiolvassa az evszamot a forras_id-bol
3. Ket listat ad:

   A) VERZIOGYANUS PAROK — ugyanarra a temara ket fajl, kulonbozo evvel.
      Ez a LEJART eset: ha ugyanaz a kibocsato adta ki ujra, a regi
      lejart, es az _ARCHIV_LEJART/ mappaba valo.

   B) REGI FORRASOK — X evnel regebbiek. Ezek NEM feltetlenul lejartak!
      Ha nincs ujabb magyar valtozat, ez marad a kanonikus forras.
      Csak annyit jelent: nezd meg a kibocsatoi oldalon, jott-e ujabb.

AMIT NEM TUD ELDONTENI
----------------------
Hogy egy 2012-es magyar ajanlast "felulir-e" egy 2024-es KDIGO. NEM irja felul:
mas kibocsato, mas hierarchiaszint. A magyar marad a merce a vizsgan, es az
agent a kulonbseget ⚠️ ELTERES-kent jelzi. Lasd: MODSZERTAN_v4.0.md, 7.2.
"""
from __future__ import annotations

import pathlib, re, sys, datetime

from _kozos import GYOKER, PDF_MAPPAK
MAPPAK = PDF_MAPPAK

# kibocsato- es tipusjelolok, amiket a tema-torzs kepzesenel elhagyunk
ZAJ = {"BM", "EMMI", "MANET", "MHT", "KDIGO", "AJKD", "ERBP", "NJT", "WEB",
       "IRANYELV", "ALLASFOGLALAS", "AJANLAS", "CC", "SUPPL", "LEJART"}

EV = re.compile(r"-(19|20)\d{2}(?:-\d{2}-\d{2})?(?=-|$)")


def evszam(fid: str):
    talalatok = re.findall(r"(?:19|20)\d{2}", fid)
    return int(talalatok[-1]) if talalatok else None


def tema_torzs(fid: str) -> str:
    """A forras_id 'temaja': evszam es kibocsato nelkul."""
    t = EV.sub("", fid)
    reszek = [r for r in t.split("-") if r and r.upper() not in ZAJ]
    return "-".join(reszek) or t


def main():
    hatar = 2018
    if "--ev" in sys.argv:
        try:
            hatar = int(sys.argv[sys.argv.index("--ev") + 1])
        except (IndexError, ValueError):
            sys.exit("Hasznalat:  --ev 2020")

    forrasok = []
    for m in MAPPAK:
        be = GYOKER / m
        if not be.exists():
            continue
        for pdf in sorted(be.glob("*.pdf")):
            forrasok.append((pdf.stem, m, evszam(pdf.stem)))

    if not forrasok:
        sys.exit("Nem talaltam PDF-et a _pdf/ mappakban.\n"
                 "Eloszor tolts le valamit, es futtasd az atnevezo.py-t.")

    print(f"\n{len(forrasok)} forras a munkakonyvtarban.\n")

    # ---- A) verziogyanus parok ----
    temak = {}
    for fid, mappa, ev in forrasok:
        temak.setdefault(tema_torzs(fid), []).append((fid, mappa, ev))
    parok = {k: v for k, v in temak.items() if len(v) > 1}

    print("=" * 68)
    print("A) VERZIOGYANUS PAROK — ugyanaz a tema, tobb fajl")
    print("=" * 68)
    if not parok:
        print("  Nincs ilyen. (Ez a jo eset.)")
    else:
        for tema, lista in sorted(parok.items()):
            print(f"\n  [{tema}]")
            for fid, mappa, ev in sorted(lista, key=lambda x: x[2] or 0, reverse=True):
                jel = "  <- ez a legujabb" if ev == max(
                    (e for _, _, e in lista if e), default=None) else ""
                print(f"     {ev or '????'}  {fid}{jel}")
            print("     -> Ha UGYANAZ a kibocsato adta ki ujra: a regi LEJART.")
            print("        Mozgasd az _ARCHIV_LEJART/_pdf/ mappaba, -LEJART utotaggal,")
            print("        es cserled le a forrast az erintett notebookokban.")
            print("     -> Ha MAS kibocsato (pl. magyar vs KDIGO): EGYIK SEM lejart.")
            print("        Mindketto marad, a forrashierarchia dont. Lasd lentebb.")

    # ---- B) regi forrasok ----
    regiek = sorted([f for f in forrasok if f[2] and f[2] < hatar],
                    key=lambda x: x[2])
    print("\n" + "=" * 68)
    print(f"B) {hatar} ELOTTI FORRASOK — nezd meg, jott-e ujabb")
    print("=" * 68)
    if not regiek:
        print(f"  Nincs {hatar} elotti forras.")
    else:
        for fid, mappa, ev in regiek:
            print(f"  {ev}  {fid:<34} {mappa}")
        print(f"\n  {len(regiek)} db. EZEK NEM FELTETLENUL LEJARTAK.")
        print("  Ha nincs ujabb magyar valtozat, ez marad a kanonikus forras —")
        print("  akkor is, ha kozben megjelent egy ujabb KDIGO ugyanarrol.")

    print("\n" + "-" * 68)
    print("Ez a riport NEM mozgat semmit. A dontes a tied.")
    print("A harom kategoria: MODSZERTAN_v4.0.md, 13.3 fejezet.")
    print(f"Futtatva: {datetime.date.today().isoformat()}\n")


if __name__ == "__main__":
    main()
