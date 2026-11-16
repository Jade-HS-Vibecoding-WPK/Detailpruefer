# PLAN – Detailprüfer Architektur

> Umsetzungsplan für die Vibecoding KI-Werkstatt (Jade Hochschule, 16.–20.11.2026).
> Stand: Mo 16.11.2026 – Interview abgeschlossen, Plan zum Gegenlesen.

---

## 1. Die Idee in einem Satz

Ein **Claude-Skill**, der eine hochgeladene Detailzeichnung (PDF) im **Holzbau** prüft,
Fehler **rot in der Zeichnung markiert**, über eine **Checkliste** offene Punkte klärt und
einen **PDF-Prüfbericht** mit Mängelliste, Begründung, Folgen und Verbesserungsskizze erstellt.

## 2. Warum?

Standarddetails passen selten zu 100 % und müssen angepasst werden. Dabei entsteht
Unsicherheit: *Ist mein angepasstes Detail noch richtig?* Der Detailprüfer gibt eine
schnelle **technische Zweitmeinung**.

- **Zielgruppe:** Architekturstudierende – perspektivisch auch Planungsbüros.
- **Wichtig:** Es ist eine **Hilfestellung**, keine fachliche Prüfung und kein Nachweis.
  Die KI kann sich irren. Dieser Hinweis steht deutlich in jedem Bericht.

## 3. So funktioniert es (Ablauf für Nutzer:innen)

1. In claude.ai (oder Claude Code) den Skill „Detailprüfer Architektur“ aktivieren.
2. Detailzeichnung als **PDF** in den Chat ziehen (z. B. Export aus Archicad).
3. Claude liest Zeichnung + Legende (Wandaufbau) und erkennt die Detailart.
4. Claude stellt **Checklisten-Fragen** zu dem, was die Zeichnung nicht verrät
   (z. B. Gebäudeklasse, Nutzung, Fassadenart, Klimaregion).
5. Claude prüft das Detail anhand des **Prüfkatalogs** (Regeln mit Quellenangabe).
6. Ein Skript im Skill erzeugt den **PDF-Prüfbericht**:
   - Deckblatt mit Haftungshinweis
   - Originalzeichnung mit **roten Kreisen / Schraffuren** und nummerierten Mängeln
   - **Mängelliste:** Nr. · Prüfbereich · Befund · *Warum ist das ein Fehler?* ·
     *Mögliche Folgen (Bauschaden)* · Verbesserungsvorschlag · Quelle/Norm · Sicherheit der Einschätzung
   - **Verbesserungsskizze** je Mangel, schematisch im CAD-Look (DIN-Schraffuren, Linienstärken)
   - Offene Fragen / Annahmen

## 4. Technik (einfach erklärt)

Ein **Skill** ist ein Ordner mit Anweisungen und Werkzeugen, den Claude bei Bedarf liest.
Er läuft mit dem **Claude-Pro-Abo – ohne API-Key**.

```
detailpruefer-architektur/
├─ CLAUDE.md                ← Regeln für die Zusammenarbeit (für den Coding-Agenten)
├─ PLAN.md                  ← dieser Plan + Stand
├─ README.md                ← Erklärung für GitHub (am Ende)
├─ skill/                   ← DAS ist der eigentliche Skill (wird als ZIP hochgeladen)
│  ├─ SKILL.md              ← Hauptanweisung: Ablauf der Prüfung
│  ├─ pruefkatalog/         ← Prüfregeln je Bereich, jede Regel mit Quelle
│  ├─ checkliste.md         ← Rückfragen an Nutzer:innen
│  ├─ referenzdetails/      ← eigene, korrekte Musterdetails (selbst gezeichnet)
│  └─ scripts/              ← kleine Python-Programme: markieren, skizzieren, Bericht bauen
└─ tests/
   ├─ details/              ← Test-PDFs (korrekt + mit Fehlern)
   └─ loesung/              ← Lösungsschlüssel – NICHT Teil des Skills
```

- **Wo läuft er?** Hauptsächlich **claude.ai** (Skill als ZIP hochladen; „Code-Ausführung“
  muss in den Einstellungen aktiv sein). Zusätzlich in **Claude Code**.
- **Markierungen:** Claude schätzt die Position der Fehler auf der Zeichnung; das Skript
  zeichnet dort Kreis + Nummer. → Die Kreise sitzen **ungefähr**, nicht millimetergenau.

## 5. Fachliche Grundlage

**Maßstab sind die deutschen Regeln (DIN).** Prüfregeln werden in eigenen Worten
formuliert und mit Fundstelle versehen (Normtexte selbst sind urheberrechtlich geschützt
und werden nicht kopiert).

| Prüfbereich | Wesentliche Grundlage |
|---|---|
| Wärmeschutz & Wärmebrücken | GEG, DIN 4108-2, DIN 4108 Beiblatt 2 |
| Feuchteschutz / Diffusion / Tauwasser | DIN 4108-3 („innen dichter als außen“) |
| Luftdichtheit | DIN 4108-7 (durchgehende Ebene, verklebte Anschlüsse) |
| Winddichtheit | DIN 4108-7 |
| Hinterlüftung / Fassade | DIN 18516-1, DIN 68800-2 |
| Konstruktiver Holzschutz | DIN 68800-1/-2 |
| Konstruktion (Plausibilität) | Holzrahmenbau-Regeln: Stiele, Eckausbildung, Befestigung |
| Zeichnungsqualität | Legende ↔ Zeichnung ↔ Maßketten stimmen überein |
| Brandschutz, Schallschutz | MBO/LBO, DIN 4109 – **nur als Checklisten-Frage** (Must) |

**Quellen – Ergebnis der Prüfung von dataholz.eu (16.11.2026):**
Laut Nutzungsbedingungen sind Ausdruck/Reproduktion nur ohne kommerzielle Absicht erlaubt;
Bearbeitung, Verbreitung und **öffentliche Wiedergabe** gelten als Urheberrechtsverstoß.
Ein öffentliches GitHub-Repo ist öffentliche Wiedergabe. Daraus folgt:

- ❌ Keine Dataholz-Zeichnungen oder -PDFs in den Skill kopieren.
- ✅ Dataholz als **Nachschlage-Quelle verlinken** („vergleiche dataholz.eu, Wandknoten …“).
- ✅ Fachliche **Regeln und Kennwerte in eigenen Worten** übernehmen, mit Quellenangabe.
- ✅ **Referenzdetails selbst zeichnen** (Skript im CAD-Look) bzw. von dir gelieferte eigene Details.
- Optional: Bei info@dataholz.eu um Erlaubnis fragen (das müsstest du selbst tun).

## 6. Must · Should · Could

### M – Must (läuft am Freitag)
- Holzrahmenbau-**Außenwand**: Regelquerschnitt und **Außenecke** (Horizontalschnitt)
- PDF hochladen → Detailart + Wandaufbau aus der Legende erkennen
- Prüfkatalog für alle Bereiche aus Abschnitt 5 (Brand/Schall nur als Frage)
- Checkliste mit Rückfragen
- Rote Markierungen (Kreis + Nummer, Schraffur) in der Originalzeichnung
- PDF-Prüfbericht mit Mängelliste (Befund, Warum, Folgen, Verbesserung, Quelle)
- Deutlicher Haftungshinweis
- Test: Fehler im Testdetail werden gefunden, das korrekte Detail erzeugt keine groben Fehlalarme

### S – Should
- Verbesserungsskizze im CAD-Look je Mangel
- Weitere Holzbau-Details: **Innenecke**, **Sockel**, **Fensteranschluss**
- Eigene Referenzdetails als „so wäre es richtig“-Beispiel

### C – Could
- Dach-Wand-Anschluss, Geschossdecke
- IFC-Datei als Eingabe
- U-Wert-Berechnung aus der Legende
- Massivbau-Details

## 7. Etappen (an die Kurstage gekoppelt)

| Tag | Etappe | Ergebnis |
|---|---|---|
| **Mo 16.11.** | Idee & Plan | PLAN.md + CLAUDE.md stehen ✅ (nach deiner Freigabe) |
| **Di 17.11.** | Grundgerüst & Aussehen | `SKILL.md` + Markier-Skript: Testdetail wird rot markiert; Berichtslayout steht |
| **Mi 18.11.** | Daten | Prüfkatalog mit Quellen füllen, Checkliste, erster vollständiger Testlauf |
| **Do 19.11.** | Fertig & veröffentlichen | Skill als ZIP, Test in claude.ai, Upload auf GitHub. **12 Uhr Freeze**, dann Poster |
| **Fr 20.11.** | Polieren & präsentieren | README, Poster, Präsentation (Abgabe 16 Uhr) |

Rhythmus pro Sitzung: **neue Sitzung → ein Feature → testen & speichern → Stand hier eintragen.**

## 8. So testen wir

- `tests/details/wandeck_korrekt.pdf` – korrektes Außeneck-Detail (Holzrahmenbau, 1:5)
- `tests/details/wandeck_mit_fehlern.pdf` – gleiches Detail mit eingebauten Fehlern
- Lösungsschlüssel liegt getrennt in `tests/loesung/` und ist **nicht** Teil des Skills.
  Er wird erst **nach** einem Testlauf geöffnet, um das Ergebnis zu bewerten.
- **Erfolg =** alle eingebauten Fehler gefunden und an der richtigen Stelle markiert,
  beim korrekten Detail keine groben Fehlalarme.

## 9. Risiken & offene Punkte

- **KI-Irrtum:** Die KI kann Fehler übersehen oder erfinden → Haftungshinweis, Quellen
  je Regel, „Sicherheit der Einschätzung“ in der Mängelliste, deine fachliche Durchsicht.
- **Markierungsgenauigkeit:** Kreise sitzen ungefähr. Für Must ausreichend.
- **Auf deinem Rechner fehlen noch Python und Git.** Python brauchen wir zum Testen der
  Skripte hier in Claude Code, Git für den Upload auf GitHub. (In claude.ai ist Python
  schon eingebaut.) → Installation am Dienstag zu Beginn, Schritt für Schritt.
- **Nutzungslimit Pro-Abo:** Bildprüfungen verbrauchen viel → kurze Sitzungen.
- **Lizenzen:** siehe Abschnitt 5.

## 10. Stand & nächste Schritte

- [x] Interview geführt
- [x] Projektordner angelegt, Testdetails abgelegt, Lösungsschlüssel getrennt abgelegt
- [x] Nutzungsbedingungen dataholz.eu geprüft
- [x] Python 3.12 + Git 2.56 installiert, PDF-Bausteine (pypdf, reportlab, pypdfium2, pillow)
- [x] **Feature 1 (Mo 16.11.):** `skill/SKILL.md`-Grundgerüst (Ablauf, Pflichthinweis, Format `maengel.json`)
- [x] `skill/scripts/raster.py` – Zeichnung mit Prozent-Raster als Bild (auch Zoom-Ausschnitt)
- [x] `skill/scripts/markieren.py` – rote Kreise, Nummern, Schraffur, gestrichelt = unsicher,
      Nummernposition wählbar; Original bleibt Vektor-PDF
- [x] Markier-Test am Testdetail erfolgreich (`tests/test_maengel.json` → `tests/ausgabe/`)
- [ ] **Du:** PLAN.md und CLAUDE.md lesen und korrigieren
- [x] Git eingerichtet, erster Speicherstand hochgeladen: https://github.com/Ozan44336/Detailpr-fer
- [ ] Vor der Abgabe: Repository in die Kurs-Organisation verschieben (Settings → Transfer) oder dort neu anlegen
- [ ] Nächstes Feature: `checkliste.md` + Prüfkatalog Teil 1 (Luftdichtheit, Feuchte, Wärmebrücken)
- [ ] Danach: Berichts-Skript (PDF-Prüfbericht mit Mängelliste)
