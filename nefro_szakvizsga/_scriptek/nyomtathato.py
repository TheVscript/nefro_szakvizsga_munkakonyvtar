# -*- coding: utf-8 -*-
"""
Markdown -> nyomtathato HTML (onallo fajl), amibol a bongeszovel PDF-et nyomtatsz.

Miert nem kozvetlenul PDF: a pandoc+xelatex utvonalhoz LaTeX kell (tobb GB),
a magyar ekezetekhez kulon betutipus, a Mermaid abrakhoz pedig Node.js.
A bongeszo mindezt tudja, es minden gepen ott van.

HASZNALAT
---------
    python _scriptek/nyomtathato.py                      # minden md
    python _scriptek/nyomtathato.py _output/tetelek/047.md
    python _scriptek/nyomtathato.py --ellenorzes         # csak a forrasjegyzekek

Utana: nyisd meg a .html-t, Ctrl+P -> "Mentes PDF-be". A laptores, a margo
es a betumeret mar be van allitva.

MERMAID
-------
Ha az md-ben van ```mermaid blokk, a bongeszo kirajzolja. Ehhez internet
kell az elso megnyitaskor (CDN). Offline a forraskod latszik helyette --
ami nem katasztrofa, csak csunya.
"""
from __future__ import annotations

import pathlib, sys, re, html as htmlmod

CELLA_HATAR = re.compile(r"(?<!\\)\|")   # | ami ELOTT nincs backslash

def cellak(sor: str) -> list[str]:
    """Markdown-tablazatsor -> cellak.

    A \\| (escape-elt pipe) a CELLAN BELUL marad, es sima |-re alakul.
    Enelkul a [FORRAS-ID \\| p.047] hivatkozas ket cellara esne szet,
    es a nyomtatott lapon stray backslash maradna.
    """
    mag = sor.strip()
    if mag.startswith("|"):
        mag = mag[1:]
    if mag.endswith("|") and not mag.endswith("\\|"):
        mag = mag[:-1]
    return [c.strip().replace("\\|", "|") for c in CELLA_HATAR.split(mag)]

from _kozos import GYOKER
KI = GYOKER / "_output" / "nyomtathato"

CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
body { font-family: Georgia, "Times New Roman", serif; font-size: 10.5pt;
       line-height: 1.45; color: #111; max-width: 180mm; margin: 0 auto;
       padding: 10mm; }
h1 { font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 4pt;
     margin-top: 0; }
h2 { font-size: 13pt; margin-top: 16pt; border-bottom: 1px solid #bbb;
     padding-bottom: 2pt; page-break-after: avoid; }
h3 { font-size: 11.5pt; margin-top: 12pt; page-break-after: avoid; }
h4 { font-size: 10.5pt; margin-top: 10pt; page-break-after: avoid; }
p, li { orphans: 3; widows: 3; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0;
        font-size: 9pt; page-break-inside: avoid; }
th, td { border: 1px solid #999; padding: 3pt 5pt; text-align: left;
         vertical-align: top; }
th { background: #eee; font-weight: bold; }
code { font-family: "DejaVu Sans Mono", Consolas, monospace; font-size: 9pt;
       background: #f4f4f4; padding: 1pt 3pt; }
pre { background: #f4f4f4; border-left: 3px solid #999; padding: 6pt 8pt;
      font-size: 8.5pt; overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { border-left: 3px solid #888; margin: 8pt 0; padding: 2pt 0 2pt 10pt;
             color: #444; }
hr { border: none; border-top: 1px solid #ccc; margin: 12pt 0; }
.horgony { font-family: monospace; font-size: 8.5pt; color: #555; }
.mermaid { text-align: center; margin: 10pt 0; page-break-inside: avoid; }
.lablec { margin-top: 18pt; padding-top: 6pt; border-top: 1px solid #ccc;
          font-size: 8pt; color: #666; }
.figyelem { border: 1.5pt solid #b00; background: #fff4f4; padding: 6pt 9pt;
            margin: 10pt 0; page-break-inside: avoid; }
@media print { .nyomtatas-info { display: none; } }
.nyomtatas-info { background: #eef4ff; border: 1px solid #99b;
                  padding: 8pt 10pt; margin-bottom: 14pt; font-size: 9pt; }
"""

FEJ = """<!DOCTYPE html>
<meta charset="utf-8">
<title>{cim}</title>
<style>{css}</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  window.addEventListener('load', function () {{
    if (window.mermaid) mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
  }});
</script>
<div class="nyomtatas-info">
  <b>Nyomtatás PDF-be:</b> Ctrl+P (Cmd+P) → cél: „Mentés PDF-be”.
  A háttérszínekhez kapcsold be a „Háttérgrafika” opciót.
  Ez a doboz nyomtatásban nem jelenik meg.
</div>
"""

LAB = """
<div class="lablec">
  <b>Ellenőrizetlen piszkozat.</b> A 🔢 jelölt értékeket a megadott forrásban
  vissza kell ellenőrizni felhasználás előtt. Nem klinikai döntéstámogatás.<br>
  Forrás: <code>{forras}</code> &nbsp;·&nbsp; Generálva: {datum}<br>
  <i>Created using Anthropic Claude</i>
</div>
"""

def md_to_html(md: str) -> str:
    """Minimalista markdown -> HTML. Nincs kulso fuggoseg."""
    out, i = [], 0
    sorok = md.split("\n")
    while i < len(sorok):
        s = sorok[i]

        # kodblokk / mermaid
        m = re.match(r"^```(\w*)", s)
        if m:
            nyelv = m.group(1)
            i += 1
            blokk = []
            while i < len(sorok) and not sorok[i].startswith("```"):
                blokk.append(sorok[i]); i += 1
            i += 1
            tart = "\n".join(blokk)
            if nyelv == "mermaid":
                out.append(f'<div class="mermaid">{htmlmod.escape(tart)}</div>')
            else:
                out.append(f"<pre><code>{htmlmod.escape(tart)}</code></pre>")
            continue

        # tablazat
        if s.startswith("|") and i + 1 < len(sorok) and re.match(r"^\|[\s:|-]+\|$", sorok[i+1]):
            fej = cellak(s)
            i += 2
            sorokk = []
            while i < len(sorok) and sorok[i].startswith("|"):
                sorokk.append(cellak(sorok[i]))
                i += 1
            t = ["<table><thead><tr>"] + [f"<th>{inline(c)}</th>" for c in fej]
            t.append("</tr></thead><tbody>")
            for r in sorokk:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        # cimsor
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            sz = len(m.group(1))
            out.append(f"<h{sz}>{inline(m.group(2))}</h{sz}>"); i += 1; continue

        # idezet
        if s.startswith(">"):
            blokk = []
            while i < len(sorok) and sorok[i].startswith(">"):
                blokk.append(sorok[i].lstrip(">").strip()); i += 1
            szov = inline(" ".join(blokk))
            oszt = ' class="figyelem"' if any(x in szov for x in ("🔴", "⚠️")) else ""
            out.append(f"<blockquote{oszt}>{szov}</blockquote>")
            continue

        # lista
        if re.match(r"^\s*([-*]|\d+\.)\s+", s):
            szamozott = bool(re.match(r"^\s*\d+\.", s))
            tag = "ol" if szamozott else "ul"
            tetelek = []
            while i < len(sorok) and re.match(r"^\s*([-*]|\d+\.)\s+", sorok[i]):
                tetelek.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", sorok[i])); i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(t)}</li>" for t in tetelek) + f"</{tag}>")
            continue

        if s.strip() == "---":
            out.append("<hr>"); i += 1; continue
        if not s.strip():
            i += 1; continue

        bek = [s]; i += 1
        while i < len(sorok) and sorok[i].strip() and not re.match(
                r"^(#{1,6}\s|>|\||```|\s*([-*]|\d+\.)\s|---$)", sorok[i]):
            bek.append(sorok[i]); i += 1
        out.append(f"<p>{inline(' '.join(bek))}</p>")
    return "\n".join(out)

def inline(s: str) -> str:
    s = htmlmod.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = s.replace("[ ]", "☐").replace("[x]", "☑")
    # horgony kiemelese
    s = re.sub(r"\[([A-Z0-9-]+ \| p\.\d+)\]", r'<span class="horgony">[\1]</span>', s)
    s = s.replace("&lt;br&gt;", "<br>")
    return s

def feldolgoz(md_ut: pathlib.Path):
    import datetime
    md = md_ut.read_text(encoding="utf-8")
    cim = next((l.lstrip("# ").strip() for l in md.split("\n") if l.startswith("# ")), md_ut.stem)
    KI.mkdir(parents=True, exist_ok=True)
    cel = KI / (md_ut.stem + ".html")
    cel.write_text(
        FEJ.format(cim=htmlmod.escape(cim), css=CSS)
        + md_to_html(md)
        + LAB.format(forras=md_ut.name, datum=datetime.date.today().isoformat()),
        encoding="utf-8")
    print(f"{md_ut.name}  ->  _output/nyomtathato/{cel.name}")
    return cel

def index_keszit():
    """Egy kezdolap, ahonnan minden tetel megnyithato."""
    import datetime, re as _re
    tetelek, ellenorzesek = [], []
    for f in sorted(KI.glob("*.html")):
        if f.name == "index.html":
            continue
        cim = ""
        try:
            m = _re.search(r"<title>(.*?)</title>", f.read_text(encoding="utf-8"))
            cim = m.group(1) if m else f.stem
        except Exception:
            cim = f.stem
        (ellenorzesek if "forrasjegyzek" in f.name else tetelek).append((f.name, cim))

    def tabla(sorok, fejlec):
        if not sorok:
            return ""
        ki = [f"<h2>{fejlec}</h2>", "<table><thead><tr><th>#</th><th>Cim</th></tr>"
              "</thead><tbody>"]
        for nev, cim in sorok:
            sz = nev.split("_")[0].split(".")[0]
            ki.append(f'<tr><td>{sz}</td><td><a href="{nev}">{cim}</a></td></tr>')
        ki.append("</tbody></table>")
        return "\n".join(ki)

    KI.mkdir(parents=True, exist_ok=True)
    (KI / "index.html").write_text(
        FEJ.format(cim="Nefrologiai szakvizsga - tetelek", css=CSS)
        + "<h1>Nefrologiai szakvizsga</h1>"
        + f"<p>{len(tetelek)} tetel, {len(ellenorzesek)} forrasjegyzek. "
          f"Frissitve: {datetime.date.today().isoformat()}</p>"
        + '<blockquote class="figyelem"><b>Ellenorizetlen piszkozat.</b> '
          'Minden tetel addig piszkozat, amig a hozza tartozo forrasjegyzeket '
          'konyvvel a kezben vegig nem pipaltad.</blockquote>'
        + tabla(tetelek, "Tetelek")
        + tabla(ellenorzesek, "Forrasjegyzekek (nyomtatando)")
        + LAB.format(forras="_output/", datum=datetime.date.today().isoformat()),
        encoding="utf-8")
    print(f"index.html  ({len(tetelek)} tetel, {len(ellenorzesek)} forrasjegyzek)")

def sablon(ut: pathlib.Path) -> bool:
    """A mintafajl nem valodi tartalom - nem kerul a nyomtatasi indexbe."""
    return ut.stem.startswith("000_") or "MINTA" in ut.stem.upper()

def main():
    argok = [a for a in sys.argv[1:] if not a.startswith("--")]
    if argok:
        fajlok = [pathlib.Path(a) for a in argok]
    elif "--ellenorzes" in sys.argv:
        fajlok = sorted((GYOKER / "_output" / "ellenorzes").glob("*.md"))
    else:
        fajlok = (sorted((GYOKER / "_output" / "tetelek").glob("*.md"))
                  + sorted((GYOKER / "_output" / "ellenorzes").glob("*.md")))
    fajlok = [f for f in fajlok if f.exists()]
    if not argok:                       # csak automatikus listazasnal szurunk
        kihagyott = [f for f in fajlok if sablon(f)]
        fajlok = [f for f in fajlok if not sablon(f)]
        for f in kihagyott:
            print(f"kihagyva (sablon): {f.name}")
    if not fajlok:
        print("Nem talaltam markdown fajlt az _output/ alatt.")
        return
    for f in fajlok:
        feldolgoz(f)
    index_keszit()
    print(f"\nKesz: {len(fajlok)} fajl.")
    print("Nyisd meg: _output/nyomtathato/index.html")
    print("PDF-hez:   Ctrl+P -> Mentes PDF-be.")

if __name__ == "__main__":
    main()
