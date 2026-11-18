# HANDOFF – Detailprüfer Architektur

> Übergabe für eine neue Sitzung. Stand: **Mi 18.11.2026**, letzter Speicherstand `68ec816`
> (lokal = GitHub, Kurs-Repo). In claude.ai ist **Skill-Version v8** aktiv (18.11.) = lokaler Stand:
> Feature 11, Nachbesserung Ortgang (Konterlatte, Rähm, ZQ-06 Rechtschreibung …) und Werkzeug
> `verschieben` – alles seit `68ec816` noch **nicht gespeichert** (kein Commit).
> Zuerst diese Datei, dann `CLAUDE.md` (Dauerregeln) und `PLAN.md` (Plan, Stand, Entscheidungen).

---

## 1. Ziel des Projekts

Ein **Claude-Skill „Detailprüfer Architektur“** für die WPK *Vibecoding KI-Werkstatt*
(Jade Hochschule, 16.–20.11.2026). Der Skill prüft eine hochgeladene **Baudetail-Zeichnung
(PDF, z. B. Archicad-Export)** im Holzbau **qualitativ** nach deutschen Regeln und erzeugt
einen **PDF-Prüfbericht** mit:
- Kurzfazit, Befundliste und Maßnahmenliste zum Abhaken,
- farbig markierter Zeichnung (Kreise + Badges B1 …),
- **Korrekturskizze** (korrigierter Zustand grün eingezeichnet, zusätzlich als Vektor-PDF),
- Befundkarten (Ist / Korrektur nebeneinander), Schichtenaufbau mit **üblichen Dicken**,
  nicht Prüfbarem, offenen Fragen, Positivem,
- Anhang mit Methode, Annahmen, Code-Legende und **Quellenverzeichnis mit verlinkten Fußnoten**.

Nutzer: Architekturstudent (5. Sem.), **keine Programmierkenntnisse**, fachlich der Experte.
Abgabe: Projekt auf GitHub mit **README** + **Poster**, **Fr 20.11., 16 Uhr**;
empfohlener **Freeze Do 19.11., 12 Uhr**.

## 2. Aktueller Stand – Dateien und Zweck

```
detailpruefer-architektur/
├─ CLAUDE.md                 Dauerregeln (immer zuerst lesen)
├─ PLAN.md                   Plan, Etappen, Stand-Liste, Entscheidungen aus dem Interview (17.11.)
├─ HANDOFF.md                diese Übergabe
├─ .gitignore                tests/ausgabe/, dist/, __pycache__, .env
├─ skill/                    ← DER SKILL (als .zip/.skill in claude.ai hochgeladen)
│  ├─ SKILL.md               Hauptanweisung: Grundsätze, Einstufungen, Ablauf 1–7
│  │                         (Tragsystem, Bauteil-Check, Abgleiche, Fragerunde, Korrekturskizze,
│  │                         Dämmstoff-Schraffuren), Format befunde.json inkl. aller Zeichenwerkzeuge
│  ├─ checkliste.md          Rückfragen K1–K5 – nur konstruktiv relevante (kein Projektname, keine sd-Werte)
│  ├─ pruefkatalog/          Prüfregeln, jede mit Quelle
│  │  ├─ 00_uebersicht.md    Ziel, Quellenpflicht, Funktionstrennung, Grundsätze (u. a. 5: Fehlteile,
│  │  │                      7: mehrere richtige Varianten), Einstufungen, Vorgehen
│  │  ├─ 01_luftdichtheit.md          LD-01…06
│  │  ├─ 02_feuchteschutz.md          FS-01…05
│  │  ├─ 03_waermeschutz_waermebruecken.md   WB-01…04 (WB-01 mit Luftschicht- und Schraffur-Abgleich)
│  │  ├─ 04_winddichtheit_hinterlueftung.md  WH-01…07 (Wind, Hinterlüftung, Schlagregen, Steildach)
│  │  ├─ 05_holzschutz.md             HS-01…03
│  │  ├─ 06_konstruktion_holzrahmenbau.md    KO-01…07 (keine Statik; KO-07 Schichtenden)
│  │  ├─ 07_zeichnungsqualitaet.md    ZQ-01…05 (ZQ-05 prüft auch Dämmschraffur ↔ Dämmstoffart)
│  │  ├─ 08_dach_steildach.md         Bauteil-Katalog DA-01…06: Tragsystem, First, Belüftung,
│  │  │                               Traufe, Ortgang, Lattung (Pflichtbauteile, Varianten, Korrektur)
│  │  ├─ 09_wand_sockel.md            Bauteil-Katalog SO-01…04: Wand, Spritzwasserabstand,
│  │  │                               Schwelle/Feuchteschutz, Bodenaufbau
│  │  ├─ 10_bauteildicken.md          RW-01: übliche Dicken je Schicht (Praxis-Richtwerte mit Quelle)
│  │  ├─ 11_baustoffe.md              BS-01: geeignete Baustoffe je Einbaulage (fehlende Materialangabe)
│  │  ├─ quellen.json        40 Quellen (IDs, Titel, Links) – maßgeblich für Fußnoten im Bericht
│  │  └─ quellen.md          Erläuterung des Normstands (Recherche 16./17.11.2026)
│  └─ scripts/
│     ├─ raster.py           Zeichnung mit Prozent-Raster als PNG (--ausschnitt zum Zoomen)
│     ├─ markieren.py        Befund-Markierung + alle Zeichenwerkzeuge der Korrekturskizze
│     ├─ skizze.py           Korrekturskizze als eigene Vektor-PDF
│     ├─ bericht.py          PDF-Prüfbericht (reportlab; enthält das Berichtslayout – es gibt
│     │                      keine separaten Templates)
│     └─ requirements.txt    pypdf, reportlab, pypdfium2, pillow
├─ dist/                     (nicht auf GitHub) detailpruefer-architektur.zip / .skill für claude.ai
├─ beispiel/                 ältere Beispielberichte (Wandecke, Blindtest 2, Traufe) für README/Poster
└─ tests/
   ├─ details/               Testzeichnungen: wandeck_korrekt/_mit_fehlern, blindtest_2 (Ecke),
   │                         blindtest_3_traufe, traufe_korrekt, blindtest_4_first, blindtest_5_sockel
   ├─ befunde_*.json         Befundlisten je Testdetail (Eingabe für bericht.py);
   │                         befunde_werkzeugtest_first.json = reiner Test der Zeichenwerkzeuge
   ├─ test_maengel.json      Altlast (altes Format, ungenutzt)
   ├─ loesung/               Musterlösungen + Auswertungen – NICHT Teil des Skills
   └─ ausgabe/               Zwischenbilder/Testberichte (nicht auf GitHub)
```

**Zeichenwerkzeuge der Korrekturskizze** (Feld `korrektur` je Befund, Details in SKILL.md):
`entfernen` (weiß abdecken) · `daemmung` (`art`: weich = Schlaufen, hart = Zickzack,
hart_doppelt, geschlaengelt = Welle; `band` = Schichtrichtung/-dicke) · `platte`
(`schraffur`: striche/zickzack/punkte/diagonal) · `holz` (Rechteck oder `mitte`/`auf` +
`querschnitt_cm` + `richtung`/`winkel`, `schnitt` quer/laengs) · `lattenreihe` · `firstlatte`
(mit Halter) · `firstziegel` (mit Lüftungselement) · `profil` (freie Form, auch mit Dicke) ·
`bahn` (luftdicht/winddicht/abdichtung/unterdeckbahn/lueftungsband) · `abklebung` · `linie` ·
`durchstreichen` · `text` (umbrochen, nie abgeschnitten; `"farbe": "original"` = verdeckte
Kote/Beschriftung schwarz neu setzen). **Maße in cm** brauchen `detail.massstab` (z. B. "1:5").

**Befehle (Windows):**
```
%LOCALAPPDATA%\Programs\Python\Python312\python.exe skill/scripts/bericht.py <zeichnung.pdf> <befunde.json> <bericht.pdf>
```
In Git Bash: `/c/Users/ozand/AppData/Local/Programs/Python/Python312/python.exe`.
**ZIP für claude.ai neu packen** (nach jeder Änderung an `skill/`): Ordnerinhalt von `skill/`
als `detailpruefer-architektur/…` in `dist/detailpruefer-architektur.zip` packen und als
`dist/detailpruefer-architektur.skill` kopieren (Python-`zipfile`, siehe frühere Sitzungen).
**In claude.ai einspielen:** claude.ai → Plugins → bei „Detailpruefer architektur“ ⋯ →
„Neue Version hochladen“ → `.skill`-Datei → Hochladen (Erfolg: Meldung „ersetzt“, Version +1).
Browser dafür: Claude in Chrome (dort ist der Nutzer angemeldet; im eingebauten Browser nicht).
**GitHub:** https://github.com/Jade-HS-Vibecoding-WPK/Detailpruefer (Remote `origin`, Branch
`main`); altes Repo `Ozan44336/Detailpr-fer` als Remote `alt`.

## 3. Wichtige Entscheidungen und Regeln (vollständig in CLAUDE.md und PLAN.md)

- **Skill**, läuft mit dem Claude-Pro-Abo ohne API-Key (claude.ai, Code-Ausführung an,
  ohne Netzwerkzugriff) und in Claude Code.
- **Qualitative Prüfung, keine Berechnungen** → sonst „Nachweis erforderlich“. Längen im
  Maßstab ablesen und Maßketten addieren ist erlaubt.
- **Einstufungen:** klarer Aufbaufehler (Rot) · mögliche Auffälligkeit (Orange) ·
  Verbesserungshinweis (Blau) · aus der Datei nicht prüfbar; + Aussagesicherheit.
- **Fehlt ein funktional notwendiges Bauteil** (Regensicherheit, Lastabtrag, Dichtheit,
  Dämmung, Belüftung) → **klarer Aufbaufehler**, auch wenn es „geplant“ sein könnte.
- **Mehrere richtige Ausführungen anerkennen**; nicht gegen eine Musterlösung prüfen; die am
  besten geeignete Verbesserung zeichnen, Alternativen im Text. Musterlösungen nur zum
  Bewerten – keine detailbezogenen Koordinaten/Lösungen in den Skill.
- **Tragsystem erkennen** (Pfetten-/Sparren-/Kehlbalkendach) und danach prüfen.
- **Rückfragen nur konstruktiv relevant**; gibt es keine, direkt prüfen.
- **Interner Bauteil-Check** vor jeder Prüfung (jede Schicht + Pflichtbauteile: vorhanden?
  Dicke gezeichnet/Legende/üblich? Schraffur vollständig?) – erscheint nicht im Bericht.
- **Übliche Bauteildicken** nur aus offiziellen, nachweisbaren Quellen (dataholz-Standardaufbauten
  u. a.), nur als Empfehlung; Abweichung → mögliche Auffälligkeit; im Schichtenaufbau Spalte „üblich“.
- **Korrekturskizze = korrigierter Zustand** wie eine überarbeitete Zeichnung: Falsches
  entfernen, Schichten mit derselben Schraffur durchgehend, Dämmung in voller Dicke über das
  ganze Feld, vollständige Bauteile (z. B. First: Ziegel + Lüftung + Latte + Halter).
- **Dämmstoff-Schraffuren sinngemäß:** weich (Faserdämmung) · hart (Platten) · geschlängelt
  (dünne weiche Lagen); Vorrang hat die Darstellung in der Zeichnung.
- **Quellenpflicht** `[[ID]]`; Foren sind keine Quelle; unsichere Zahlen weglassen.
- **Speicherstand (Commit + Push) nur auf Anweisung** des Nutzers.
- Vor Arbeiten mit offenen Fragen: **erst fragen, dann umsetzen**; alles Schritt für Schritt erklären.

## 4. Was zuletzt gemacht wurde (17./18.11.)

1. Blindtest 3 (Traufe) ausgewertet → KO-07; Skill erstmals in claude.ai getestet.
2. Korrekturskizze nach Musterlösung (entfernen, Schraffur fortführen), Dämmstoff-Schraffuren.
3. Interview zum First → neue Checkliste, Fehlteile = Aufbaufehler, Varianten, Tragsystem,
   neue Zeichenwerkzeuge, Bauteil-Kataloge 08/09 (Feature 9).
4. Blindtest 4 (First): Dämmung halbiert → Schraffur-Abgleich in WB-01.
5. Repository in die Kurs-Organisation umgezogen.
6. Blindtest 5 (Sockel, claude.ai v5): 2/5 voll, 1 teilweise, 2 übersehen → Höhen-Abgleich bis
   zur Schicht, SO-04 Bodenaufbau, `text` „original“.
7. **Feature 10 (18.11.):** übliche Bauteildicken (`10_bauteildicken.md`, 6 neue Quellen),
   interner Bauteil-Check, Spalte „üblich“ im Bericht → claude.ai **v6**, Speicherstand `68ec816`.

## 5. Was als Nächstes ansteht

0. v8 ist eingespielt → Ortgang (`tests/details/blindtest_6_ortgang.pdf`) in einem
   **neuen** claude.ai-Chat erneut testen – Blindtest 6 lief im alten Sockel-Chat mit v5.

1. **Blindtest mit v6** in einem **neuen** claude.ai-Chat (z. B. Ortgang; Detail liefert der
   Nutzer) → Auswertung `tests/loesung/AUSWERTUNG_<name>.md`.
2. **README.md** für GitHub (Was, Wie benutzen inkl. Upload in claude.ai, Beispielbilder,
   Grenzen, KI-Kennzeichnung) – **Pflicht für die Abgabe**.
3. **Beispielberichte** in `beispiel/` mit dem aktuellen Stand neu erzeugen (z. B. First aus
   `tests/befunde_blindtest_4_first.json`, Traufe v2) – für README und Poster.
4. **Poster** (Vorlage auf Moodle) – Inhalte/Bilder aus `beispiel/`.
5. Optional: fehlerfreies Detail für Fehlalarm-Quote; Fenster-/Ortgang-Details.

## 6. Bekannte Probleme / offene Punkte

- **v6 ist in claude.ai noch nicht mit einem Blindtest geprüft.**
- Fehler werden je Lauf unterschiedlich gefunden (Traufe lokal: OSB übersehen; claude.ai:
  Dämmung falsch gedeutet; Sockel: Sauberkeitsschicht, Fußleiste übersehen) – der neue
  Bauteil-Check soll das beheben, ist aber unerprobt.
- **Höhenänderungen:** neues Werkzeug `verschieben` (18.11.) – lokal am Ortgang erprobt
  (15 → 24 cm, Innenaufbau 9 cm nach innen); in claude.ai noch nicht getestet. Schnittkanten
  müssen sorgfältig gewählt werden (nie durch Texte/Maßzahlen).
- Koordinaten für Kreise, Badges und Korrekturen werden aus dem Rasterbild geschätzt →
  Kontrollbilder nötig; neue Bauteile können Original-Beschriftungen verdecken (dann
  `text` „original“ nutzen).
- Zeichnung im Bericht ist ein Rasterbild (200 dpi); vektorgenau nur `*_korrekturskizze.pdf`.
- **Quellen:** DIN 4108-2:2026-05 inhaltlich nicht geprüft; f_Rsi ≥ 0,70 nur über
  Sekundärquelle; ZVDH-Fachregeln nur über Übersicht (Bauprofessor); DIN 18516-1-,
  Lüftungsquerschnitts- (DIN 4108-3) und Kiesbett-Zahlen (DIN 68800-2) bewusst weggelassen;
  keine belegten Richtwerte für Bodenplatte, Pfetten, Perimeter-/Bodendämmung, Holzfaser-Außendämmung.
- Traufe: Winkel laut Musterlösung 35°, gezeichnet ca. 25° – mit dem Nutzer nicht geklärt.
- Wiederkehrender Fehlalarm-Typ: kurze Querlinien in Platten als „möglicher Plattenstoß“.
- Befundkarten mit Bildpaar sind hoch → teils Weißraum am Seitenende.
- Brand- und Schallschutz werden nicht geprüft (nur Hinweis).
- `beispiel/` enthält noch ältere Berichtsversionen; `tests/test_maengel.json` ist Altlast.
- Nutzer-E-Mail steht in den Git-Commits (bewusst so gewählt).
