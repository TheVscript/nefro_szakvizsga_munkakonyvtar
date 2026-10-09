# `_output/forras/` — a kinyert, ellenőrzött idézetblokkok

Ide kerül tételenként egy `NNN_forras.md`: a tételhez tartozó **szó szerinti
idézetek**, oldalhorgonyokkal csoportosítva.

```
===== [CKD-IRANYELV-BM-2025 | p.047] =====
"A stádiumbeosztás alapja a becsült GFR és az albuminuria."
```

## Honnan jön

| Útvonal | Ki állítja elő |
|---|---|
| **Hibrid** | a NotebookLM kinyerő lépése → **te** mented ide másolás-beillesztéssel |
| **Csak Claude** | a Claude olvassa a `md/` forrásfájlt és ide írja |

> 🔴 **A hibrid úton te mented a fájlt, nem a Claude.** Ha a modellel menteted
> el, újra ki kell írnia a teljes szöveget — és egy hosszú idézetblokk
> újragépelése közben csendben megváltozhat egy szám. A másolás-beillesztés
> nem megy át modellen.

## Mielőtt bármit gyártasz belőle

```powershell
python _scriptek\ellenoriz_idezet.py _output\forras\047_forras.md
```

> **Mindkét útvonalon futtasd le.**
>
> A **Claude-only** úton ez nem kihagyható: ott semmi más nem méri, hogy a
> modell tényleg másolt-e, vagy átfogalmazott.
>
> A **hibrid** úton a NotebookLM nem fogalmaz át — **de a horgony
> elcsúszhat.** Ha a szomszédos oldal horgonyát másolja az idézet elé, a
> hivatkozásod hamis lesz, és pont ezt nem veszed észre a kézi
> ellenőrzésnél: kinyitod a 47. oldalt, nem találod, és azt hiszed, te nézed
> rosszul. Legalább az első 10 tételnél mindig futtasd le.
>
> A szerencse az, hogy ezt **nem kell AI-nak ellenőriznie**: egy idézet vagy
> ott van a forrásban, vagy nincs. Szövegösszehasonlítás.

Ha hiba van, **ne menj tovább** — futtasd újra a kinyerést szigorúbb
prompttal. A hiányzó idézet még vállalható; a hamis nem.
