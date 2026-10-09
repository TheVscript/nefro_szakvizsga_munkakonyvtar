# Tételsor — két fájl, ne keverd össze

| Fájl | Mi ez | Ki állítja elő |
|---|---|---|
| `tetelsor_2024-07-25.md` | **Navigációs változat.** A 70 tétel blokkokba rendezve, linkelve a forráslapokra | **Készen érkezett** a munkakönyvtárral. Kézzel szerkeszthető |
| `TETELSOR-NEFROLOGIA-2024-07-25.md` | **Nyers kivonat** a PDF-ből, oldalhorgonyokkal | `pdf_horgonnyal.py` — ez megy a NotebookLM-be |
| `_pdf/TETELSOR-...pdf` | Az eredeti PDF | **A ZIP-ben benne van.** Ez a hiteles példány — ellenőrzéskor ebben keresel vissza |

A vizsgán a honlapról **aktuálisan letöltött** verzió használható. A pontos
hitelesítési szabályokat a vizsgaszervezőtől kérdezd meg.

## Ha új verzió jelenik meg

```powershell
# 1. töltsd le az újat a _letoltve/ mappába
python _scriptek\atnevezo.py

# 2. nézd meg, mi változott
python _scriptek\tetelsor_diff.py
```

A szkript összeveti az új PDF kérdéslistáját a jelenlegi 70 tétellel, és
kiírja, mi került bele, mi tűnt el, és mi fogalmazódott át. A **blokkbeosztás
és a forrás-hozzárendelés viszont szerkesztői döntés** — azt a diff alapján
neked (vagy az AI-nak) kell átvezetned a `tetelek_forrasok/` lapokon.


## A tételcímekről

A címeket a PDF-hez képest **enyhén normalizáltam**: feloldottam a
rövidítéseket és javítottam a nyilvánvaló elütéseket. Hét sorban tér el a nyers szövegtől (a 42-esben két helyen):

| # | PDF-ben | Itt |
|---|---|---|
| 17 | „…glom. káros" *(csonka)* | „…glom. károsodás" |
| 19 | „klinikai manif-k" | „klinikai manifesztációi" |
| 28 | „Lidle sy" | „Liddle sy" |
| 42 | „epidemiológiai", „klin. tünetek" | „epidemiológia", „klinikai tünetek" |
| 43 | „nondialítikus th" | „nondialítikus th." |
| 53 | „ásv. anyagcsere… vesebetegégekben" | „ásványi anyagcsere… vesebetegségekben" |
| 64 | „TX imm. szupresszív szerek" | „TX immunszupresszív szerek" |

Ezért a `tetelsor_diff.py` önmagán futtatva **7 kozmetikai eltérést** jelez —
ez normális, nem hiba.

> **A vizsgán a hivatalos, nyers megfogalmazás a mérvadó.** Ha a tétel
> szövegén múlik valami, a `_pdf/` mesterpéldányt nézd, ne ezt a fájlt.
