# Detailprüfer Architektur

## Ziel
Ein Claude-Skill, der Holzbau-Detailzeichnungen (PDF) nach deutschen Regeln (DIN) prüft,
Fehler rot in der Zeichnung markiert, über eine Checkliste Rückfragen stellt und einen
PDF-Prüfbericht mit Mängelliste und Verbesserungsskizzen erzeugt.
Details und aktueller Stand: siehe `PLAN.md` – zu Beginn jeder Sitzung lesen.

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

## Testen
- Testzeichnungen: `tests/details/`
- `tests/loesung/` enthält den Lösungsschlüssel. **Nie in den Skill übernehmen** und erst
  **nach** einem Testlauf öffnen, um das Ergebnis zu bewerten.

## Gestaltung
- Schlicht und verständlich; der Fokus liegt auf der **Richtigkeit** der Prüfung.
- Markierungen: Kreis ohne Füllung + Badge „B1…“ mit Führungslinie neben der Zeichnung.
  **Rot** durchgezogen = klarer Aufbaufehler · **Orange** gestrichelt = mögliche Auffälligkeit ·
  **Blau** gepunktet = Verbesserungshinweis. Rot nur für klare Aufbaufehler.
- **Korrekturskizze (grün):** Was fehlt oder falsch ist, wird immer auch eingezeichnet
  (Latten, Konterlatten, Stiele, Platten mit Schraffur, Abklebungen, korrigierte Werte),
  damit die Korrektur visuell verständlich ist – nicht nur textlich.
- Kein Berichtskopf-Block auf Seite 1 (Projekt/ID/Version stehen in der Kopfzeile).
- Präfixe: B1… = Befunde, S1… = Schichten (außen → innen wie die Legende), F1… = offene Fragen.
- **Quellenpflicht:** Jede Norm-/Gesetzes-/Paragraphennennung im Bericht mit `[[ID]]` aus
  `skill/pruefkatalog/quellen.json` belegen (wird zur verlinkten Fußnote).
- Der Bericht steht für sich: keine Dateipfade, keine Verweise auf den Chat;
  Disclaimer nur einmal auf Seite 1 + dezent in der Fußzeile.
- Skizzen im **CAD-Look**: schwarze Linien, klare Linienstärken, DIN-Schraffuren
  (Dämmung, Holz, Plattenwerkstoffe), Beschriftung mit Hinweislinien.

## Technik
- Skill-Ordner: `skill/` (SKILL.md, pruefkatalog/, checkliste.md, scripts/).
- Ablauf der Skripte: `raster.py` (Positionen ablesen) → `befunde.json` →
  `markieren.py` (Kontrolle) → `bericht.py` (PDF-Prüfbericht).
- Beispielbericht für README/Poster: `beispiel/`.
- Skripte in Python; sie müssen in claude.ai (Code-Ausführung) und in Claude Code laufen.
