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
- **Maßstab sind deutsche Normen** (DIN 4108, DIN 68800, DIN 4109, GEG, MBO/LBO).
- Jede Prüfregel im Skill hat eine **Quelle/Fundstelle**. Keine Regel ohne Quelle.
- Normtexte und fremde Zeichnungen (z. B. dataholz.eu) **nicht kopieren** – Regeln in
  eigenen Worten, fremde Quellen nur verlinken. Referenzdetails selbst zeichnen.
- Unsichere Einschätzungen als **unsicher kennzeichnen** statt zu raten.
- Jeder Prüfbericht enthält den Hinweis: *Hilfestellung – ersetzt keine fachliche Prüfung
  und keinen Nachweis. Die KI kann sich irren; Ergebnisse sind zu überprüfen.*

## Testen
- Testzeichnungen: `tests/details/`
- `tests/loesung/` enthält den Lösungsschlüssel. **Nie in den Skill übernehmen** und erst
  **nach** einem Testlauf öffnen, um das Ergebnis zu bewerten.

## Gestaltung
- Schlicht und verständlich; der Fokus liegt auf der **Richtigkeit** der Prüfung.
- Markierungen: **Rot** = Mangel (Kreis + Nummer, Schraffur). Nummern = Mängelliste.
- Skizzen im **CAD-Look**: schwarze Linien, klare Linienstärken, DIN-Schraffuren
  (Dämmung, Holz, Plattenwerkstoffe), Beschriftung mit Hinweislinien.

## Technik
- Skill-Ordner: `skill/` (SKILL.md, pruefkatalog/, checkliste.md, referenzdetails/, scripts/).
- Skripte in Python; sie müssen in claude.ai (Code-Ausführung) und in Claude Code laufen.
