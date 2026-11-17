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
  Fehlende/unklare Zeichnungsangabe ≠ Baufehler.
- Keine Pauschalaussagen „sicher/normgerecht“. Jeder Befund: woran in der Zeichnung erkennbar.
- Jeder Prüfbericht enthält den Hinweis: *Hilfestellung – ersetzt keine fachliche Prüfung
  und keinen Nachweis. Die KI kann sich irren; Ergebnisse sind zu überprüfen.*
- **Neue Quellen nur nach Web-Recherche** mit funktionierendem Link in `quellen.json`
  aufnehmen (Ausgabe/Stand angeben). Widerspricht eine Quelle einer bestehenden Regel,
  die Regel korrigieren (Beispiel: Gehrung an Holzfassaden-Außenecken ist empfohlen).
- **Fehlt für eine Bauteilart eine Regel** (z. B. Dach, Sockel, Fenster), zuerst den
  Prüfkatalog mit Quelle ergänzen, dann prüfen – und das im Bericht/der Antwort offenlegen.
- Ablauf jeder Prüfung: Zeichnung erfassen (Raster, Zooms, Texte mit Positionen) →
  eine Fragerunde → alle Regeln → `befunde.json` → markieren → Korrekturskizze → Bericht →
  **jede Berichtsseite als Bild kontrollieren** (Überlappungen, Umbrüche, leere Seiten).

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
- Skill-Ordner: `skill/` (SKILL.md, pruefkatalog/, checkliste.md, scripts/).
- Ablauf der Skripte: `raster.py` (Positionen ablesen) → `befunde.json` →
  `markieren.py` (Kontrolle) → `skizze.py` (Korrekturskizze) → `bericht.py` (PDF-Prüfbericht).
- Python: `%LOCALAPPDATA%\Programs\Python\Python312\python.exe` (in Git Bash:
  `/c/Users/ozand/AppData/Local/Programs/Python/Python312/python.exe`); Git 2.56.
- GitHub: https://github.com/Ozan44336/Detailpr-fer (Branch `main`).
- Keine `rm`-Befehle mit Shell-Variablen; Zwischenbilder in `tests/ausgabe/` dürfen bleiben.
- Beispielbericht für README/Poster: `beispiel/`.
- Skripte in Python; sie müssen in claude.ai (Code-Ausführung) und in Claude Code laufen.
