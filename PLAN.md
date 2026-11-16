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
   - **Befundliste** in vier Einstufungen (Aufbaufehler · Risiko/Klärungsbedarf ·
     Verbesserungshinweis · Nicht beurteilbar): Nr. · Fundstelle · woran erkennbar ·
     *Warum ein Fehler?* · *Mögliche Folgen (Bauschaden)* · Verbesserung · Quelle/Norm
   - **Keine bauphysikalischen Berechnungen** – qualitative Plausibilitätsprüfung
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
- Massivbau-Details
- ~~U-Wert-Berechnung~~ → verworfen (16.11.): bewusst nur qualitative Plausibilitätsprüfung

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
- [x] **Feature 2 (Mo 16.11.):** `skill/checkliste.md` (9 Rückfragen mit Annahmen) +
      Prüfkatalog Teil 1: `00_uebersicht`, `01_luftdichtheit` (LD-01…06),
      `02_feuchteschutz` (FS-01…04), `03_waermeschutz_waermebruecken` (WB-01…04)
- [x] Testprüfung nach deinem Prüf-Prompt am Testdetail (nicht blind): beide eingebauten
      Fehler gefunden
- [x] **Feature 3 (Mo 16.11.):** Prüf-Prompt eingebaut – keine Berechnungen, vier
      Einstufungen, Ausgabegliederung (SKILL.md, 00_uebersicht, Teil 1 angepasst);
      markieren.py: durchgezogen/gestrichelt/gepunktet nach Einstufung
- [x] Prüfkatalog Teil 2: `04_winddichtheit_hinterlueftung` (WH-01…04), `05_holzschutz`
      (HS-01…03), `06_konstruktion_holzrahmenbau` (KO-01…04), `07_zeichnungsqualitaet` (ZQ-01…05)
- [x] **Feature 4 (Mo 16.11.):** Prüfliste nach deinen Vorgaben überarbeitet:
      Normstand 16.11.2026 recherchiert (`pruefkatalog/quellen.md`; u. a. GEG → GModG,
      DIN 4108-7:2026-04, DIN 4108-2:2026-05, DIN 18516-1:2024-10 ohne unverifizierte
      Zahlenwerte); Einstufungen „klarer Aufbaufehler / mögliche Auffälligkeit /
      Verbesserungshinweis / aus der Datei nicht prüfbar“ + „Nachweis erforderlich“;
      Funktionen getrennt (WH Teil A/B/C); „Gilt für“ je Regel; Risiken vorsichtig;
      mehrere Lösungswege; Doppelbefunde per Verweis; neue Regeln FS-05, WH-05
- [x] **Feature 5 (Mo 16.11.):** `scripts/bericht.py` – PDF-Prüfbericht (Deckblatt mit
      Pflichthinweis und Legende, markierte Zeichnung, Befundliste nach Einstufung,
      nicht Prüfbares, Positives, Annahmen, Grundlagen, Fußzeile); Format `befunde.json`
- [x] Beispielbericht: `beispiel/pruefbericht_wandeck_mit_fehlern.pdf` (7 Seiten)
- [x] **Blindtest 2 (Mo 16.11.):** `tests/details/blindtest_2.pdf` geprüft →
      `beispiel/pruefbericht_blindtest_2.pdf` (1 klarer Aufbaufehler, 5 mögliche
      Auffälligkeiten, 2 Hinweise, 5 nicht prüfbar). Dabei Katalog ergänzt: **KO-05**
      (Unterkonstruktion von Bekleidungen, auch an Ecken) und **Wand-zu-Wand-Abgleich**
      (ZQ-01, SKILL.md Schritt 1)
- [ ] **Du:** Lösungsschlüssel zu Blindtest 2 schicken → Trefferquote auswerten
- [ ] **Du:** Prüfkatalog und Beispielberichte fachlich gegenlesen
- [ ] Skill als ZIP für claude.ai packen und dort testen (Code-Ausführung aktivieren)
- [ ] Should: Verbesserungsskizze im CAD-Look
- [ ] README.md für GitHub, Poster
- [ ] Danach: Berichts-Skript (PDF-Prüfbericht mit Mängelliste)
