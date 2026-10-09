# LEJÁRT irányelvek – EZT A MAPPÁT SOHA NE CSATOLD

> ## 🔴 Miért van kívül a munkakönyvtáron
>
> Ha a Claude asztali alkalmazásnak csatolod a `nefro_szakvizsga/` mappát,
> minden benne lévő fájl **egyetlen olvasásnyira** van. Egy `lejart/`
> almappa tehát nem véd semmitől: ha a modell „alaposan" akar dolgozni,
> megnyitja — és idézi a 2021-es, felülírt CKD-irányelvet.
>
> A metaadatos jelölés (`statusz: lejart`) sem elég: az arra épülne, hogy a
> modell engedelmeskedik, és mérések szerint a promptkövetés orvosi
> kontextusban a hibák mintegy felét bent hagyja.
>
> **Ami nincs a csatolt mappában, azt nem tudja megnyitni.**
> Ez az egyetlen 100%-os védelem a rendszerben.

## Mi jön ide

- A CKD-irányelv **2021-es EMMI-verziója** (felülírta a 2025-ös BM-verzió)
- Minden más dokumentum, amit egy frissebb azonos témájú felülírt
- A 2001-es MANET curriculum

Elnevezés: a `forras_id` végére `-LEJART`.
Pl. `CKD-IRANYELV-EMMI-2021-LEJART.pdf`

## Hogyan használd mégis

A `pdf_horgonnyal.py` **ennek a mappának a `_pdf\`-jét is feldolgozza** —
külön szakaszban, a futás végén, hangos figyelmeztetéssel:

```
*** FIGYELEM ***
Ezek KIZAROLAG a '99 - ARCHIV' notebookba mehetnek, verzio-osszevetesre.
```

Verzió-összehasonlításra — „mi változott 2021 és 2025 között?" — **a
NotebookLM `99 – ARCHÍV` notebookjában**, ahova ennek a mappának a
`md\` tartalmát töltöd fel. Ott a szeparáció megmarad: az a notebook
külön van a generáló notebookoktól.

**Soha ne a csatolt mappából.**

---

*Created using Anthropic Claude* — ellenőrizetlen munkaanyag.
