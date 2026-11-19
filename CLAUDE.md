# Detailprüfer Architektur

## Ziel
Ein Claude-Skill, der Holzbau-Detailzeichnungen (PDF) qualitativ nach deutschen Regeln prüft,
Befunde farbig in der Zeichnung markiert, über eine Checkliste Rückfragen stellt, Korrekturen
grün einzeichnet und einen PDF-Prüfbericht mit Befundliste, Maßnahmenliste und Quellen erzeugt.
Zu Beginn jeder Sitzung lesen: `HANDOFF.md` (Übergabe), dann `PLAN.md` (Plan und Stand).

## Über mich (Nutzer)
- Architekturstudent, 5. Semester, **keine Programmierkenntnisse**.
- Fachlich (Baukonstruktion, Bauphysik) bin ich der Experte – die KI baut, ich entscheide.

## Regeln für die Zusammenarbeit
- Antworte auf **Deutsch** und erkläre **jeden Schritt einfach**, ohne Fachchinesisch aus der Programmierung.
- **Ein Feature pro Sitzung.** Am Ende den Stand in `PLAN.md` (Abschnitt 10) eintragen.
- Vor größeren Änderungen kurz sagen, was du vorhast.
- Nur in diesem Projektordner arbeiten.
- Keine API-Keys, Passwörter oder persönlichen Daten in Dateien oder auf GitHub.
- Keine Büro- oder Kundendaten verwenden.
- **Speicherstand (Commit + Push) nur, wenn der Nutzer es ausdrücklich sagt.**
  Commit-Nachricht auf Deutsch, mit kurzer Aufzählung der Änderungen.
- Nach jedem Arbeitsschritt **Schritt für Schritt erklären**, was gemacht wurde.
- Vor einer neuen Sitzung bzw. wenn der Kontext voll wird: `HANDOFF.md` aktualisieren.
- Rückfragen an den Nutzer gesammelt in **einer** Runde stellen (Fragedialog mit Antwortoptionen).
- **Erst fragen, dann umsetzen:** Gibt es offene Fragen zu einer Aufgabe, diese vor Beginn mit
  dem Nutzer klären (bei größeren Vorhaben kurz interviewen) – nicht mit Annahmen loslegen.
- Bei jeder neuen Fassung, die in claude.ai eingespielt wird, `skill/VERSION` hochzählen
  (die Version steht im Bericht).
- Nach jeder Änderung an `skill/`: `dist/detailpruefer-architektur.zip` und `.skill` neu packen.
  In claude.ai einspielen (Plugins → ⋯ → „Neue Version hochladen“) nur auf Wunsch des Nutzers;
  danach die aktive Version (v…) in `HANDOFF.md` vermerken.

## Fachliche Regeln
- **Maßstab sind deutsche Normen und Gesetze** (DIN 4108, DIN 68800, DIN 4109, GModG –
  vormals GEG –, MBO/LBO). Normausgaben und Status: `skill/pruefkatalog/quellen.md`
  (Stand 16.11.2026). Keine Norminhalte oder Grenzwerte ergänzen, die dort nicht verifiziert sind.
- **Faustregeln/typische Bauweisen** als „(Praxisempfehlung)“ kennzeichnen – keine Normpflicht.
- **Funktionen trennen:** Luftdichtheit (LD) · Dampfbremse (FS) · Winddichtheit,
  Hinterlüftung, Schlagregenschutz (WH A/B/C). Keine Doppelbefunde – verweisen.
- **Risiken vorsichtig formulieren** („kann … begünstigen“), nie als automatische Folge.
- Jede Prüfregel im Skill hat eine **Quelle/Fundstelle**. Keine Regel ohne Quelle.
- Normtexte und fremde Zeichnungen (z. B. dataholz.eu) **nicht kopieren** – Regeln in
  eigenen Worten, fremde Quellen nur verlinken. Referenzdetails selbst zeichnen.
- **Qualitative Plausibilitätsprüfung – keine Berechnungen** (keine sd-, R-, U-Werte, kein
  f_Rsi, kein Tauwasser, keine Tragfähigkeit/Schraubenbemessung) → sonst „Nachweis erforderlich“.
  Keine fehlenden Werte schätzen oder erfinden.
- Einstufungen: **klarer Aufbaufehler** (nur wenn eindeutig) · **mögliche Auffälligkeit** ·
  **Verbesserungshinweis** · **aus der Datei nicht prüfbar**; Zusatz „Nachweis erforderlich“.
  **Fehlt ein funktional notwendiges Bauteil** (Regensicherheit, Lastabtrag, Dichtheit,
  Dämmung, Belüftung), ist das ein **klarer Aufbaufehler** – auch wenn es „geplant“ ist.
  Fehlende **Angaben** (Material, Maß, Produkt) bleiben Hinweis bzw. „nicht prüfbar“.
- **Mehrere richtige Ausführungen anerkennen:** Der Skill prüft gegen allgemeine, belegte
  Regeln, nicht gegen eine Musterlösung. Musterlösungen dienen nur zum Bewerten; keine
  detailbezogenen Koordinaten oder Lösungen in den Skill übernehmen. Als Verbesserung die
  am besten geeignete Lösung zeichnen, Alternativen im Text nennen.
- **Tragsystem erkennen** (Pfetten-/Sparrendach usw.) und danach prüfen.
- **Rückfragen nur konstruktiv relevant** (kein Projektname, keine sd-Werte, nie „geplant?“).
- **Interner Bauteil-Check vor jeder Prüfung:** jede Schicht und jedes Bauteil der Zeichnung
  plus alle Pflichtbauteile der Detailart (Kataloge `08_…`/`09_…`) einzeln abhaken –
  vorhanden? Dicke gezeichnet/Legende/Maßkette/Höhenkoten? üblicher Bereich? Schraffur über
  die ganze Schichtdicke? Erscheint nicht als eigene Tabelle im Bericht.
- **Höhen-Abgleich bis zur Schicht:** Widersprechen sich Koten, Maßketten und Schichtdicken,
  die verursachende Schicht benennen und in der Korrekturskizze in richtiger Dicke zeichnen.
- **Beschriftung ≠ vollständiger Verlauf:** Eine Hinweislinie belegt eine Schicht nur an ihrer
  Spitze. Jede Schicht über **alle Abschnitte** verfolgen, in denen sie liegen muss (z. B.
  Sauberkeitsschicht unter Fundament **und** ganzer Bodenplatte; Abdichtung unter Wand, in der
  Fläche und an der Aufkantung). Fehlt sie in einem Abschnitt, ist das ein Befund – auch wenn
  sie anderswo gezeichnet und beschriftet ist. „Positiv“ erst nach diesem Abschnitts-Check.
- **Gleiches Detail → gleiches Ergebnis:** immer zuerst `scripts/fakten.py`; Legende, Maße,
  Winkel und Texte nur aus `fakten.json`; Prüfsumme in `detail.pruefsumme`; alle Regeln in
  fester Reihenfolge ins `pruefprotokoll`; Einstufung wörtlich nach Regeltext (im Zweifel die
  vorsichtigere); vor jedem klaren Aufbaufehler Gegenbeweis suchen. Berichte nur vergleichen,
  wenn Datei-Prüfsumme **und** Skill-Version übereinstimmen.
- **Fehlerklassen statt Einzelfälle beheben:** Wird ein Fehler übersehen, die allgemeine
  Ursache in Katalog/SKILL.md verankern (gilt für alle Details), nie die Lösung eines
  einzelnen Details (keine detailbezogenen Koordinaten) – und am Testdetail nachprüfen.
- **Übliche Bauteildicken** (`skill/pruefkatalog/10_bauteildicken.md`) nur aus offiziellen,
  nachweisbaren Quellen (z. B. dataholz-Standardaufbauten) – als **Empfehlung**, kein
  Grenzwert; Abweichung → mögliche Auffälligkeit; im Schichtenaufbau Feld `ueblich`. Ohne
  belegbare Quelle: „kein Richtwert – nach Nachweis“.
- **Foren sind keine Quelle** (auch nicht als Beleg für Zahlen); widersprüchliche oder
  ungeprüfte Zahlen weglassen.
- Keine Pauschalaussagen „sicher/normgerecht“. Jeder Befund: woran in der Zeichnung erkennbar.
- Jeder Prüfbericht enthält den Hinweis: *Hilfestellung – ersetzt keine fachliche Prüfung
  und keinen Nachweis. Die KI kann sich irren; Ergebnisse sind zu überprüfen.*
- **Neue Quellen nur nach Web-Recherche** mit funktionierendem Link in `quellen.json`
  aufnehmen (Ausgabe/Stand angeben). Widerspricht eine Quelle einer bestehenden Regel,
  die Regel korrigieren (Beispiel: Gehrung an Holzfassaden-Außenecken ist empfohlen).
- **Fehlt für eine Bauteilart eine Regel** (z. B. Dach, Sockel, Fenster), zuerst den
  Prüfkatalog mit Quelle ergänzen, dann prüfen – und das im Bericht/der Antwort offenlegen.
- Ablauf jeder Prüfung: Zeichnung erfassen (Raster, Zooms, Texte mit Positionen, Tragsystem)
  → Bauteil-Check → Fragerunde (nur falls konstruktiv relevante Fragen) → alle Regeln →
  `befunde.json` → markieren → Korrekturskizze → Bericht → **jede Berichtsseite als Bild
  kontrollieren** (Überlappungen, Umbrüche, leere Seiten, abgeschnittene Texte).

## Testen
- Testzeichnungen: `tests/details/`
- `tests/loesung/` enthält den Lösungsschlüssel. **Nie in den Skill übernehmen** und erst
  **nach** einem Testlauf öffnen, um das Ergebnis zu bewerten.
- Blindtests: Details liefert der Nutzer (nie selbst ausdenken). Nach der Musterlösung eine
  Auswertung `tests/loesung/AUSWERTUNG_<name>.md` schreiben (Treffer, Fehlalarme, Lehren).
- Befundlisten der Tests: `tests/befunde_<name>.json`; Berichte nach `beispiel/`.

## Gestaltung
- Schlicht und verständlich; der Fokus liegt auf der **Richtigkeit** der Prüfung.
- Markierungen: Kreis ohne Füllung + Badge „B1…“ mit Führungslinie neben der Zeichnung.
  **Rot** durchgezogen = klarer Aufbaufehler · **Orange** gestrichelt = mögliche Auffälligkeit ·
  **Blau** gepunktet = Verbesserungshinweis. Rot nur für klare Aufbaufehler.
- **Korrekturskizze (grün):** Was fehlt oder falsch ist, wird immer auch eingezeichnet
  (Latten, Konterlatten, Stiele, Platten mit Schraffur, Abklebungen, korrigierte Werte),
  damit die Korrektur visuell verständlich ist – nicht nur textlich.
  **Festes Prinzip für alle Details:** Die Skizze zeigt den korrigierten Zustand wie eine
  überarbeitete Zeichnung – falsch Gezeichnetes wird entfernt
  (weiß abgedeckt), fortzuführende Schichten werden mit **derselben Schraffur wie in der
  Zeichnung** und **durchgehend** bis an das nächste Bauteil eingezeichnet (z. B. Dämmung als
  Schlaufen in voller Schichtdicke). Keine bloßen Grenzstriche. Hinweistexte müssen vollständig
  lesbar sein (nie abgeschnitten).
  **Dämmstoff-Schraffuren unterscheiden und sinngemäß einsetzen:** weich = Schlaufen
  (Faserdämmstoffe in Gefach/Sparrenfeld), hart = Zickzack (Dämmplatten: Holzfaserplatte,
  EPS, XPS, PUR), geschlängelt = Wellenlinie (dünne weiche Lagen, z. B. Trittschall).
  Vorrang hat immer die Darstellung derselben Schicht in der Zeichnung (Tabelle in SKILL.md 5b).
- Kein Berichtskopf-Block auf Seite 1 (Projekt/ID/Version stehen in der Kopfzeile).
- Präfixe: B1… = Befunde, S1… = Schichten (außen → innen wie die Legende; bei mehreren
  Bauteilen z. B. D1… Dach, W1… Wand), F1… = offene Fragen.
- Bauteile in der Zeichnung mit Kästchen beschriften (z. B. „Wand A“, „Dach“, „innen“, „außen“).
- **Quellenpflicht:** Jede Norm-/Gesetzes-/Paragraphennennung im Bericht mit `[[ID]]` aus
  `skill/pruefkatalog/quellen.json` belegen (wird zur verlinkten Fußnote).
- Der Bericht steht für sich: keine Dateipfade, keine Verweise auf den Chat;
  Disclaimer nur einmal auf Seite 1 + dezent in der Fußzeile.
- Skizzen im **CAD-Look**: schwarze Linien, klare Linienstärken, DIN-Schraffuren
  (Dämmung, Holz, Plattenwerkstoffe), Beschriftung mit Hinweislinien.

## Technik
- Skill-Ordner: `skill/` (SKILL.md, VERSION, pruefkatalog/, checkliste.md, referenz/, scripts/).
- Ablauf der Skripte: `fakten.py` (feste Fakten + Prüfsumme) → `raster.py`/`linien.py`
  (Positionen, exakte Kanten) → `befunde.json` → `markieren.py` (Kontrolle) → `skizze.py`
  (Korrekturskizze) → `bericht.py` (PDF-Prüfbericht).
- Skripte **modellneutral** halten (reines Python, keine Claude-spezifischen Aufrufe) – damit
  der Skill später auch mit anderen KI-Modellen (z. B. Codex über `AGENTS.md`) nutzbar bleibt.
- Python: `%LOCALAPPDATA%\Programs\Python\Python312\python.exe` (in Git Bash:
  `/c/Users/ozand/AppData/Local/Programs/Python/Python312/python.exe`); Git 2.56.
- GitHub: https://github.com/Jade-HS-Vibecoding-WPK/Detailpruefer (Branch `main`, Kurs-Organisation; Remote `origin`). Altes Repo als Remote `alt`.
- Keine `rm`-Befehle mit Shell-Variablen; Zwischenbilder in `tests/ausgabe/` dürfen bleiben.
- Beispielbericht für README/Poster: `beispiel/`.
- Skripte in Python; sie müssen in claude.ai (Code-Ausführung) und in Claude Code laufen.
