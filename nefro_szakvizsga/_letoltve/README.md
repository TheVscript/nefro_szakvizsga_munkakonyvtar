# Ide töltsd le a PDF-eket — bármilyen néven

Ne törődj a fájlnevekkel. A böngésző adta `docread.pdf`,
`pfile_file_path=... (3).pdf`, `letoltes(7).pdf` — mind jó.

Amikor végeztél:

```powershell
pip install pymupdf
python _scriptek\atnevezo.py
```

A szkript minden PDF elejét elolvassa, felismeri, melyik dokumentum,
átnevezi a `forras_id`-ra, és bemozgatja a megfelelő mappába.
Te csak Entert nyomsz.

| Kapcsoló | Mit csinál |
|---|---|
| *(semmi)* | Minden fájlnál megkérdez. **Ezt használd elsőre.** |
| `--auto` | Csak a teljesen egyértelműeket mozgatja, a többit kihagyja |
| `--szaraz` | Csak mutatja, mit csinálna. Nem nyúl semmihez |

**A felismerés nem tévedhetetlen.** A tipp mellett megjelenik a dokumentum
első húsz szava — abból azonnal látod, jól tippelt-e. Ha nem:

- `1`, `2`, `3` → a felkínált másik lehetőség
- `s` → kihagyás, majd kézzel
- vagy beírod a saját azonosítót

Ami itt marad a futás után, azt kézzel nevezd át a
`00_FORRAS_ID_LISTA.md` alapján.

> **Szkennelt PDF-nél** (nincs szövegréteg) a szkript nem tud felismerni —
> kihagyja, és szól. Azokat kézzel nevezd el.
