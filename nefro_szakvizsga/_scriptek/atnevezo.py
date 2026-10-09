# -*- coding: utf-8 -*-
"""
Letoltott PDF-ek felismerese, atnevezese forras_id-ra, es bemozgatasa
a megfelelo mappaba.

HASZNALAT
---------
1. Tolts le mindent a bongeszovel barmilyen nevvel a  _letoltve/  mappaba.
   Ne torodj a fajlnevekkel.
2. pip install pymupdf
3. python _scriptek/atnevezo.py

A szkript minden PDF elso oldalat elolvassa, megprobalja felismerni, melyik
dokumentum, es megkerdezi, hogy jol tippelt-e. Te csak Entert nyomsz.

  python _scriptek/atnevezo.py --auto     # a biztos talalatokat kerdes nelkul
  python _scriptek/atnevezo.py --szaraz   # csak mutatja, nem nevez at
"""
from __future__ import annotations

import pathlib, sys, re, unicodedata, shutil

from _kozos import GYOKER, PAROK, ARCHIV_PDF, ARCHIV_MD, pymupdf_betolt

fitz = pymupdf_betolt()

from _kozos import GYOKER
BE = GYOKER / "_letoltve"

# forras_id: (celmappa, [kotelezo kulcsszavak], [megkulonbozteto kulcsszavak], [kizaro])
K = {
"TETELSOR-NEFROLOGIA-2024-07-25": ("00_tetelsor/_pdf",
    ["nephrologiai szakkepzes"], ["vizsgakerdesek", "nefrologia"], []),

"CKD-IRANYELV-BM-2025": ("01_iranyelv_hu/_pdf",
    ["idult vesebetegseg", "diagnozisarol", "kezeleserol"],
    ["belugyminiszterium", "2025"], ["supplementum", "emberi eroforrasok"]),
"CKD-IRANYELV-BM-2025-SUPPL": ("01_iranyelv_hu/_pdf",
    ["idult vesebetegseg", "diagnozisarol"],
    ["supplementum", "hypertonia es nephrologia"], ["emberi eroforrasok"]),
"CKD-IRANYELV-EMMI-2021-LEJART": (ARCHIV_PDF,
    ["idult vesebetegseg", "diagnozisa"],
    ["emberi eroforrasok", "2021"], []),
"TTP-HUS-IRANYELV-BM-2026": ("01_iranyelv_hu/_pdf",
    ["thromboticus", "purpura"], ["haemolyticus", "uraemias"], []),
"HYPONATRAEMIA-IRANYELV": ("01_iranyelv_hu/_pdf",
    ["hyponatraemia"], ["diagnosztika", "kezeles"], []),

"MHT-HT-IRANYELV-2025": ("02_manet_tarsasag/_pdf",
    ["magasvernyomas"], ["2025", "gyakorlati iranyelv"], []),
"MANET-MHT-HT-2023": ("02_manet_tarsasag/_pdf",
    ["hypertonia"], ["2023", "supplementum"], ["magasvernyomas-betegseg ellatasarol"]),
"VESEBIOPSZIA-MANET-2025": ("02_manet_tarsasag/_pdf",
    ["vesebiopszia"], ["percutan", "nativ"], []),
"IMMUNSZEROLOGIA-MANET-2024": ("02_manet_tarsasag/_pdf",
    ["immunserologiai", "vesebetegseg"], ["vizsgalatok"], []),
"SGLT2-CKD-MANET-2024": ("02_manet_tarsasag/_pdf",
    ["sglt2", "idult vesebetegseg"], ["gatlo"], ["ellenorzo lista"]),
"SGLT2-T2DM-CHECKLIST-2026": ("02_manet_tarsasag/_pdf",
    ["sglt", "haziorvos"], ["ellenorzo lista", "t2dm"], []),
"LIPID-CKD-MANET-2024": ("02_manet_tarsasag/_pdf",
    ["lipidcsokkento"], ["idult vesebetegseg"], []),
"ALBUMINURIA-EGFR-LABOR-2025": ("02_manet_tarsasag/_pdf",
    ["albuminuria", "egfr"], ["laboratorium", "allasfoglalas"], ["szurese"]),
"BEUTALAS-HAZIORVOS-2024": ("02_manet_tarsasag/_pdf",
    ["vesebetegsegre", "nephrologushoz"], ["mikor"], []),
"ALBUMINURIA-SZURES-2012": ("02_manet_tarsasag/_pdf",
    ["albuminuria", "proteinuria", "haematuria"], ["szurese"], []),
"DIALIZIS-UTMUTATO-MANET-2021": ("02_manet_tarsasag/_pdf",
    ["dializiskezeles"], ["korszeru", "utmutato"], []),
"KONTRASZT-NEPHROPATHIA-2022": ("02_manet_tarsasag/_pdf",
    ["kontrasztanyag", "vesekarosodas"], ["orvosi hetilap", "megelozese"], ["allasfoglalas"]),
"KONTRASZT-ALLASFOGLALAS-2012": ("02_manet_tarsasag/_pdf",
    ["kontrasztanyag", "vesekarosito"], ["allasfoglalas"], []),
"MR-KONTRASZT-NSF-2014": ("02_manet_tarsasag/_pdf",
    ["nephrogen", "fibrosis"], ["mr kontrasztanyag", "szisztemas"], []),
"GYOGYSZERDOZIS-CKD-2012": ("02_manet_tarsasag/_pdf",
    ["gyogyszerek", "adagolas"], ["vesefunkcio"], []),
"RAS-GATLAS-CKD-2012": ("02_manet_tarsasag/_pdf",
    ["angiotensin"], ["konvertalo", "receptor blokkolo"], []),
"VESEKO-MANET-2012": ("02_manet_tarsasag/_pdf",
    ["vesekobetegseg"], ["belgyogyaszati"], []),
"CKD-MBD-MANET-2012": ("02_manet_tarsasag/_pdf",
    ["csont", "asvanyi"], ["anyagcsere zavar"], []),
"ERBP-TX-2013": ("02_manet_tarsasag/_pdf",
    ["vesetranszplantacio"], ["donor", "recipiens", "erbp"], []),
"EGFR-BEOSZTAS-2014": ("02_manet_tarsasag/_pdf",
    ["szamitott gfr"], ["feherjevizeles", "beosztasa"], []),
"DM-CKD3B-2016": ("02_manet_tarsasag/_pdf",
    ["cukorbetegek"], ["3b", "vesekarosodas"], []),
"MANET-KV-KONSZENZUS-2020": ("02_manet_tarsasag/_pdf",
    ["kardiovascularis", "konszenzus"], ["2020"], []),
"NEPHRO-BEUTALAS-2009": ("02_manet_tarsasag/_pdf",
    ["beutalas"], ["javallatai", "kisero informacio"], []),
"METFORMIN-CKD-2012": ("02_manet_tarsasag/_pdf",
    ["metformin"], ["vesebetegseg"], []),

"KDIGO-ANEMIA-2026": ("03_kdigo/_pdf", ["kdigo", "anemia"], ["2026"], []),
"KDIGO-CKD":        ("03_kdigo/_pdf", ["kdigo", "chronic kidney disease"],
                      ["evaluation", "management"], ["anemia", "diabetes", "lipid", "blood pressure"]),
"KDIGO-GN":         ("03_kdigo/_pdf", ["kdigo", "glomerular"], ["diseases"], []),
"KDIGO-DIABETES":   ("03_kdigo/_pdf", ["kdigo", "diabetes"], ["management"], []),
"KDIGO-BP-2021":    ("03_kdigo/_pdf", ["kdigo", "blood pressure"], ["management"], []),
"KDIGO-AKI":        ("03_kdigo/_pdf", ["kdigo", "acute kidney injury"], [], []),
"KDIGO-CKD-MBD":    ("03_kdigo/_pdf", ["kdigo", "mineral and bone"], ["ckd-mbd"], []),
"KDIGO-TX":         ("03_kdigo/_pdf", ["kdigo", "transplant"], ["recipient", "living donor"], []),
"KDIGO-ADPKD":      ("03_kdigo/_pdf", ["kdigo", "polycystic"], ["adpkd"], []),
"KDIGO-LIPID":      ("03_kdigo/_pdf", ["kdigo", "lipid"], ["management"], []),

"AJKD-CC-VASCULAR-ACCESS-2025": ("05_tankonyv_en/_pdf",
    ["core curriculum", "vascular access"], ["hemodialysis"], []),
"AJKD-CC-HEART-FAILURE-2025": ("05_tankonyv_en/_pdf",
    ["core curriculum", "heart failure"], ["kidney dysfunction"], []),
"AJKD-CC-ONCONEPHROLOGY-2023": ("05_tankonyv_en/_pdf",
    ["core curriculum", "onconephrology"], [], []),
"AJKD-CC-NUTRITION-2022": ("05_tankonyv_en/_pdf",
    ["core curriculum", "nutrition"], ["kidney disease"], []),

# Fallback a vakfolt-tetelekhez (6, 8, 28-32, 39) - a cikk cime nem rogzitett.
"AJKD-CC-KALIUM": ("05_tankonyv_en/_pdf",
    ["core curriculum", "potassium"], ["hyperkalemia", "hypokalemia"], []),
"AJKD-CC-SAV-BAZIS": ("05_tankonyv_en/_pdf",
    ["core curriculum", "acid"], ["base", "metabolic acidosis", "alkalosis"],
    ["renal tubular acidosis"]),
"AJKD-CC-RTA": ("05_tankonyv_en/_pdf",
    ["core curriculum", "renal tubular acidosis"], ["distal", "proximal"], []),
"AJKD-CC-TUBULOPATIA": ("05_tankonyv_en/_pdf",
    ["core curriculum", "gitelman"], ["bartter", "tubulopath", "liddle"], []),
"AJKD-CC-CAKUT": ("05_tankonyv_en/_pdf",
    ["core curriculum", "congenital"], ["anomalies", "urinary tract", "cakut"], []),
"AJKD-CC-UTI": ("05_tankonyv_en/_pdf",
    ["core curriculum", "urinary tract infection"], ["pyelonephritis", "cystitis"],
    ["congenital"]),
"AJKD-CC-RENOVASZKULARIS": ("05_tankonyv_en/_pdf",
    ["core curriculum", "renal artery"], ["thrombosis", "embol", "renal vein"],
    ["vascular access"]),
}

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s)

def szoveg_kinyer(pdf: pathlib.Path):
    """(cimresz, teljes) - a cimresz az elso oldal eleje, ott all a dokumentum cime."""
    try:
        doc = fitz.open(pdf)
    except Exception:
        return "", ""
    teljes = norm(" ".join(doc[i].get_text() for i in range(min(6, len(doc)))))
    cim = norm(doc[0].get_text())[:600] if len(doc) else ""
    return cim, teljes

def pontoz(cim: str, teljes: str):
    """
    A talalat csak akkor szamit, ha a kulcsszavak a CIMRESZBEN is megjelennek.
    Enelkul a hosszu dokumentumok (pl. a tetelsor kovetelmenylistaja) minden
    masik dokumentum kulcsszavara illeszkednenek.
    """
    talalatok = []
    for fid, (celmappa, kotelezo, megkul, kizaro) in K.items():
        if any(norm(x) in cim for x in kizaro):
            continue
        # minden kotelezo kulcsszo legyen benne valahol
        if not all(norm(x) in teljes for x in kotelezo):
            continue
        # es legalabb egy a CIMRESZBEN
        cim_kot = sum(1 for x in kotelezo if norm(x) in cim)
        if cim_kot == 0:
            continue
        cim_extra = sum(1 for x in megkul if norm(x) in cim)
        teljes_extra = sum(1 for x in megkul if norm(x) in teljes)
        pont = cim_kot * 10 + cim_extra * 4 + teljes_extra
        talalatok.append((pont, teljes_extra == len(megkul), fid, celmappa))
    talalatok.sort(reverse=True)
    return talalatok

def main():
    auto = "--auto" in sys.argv
    szaraz = "--szaraz" in sys.argv
    BE.mkdir(exist_ok=True)
    pdfek = sorted(BE.glob("*.pdf")) + sorted(BE.glob("*.PDF"))
    if not pdfek:
        print(f"Nincs PDF a {BE.name}/ mappaban.")
        print("Tolts le mindent oda barmilyen nevvel, aztan futtasd ujra.")
        return

    kesz, kihagy = 0, []
    for pdf in pdfek:
        cim, szoveg = szoveg_kinyer(pdf)
        if not szoveg.strip():
            print(f"\n[{pdf.name}]  <-- nincs szovegreteg (szkennelt?). Kihagyva.")
            kihagy.append(pdf.name); continue

        tal = pontoz(cim, szoveg)
        elonezet = " ".join(cim.split()[:20])
        print(f"\n[{pdf.name}]")
        print(f"  eleje: {elonezet}…")

        if not tal:
            print("  nem ismertem fel. Nevezd at kezzel (lasd 00_FORRAS_ID_LISTA.md).")
            kihagy.append(pdf.name); continue

        pont, teljes, fid, celmappa = tal[0]
        tobbi = [t[2] for t in tal[1:4]]
        print(f"  tipp:  {fid}   ->  {celmappa}/")
        if tobbi:
            print(f"  egyeb lehetoseg: {', '.join(tobbi)}")

        if szaraz:
            continue

        biztos = teljes and (len(tal) == 1 or tal[0][0] > tal[1][0])
        if auto:
            if not biztos:
                print("  nem egyertelmu -> kihagyva (--auto). Futtasd auto nelkul.")
                kihagy.append(pdf.name); continue
            valasz = ""
        else:
            try:
                valasz = input("  Enter = elfogad | szam (1-3) = masik | "
                               "s = kihagy | sajat azonosito: ").strip()
            except EOFError:
                print("  nincs bemenet -> kihagyva.")
                kihagy.append(pdf.name); continue

        if valasz.lower() == "s":
            kihagy.append(pdf.name); continue
        if valasz in ("1", "2", "3") and len(tal) > int(valasz):
            pont, teljes, fid, celmappa = tal[int(valasz)]
        elif valasz and not valasz.isdigit():
            fid = valasz.upper()
            celmappa = K.get(fid, (None,))[0]
            if celmappa is None:
                celmappa = input("  Celmappa (pl. 04_tankonyv_hu/_pdf): ").strip()

        cel = GYOKER / celmappa
        cel.mkdir(parents=True, exist_ok=True)
        ut = cel / f"{fid}.pdf"
        if ut.exists():
            print(f"  FIGYELEM: {ut.name} mar letezik ebben a mappaban.")
            if auto:
                print("  --auto modban kihagyva. Futtasd auto nelkul a dontesehez.")
                kihagy.append(pdf.name); continue
            print("    c = CSERE  (a regi -REGI-<datum> utotaggal felreteve)")
            print("    s = kihagyas (a letoltott fajl marad a _letoltve/-ben)")
            print("    vagy adj meg egy MASIK azonositot")
            try:
                d = input("  Mit csinaljak? [c / s / sajat azonosito]: ").strip()
            except EOFError:
                print("  nincs bemenet -> kihagyva.")
                kihagy.append(pdf.name); continue
            if d.lower() == "c":
                import datetime
                bel = ut.with_name(f"{fid}-REGI-{datetime.date.today():%Y-%m-%d}.pdf")
                shutil.move(str(ut), str(bel))
                print(f"  a regi felreteve: {bel.name}")
                print("  FIGYELEM: ha ez egy IRANYELV, a regi valtozat LEJART —")
                print("            mozgasd at az _ARCHIV_LEJART/_pdf/ mappaba,")
                print("            es cserled le a forrast a NotebookLM-ben is.")
            elif d.lower() == "s" or not d:
                kihagy.append(pdf.name); continue
            else:
                fid = d.upper()
                ut = cel / f"{fid}.pdf"
                if ut.exists():
                    print("  ez is letezik -> kihagyva.")
                    kihagy.append(pdf.name); continue
        shutil.move(str(pdf), str(ut))
        print(f"  OK -> {celmappa}/{fid}.pdf")
        kesz += 1

    print(f"\n==== {kesz} fajl atnevezve es bemozgatva.")
    if kihagy:
        print(f"Kihagyva ({len(kihagy)}): " + ", ".join(kihagy))
        print("Ezeket nevezd at kezzel a 00_FORRAS_ID_LISTA.md alapjan.")
    if kesz:
        print("\nKovetkezo lepes:  python _scriptek/pdf_horgonnyal.py")

if __name__ == "__main__":
    main()
