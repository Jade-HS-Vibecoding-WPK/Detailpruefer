# HANDOFF – Detailprüfer Architektur

> Übergabe für eine neue Sitzung. Stand: **Do 19.11.2026** (v12 in claude.ai aktiv).
> Letzter Speicherstand `0609cc8` (lokal = GitHub, Kurs-Repo).
> **Nicht gespeichert (uncommitted):** alle Änderungen für **Skill-Version 11 und 12**
> (u. a. `skill/VERSION`, `fakten.py`, `bericht.py`, `markieren.py`, `SKILL.md`, Katalog 00/06/07/09/12,
> Tests, `HANDOFF.md`, `PLAN.md`). In claude.ai ist **v12** eingespielt (19.11., Plugin-Seite zeigt „v12“).
> Speicherstand nur, wenn der Nutzer es sagt.
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
- Anhang: Methode, Annahmen, **Prüfprotokoll aller Regeln**, Code-Legende,
  **Quellenverzeichnis mit verlinkten Fußnoten**.

Nutzer: Architekturstudent (5. Sem.), **keine Programmierkenntnisse**, fachlich der Experte.
Abgabe: Projekt auf GitHub mit **README** + **Poster**, **Fr 20.11., 16 Uhr**
(empfohlener Freeze war Do 19.11., 12 Uhr).

## 2. Aktueller Stand – Dateien und Zweck

```
detailpruefer-architektur/
├─ CLAUDE.md                 Dauerregeln (immer zuerst lesen)
├─ PLAN.md                   Plan, Etappen, Stand-Liste, Entscheidungen aus dem Interview (17.11.)
├─ HANDOFF.md                diese Übergabe
├─ .gitignore                tests/ausgabe/, dist/, __pycache__, .env
├─ skill/                    ← DER SKILL (als .zip/.skill in claude.ai hochgeladen)
│  ├─ VERSION                Skill-Version (eine Zeile, aktuell „12 (19.11.2026)“) – erscheint im Bericht
│  ├─ SKILL.md               Hauptanweisung: Grundsätze, Einstufungen, „Gleiches Detail → gleiches
│  │                         Ergebnis“, Ablauf 1–8 (Fakten, Tragsystem, Detailtyp, Bauteil-Check,
│  │                         Abgleiche, Fragerunde, Prüfen, Korrekturskizze, Bericht), Format befunde.json
│  ├─ checkliste.md          Rückfragen K0–K5 – nur konstruktiv relevante
│  ├─ referenz/              Referenzskizzen je Detailtyp (PNG) für die Lage der Bauteile
│  ├─ pruefkatalog/          Prüfregeln, jede mit Quelle
│  │  ├─ 00_uebersicht.md    Ziel, Quellenpflicht, Funktionstrennung, Grundsätze, Einstufungen, Vorgehen
│  │  ├─ 01_luftdichtheit.md          LD-01…06
│  │  ├─ 02_feuchteschutz.md          FS-01…05
│  │  ├─ 03_waermeschutz_waermebruecken.md   WB-01…04
│  │  ├─ 04_winddichtheit_hinterlueftung.md  WH-01…07
│  │  ├─ 05_holzschutz.md             HS-01…03
│  │  ├─ 06_konstruktion_holzrahmenbau.md    KO-01…08 (KO-05 Eck-Latten-Regel, KO-08 Schicht in allen Abschnitten)
│  │  ├─ 07_zeichnungsqualitaet.md    ZQ-01…06
│  │  ├─ 08_dach_steildach.md         DA-01…06 (Tragsystem, First, Belüftung, Traufe, Ortgang, Lattung)
│  │  ├─ 09_wand_sockel.md            SO-01…04 (Wand, Spritzwasser, Schwelle, Bodenaufbau)
│  │  ├─ 10_bauteildicken.md          RW-01 übliche Dicken (Praxis-Richtwerte mit Quelle)
│  │  ├─ 11_baustoffe.md              BS-01 geeignete Baustoffe je Einbaulage
│  │  ├─ 12_detailtypen.md            DT-00 Detail-Datenbank (Erkennungsmerkmale, Pflichtbauteile)
│  │  ├─ quellen.json        Quellen (IDs, Titel, Links) – maßgeblich für Fußnoten im Bericht
│  │  └─ quellen.md          Erläuterung des Normstands (Recherche 16./17.11.2026)
│  └─ scripts/               (alle modellneutral, reines Python)
│     ├─ fakten.py           NEU v11: Prüfsumme, Legende, Maßzahlen, Winkel, Texte exakt aus der PDF
│     ├─ raster.py           Zeichnung mit Prozent-Raster als PNG (--ausschnitt zum Zoomen)
│     ├─ linien.py           Vektorlinien exakt aus der PDF (Kanten, Schnittpunkte, Parallelen)
│     ├─ referenz.py         Referenzskizzen der Detailtypen erzeugen
│     ├─ markieren.py        Befund-Markierung + alle Zeichenwerkzeuge der Korrekturskizze
│     ├─ skizze.py           Korrekturskizze als eigene Vektor-PDF
│     ├─ bericht.py          PDF-Prüfbericht (reportlab; enthält das Layout – keine separaten Templates);
│     │                      ab v11: Datei/Prüfsumme/Skill-Version auf Seite 1, Warnung bei falscher
│     │                      Zeichnung, Anhang A3 Prüfprotokoll
│     └─ requirements.txt    pypdf, reportlab, pypdfium2, pillow
├─ dist/                     (nicht auf GitHub) detailpruefer-architektur.zip / .skill (Stand v12)
├─ beispiel/                 ältere Beispielberichte (Wandecke, Blindtest 2, Traufe) für README/Poster
└─ tests/
   ├─ details/               Testzeichnungen (u. a. wandeck_mit_fehlern, blindtest_2, blindtest_3_traufe,
   │                         traufe_korrekt, blindtest_4_first, blindtest_5_sockel, blindtest_6_ortgang)
   ├─ befunde_*.json         Befundlisten je Testdetail (Eingabe für bericht.py)
   ├─ loesung/               Musterlösungen + Auswertungen – NICHT Teil des Skills
   └─ ausgabe/               Zwischenbilder/Testberichte (nicht auf GitHub)
```
Weitere Musterlösungen des Nutzers liegen außerhalb des Projekts in
`C:\Users\ozand\Desktop\KI_Werkstatt\Details\` (u. a. `Sockel Detail Lösung.pdf`,
`Sockel Detail fehler.pdf` = `tests/details/blindtest_5_sockel.pdf`, Prüfsumme `0A1CA30A1524`).
Vom Nutzer erzeugte claude.ai-Berichte: `C:\Users\ozand\Desktop\KI_Werkstatt\Prüfberichte\`.

**Zeichenwerkzeuge der Korrekturskizze** (Feld `korrektur` je Befund, Details in SKILL.md):
`entfernen` · `verschieben` · `daemmung` (weich/hart/hart_doppelt/geschlaengelt, `band`) ·
`platte` (striche/zickzack/punkte/diagonal/kreuz) · `holz` · `lattenreihe` · `firstlatte` ·
`firstziegel` · `profil` · `bahn` · `abklebung` · `linie` · `durchstreichen` · `text`
(`"farbe": "original"` = verdeckte Beschriftung schwarz neu setzen). Maße in cm brauchen
`detail.massstab`.

**Befehle (Windows / Git Bash):**
```
/c/Users/ozand/AppData/Local/Programs/Python/Python312/python.exe skill/scripts/fakten.py <zeichnung.pdf> fakten.json
/c/Users/ozand/AppData/Local/Programs/Python/Python312/python.exe skill/scripts/bericht.py <zeichnung.pdf> <befunde.json> <bericht.pdf>
```
**ZIP neu packen** (nach jeder Änderung an `skill/`): Inhalt von `skill/` als
`detailpruefer-architektur/…` (ohne `__pycache__`) in `dist/detailpruefer-architektur.zip`,
Kopie als `dist/detailpruefer-architektur.skill` (Python-`zipfile`). **Version in `skill/VERSION`
hochzählen**, wenn eine neue Fassung eingespielt wird.
**In claude.ai einspielen (nur auf Wunsch):** Claude in Chrome → claude.ai/plugins →
„Detailpruefer architektur“ ⋯ → „Neue Version hochladen“ → `.skill` per Datei-Upload → Hochladen
(Erfolg: Meldung „ersetzt“, Version v… auf der Plugin-Seite).
**GitHub:** https://github.com/Jade-HS-Vibecoding-WPK/Detailpruefer (Remote `origin`, Branch `main`).

## 3. Wichtige Entscheidungen und Regeln (vollständig in CLAUDE.md und PLAN.md)

- **Skill** läuft mit dem Claude-Pro-Abo ohne API-Key (claude.ai mit Code-Ausführung, ohne
  Netzwerkzugriff) und in Claude Code.
- **Qualitative Prüfung, keine Berechnungen** → sonst „Nachweis erforderlich“. Längen im
  Maßstab ablesen und Maßketten addieren ist erlaubt.
- **Einstufungen:** klarer Aufbaufehler (Rot) · mögliche Auffälligkeit (Orange) ·
  Verbesserungshinweis (Blau) · aus der Datei nicht prüfbar; + Aussagesicherheit.
- **Fehlt ein funktional notwendiges Bauteil** → klarer Aufbaufehler.
- **Mehrere richtige Ausführungen anerkennen**; Musterlösungen nur zum Bewerten.
- **Gleiches Detail → gleiches Ergebnis (v11):** zuerst `fakten.py`; Legende/Maße/Winkel nur
  aus `fakten.json`; `detail.pruefsumme` eintragen; alle Regeln in fester Reihenfolge ins
  `pruefprotokoll`; Einstufung wörtlich nach Regeltext (im Zweifel die vorsichtigere);
  Gegenprüfung vor jedem klaren Aufbaufehler; frühere Prüfung derselben Datei übernehmen.
  Berichte sind nur vergleichbar bei gleicher **Datei-Prüfsumme und Skill-Version**.
- **Korrekturskizze = korrigierter Zustand**; Dämmstoff-Schraffuren sinngemäß.
- **Quellenpflicht** `[[ID]]`; Foren sind keine Quelle.
- **Speicherstand nur auf Anweisung**; **erst fragen, dann umsetzen**; alles Schritt für Schritt erklären.

## 4. Was zuletzt gemacht wurde (18./19.11.)

1. **Reproduzierbarkeit (v11, in claude.ai eingespielt):** Ursache der „unterschiedlichen
   Ergebnisse“ waren verschiedene Zeichnungen (Gebäudeecke: Testdetail 1 vs. Blindtest 2;
   „Ortgang___“ war die Traufe) und verschiedene Skill-Stände; dazu ein echter Fehlalarm
   (Eck-Latte 12 cm vor der Ecke). Umgesetzt: `fakten.py`, Prüfsumme/Version im Bericht,
   Prüfprotokoll, Abschnitt „Gleiches Detail → gleiches Ergebnis“, KO-05-Entscheidungsregel.
2. **Frage „Skill auf andere KI-Modelle übertragen“** beantwortet (noch **nichts umgesetzt**,
   Entscheidung des Nutzers offen): Katalog + Skripte sind modellneutral; nötig wären eine
   neutrale Anleitung (`ANLEITUNG_KI.md`/`AGENTS.md`), Paketprüfung und Einrichtung je
   Plattform. Realistisch: **OpenAI Codex** (liest `AGENTS.md`, arbeitet im Ordner) gut;
   ChatGPT-GPT mittel (kurze Anweisung, Pakete unsicher); Gemini eingeschränkt (PDF-Erzeugung);
   offene Modelle aufwendig. Prüfqualität je Modell **nicht garantierbar**.
3. **Sockel – Sauberkeitsschicht übersehen (Analyse fertig, Umsetzung OFFEN):**
   claude.ai-Bericht `Downloads\Pruefbericht_Sockel.pdf` (v11, Datei `0A1CA30A1524`) hat die
   fehlende Sauberkeitsschicht nicht erkannt und die Schichtenfolge sogar als positiv gewertet.
   **Befund:** In der Fehlerzeichnung liegt die Sauberkeitsschicht (5 cm) **nur unter dem
   Fundament** (−0,80 m); unter der Bodenplatte im Innenbereich (UKRD −0,44 m) fehlt sie.
   Laut Musterlösung läuft sie unter der **ganzen** Bodenplatte durch.
   **Ursache:** Die Beschriftung „Sauberkeitsschicht“ zeigt auf das Fundament → der Skill
   hielt die Schicht für vorhanden. Fehlerklasse: *Schicht ist irgendwo gezeichnet und
   beschriftet, fehlt aber in einem Teilabschnitt* (gilt ebenso für Abdichtung, Dämmung,
   Trennlagen, Bahnen).

4. **Sauberkeitsschicht-Fix umgesetzt (v12, 19.11.):** Nutzer-Entscheidung: fehlt die
   Sauberkeitsschicht (ganz oder teilweise) → klarer Aufbaufehler. Neue allgemeine Regel
   **KO-08** (jede Schicht in allen Abschnitten, Protokoll mit Abschnitten), SKILL.md
   Bauteil-Check Punkt 8 (Abschnitts-Check) + 9 (Unterkanten-/Rand-Check), Positiv erst nach
   Abschnitts-Check; SO-04, ZQ-04, DT-W1, `00_uebersicht`; `platte` Schraffur `kreuz`.
   Quelle: keine gesicherte Normfundstelle gefunden → `BAUPROFESSOR-SAUBERKEITSSCHICHT` + PRAXIS.
   Test: `tests/befunde_test_sauberkeitsschicht.json` → `tests/ausgabe/sks_test_bericht.pdf`;
   Auswertung `tests/loesung/AUSWERTUNG_blindtest_5_v11.md`.

## 5. Was als Nächstes ansteht

0. **Sockel mit v12 in einem neuen Chat prüfen** (v12 ist eingespielt): Wird die fehlende Sauberkeitsschicht unter der Sohle als klarer Aufbaufehler
   gemeldet, und nennt das Prüfprotokoll bei KO-08 die Abschnitte?
1. **Speicherstand** für v11 + v12 – nur auf Anweisung.
2. **README.md** für GitHub (Was, Wie benutzen inkl. Upload in claude.ai, Beispielbilder,
   Grenzen, KI-Kennzeichnung) – **Pflicht für die Abgabe (Fr 20.11., 16 Uhr)**.
3. **Beispielberichte** in `beispiel/` mit aktuellem Stand neu erzeugen (für README/Poster).
4. **Poster** (Vorlage auf Moodle).
5. Optional: Übertragbarkeit auf andere Modelle (Entscheidung des Nutzers); Reproduzierbarkeit
   in claude.ai testen (zwei neue Chats, dieselbe Datei, Prüfprotokolle vergleichen).

## 6. Bekannte Probleme / offene Punkte

- **Sauberkeitsschicht / Teilabschnitte:** in v12 behoben (KO-08, SKILL.md Punkt 8/9, SO-04),
  lokal getestet, v12 in claude.ai eingespielt; Test in claude.ai steht aus.
- KI-Läufe schwanken weiterhin bei Bilddeutungen; fest sind nur die Text-Fakten (`fakten.py`)
  und die Entscheidungsregeln. v11 in claude.ai noch nicht auf Reproduzierbarkeit getestet.
- Alte Testbefundlisten (`tests/befunde_*.json`) haben kein `pruefprotokoll` → Bericht meldet
  „nicht dokumentiert“ für viele Regeln.
- `verschieben` in claude.ai nicht getestet; Schnittkanten nie durch Texte/Maßzahlen legen.
- Koordinaten für Kreise/Badges/Korrekturen geschätzt → Kontrollbilder nötig.
- Zeichnung im Bericht ist ein Rasterbild (200 dpi); vektorgenau nur `*_korrekturskizze.pdf`.
- **Quellen:** DIN 4108-2:2026-05 inhaltlich nicht geprüft; f_Rsi ≥ 0,70 nur Sekundärquelle;
  ZVDH nur über Übersicht; mehrere Zahlenwerte bewusst weggelassen.
- Traufe: Winkel laut Musterlösung 35°, gezeichnet ca. 25° – nicht geklärt.
- Wiederkehrender Fehlalarm-Typ: kurze Querlinien in Platten als „möglicher Plattenstoß“.
- Befundkarten mit Bildpaar teils mit Weißraum am Seitenende.
- Brand- und Schallschutz werden nicht geprüft (nur Hinweis).
- `beispiel/` enthält ältere Berichtsversionen; `tests/test_maengel.json` ist Altlast.
- Nutzer-E-Mail steht in den Git-Commits (bewusst so gewählt).
