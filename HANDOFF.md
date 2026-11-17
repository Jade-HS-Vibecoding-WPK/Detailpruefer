# HANDOFF – Detailprüfer Architektur

> Übergabe für eine neue Sitzung. Stand: **Di 17.11.2026**, letzter Speicherstand `adefb13`
> (lokal = GitHub). Zuerst diese Datei, dann `CLAUDE.md` und `PLAN.md` lesen.

---

## 1. Ziel des Projekts

Ein **Claude-Skill „Detailprüfer Architektur“** für die WPK *Vibecoding KI-Werkstatt*
(Jade Hochschule, 16.–20.11.2026). Der Skill prüft eine hochgeladene **Baudetail-Zeichnung
(PDF, z. B. Archicad-Export)** im Holzbau **qualitativ** nach deutschen Regeln und erzeugt
einen **PDF-Prüfbericht** mit:
- Kurzfazit, kompakter Befundliste und Maßnahmenliste zum Abhaken,
- farbig markierter Zeichnung (Kreise + Badges B1 …),
- **Korrekturskizze** (fehlende Teile grün eingezeichnet),
- Befundkarten (Ist / Korrektur nebeneinander), offenen Fragen, Positivem,
- Anhang mit Methode, Annahmen, Code-Legende und **Quellenverzeichnis mit verlinkten Fußnoten**.

Nutzer: Architekturstudent (5. Sem.), **keine Programmierkenntnisse**, fachlich der Experte.
Abgabe laut Kurs: Projekt auf GitHub mit README (Fr 20.11., 16 Uhr) + Poster;
empfohlen: **Do 19.11., 12 Uhr Freeze**.

## 2. Aktueller Stand – Dateien und Zweck

```
detailpruefer-architektur/
├─ CLAUDE.md                 Dauerregeln für die Zusammenarbeit (immer zuerst lesen)
├─ PLAN.md                   Plan (Must/Should/Could, Etappen) + Stand-Liste (Abschnitt 10)
├─ HANDOFF.md                diese Übergabe
├─ .gitignore                tests/ausgabe/, __pycache__, .env
├─ skill/                    ← DER SKILL (wird als ZIP in claude.ai hochgeladen)
│  ├─ SKILL.md               Hauptanweisung: Grundsätze, Einstufungen, Ablauf 1–7, Format befunde.json
│  ├─ checkliste.md          Rückfragen C0–C9 mit Annahmen (Projektname, Neubau/Bestand, Nutzung …)
│  ├─ pruefkatalog/
│  │  ├─ 00_uebersicht.md    Ziel, Quellenpflicht, Funktionstrennung, 10 Grundsätze, Einstufungen,
│  │  │                      Aussagesicherheit, Priorität, Regelschema, Vorgehen
│  │  ├─ 01_luftdichtheit.md          LD-01…06
│  │  ├─ 02_feuchteschutz.md          FS-01…05
│  │  ├─ 03_waermeschutz_waermebruecken.md   WB-01…04
│  │  ├─ 04_winddichtheit_hinterlueftung.md  WH-01…07 (A Wind, B Hinterlüftung, C Schlagregen, D Steildach)
│  │  ├─ 05_holzschutz.md             HS-01…03
│  │  ├─ 06_konstruktion_holzrahmenbau.md    KO-01…07 (keine Statik; KO-07 Schichtenden)
│  │  ├─ 07_zeichnungsqualitaet.md    ZQ-01…05 (inkl. Wand-zu-Wand-Abgleich)
│  │  ├─ quellen.json        Quellenverzeichnis (IDs, Titel, Links) – maßgeblich für den Bericht
│  │  └─ quellen.md          Erläuterung des Normstands (Recherche 16./17.11.2026)
│  └─ scripts/
│     ├─ raster.py           Zeichnung mit Prozent-Raster als PNG (auch --ausschnitt zum Zoomen)
│     ├─ markieren.py        Befund-Kreise/Badges/Schraffur + Funktionen für die Korrekturskizze
│     ├─ skizze.py           Korrekturskizze als eigene Vektor-PDF
│     ├─ bericht.py          PDF-Prüfbericht (reportlab, 2–3 Durchläufe für Seitenverweise)
│     └─ requirements.txt    pypdf, reportlab, pypdfium2, pillow
├─ beispiel/                 fertige Beispielberichte + Korrekturskizzen (für README/Poster)
└─ tests/
   ├─ details/               Testzeichnungen: wandeck_korrekt, wandeck_mit_fehlern,
   │                         blindtest_2 (Gebäudeecke), blindtest_3_traufe
   ├─ befunde_*.json         Befundlisten je Testdetail (Eingabe für bericht.py)
   ├─ test_maengel.json      alter Markier-Test (veraltetes Format, nur noch Altlast)
   ├─ loesung/               Lösungsschlüssel + Auswertungen – NICHT Teil des Skills
   └─ ausgabe/               Zwischenbilder (nicht auf GitHub)
```

**Befehle (Windows, Python ist installiert, aber evtl. nicht im PATH alter Terminals):**
```
%LOCALAPPDATA%\Programs\Python\Python312\python.exe skill/scripts/bericht.py <zeichnung.pdf> <befunde.json> <bericht.pdf>
```
In Git Bash: `/c/Users/ozand/AppData/Local/Programs/Python/Python312/python.exe`.
Git 2.56 ist installiert; Repo: **https://github.com/Jade-HS-Vibecoding-WPK/Detailpruefer** (Kurs-Organisation, Branch `main`, Remote `origin`; altes Repo = Remote `alt`,
Anmeldung über Git Credential Manager erledigt).

## 3. Wichtige Entscheidungen und Regeln (Kurzfassung – vollständig in CLAUDE.md)

- **Skill (Weg 2)**, läuft mit dem Claude-Pro-Abo ohne API-Key; zusätzlich in Claude Code.
- **Qualitative Prüfung, keine Berechnungen** (sd, U, R, f_Rsi, Tauwasser, Statik) →
  sonst „Nachweis erforderlich“. Längen im Maßstab ablesen und Maßketten addieren ist erlaubt.
- **Einstufungen:** klarer Aufbaufehler (nur wenn eindeutig, Rot) · mögliche Auffälligkeit
  (Orange) · Verbesserungshinweis (Blau) · aus der Datei nicht prüfbar (keine Markierung);
  dazu Aussagesicherheit hoch/mittel/gering.
- **Quellenpflicht:** Jede Norm-/Gesetzes-/Paragraphennennung im Bericht mit `[[ID]]` aus
  `quellen.json`; nur verifizierte Inhalte/Grenzwerte. Normstand: **GModG** (vormals GEG,
  in Kraft 29.07.2026), DIN 4108-7:2026-04, DIN 4108-2:2026-05 (GModG § 11 verweist auf 2013-02),
  DIN 4108-3:2024-03, DIN 18516-1:2024-10 (Zahlen nicht verifiziert → keine Zahlen), u. a.
- **Gehrung an Holzfassaden-Außenecken ist empfohlen** (BauNetz Wissen) – kein Befund.
- **Funktionen trennen** (LD / FS / WH A–D), **keine Doppelbefunde**, Risiken vorsichtig formulieren.
- **Bericht:** kein Kopfblock auf Seite 1; Disclaimer nur einmal (Seite 1) + Fußzeile;
  Präfixe B (Befunde), S bzw. D/W (Schichten, außen → innen wie Legende), F (offene Fragen);
  Codes klein/grau mit Code-Legende; keine Dateipfade/Chat-Verweise im Bericht.
- **Korrekturskizze immer** (grün): fehlende Latten, Stiele, Platten, Dämmung, Abklebungen,
  korrigierte Werte einzeichnen – Beschriftung „Bx: …“ mit Hinweislinie.
- **Ablauf je Prüfung:** Zeichnung erfassen (Raster/Zoom/Texte mit Positionen) → **eine**
  Fragerunde (Checkliste) → alle Regeln → befunde.json → markieren/kontrollieren →
  skizze → bericht → **jede Seite als Bild prüfen**.
- **Speicherstand (Commit + Push) nur, wenn der Nutzer es sagt.**

## 4. Was zuletzt gemacht wurde

1. Bericht nach Nutzer-Feedback komplett neu aufgebaut (Kurzfazit, Maßnahmenliste,
   Fußnoten-Quellen, Befundkarten, Code-Legende).
2. **Blindtest 2** (Gebäudeecke) ausgewertet: **4 von 4** eingebauten Fehlern gefunden,
   1 Fehlalarm (möglicher Plattenstoß, Aussagesicherheit „gering“) → `tests/loesung/AUSWERTUNG_blindtest_2.md`.
3. **Korrekturskizze** eingeführt (`skizze.py`, Feld `korrektur`, Ist/Korrektur in Karten).
4. **Blindtest 3 – Traufe** geprüft (Bericht in `beispiel/`): B1 Sparrenfeld nur halb gedämmt
   (10 cm Luftschicht), B2 Fußpfette 16/20 ohne Auflager und zu klein gezeichnet,
   B3 Dachlegende widersprüchlich (Lattung/Konterlattung, Maßkette), B4 Dachneigung 45°
   beschriftet / ca. 25° gezeichnet, B5 Folie/Dämmstoffe nicht in Legende.
   Dabei Regeln WH-06, WH-07, KO-06 + Quelle ZVDH ergänzt.
5. Speicherstand `adefb13` auf GitHub.

## 4b. Stand Feature 9 (17.11., nach Interview zum First)

Entscheidungen des Nutzers stehen in PLAN.md („Entscheidungen aus dem Interview“). Umgesetzt:
neue Checkliste (nur konstruktiv relevante Fragen), Fehlteile = klarer Aufbaufehler,
mehrere richtige Varianten, Tragsystem erkennen, neue Zeichenwerkzeuge (cm-Maße, gedrehte
Hölzer, Firstziegel/-latte, Profile, Bahnen), Bauteil-Kataloge `08_dach_steildach.md` und
`09_wand_sockel.md`. In claude.ai ist diese Version aktiv. Testdetail First:
`tests/details/blindtest_4_first.pdf`, Musterlösung `tests/loesung/blindtest_4_first_musterloesung.pdf`.
Lüftungsquerschnitte (DIN 4108-3) und Kiesbett-Regeln (DIN 68800-2) bewusst ohne Zahlen
(Quellen widersprüchlich bzw. nicht im Original geprüft).

## 5. Was als Nächstes ansteht

1. ~~Auswertung Blindtest 3~~ erledigt (17.11.): 3 von 4, OSB-Überstand übersehen → KO-07.
   Offen: Winkel laut Musterlösung 35°, gezeichnet ca. 25° (Nutzer fragen).
2. ~~claude.ai-Test~~ erledigt (17.11., über Claude in Chrome): Skill als Plugin hochgeladen
   (claude.ai → Plugins → Hinzufügen → Plugin hochladen → `dist/detailpruefer-architektur.zip`).
   Technik läuft vollständig (auch ohne Netzwerkzugriff). Die drei Nachbesserungen
   (Fragerunde, Luftschicht, Überschrift) und das neue **Korrekturskizzen-Prinzip**
   (entfernen + gleiche Schraffur durchgehend, Dämm-Schlaufen, Texte nie abgeschnitten) sind
   seit Feature 8 umgesetzt, dazu **Dämmstoff-Schraffuren** weich/hart/hart_doppelt/
   geschlaengelt (Tabelle SKILL.md 5b). In claude.ai ist **v3** aktiv (Update:
   Plugins → Detailpruefer architektur → ⋯ → „Neue Version hochladen“ → `dist/…​.skill`).
   Zweiter claude.ai-Lauf (v2): Fragerunde ok, 4 von 4 Fehlern. v3 noch nicht getestet.
   Nach jeder Änderung an `skill/` ZIP und `.skill` neu packen.
   Überarbeitete Traufe-Befunde: `tests/befunde_blindtest_3_traufe_v2.json`.
3. **README.md** für GitHub schreiben (Was, Wie benutzen, Beispielbericht-Bilder, Grenzen,
   KI-Kennzeichnung) – Pflicht für die Abgabe.
4. ~~Repository in die Kurs-Organisation übertragen~~ erledigt (17.11.) (GitHub → Settings → Transfer) –
   macht der Nutzer selbst.
5. **Poster** (Vorlage auf Moodle) – Inhalte/Bilder aus `beispiel/` vorbereiten.
6. Optional: weitere Blindtests (Sockel, Fenster), fehlerfreies Detail für Fehlalarm-Quote.

## 6. Bekannte Probleme / offene Punkte

- **Nicht in claude.ai getestet** – bisher nur lokal in Claude Code.
- **Koordinaten von Kreisen, Badges und Korrekturelementen** werden von Hand (aus dem
  Rasterbild) geschätzt; Überlappungen müssen per Kontrollbild geprüft und nachjustiert werden.
- **Zeichnung im Bericht ist ein Rasterbild** (200 dpi); vektorgenau nur die separate
  `*_korrekturskizze.pdf`.
- Befundkarten mit Bildpaar sind hoch → teils Weißraum am Seitenende (Karten werden
  bewusst nicht geteilt). Seite 1 kann unten leer bleiben, wenn die Maßnahmenliste umbricht.
- **Quellen:** DIN 4108-2:2026-05 inhaltlich nicht geprüft; f_Rsi ≥ 0,70 nur über eine
  Sekundärquelle (Firmenseite) belegt; ZVDH-Link ist eine Übersichtsseite (Bauprofessor),
  keine Primärquelle; DIN 18516-1-Zahlenwerte bewusst weggelassen.
- **Blindtest 3 war nicht vollständig „blind“** für den Katalog: Dachregeln entstanden während
  der Prüfung. Die Erkennung bei Vertikalschnitten/Dächern ist erst einmal erprobt.
- Wiederkehrender **Fehlalarm-Typ:** kurze Querlinien in Platten (als möglicher Plattenstoß
  gedeutet) – bei geringer Aussagesicherheit eher als Hinweis einstufen.
- `tests/test_maengel.json` ist im alten Format (nur Altlast, nicht mehr benutzt).
- Nutzer-E-Mail steht in den Git-Commits (bewusst so gewählt).
- Brand- und Schallschutz werden nicht geprüft (nur Rückfrage).
