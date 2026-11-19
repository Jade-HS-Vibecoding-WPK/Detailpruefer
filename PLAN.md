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
- [x] Repository in der Kurs-Organisation: https://github.com/Jade-HS-Vibecoding-WPK/Detailpruefer
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
- [x] **Feature 6 (Di 17.11.):** Bericht nach Feedback neu aufgebaut – Kurzfazit mit
      Befundliste und Seitenverweisen, Maßnahmenliste zum Abhaken (Priorität automatisch),
      markierte Zeichnung (Rot/Orange/Blau, Badges mit Führungslinie, „Wand A/B“),
      Befundkarten mit Zeichnungsausschnitt und Aussagesicherheit, offene Fragen im Bericht,
      Anhang mit Methode, Annahmen, Code-Legende und **Quellenverzeichnis mit verlinkten
      Fußnoten** (`pruefkatalog/quellen.json`, 23 Quellen mit Links). Präfixe B/S/F,
      Schichten außen → innen. Disclaimer nur Seite 1 + Fußzeile.
- [x] WH-04 korrigiert: Gehrung an der Außenecke ist laut BauNetz Wissen empfohlen (kein Befund)
- [x] Checkliste: Projektname (C0); Berichtskopf mit leerem Feld „Fachlich geprüft von“
- [x] **Blindtest 2 ausgewertet (Di 17.11.):** 4 von 4 eingebauten Fehlern gefunden
      (B1 Latten Ecke, B2 OSB Wand A, B3 Legende, B5 Installationslatte); 1 Fehlalarm
      (B4, Aussagesicherheit „gering“). Details: `tests/loesung/AUSWERTUNG_blindtest_2.md`
- [x] **Feature 7 (Di 17.11.):** Korrekturskizze – fehlende Teile werden grün in die Zeichnung
      eingezeichnet (`scripts/skizze.py`, Feld `korrektur`); im Bericht eigene Seite
      „Korrekturskizze“ und je Befundkarte Ist/Korrektur nebeneinander; zusätzlich
      `*_korrekturskizze.pdf` als Vektor-PDF. Berichtskopf-Tabelle auf Seite 1 entfernt.
- [x] **Blindtest 3 – Traufe (Di 17.11.):** `beispiel/pruefbericht_blindtest_3_traufe.pdf`
      (2 klare Aufbaufehler, 2 mögliche Auffälligkeiten, 1 Hinweis, 3 nicht prüfbar) mit
      Korrekturskizze. Katalog ergänzt: WH-06/WH-07 (geneigtes Dach), KO-06 (Auflager
      tragender Hölzer), Quelle ZVDH-Fachregeln; Korrekturelement „daemmung“
- [x] **Blindtest 3 ausgewertet (Di 17.11.):** 3 von 4 eingebauten Fehlern gefunden
      (Dämmung, Fußpfette, Winkelangabe); **übersehen:** OSB der Wand läuft über den Wandkopf
      durch die Dachdämmung. Keine Fehlalarme. → neue Regel **KO-07** (Schichten enden am
      Anschluss) und **vierter Abgleich** „jede Schicht bis zu ihrem Ende verfolgen“
      (SKILL.md, 00_uebersicht). Details: `tests/loesung/AUSWERTUNG_blindtest_3.md`
- [x] Skill als ZIP gepackt: `dist/detailpruefer-architektur.zip` (nicht auf GitHub)
- [x] **Skill in claude.ai getestet (Di 17.11.):** Upload über Plugins → Hinzufügen → Plugin
      hochladen; alle Skripte laufen, Bericht + Korrekturskizze korrekt. Traufe: OSB (KO-07),
      Fußpfette, Winkel gefunden; Dämmlücke nur als Legendenwiderspruch. Details in
      `tests/loesung/AUSWERTUNG_blindtest_3.md`
- [x] **Feature 8 (Di 17.11.): Korrekturskizze nach Musterlösung + Nachbesserungen**
      - Festes Prinzip (SKILL.md 5b, CLAUDE.md): Skizze zeigt den korrigierten Zustand –
        falsch Gezeichnetes `entfernen` (weiß), Schichten mit **derselben Schraffur** und
        **durchgehend** fortführen; keine Grenzstriche
      - `daemmung` zeichnet jetzt Dämm-Schlaufen in Schichtdicke und -richtung (`band`),
        `platte` mit Schraffur `striche`/`zickzack`/`punkte`/`diagonal`
      - Hinweistexte werden umbrochen und auf dem Blatt gehalten; Bericht schneidet die
        Skizze so zu, dass alle Texte sichtbar sind; Befundkarten ohne abgeschnittene Texte
      - Überschrift „Befunde im Detail“ bleibt bei der ersten Karte
      - Fragerunde ist Pflicht (anhalten und Antwort abwarten)
      - WB-01: Luftschicht/Hohlraum im Dämmfeld laut Legende = Befund
      - Test: `tests/befunde_blindtest_3_traufe_v2.json` (mit OSB-Befund B3) →
        `tests/ausgabe/bt3v2_bericht.pdf`; Blindtest 2 und Wandecke laufen weiter fehlerfrei
- [x] **Dämmstoff-Schraffuren unterschieden (Di 17.11.):** `daemmung` mit `art` = `weich`
      (Schlaufen, Faserdämmstoffe), `hart` (Zickzack, Dämmplatten), `hart_doppelt` (Rauten),
      `geschlaengelt` (Wellenlinie, dünne weiche Lagen/Trittschall); Zuordnungstabelle und
      Entscheidungsreihenfolge in SKILL.md 5b (Vorrang: Darstellung in der Zeichnung);
      ZQ-05 prüft, ob die Dämmschraffur zur Dämmstoffart passt. Musterblatt:
      `tests/ausgabe/daemmarten_muster.png`
- [x] **claude.ai, zweiter Lauf (v2):** Fragerunde kommt, **4 von 4** Fehlern gefunden,
      Hinweistexte vollständig. Schwäche: Dämmung über dem Wandkopf nicht bis zum Füllholz
      fortgeführt → KO-07 ergänzt, als **v3** eingespielt
- [ ] v3 in claude.ai testen (am besten mit einem neuen Blindtest-Detail)
- [x] **Blindtest 4 – First in claude.ai (Nutzer, 17.11.):** Fehler nur teilweise erkannt;
      Firstabdeckung nur als Auffälligkeit (Rückfrage „geplant?“ hat sie entschärft),
      Firstpfette nicht erkannt, Korrekturskizze ohne Firstziegel/Firstlatte/Pfette
      (Werkzeuge fehlen). Musterlösung: `Firstmuster 2.pdf`, Testdetail: `first mit fehler.pdf`

### Entscheidungen aus dem Interview (17.11.2026)
- **Mehrere richtige Lösungen:** Der Skill prüft gegen allgemeine, belegte Regeln und
  erkennt verschiedene korrekte Ausführungen an (keine Bindung an eine Musterlösung). Bei
  Mängeln zeichnet er **die am besten geeignete Verbesserung**; Alternativen im Text.
  Musterlösungen dienen nur zum Bewerten – keine detailbezogenen Koordinaten/Lösungen in
  den Skill.
- **Korrekturskizze:** muss praktisch jedes Bauteil zeichnen können, damit ein vollständiges
  technisches Detail entsteht – Firstziegel/-pfanne, Firstlatte + Halter, Pfetten/Sparren/
  Latten auch schräg in Dachneigung, Folien/Bahnen mit Anschlüssen.
- **Fragerunde:** nur konstruktiv relevante Fragen (ohne die ein Befund nicht beurteilbar
  ist); kein Projektname, keine sd-Werte; keine Fragen „ist X geplant, aber nicht gezeichnet?“.
- **Fehlende Bauteile:** Fehlt ein funktional notwendiges Bauteil (Regensicherheit,
  Lastabtrag, Dichtheit), ist das ein **klarer Aufbaufehler** – auch wenn es „geplant“ ist.
- **Tragsystem:** Skill erkennt Pfetten- oder Sparrendach; ist am First kein Lastabtrag
  erkennbar → Befund; Korrektur nach dem passendsten System.
- **Umfang bis Freeze (Do 19.11., 12 Uhr):** Wand, Traufe, First, Sockel, Ortgang.
- **Quellen:** freie Web-Recherche, nur seriöse, technisch richtige Quellen (Fachregeln,
  Verbände, Hersteller-Verlegeanleitungen, BauNetz Wissen), jede Regel mit Link.

- [x] **Feature 9 (Di 17.11.): Umsetzung der Interview-Entscheidungen**
      - Checkliste neu: nur konstruktiv relevante Fragen (K1–K5), kein Projektname, keine
        sd-Werte, nie „geplant?“; ohne relevante Frage direkt prüfen
      - Grundsatz 5 neu: fehlendes funktional notwendiges Bauteil = klarer Aufbaufehler;
        Grundsatz 7: mehrere richtige Ausführungen anerkennen, beste Korrektur zeichnen;
        Tragsystem erkennen (SKILL.md Schritt 1); Traufe-Koordinaten-Beispiel entfernt
      - Neue Zeichenwerkzeuge: Maße in cm über den Maßstab; `holz` in jeder Lage/Neigung
        (quer/längs), `lattenreihe`, `firstlatte` (mit Halter), `firstziegel` (mit
        Lüftungselement), `profil` (freie Form, auch mit Dicke), `bahn` (luftdicht, winddicht,
        Abdichtung, Unterdeckbahn, Lüftungsband)
      - Bauteil-Datenbank: `08_dach_steildach.md` (DA-01 Tragsystem, DA-02 Firstabdeckung,
        DA-03 Belüftung/Unterdeckung First, DA-04 Traufe, DA-05 Ortgang, DA-06 Lattung) und
        `09_wand_sockel.md` (SO-01 Wand-Schichtenfolge, SO-02 Spritzwasserabstand, SO-03
        Schwelle/Feuchteschutz); 7 neue Quellen (BauNetz Wissen, Nelskamp-Verlegeanleitung)
      - Test First lokal: `tests/befunde_blindtest_4_first.json` → `tests/ausgabe/bt4_bericht.pdf`
        (Firstziegel, Firstlatte, Pfette, Dampfbremsen-Anschluss gezeichnet); alte Berichte
        laufen weiter; in claude.ai als neue Version eingespielt
- [ ] **Du:** neue Blindtests (Ortgang, Sockel, ggf. anderer First) in claude.ai durchspielen
- [ ] **Du:** Winkel Traufe klären – Musterlösung 35°, gezeichnet ca. 25°
- [ ] **Du:** Prüfkatalog und Beispielberichte fachlich gegenlesen
- [ ] README.md für GitHub, Poster
- [x] ~~Verbesserungsskizze im CAD-Look~~ und ~~Berichts-Skript~~ → erledigt durch Feature 5 und 7
- [x] **Nachbesserung First (17.11.):** Dämmung im Blindtest halbiert gezeichnet, Korrektur
      zeigte sie nicht vollständig → WB-01 und SKILL.md: **Schraffur-Abgleich** (jede
      Dämmschraffur muss die ganze Schichtdicke füllen); Korrekturskizze zeichnet das ganze
      Dämmfeld in voller Dicke auf beiden Dachseiten. Test: `tests/ausgabe/bt4_bericht.pdf`
- [x] **Blindtest 5 – Sockel in claude.ai (v5, 17.11.):** keine Fragerunde (richtig), Schwelle
      (klarer Aufbaufehler) und Randdämmstreifen (geschlängelt eingezeichnet) gefunden;
      XPS 10 statt 16 cm nur als Höhenwiderspruch erkannt; Sauberkeitsschicht und Fußleiste
      übersehen. Details: `tests/loesung/AUSWERTUNG_blindtest_5_sockel.md`
- [x] Nachbesserung danach: Höhen-Abgleich bis zur verursachenden Schicht (SKILL.md),
      neue Regel **SO-04 Bodenaufbau** (Sauberkeitsschicht, Randdämmstreifen, Fußleiste,
      Höhen), Textoption `"farbe": "original"` für verdeckte Beschriftungen/Koten
- [x] Nachbesserung Sockel in claude.ai eingespielt (v6, 18.11.)
- [x] **Feature 10 (Mi 18.11.): Übliche Bauteildicken + Bauteil-Check**
      - Rückfragen geklärt: Richtwerte für alle Bauteile; prüfen + anzeigen; Bauteil-Check nur
        intern; Werte aus offiziellen, nachweisbaren Quellen (Standardaufbauten), nur Empfehlung
      - Neu `pruefkatalog/10_bauteildicken.md` (RW-01) mit Richtwerten aus dataholz.eu
        (awrhhi01a/04a, sdrhzi01a/03a, gdmnxa02a), Bauprofessor, BauNetz Wissen, Nelskamp;
        wo keine belegbare Quelle: „kein Richtwert – nach Nachweis“ (Bodenplatte, Pfetten,
        Perimeter- und Bodendämmung, Holzfaser-Außendämmung)
      - SKILL.md: interner **Bauteil-Check** (jede Schicht/jedes Bauteil + Pflichtbauteile:
        vorhanden? Dicke gezeichnet/Legende/üblich? Schraffur vollständig?) vor der Prüfung
      - Bericht: Schichtenaufbau mit Spalte „üblich¹“ (Feld `ueblich`) und Hinweis
        „Praxis-Richtwert, kein Grenzwert“; 6 neue Quellen
      - in claude.ai als **v6** eingespielt
- [x] **Blindtest 6 – Ortgang in claude.ai (18.11.):** lief im **alten Sockel-Chat** → Skill-Stand
      v5, die Bauteildicken (v6) waren nicht aktiv. Treffer: Rähm, Hinterlüftung oben zu,
      Fugenabdichtung, vertauschte Hinweislinien; Dämmung/Sparren 15 statt 24 cm nur teilweise;
      obere Fassadenlatte und Installationslatte übersehen; B3 (Holzplatte des Überstands) =
      Fehlalarm. Nachfrage „Reicht 15 cm?“ → claude.ai hat einen U-Wert überschlagen (Regelverstoß).
      Details: `tests/loesung/AUSWERTUNG_blindtest_6_ortgang.md`
- [x] **Feature 11 (Mi 18.11.): Baustoff-Empfehlung + Regeln für Nachfragen**
      - Rückfragen geklärt: Empfehlung für **alle Schichten**; Detail funktioniert → Anmerkung im
        Schichtenaufbau, funktioniert technisch nicht → **eigener Abschnitt**; 15 statt 24 cm
        bleibt **mögliche Auffälligkeit**; B3 = Fehlalarm
      - Neu `pruefkatalog/11_baustoffe.md` (BS-01): geeignete Baustoffe je Einbaulage
        (Sparrenfeld, Gefach, Installationsebene, Unterdeckung, WDVS, Trittschall, Perimeter,
        Platten, Bahnen) aus dataholz-Varianten und BauNetz Wissen; 4 neue Quellen
        (DIN 4108-10:2021-11, BauNetz Anwendungsbereiche, Holzfaserdämmungen, Perimeterdämmung)
      - SKILL.md: Bauteil-Check Punkt 5 „Material angegeben?“; Schritt 8 **Nachfragen nach dem
        Bericht** – keine U-/λ-Werte, stattdessen üblicher Bereich + Baustoffe + Nachweis
      - DA-05 Ortgang: Rähm, Abluft der Hinterlüftung mit Insektenschutz, oberste Fassadenlatte,
        Dämmung in voller Sparrenhöhe; Dachüberstandsplatte als anerkannte Variante (auch KO-07)
      - Bericht: Feld `empfehlung` je Schicht (grün „Empfehlung:“), Abschnitt
        „Baustoff-Empfehlungen“ (`baustoff_empfehlungen`); Test `tests/ausgabe/bs_test_bericht.pdf`
      - ZIP/.skill neu gepackt und in claude.ai als **v7** eingespielt (18.11.)
- [x] **Blindtest 6, zweiter Lauf (v7, neuer Chat):** 6 von 7 Fehlern gefunden (vorher 4);
      Fehlalarme: Konterlatte 3 cm, DWD-Schraffur; Rähm nur 24/6, Schreibfehler nicht korrigiert,
      Positiv-Liste widersprüchlich → siehe `AUSWERTUNG_blindtest_6_ortgang.md`
- [x] **Nachbesserung Ortgang (18.11.):** Konterlatte mind. 30 mm bei Sparren < 8 m (Nelskamp),
      Rähm = Schwellenquerschnitt bzw. 10 × Wanddicke (Praxisempfehlung), Platte bleibt auf dem
      Rähm, Installationslatte am Rand, Windsog = Hinweis, Schraffur bei eindeutiger Beschriftung
      kein Befund, neu **ZQ-06 Rechtschreibung** (Korrektur in der Skizze), Positiv-Abgleich;
      neue Quelle BauNetz Tafelbau/Rahmenbau. Zusammen mit `verschieben` als **v8** eingespielt (18.11.)
- [x] **Dämmung in richtiger Dicke + Innenaufbau verschieben (18.11.):** neues Zeichenwerkzeug
      `verschieben` (Bereich der Originalzeichnung als Vektor versetzt, alter/neuer Ort weiß
      abgedeckt), `linie`/`text` mit `"farbe": "original"` (schwarz, Text auch gedreht
      `winkel`); SKILL.md 5b Punkt 7 (Ablauf: Zieldicke → verschieben → Dämmung/Hölzer neu →
      Linien und Maßzahlen schließen → Kontrolle), RW-01 Punkt 4 (Zieldicke = Legende bzw.
      Untergrenze üblich). Test Ortgang 15 → 24 cm: `tests/befunde_test_verschieben_ortgang.json`
      → `tests/ausgabe/verschieben_bericht.pdf`
- [x] **Blindtest 4 – First, zweiter Lauf (v8):** Firstabdeckung, Dämmung, EPDM, Dampfbremse,
      Schreibfehler richtig; Firstpfette als Befund erkannt, aber Sparrendach geraten und Pfette
      als Sechseck in der Dämmebene gezeichnet → `tests/loesung/AUSWERTUNG_blindtest_4_first_v8.md`
- [x] **Feature 12 (Mi 18.11.): Detail-Datenbank + exakte Geometrie**
      - Rückfragen geklärt: alle Bereiche (Steildach, Wand, Fenster/Türen, Flach-/Pultdach);
        Quellen Fachverbände/Institute + BauNetz Wissen; unklare Konstruktion → **immer fragen**;
        Katalog **und** eigene Referenzskizzen
      - Neu `pruefkatalog/12_detailtypen.md` (DT-00 Zuordnung, DT-D1…D7, DT-W1…W3, DT-F1,
        DT-FD0…FD2, DT-P1) mit Erkennen, Bauteilen in ihrer Lage, Varianten, Zeichenanleitung
      - 6 neue Quellen: holzbau handbuch Holzschutz (2023) und Flachdächer (2019) des
        Informationsdienst Holz, BauNetz belüftete Dächer, Luftdichtheit, Anschlussfugen, RAL-Leitfaden
      - Eigene Referenzskizzen `skill/referenz/*.png` (First Pfetten-/Sparrendach, Traufe, Ortgang,
        Sockel, Fenster unten, Attika), erzeugt mit `scripts/referenz.py`
      - Neues Werkzeug `scripts/linien.py` (Vektorlinien, Schnittpunkte, Parallelen)
      - Checkliste K0 (Konstruktion nicht zuordenbar → Pflichtfrage); SKILL.md Schritt 1 + 5b 3a
      - Test: Firstpfette lokal richtig gezeichnet → `tests/ausgabe/firstpfette_test.pdf`
- [x] Feature 12 gespeichert (`e86ded6`) und in claude.ai als **v9** eingespielt (18.11.)
- [x] **Blindtest 4 – First, dritter Lauf (v9):** Pfette wieder nicht gezeichnet – Schrauben als
      Sparrendach-Firstverbindung gedeutet, keine Rückfrage K0; Maß „21,5“ ins Leere nicht gelesen
- [x] **Nachbesserung First (18.11.):** Spuren fehlender Bauteile lesen (Maße/Schrauben ins Leere),
      Sparrendach nur bei gezeichneter + beschrifteter Firstverbindung, sonst K0; Pfettenoberkante
      zuerst nach Maß der Zeichnung; Bauteil-Check Punkt 7; Referenzskizze mit Schrauben;
      lokaler Test deckt sich mit der Musterlösung – gespeichert `0609cc8`, in claude.ai als **v10**
- [ ] **Du:** First + Ortgang mit der neuen Version in **neuen** Chats testen
- [x] **Reproduzierbarkeit (v11, 18.11.):** `scripts/fakten.py` (Prüfsumme, Legende, Maße,
      Winkel, Texte exakt aus der PDF), Datei/Prüfsumme/Skill-Version auf Seite 1, Anhang A3
      Prüfprotokoll, Abschnitt „Gleiches Detail → gleiches Ergebnis“, KO-05-Entscheidungsregel
      (Eck-Latte); in claude.ai als **v11** eingespielt
- [x] **Blindtest 5 – Sockel mit v11 (claude.ai, 19.11.):** 4 von 5 Fehlern; **Sauberkeitsschicht
      unter der Sohle übersehen** (Beschriftung zeigt aufs Fundament) und sogar als positiv
      gewertet → `tests/loesung/AUSWERTUNG_blindtest_5_v11.md`
- [x] **Feature 13 (Do 19.11.): Schicht über alle Abschnitte verfolgen (v12)**
      - Rückfragen geklärt: Sauberkeitsschicht fehlt (ganz oder teilweise) = **klarer
        Aufbaufehler**; Quelle recherchiert (keine gesicherte Normfundstelle gefunden →
        Bauprofessor + Praxisempfehlung)
      - Neue allgemeine Regel **KO-08** (jede Schicht in allen Abschnitten; Protokoll mit
        Abschnitten); SKILL.md Bauteil-Check Punkt 8 (Abschnitts-Check) und 9 (Unterkanten-/
        Rand-Check), Positiv erst nach Abschnitts-Check; SO-04, ZQ-04, DT-W1, `00_uebersicht`
      - `platte` mit Schraffur `kreuz` (Magerbeton/Sauberkeitsschicht)
      - Lokaler Test: `tests/befunde_test_sauberkeitsschicht.json` → `tests/ausgabe/sks_test_bericht.pdf`
        (Lücke erkannt, Korrektur wie Musterlösung); alte Berichte laufen weiter
      - `skill/VERSION` → 12, ZIP/.skill gepackt; in claude.ai als **v12** eingespielt (19.11.)
- [ ] **Du:** Sockel mit v12 in einem **neuen** Chat prüfen
- [x] Speicherstand v11 + v12 (`42954cb`, 19.11.)
- [x] **README.md** geschrieben (Was, Beispielbilder in `docs/`, Bericht, Einstufungen, Prüfbereiche,
      Benutzung claude.ai/Claude Code, Grenzen, Blindtests, Projektaufbau, KI-Kennzeichnung)
- [x] README gegengelesen (Traufe → Gebäudeecke als Beispiel, „Warum?“ neu) und gespeichert (19.11.)
- [ ] Poster
- [x] **Feature 14 (Do 19.11.): Zusatzhölzer nach Funktion (v13)** – Wandecke v12: Eckstiel erkannt, aber
      an falscher Stelle/über volle Dämmdicke gezeichnet. Nutzer bestätigt Prinzip; neu **KO-09**, SKILL.md 3b,
      KO-02/DT-W2, Referenzskizze `ecke_aussen.png`; lokaler Test richtig; gespeichert und in claude.ai als **v13** eingespielt (19.11.)
- [ ] **Du:** v13 in claude.ai testen (Wandecke + Sockel, neue Chats)
