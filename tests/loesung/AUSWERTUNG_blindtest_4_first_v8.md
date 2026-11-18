# Auswertung Blindtest 4 – First, zweiter Lauf (claude.ai v8, 18.11.2026)

> NICHT Teil des Skills. Testdetail `tests/details/blindtest_4_first.pdf`, Musterlösung
> `blindtest_4_first_musterloesung.pdf`, Bericht `blindtest_4_first_bericht_v8.pdf` (15 Seiten;
> 3 Aufbaufehler, 4 Auffälligkeiten, 2 Hinweise, 3 nicht prüfbar).

## Ergebnis

| Eingebauter Fehler (rot in der Musterlösung) | v8 | Bewertung |
|---|---|---|
| Firstabdeckung fehlt (Firstziegel, Firstlatte 3/5, Halter) | B1 Aufbaufehler, eingezeichnet | ✅ |
| **Firstpfette 14/28 fehlt** (Pfettendach) | B2 „Lastabtrag fehlt“ erkannt, aber **Sparrendach angenommen** (F1) und als grünes Sechseck **oben in der Dämmebene** gezeichnet | ⚠️ Befund richtig, Korrektur falsch |
| Dämmung nur teilweise (20 cm Sparrenfeld) | B3 Aufbaufehler + Baustoff-Empfehlung | ✅ |
| Latten der Installationsebene am unteren Rand (rot) | nicht erwähnt | ❌ |

Zusätzlich richtig: EPDM-Folie außen (B4), Dampfbremse am First (B5), Maßketten (B6),
Schreibfehler „Tondachpfahnne“, „Dampfbemse“, „Brass“ (B9, ZQ-06 greift).

## Ursache

- Der Skill kannte nur die **Regel** „Lastabtrag am First muss vorhanden sein“, aber nicht den
  **Aufbau** eines Pfettendach-Firsts (Pfette unter den Sparren). Bei fehlender Pfette wurde
  geraten (Sparrendach) statt nachgefragt.
- Koordinaten wurden aus dem Rasterbild geschätzt → Bauteil an falscher Stelle.

## Nachbesserung (Feature 12, 18.11.)

- Neu `pruefkatalog/12_detailtypen.md` (DT): Steildach (First Pfetten-/Sparren-/Kehlbalkendach,
  kalter Spitzboden, Traufe, Ortgang, Aufsparrendämmung), Wand (Sockel, Ecken, Geschossdecke),
  Fenster, Flachdach Typ I–V/Attika, Pultdach – mit Erkennungsmerkmalen, Bauteilen in ihrer
  Lage, Varianten, Zeichenanleitung; Quellen Informationsdienst Holz (holzbau handbuch R5/T2/F2
  2023, R3/T2/F1 2019), BauNetz Wissen, RAL-Leitfaden.
- Eigene Referenzskizzen `referenz/*.png` (7 Typen), Skript `scripts/referenz.py`.
- Neues Werkzeug `scripts/linien.py`: Vektorlinien exakt auslesen, Schnittpunkte berechnen.
- Checkliste **K0**: Konstruktion nicht zuordenbar → immer Rückfrage (Nutzerentscheidung).
- Lokaler Test: Firstpfette 14/28 mit Oberkante im Schnittpunkt der Sparren-Unterkanten
  (`linien.py --schnitt` → x 46,153 %, y 44,604 %) → `tests/ausgabe/firstpfette_test.pdf`.
