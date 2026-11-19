# Auswertung Gebäudeecke (wandeck_mit_fehlern) – Lauf mit Skill v12 (claude.ai, 19.11.2026)

- **Zeichnung:** `tests/details/wandeck_mit_fehlern.pdf` (= `Details/wand-mit fehler .pdf`), Prüfsumme `CEAAB8D26E3D`
- **Musterlösung:** `Details/Wandeck Muster.pdf` (außerhalb des Projekts) bzw. `LOESUNG_wandeck_mit_fehlern.md`
- **Bericht:** vom Nutzer in claude.ai erzeugt (`Pruefbericht_Gebaeudeecke.pdf`, 17 Seiten, Skill 12)

## Ergebnis

| Eingebauter Fehler | v12 | Bemerkung |
|---|---|---|
| Luftdichte Abklebung an der Innenecke fehlt | ✓ B1 klarer Aufbaufehler | Korrektur richtig (Eckband) |
| Zusätzlicher Wandstiel in der Eckverbindung fehlt | ✓ B2 erkannt (KO-01) | **Korrekturskizze falsch:** Ständer an falscher Stelle |

## Was in der Korrekturskizze falsch war

Der Skill hat den fehlenden Stiel als Ständer 6/16 **oberhalb** der Ecke und **über die volle
Gefachtiefe** von Wand A eingezeichnet. Richtig ist er (Musterlösung und Prinzip):
**direkt hinter dem OSB-Rand von Wand A**, **am Endständer von Wand B** anliegend, **raumseitig
bündig** mit der Ständerebene; **außen davor läuft die Dämmung weiter**.

**Ursache (Fehlerklasse):** Zusatzhölzer wurden nach „irgendwo an der Ecke“ platziert, nicht nach
ihrer **Funktion** (welchen Plattenrand trägt es, welches Bauteil schließt es an) und ohne Blick
auf die Dämmebene. Für die Wandecke gab es zudem keine Referenzskizze.

## Nachbesserung (Skill v13)

- **Neue Regel KO-09** „Zusatzhölzer liegen dort, wo sie gebraucht werden – Lage nach
  Funktion“ mit vier Pflichtfragen (Wozu? Wo ist die Funktion? Wie klein / Dämmung auf der
  Gegenseite? Schon vorhanden?) und Pflicht-Selbstkontrolle im Kontrollbild. Gilt für alle
  Details (Ecke, Wandanschluss, Laibung, Decke, Plattenstöße).
- **SKILL.md 5b Punkt 3b** (Zeichnen von Zusatzhölzern), KO-02 und DT-W2 mit Erkennen,
  Geometrie-Prinzip und Varianten ergänzt.
- **Eigene Referenzskizze** `referenz/ecke_aussen.png` (Außenecke Holzrahmenbau: Wand A
  durchlaufend, Wand B stumpf, Zusatzstiel raumseitig mit Dämmung davor, OSB-Ränder auf Holz,
  Abklebung, Fassadenlatten an der Ecke) – nicht aus der Musterlösung kopiert.

## Lokaler Nachtest

Mit `linien.py` bestimmt: OSB-Rand A bei y ≈ 64,7 %, Endständer B x 49,8–52,6 % / y 64,7–75,5 %,
Endständer A ab y 71,4 %. Nach den vier Fragen: Zusatzstiel x 46,9–49,8 %, y 60,7–71,4 %
(raumseitig 6 cm, Dämmung außen davor). Testbericht `tests/befunde_test_eckstiel.json` →
`tests/ausgabe/eckstiel_bericht.pdf`; Lage stimmt mit dem Prinzip der Musterlösung überein.
**Offen:** Lauf in claude.ai mit v13 (neuer Chat).

## Lehren

- Jedes ergänzte Holz braucht eine benannte Funktion – daraus folgt die Lage.
- Holz über die volle Dämmdicke nur, wenn es tragend nötig ist; sonst Dämmung davor.
- Für jede Detailart eine eigene Referenzskizze, bevor Korrekturen gezeichnet werden.
