# Checkliste – Rückfragen an Nutzer:innen

**Nur konstruktiv relevante Fragen:** Gefragt wird nur, was die Zeichnung **nicht**
beantwortet **und** ohne das ein Befund **nicht beurteilbar** wäre. Gibt es keine solche
Frage, wird **ohne Rückfrage** geprüft; alle Annahmen stehen dann im Bericht.

Fragen gesammelt, nummeriert (1, 2, …) und kurz stellen – je ein Satz, **warum** die Frage
für die Konstruktion wichtig ist, und die **Annahme**, die ohne Antwort gilt.

## Nicht fragen

- **Keinen Projektnamen** (im Bericht steht „nicht angegeben“, wenn er nicht in der
  Zeichnung steht).
- **Keine sd-Werte, λ-Werte oder Produktnamen** – fehlen sie, ist der betroffene Punkt
  „aus der Datei nicht prüfbar“ bzw. „Nachweis erforderlich“.
- **Nie fragen, ob ein fehlendes Bauteil „geplant, aber nicht gezeichnet“ ist.** Das Detail
  wird geprüft, **wie es gezeichnet ist**. Fehlt ein funktional notwendiges Bauteil, ist das
  ein Befund (siehe `pruefkatalog/00_uebersicht.md`, Grundsatz 5).
- Nichts, was die Zeichnung beantwortet (Legende, Beschriftung, Maßkette, andere Bauteile).
- Brand- und Schallschutz nicht abfragen; im Bericht steht: „Brand- und Schallschutz nicht
  Teil dieser Prüfung – gesondert nachweisen.“

## Mögliche Fragen (nur wenn für dieses Detail entscheidend)

| Nr. | Frage | Warum wichtig? | Annahme, wenn keine Antwort |
|---|---|---|---|
| K0 | **Konstruktion/Tragsystem nicht eindeutig zuordenbar** (z. B. am First weder Firstpfette noch Sparrenverbindung → „Pfettendach oder Sparren-/Kehlbalkendach?“; Aufsparren- oder Zwischensparrendämmung?; Flachdach-Typ?) – **immer fragen**, Antwortoptionen aus `pruefkatalog/12_detailtypen.md` | Davon hängen Pflichtbauteile, Befunde und die Korrekturskizze ab (DT-00) | **keine** – erst nach der Antwort prüfen und zeichnen |
| K1 | Ist der Raum hinter dem Detail **beheizt** (z. B. ausgebautes Dachgeschoss) oder **unbeheizt** (Kaltdach, Spitzboden)? | Bestimmt, ob Dämmung, Luftdichtheit und Dampfbremse an dieser Stelle nötig sind | wie gezeichnet: gedämmt = beheizt |
| K2 | **Neubau oder Bestand/Sanierung?** | Bestand kann vorhandene Bauteile erklären, die man neu anders lösen würde | Neubau |
| K3 | **Besondere Raumnutzung** mit hoher Feuchte (Bad, Schwimmbad, Küche gewerblich)? | Hohe Raumfeuchte verschärft die Anforderungen an die Dampfbremse | Wohnen, normales Raumklima |
| K4 | **Funktion eines unklaren Bauteils**, das weder beschriftet noch eindeutig erkennbar ist (z. B. „Was ist das senkrechte Bauteil in der Firstachse?“) | Ohne Funktion lässt sich der Lastabtrag bzw. die Schichtfolge nicht beurteilen | Deutung, die zur Zeichnung am besten passt – mit Aussagesicherheit „mittel“ |
| K5 | **Hohe Wetterbeanspruchung** (Küste, Gebirge, freie Lage) – nur bei Fassaden-, Sockel- und Ortgangdetails | Bestimmt Schlagregen- und Windsogschutz | normale Lage (Schlagregen-Beanspruchungsgruppe II) |

## Regeln

- Höchstens **eine** Fragerunde, danach prüfen. **K0 ist Pflicht**, sobald die Konstruktion
  nicht eindeutig zugeordnet werden kann (Entscheidung Nutzer 18.11.2026) – dann nie raten.
- Unbeantwortete Fragen und verwendete Annahmen kommen **in den Bericht** (Feld
  `offene_fragen` bzw. `annahmen`); im Bericht F1, F2 … statt K-Nummern.
- Mehrere Details desselben Projekts: Antworten aus der vorigen Prüfung übernehmen und
  nicht noch einmal fragen.
