# Pontos parancsok — Windows 11 · `D:\Szakvizsga`

**Útvonal:** hibrid (NotebookLM = kinyerés · Claude = gyártósor)
**A ZIP tartalma ellenőrizve** — 8 szkript + `_kozos.py`, a tételsor benne van, az `_ARCHIV_LEJART\` már testvérkönyvtár.

*Created using Anthropic Claude* — a megjegyzés maradjon rajta, amíg egy ember át nem nézte és nem validálta.

---

## Jelölések

| | |
|---|---|
| 💻 | **PowerShell-parancs** — másold be, Enter |
| ✋ | **Manuális lépés** — neked kell megcsinálni, nincs rá parancs |
| 🔴 | Ha ez elromlik, a rendszer csendben rossz lesz |

**Nyisd meg a Windows Terminalt** (Start → „Terminal"). Rendszergazda **nem kell**.

> **Egy Windows-sajátosság előre.** A `python` parancs frissen telepített gépen néha a Microsoft Store-t nyitja meg a futtatás helyett. Ha ezt látod, használd végig a `py` parancsot a `python` helyett — minden más ugyanaz.

---

# A. SZAKASZ — Környezet (~20 perc)

## 1. 💻 Python ellenőrzése

```powershell
python --version
```

**Jó válasz:** `Python 3.9.x` vagy újabb.
**Ha a Store nyílik meg vagy hibát ír:** telepítsd a [python.org](https://www.python.org/downloads/windows/) oldaláról, és a telepítőben **pipáld be az „Add python.exe to PATH"** dobozt. Utána nyiss **új** Terminal-ablakot.

---

## 2. 💻 Gyökérmappa és a ZIP kicsomagolása

✋ Előbb **másold be a `nefro_szakvizsga_munkakonyvtar.zip`-et** a `D:\Szakvizsga` mappába.

```powershell
New-Item -ItemType Directory -Force -Path "D:\Szakvizsga" | Out-Null
Expand-Archive -Path "D:\Szakvizsga\nefro_szakvizsga_munkakonyvtar.zip" -DestinationPath "D:\Szakvizsga" -Force
```

---

## 3. 💻 🔴 A szeparáció ellenőrzése — ez a legfontosabb egy sor

```powershell
Get-ChildItem "D:\Szakvizsga" -Directory | Select-Object Name
```

**Ezt KELL látnod — a kettőt EGYMÁS MELLETT:**

```
Name
----
_ARCHIV_LEJART
nefro_szakvizsga
```

> 🔴 Ha az `_ARCHIV_LEJART` a `nefro_szakvizsga`-n **belül** van, állj meg és mozgasd ki. A lejárt CKD-irányelv fizikai kizárása a rendszer **egyetlen 100%-os védelme** — minden más csak arra épül, hogy a modell engedelmeskedik a promptnak.

---

## 4. 💻 A ZIP tartalmának ellenőrzése

```powershell
cd "D:\Szakvizsga\nefro_szakvizsga"
Write-Host "`n--- SZKRIPTEK (9 fajl: 8 szkript + _kozos.py) ---" -ForegroundColor Cyan
Get-ChildItem "_scriptek\*.py" | Select-Object -ExpandProperty Name
Write-Host "`n--- TETELSOR ---" -ForegroundColor Cyan
Get-ChildItem "00_tetelsor" -Recurse -File | Select-Object -ExpandProperty Name
Write-Host "`n--- FORRASLAPOK (70 kell) ---" -ForegroundColor Cyan
(Get-ChildItem "tetelek_forrasok" -Recurse -Filter "*.md").Count
```

**Amit látnod kell:**

```
--- SZKRIPTEK (9 fajl: 8 szkript + _kozos.py) ---
_kozos.py
atnevezo.py
elavulas_riport.py
ellenoriz_idezet.py
ellenoriz_szamok.py
futtat.py
nyomtathato.py
pdf_horgonnyal.py
tetelsor_diff.py

--- TETELSOR ---
README.md
TETELSOR-NEFROLOGIA-2024-07-25.md     <- horgonyozott, EZ megy a notebookba
tetelsor_2024-07-25.md                <- kézi, a tetelsor_diff.py-nak
README.md
TETELSOR-NEFROLOGIA-2024-07-25.pdf

--- FORRASLAPOK (70 kell) ---
70
```

Ha bármelyik szám nem stimmel, **ott állj meg.**

---

## 5. 💻 pymupdf telepítése

```powershell
python -m pip install --upgrade pip
python -m pip install pymupdf
```

Ez az **egyetlen** függőség. Siker esetén a végén `Successfully installed pymupdf-...` áll.

---

# B. SZAKASZ — Anyagbeszerzés (~1,5 óra, ebből 5 perc gépmunka)

## 6. ✋ A letöltési terv megnyitása

```powershell
notepad "D:\Szakvizsga\nefro_szakvizsga\00_LETOLTESI_TERV.md"
```

*(Vagy nyisd meg bármilyen markdown-nézegetővel — olvashatóbb.)*

**Forrásoldal szerint haladj, ne tételenként.** A ~45 dokumentum nagy része több tételhez kell; tételenként indulva ugyanazt a PDF-et tízszer töltenéd le.

| Hol | Idő | Megjegyzés |
|---|---|---|
| MANET irányelv-oldal | ~40 perc | A dokumentumok ~60%-a. A „Lejárt a biztonsági időkorlát" üzenet a lap tetején **nem hiba**, görgess tovább |
| KDIGO gyűjtőoldal | ~20 perc | Nyilvános PDF-ek |
| AJKD Core Curriculum | ~20 perc | Csak a tételekhez tartozókat |
| Közvetlen linkek | ~10 perc | Hyponatraemia, MHT 2025, MaNET 2023 |

---

## 7. ✋ 🔴 Letöltés — minden a `_letoltve` mappába

A böngésző letöltési mappáját állítsd ide, vagy másold át utólag:

```
D:\Szakvizsga\nefro_szakvizsga\_letoltve\
```

**Bármilyen néven jó.** A böngésző adta `docread.pdf` is megfelel — az `atnevezo.py` a tartalomból ismeri fel.

> 🔴 **Minden letöltés után nyisd meg a PDF-et.** Harminc másodperc, és megmutatja, hogy a tartalmat kaptad-e meg vagy egy bejelentkező oldalt. **Ezt egyetlen szkript sem tudja eldönteni helyetted** — egy bejelentkező oldal is érvényes PDF, szövegréteggel.

**Amit nem tudsz tükrözővel letölteni:** a Szakmai Kollégium listája JavaScripttel töltődik, a MANET PDF-jei munkamenethez kötött `docread.aspx` linkek mögött vannak. `wget --mirror` vagy HTTrack ezeken üres oldalt hoz.

💻 Ellenőrzés, mennyi jött össze:

```powershell
(Get-ChildItem "D:\Szakvizsga\nefro_szakvizsga\_letoltve" -Filter "*.pdf").Count
```

*(~45 körül kell lennie.)*

---

## 7/b. ✋ 🔑 HTML-oldal → PDF (jogszabályok, webes források)

Ami csak weboldalként létezik — jogszabály (njt.hu), online tankönyvfejezet, társasági állásfoglalás —, azt **böngészőből nyomtasd PDF-be.** Így ugyanúgy kap oldalhorgonyt, mint bármelyik letöltött irányelv, és ugyanúgy géppel ellenőrizhető lesz.

### A beállítások számítanak

`Ctrl+P` → *Cél: **Mentés PDF-ként*** → **További beállítások**:

| Beállítás | Érték | Miért |
|---|---|---|
| **Fejlécek és láblécek** | 🔴 **KI** | Különben minden oldalra rákerül az URL és a dátum, ami **bekerül a kinyert szövegbe és beszennyezi az idézeteket** |
| Háttérgrafika | KI | Felesleges, és nehezíti a szövegkinyerést |
| Méretezés | **100%** | Ne „oldalhoz igazítás" — az összenyomja a sortörést |
| Papírméret | A4 | Következetesség |

> 🔴 **Előbb nyisd ki a lenyíló részeket.** Az njt.hu és sok más jogi oldal **összecsukva** mutatja a szakaszokat. Amit nem nyitottál ki, az **nem kerül bele a PDF-be** — és nem fogod észrevenni, mert a hiányról a rendszer nem tud.
>
> Nyomtatás után görgesd át a PDF-et: megvan minden §?

### Elnevezés — itt a dátum kötelező

```
NJT-EUTV-1997-CLIV-2026-10-08.pdf      →  06_jog\_pdf\
WEB-DIETETIKA-CKD-2026-10-08.pdf       →  04_tankonyv_hu\_pdf\
```

> **A dátum nem formalitás.** Egy weboldalról készült PDF **pillanatfelvétel**. A rendszer egész logikája a hatályosságon áll — ugyanaz a csapda, mint a 2021-es CKD-irányelvnél. Ha fél év múlva ránézel egy hivatkozásra, az azonosítóból látnod kell, mikori állapotot idéz.

⚠️ Az `atnevezo.py` ezeket **nem ismeri fel** (nincsenek a kulcsszólistájában). **Kézzel nevezd át, és kézzel tedd a helyükre** — fájlonként öt másodperc. Ezért ezeket ne a `_letoltve\`-be mentsd, hanem egyből a cél `_pdf\` mappába.

💻 Ellenőrzés, hogy van-e bennük valódi szövegréteg:

```powershell
cd "D:\Szakvizsga\nefro_szakvizsga"
python -c "import pymupdf,pathlib; [print(p.name, '->', sum(len(o.get_text().strip()) for o in pymupdf.open(p)), 'karakter') for p in pathlib.Path('06_jog/_pdf').glob('*.pdf')]"
```

Ha egy fájlnál **0 vagy nagyon kevés** karaktert ír, az képként mentődött — nyomtasd újra.

> **A jogszabály hivatkozása kettős lesz:** `[NJT-EUTV-... | p.012 | 12. § (3)]`. Az oldalszám teszi géppel ellenőrizhetővé, a §-szám az, amit a vizsgán mondasz. Ez benne van az agent-definícióban (`MODSZERTAN_v5.0.md`, 7.2).

---

# C. SZAKASZ — Rendszerezés (~20 perc)

## 8. 💻 A legegyszerűbb út — egy parancs

```powershell
cd "D:\Szakvizsga\nefro_szakvizsga"
python _scriptek\futtat.py
```

Végigvezet a teljes rendszerezésen, a helyes sorrendben:

1. ellenőrzi a `pymupdf`-et *(és felajánlja a telepítést)*
2. `atnevezo.py --szaraz` — **megvárja, hogy átnézd a tippeket**
3. `atnevezo.py` élesben *(itt te válaszolsz a kérdéseire)*
4. `pdf_horgonnyal.py` — az archívummal együtt
5. felajánlja az `elavulas_riport.py`-t
6. a végén kiírja, mi maradt rád *(táblázat-ellenőrzés, szeparáció, feltöltés)*

`--gyors` kapcsolóval a száraz próbát és a szüneteket kihagyja. **Windowson és Linuxon ugyanaz a parancs.**

> Ha inkább lépésenként akarod, a 8/a–9 pontok leírják ugyanezt kézzel.

---

## 8/a. 💻 Átnevezés és bemozgatás *(kézzel, ha nem a `futtat.py`-t használod)*

**Elsőre mindig szárazon:**

```powershell
cd "D:\Szakvizsga\nefro_szakvizsga"
python _scriptek\atnevezo.py --szaraz
```

Ez **nem nyúl semmihez**, csak kiírja, melyik fájlt minek ismerte fel. Fusd át: értelmesnek tűnnek a tippek?

**Aztán élesben:**

```powershell
python _scriptek\atnevezo.py
```

Minden fájlnál megkérdez. A billentyűk:

| Bemenet | Mi történik |
|---|---|
| `Enter` | elfogadod a tippet |
| `1` / `2` / `3` | a felkínált másik azonosító |
| `s` | kihagyás |
| *(saját szöveg)* | te adod meg a `forras_id`-t |

Amit nem ismert fel, azt a végén kilistázza — azokat nevezd át kézzel a `00_FORRAS_ID_LISTA.md` alapján.

> **Jó hír, amiről a doksi nem ír:** az `atnevezo.py` ismeri a `CKD-IRANYELV-EMMI-2021-LEJART` azonosítót, és **magától az `_ARCHIV_LEJART\_pdf\`-be mozgatja.** Nem neked kell észben tartanod.

---

## 8/b. 💻 🔴 Ellenőrizd, hogy a lejárt anyag tényleg kint van

```powershell
Write-Host "`n--- AMI AZ ARCHIVUMBAN VAN (ennek KINT kell lennie) ---" -ForegroundColor Yellow
Get-ChildItem "D:\Szakvizsga\_ARCHIV_LEJART" -Recurse -Filter "*.pdf" | Select-Object -ExpandProperty Name
Write-Host "`n--- LEJART ANYAG A MUNKAKONYVTARBAN (ITT NEM LEHET SEMMI) ---" -ForegroundColor Red
Get-ChildItem "D:\Szakvizsga\nefro_szakvizsga" -Recurse -Filter "*LEJART*" | Select-Object -ExpandProperty FullName
```

A második listának **üresnek kell lennie.** Ha nem az, mozgasd át a találatokat:

```powershell
Move-Item "D:\Szakvizsga\nefro_szakvizsga\<útvonal>\*LEJART*.pdf" "D:\Szakvizsga\_ARCHIV_LEJART\_pdf\"
```

---

## 9. 💻 PDF → markdown, oldalhorgonnyal

```powershell
python _scriptek\pdf_horgonnyal.py
```

Minden oldal elé beírja:

```
===== [CKD-IRANYELV-BM-2025 | p.047] =====
```

**Ez a lánc, amin az egész ellenőrizhetőség áll.** Ha PDF-et töltenél a NotebookLM-be, a modell az oldalszámot nem látja — vagy elhagyja, vagy **kitalálja**.

A szkript szól, ha egy PDF-ben nincs szövegréteg (szkennelt). A letöltött irányelvekhez **nem kell OCR** — digitálisan készült PDF-ek.

---

## 9/b. ℹ️ Az archívum automatikusan elkészül

A `pdf_horgonnyal.py` **javított változata** a lejárt anyagot is feldolgozza — külön szakaszban, a végén, és hangosan kiírja:

```
*** FIGYELEM ***
1 LEJART dokumentum .md-je elkeszult az _ARCHIV_LEJART/md/ alatt.
Ezek KIZAROLAG a '99 - ARCHIV' notebookba mehetnek, verzio-osszevetesre.
Generalo notebookba SOHA ne toltsd fel oket, es a mappat ne csatold.
```

> 🔴 Az itt keletkező `.md`-k a **felülírt, elavult** irányelvek. A `99 – ARCHÍV` notebookba mehetnek, verzió-összevetésre (*„mi változott 2021 és 2025 között?"*) — **generáló notebookba soha.**
>
> Ha nem akarsz verzió-összevetést, egyszerűen ne töltsd fel őket sehová. A fájlok ott maradnak a csatolt mappán kívül, ahol nem ártanak.

---

## 10. ✋ 🔴 Táblázat-ellenőrzés (~15 perc) — ezt ne hagyd ki

```powershell
Get-ChildItem "D:\Szakvizsga\nefro_szakvizsga\01_iranyelv_hu\md\*.md" | Select-Object -ExpandProperty Name
notepad "D:\Szakvizsga\nefro_szakvizsga\01_iranyelv_hu\md\CKD-IRANYELV-BM-2025.md"
```

Nyiss meg **2-3 generált `.md`-t**, és nézd meg a táblázatokat:

- CKD-stádiumbeosztás
- eGFR-kategóriák
- albuminuria-besorolás
- dóziskorrekciós táblák

**Ezek a legfontosabb adatok az egész anyagban, és a szövegkinyerés szét tudja szedni őket.** Ami szétesett, azt a néhány oldalt pótold kézzel a PDF-ből.

---

---

# D. SZAKASZ — NotebookLM (~1 óra) — **mind manuális**

## 11. ✋ Egy notebook felépítése

1. Nyisd meg a [notebooklm.google.com](https://notebooklm.google.com) oldalt
2. **Új notebook**, neve: `90 – CKD és szövődményei`
3. **Források hozzáadása** → a fájlkiválasztóban **`Ctrl` + kattintással több fájlt is kijelölhetsz**
4. Töltsd fel ezeket:

```powershell
# Ez a parancs megmutatja, melyik fájlokat jelöld ki — másold ki az útvonalakat
explorer "D:\Szakvizsga\nefro_szakvizsga\01_iranyelv_hu\md"
```

A 45–55. tételhez (90-es blokk) kellő források listáját a forráslapok adják:

```powershell
Get-Content "D:\Szakvizsga\nefro_szakvizsga\tetelek_forrasok\90_ckd\047.md"
```

**Szabályok:**

- 🔴 **`.md`-t tölts fel, NE PDF-et** — a PDF-ben a modell nem látja a horgonyt
- **Egy forrásdokumentum = egy fájl.** Ne vond össze őket egy nagy `.md`-be: elveszted a forrásszintű hivatkozást, a frissíthetőséget és a forráshierarchiát
- **Egy tankönyv marad egy fájl**, akkor is, ha 600 oldal
- A tételsorból **csak** a `TETELSOR-NEFROLOGIA-2024-07-25.md`-t töltsd fel — **H2**
- 🔴 A `07_sajat_jegyzet\` **soha nem megy generáló notebookba**

5. **Custom instructions:** másold be a `MODSZERTAN_v5.0.md` **7.3-as** rövidített agent-definícióját
6. Hozz létre egy **üres** `95 – Saját, ELLENŐRZÖTT` notebookot

---

# E. SZAKASZ — Claude (~30 perc) — **mind manuális**

## 12. ✋ 🔴 A mappa csatolása

A Claude asztali alkalmazásban csatold **pontosan ezt**:

```
D:\Szakvizsga\nefro_szakvizsga
```

> 🔴 **NE a `D:\Szakvizsga`-t csatold** — akkor az `_ARCHIV_LEJART\` is láthatóvá válik, és a lejárt 2021-es CKD-irányelvet a modell egyetlen fájlolvasásnyira megtalálja.

✋ Ellenőrzés: kérdezd meg a Claude-ot, hogy *„listázd ki a csatolt mappa gyökerét"*. Az `_ARCHIV_LEJART` **nem szerepelhet** a válaszban.

✋ Másold be a **7.2-es teljes agent-definíciót** (`MODSZERTAN_v5.0.md`) a projekt-utasításokba.

---

## 12/b. ✋ Az Anki beállítása — 6 mező, 7 oszlop

> A munkakönyvtár fájljait már javítottam (7 oszlopos CSV mindenhol). **Az Ankit viszont neked kell beállítanod** — ezt program nem tudja megcsinálni helyetted.
>
> Az eredeti leírás két helyen mondott mást a 6. mezőről. Ha a régi szerint állítanád be, **a piros „NYERS" jelzés soha nem jelenne meg** a kártyákon — és pont azt a védelmet veszted el, ami megakadályozza, hogy ellenőrizetlen kártyát tanulj.

**Amit az Ankiban csinálj** (*Eszközök → Jegyzettípusok kezelése → Hozzáadás*, neve `Nefro`), **6 mező ebben a sorrendben:**

```
Kerdes
Valasz
Horgony
Idezet
Tetel
Statusz
```

**És a CSV-fejléc 7 oszlopos legyen:**

```
#separator:Semicolon
#html:true
#notetype:Nefro
#deck:Nefrológia::00 Beérkező
#tags column:7
```

✋ **Ezt vedd fel a Claude agent-definíciójába is**, hogy a generált CSV 7 oszlopos legyen:

```
Kerdes;Valasz;Horgony;Idezet;Tetel;Statusz;Tagek
```

> **UTF-8 kódolással ments** — más kódolásban az ékezetek szétesnek.

---

## 13. ✋ 🔴 A két átvételi teszt — INNEN NEM MÉSZ TOVÁBB

### 13.1 NotebookLM — forráskötöttség

Kérdezz valamit, ami **biztosan nincs** a feltöltött anyagban (pl. egy gyermeknefrológiai dózis).

| Válasz | |
|---|---|
| `NINCS A FORRÁSOKBAN` | ✅ |
| bármi más | ❌ erősítsd a custom instructiont, teszteld újra |

### 13.2 Claude — zárt kontextus

Írd be, `<forras>` blokk **nélkül**:

> Dolgozd ki a 47. tételt.

| Válasz | |
|---|---|
| „Hiányzik a forrás." *(és nem dolgozza ki)* | ✅ |
| kidolgozza a tételt | ❌ a betanított tudásából dolgozik — pontosan az, ami ellen a rendszer épült |

**Fokozott változat:**

> Nézd meg a `01_iranyelv_hu\md\` mappát, és abból dolgozz.

A helyes válasz továbbra is a **megtagadás** — a csatolt mappa nem forrás.

---

# F. SZAKASZ — Az első teljes kör, 47. tétel (~1 óra)

## 14. ✋ A négy lépés

**1. NotebookLM-ben** (a `90 – CKD` notebookban) — a 8.1-es kinyerő prompt:

```
A 47. tétel: "CKD: kezelés".

Keresd meg a forrásokban MINDEN szövegrészt, ami erre a tételre
vonatkozik. A kimenet KIZÁRÓLAG szó szerinti idézetek listája,
mindegyik előtt a hozzá tartozó ===== horgony.

Nem foglalsz össze. Nem fogalmazol át. Nem rendszerezel.
Nem fűzöl hozzá semmit. Csak idézet és horgony.

Külön gyűjtsd ki MINDEN numerikus értéket tartalmazó mondatot,
teljes mondatként, csonkítás nélkül.

Ha egy témakörre (definíció / etiológia / diagnosztika / terápia /
prognózis) nem találsz semmit, írd ki: "NINCS TALALAT: [témakör]".
```

**2. Claude, ÚJ beszélgetés** — a kimenetet változtatás nélkül bemásolod:

````
Olvasd be: _output/forras/047_forras.md
EZ A FÁJL A <forras> BLOKK — a teljes tartalma.
Ezen kívül semmilyen más fájlt nem nyitsz meg, és a saját betanított
tudásodat nem használod.

A 47. tétel: "CKD: kezelés".

Ebben a körben CSAK ezt a kettőt készítsd el, és írd fájlba:

1. Tételkidolgozás a KIMENETI SABLON szerint
   → _output/tetelek/047.md

2. Forrásjegyzék-melléklet (A–E szakasz)
   → _output/ellenorzes/047_forrasjegyzek.md

Az Anki-kártyákat MÉG NE készítsd el — azt a következő üzenetben kérem.

Kizárólag a <forras> blokkból dolgozol. A korpuszmappákat
(01_–06_) nem nyitod meg. Az _output/-ból nem idézel.
````

**2b. Ugyanabban a beszélgetésben, külön üzenetként** — hogy a kimeneti token-limit ne csonkolja a CSV-t:

````
Most a fenti tételből készítsd el az Anki-kártyákat.
Forrás továbbra is KIZÁRÓLAG a <forras> blokk.

7 oszlop pontosvesszővel:
   Kerdes;Valasz;Horgony;Idezet;Tetel;Statusz;Tagek
A Statusz oszlopba minden sorban: NYERS
A CSV elejére tedd be a vezérlősorokat.
   → _output/anki/047_kartyak.csv
````

**3. 💻 Determinisztikus szám-ellenőrzés** — ez nem vélemény, hanem összehasonlítás:

```powershell
cd "D:\Szakvizsga\nefro_szakvizsga"
python _scriptek\ellenoriz_szamok.py _output\anki\047_kartyak.csv
```

**Ami itt kiesik, ott a modell olyan számot írt a válaszba, ami a saját idézetében sincs benne. Nem ítélet kérdése — dobd a kártyát.**

**4. Claude, HARMADIK, FRISS beszélgetés** — visszaellenőrzés a 9.3-as prompttal.

> 🔴 Ne ugyanabban a beszélgetésben. A modell a saját kimenetét nem ellenőrizni fogja, hanem **megvédeni** — ugyanaz a sycophancy, csak a saját korábbi szövege felé.
>
> A promptban benne marad: **„Ne javítsd. Csak minősíts."** Ha javíthat, javítani *fog*, és a javítás során újra generál — vagyis új hibát hozhat be, amit már senki nem ellenőriz.

---

## 15. 💻 Nyomtatható változat + kézi ellenőrzés

```powershell
python _scriptek\nyomtathato.py --ellenorzes
explorer "D:\Szakvizsga\nefro_szakvizsga\_output\nyomtathato"
```

Nyisd meg a `047_forrasjegyzek.html`-t, `Ctrl+P` → *Mentés PDF-be*, vagy nyomtasd ki.

✋ **Most jössz te, könyvvel a kézben** (~3 perc): a forrásjegyzék **A. szakaszának** minden 🔢 sorát keresd vissza az eredeti PDF-ben a horgony alapján.

> **A C. szakasznak üresnek kell lennie.** Ha nem az, ott a modell olyan számot írt le, amit nem tudott szó szerinti idézettel alátámasztani.

---

## 16. 💻 Mentés — ezt ne hagyd ki

```powershell
New-Item -ItemType Directory -Force -Path "D:\Szakvizsga\_mentes" | Out-Null
$d = Get-Date -Format "yyyy-MM-dd"
Compress-Archive -Path "D:\Szakvizsga\nefro_szakvizsga\_output\*" -DestinationPath "D:\Szakvizsga\_mentes\output_$d.zip" -Force
Write-Host "Mentve: D:\Szakvizsga\_mentes\output_$d.zip" -ForegroundColor Green
```

**Futtasd minden hétvége végén.** 27 óra munka van benne, és egyetlen meghajtón ül. Még jobb, ha a `_mentes` mappát OneDrive-ba vagy külső lemezre teszed.

---

## 17. 💻 Félévente: elavulás-riport

```powershell
python _scriptek\elavulas_riport.py
```

Megmondja, **melyik forrásnál érdemes megnézni**, jött-e újabb. Nem mozgat semmit, nem dönt el semmit — csak kiír két listát: verziógyanús párok, és egy korhatárnál régebbi források.

> 🔴 **A „régi" és a „lejárt" nem ugyanaz.** Egy 2012-es magyar ajánlás, amihez nincs újabb magyar változat, **hatályos marad** — akkor is, ha közben megjelent egy frissebb KDIGO. A három kategória: `MODSZERTAN_v5.0.md`, **13.3**.

---

# Napi rutin — a parancsok, amiket ismételni fogsz

```powershell
cd "D:\Szakvizsga\nefro_szakvizsga"

# minden új tétel után:
python _scriptek\ellenoriz_szamok.py _output\anki\NNN_kartyak.csv

# ha nyomtatni akarsz:
python _scriptek\nyomtathato.py --ellenorzes

# hetente:
Compress-Archive -Path ".\_output\*" -DestinationPath "D:\Szakvizsga\_mentes\output_$(Get-Date -Format 'yyyy-MM-dd').zip" -Force
```

> 🔴 **Egy tétel = egy friss beszélgetés.** Ugyanabban a beszélgetésben a 7. tétel hivatkozása a 3. tétel szövegére fog mutatni — formailag tökéletesen, tartalmilag hamisan. És az önellenőrző blokk „nem"-et fog írni. **Költsége nulla.**

---

# Hibaelhárítás

| Tünet | Megoldás |
|---|---|
| `python` a Microsoft Store-t nyitja | Használd a `py` parancsot, vagy telepítsd újra python.org-ról „Add to PATH"-szal |
| `Hianyzik a pymupdf` | `python -m pip install pymupdf` — ha több Pythonod van, `py -m pip install pymupdf` |
| `Nincs PDF a _letoltve/ mappaban` | A letöltések máshová mentek. Másold át őket `D:\Szakvizsga\nefro_szakvizsga\_letoltve\`-be |
| Az `atnevezo.py` semmit nem ismer fel | Valószínűleg bejelentkező oldalakat töltöttél le. Nyisd meg a PDF-eket, és nézd meg, mi van bennük |
| Ékezetek szétesnek a CSV-ben | UTF-8-ban ments. PowerShellben: `chcp 65001` |
| `Expand-Archive` hibát ír | A ZIP zárolva lehet: jobb klikk → Tulajdonságok → **Feloldás (Unblock)** |
| A Mermaid-ábrák nem látszanak a HTML-ben | Internet kell az első megnyitáskor (CDN). Offline a forráskód látszik — nem katasztrófa, csak csúnya |
| Útvonalhossz-hiba | Windows 260 karakteres limit. Ezért van `D:\Szakvizsga` és nem mélyebb mappa — ne told be egy hosszú útvonal alá |

---

# ⏭️ Mi a következő lépés — a döntések, amiket most el kell halasztanod

## Most (0 Ft)

**A 14. lépés két átvételi tesztje ingyenes szinten is elvégezhető**, és ez a legjobb vásárlásod: 0 Ft-ért kiderül, működik-e az agent-definíció.

> **Az értelmezéshez.** Az ingyenes szintek gyakran kisebb modellt adnak, ezért a logika egy irányban működik: **ha ingyenesen jó, fizetősen is jó lesz. Fordítva nem.** Ha a csapdateszt ingyenesen elbukik, javíts a prompton és próbáld újra; ha háromszor sem megy, nézd meg fizetősen, mielőtt feladod a megközelítést.

## Amikor a tesztek zöldek — Claude Pro

**A mappa-csatolás (Cowork) fizetős csomagot igényel, legalább Pro-t.** Enélkül a Claude nem tud fájlt írni az `_output\`-ba — a tételgyártás megy, de a kimenetet neked kell kézzel kimásolnod és fájlba mentened, ami 70 tételnél ~3 óra tiszta másolgatás. Pontosan ezt váltja ki a v3.0.

~9 000 Ft/hó. **Ne köss éves előfizetést a generálási szakasz előtt.**

## Amikor az első tételeid elkészültek — NotebookLM

**Az ingyenes szint 50 forrást enged notebookonként**, egy blokk ~12 forrásból áll — tehát az **első blokk és a kikérdezés elfér ingyen.** A `95 – Saját` notebookhoz pláne nem kell Pro: oda csak a kész tételeid kerülnek.

**A Google AI Pro (~9 000 Ft/hó, ebben van a NotebookLM Pro, külön nem kapható) akkor merüljön fel**, ha ténylegesen limitbe futsz — tipikusan a 11 blokk-notebook felépítésénél vagy az audio overview napi korlátjánál.

> ✋ Mielőtt Google AI Pro-t veszel, **nézd meg, van-e már Google One előfizetésed** — lehet, hogy olcsóbb az átváltás.

## Amit NE vegyél meg

| | Miért |
|---|---|
| **Claude Max 5×** (~45 000 Ft/hó) | 70 tételhez a Pro nagy eséllyel elég. Csak akkor, ha ténylegesen limitbe futsz |
| **Lokális ellenőrző modell** (a Függelék) | 5–6 óra beruházás, ~2 óra megtakarítás. **Önmagában nem térül meg** |
| **Könyvszkenner + OCR** (~12 000 Ft) | Csak ha a tankönyveidet is be akarod vinni. Az első hétvégéhez nem kell — a letöltött irányelvekben van szövegréteg |

## Az árakról

~360 Ft/USD árfolyammal és 27% ÁFA-val számolt közelítések, 2026. októberi listaárak alapján. **Ellenőrizd a szolgáltató magyar számlázási oldalán** — ezek gyorsan változnak.

---

> **Ellenőrizetlen munkaanyag.** A rendszer kimenete minden esetben ellenőrizendő piszkozat — nem kész tananyag, és végképp nem klinikai döntéstámogatás. A numerikus értékek visszaellenőrzése az eredeti forrásban **nem opcionális lépés.** A magyar szakmai irányelvek hatályosságát mindig az eredeti kibocsátói oldalon ellenőrizd, ne ebből a dokumentumból.
>
> Csak olyanokkal oszd meg, akik a forrásanyagot is jogosultak látni.
