# Auswertung Blindtest 5 – Sockel, Lauf mit Skill v11 (claude.ai, 19.11.2026)

- **Zeichnung:** `tests/details/blindtest_5_sockel.pdf` (= `Sockel Detail fehler.pdf`), Prüfsumme `0A1CA30A1524`
- **Musterlösung:** `tests/loesung/blindtest_5_sockel_musterloesung.pdf` (= `Details/Sockel Detail Lösung.pdf`)
- **Bericht:** vom Nutzer in claude.ai erzeugt (`Pruefbericht_Sockel.pdf`, 15 Seiten, Skill 11)

## Fehler laut Musterlösung und Ergebnis

| Fehler (Musterlösung) | v11 | Bemerkung |
|---|---|---|
| Schwelle 24/10 falsch dargestellt (Dämmschraffur) | ✓ B1 klarer Aufbaufehler | |
| Fußleiste fehlt | ✓ in B2 | |
| Randdämmstreifen fehlt | ✓ B2 klarer Aufbaufehler | |
| XPS 16 statt 10 cm (Höhen 24 cm) | ✓ B3 mögliche Auffälligkeit | Koten-Widerspruch erkannt, XPS als Ursache vermutet |
| **Sauberkeitsschicht fehlt unter der Sohle** | ✗ **übersehen** | im Positiv-Abschnitt sogar als „vollständig“ gewertet |

Zusätzliche Befunde (Insektenschutz, luftdichter Anschluss am Wandfuß, Beschriftungen) sind
fachlich vertretbar und keine Fehlalarme im engeren Sinn.

## Ursache des Übersehens

In der Fehlerzeichnung liegt die Sauberkeitsschicht (5 cm, Kreuzschraffur) **nur unter dem
Fundament** (−0,80 m). Unter der Sohle (UKRD −0,44 m) ist keine Schicht gezeichnet; die
Maßkette rechts endet an der UKRD. Die Beschriftung „Sauberkeitsschicht“ zeigt mit ihrer
Hinweislinie auf das Fundament – der Skill hat daraus geschlossen, die Schicht sei vorhanden,
und den Bodenaufbau als vollständig gewertet.

**Fehlerklasse:** Eine Schicht ist irgendwo gezeichnet und beschriftet, fehlt aber in einem
Teilabschnitt. Das betrifft ebenso Abdichtung, Dämmung, Trennlagen, Bahnen und Randstreifen.

## Nachbesserung (Skill v12)

- **Neue Regel KO-08** „Jede Schicht liegt in allen Abschnitten, in denen sie liegen muss“
  (gilt für alle Details) mit typischen Abschnitten je Schicht; Einstufung wie das Fehlen der
  Schicht; Pflicht, im Prüfprotokoll die Abschnitte einzeln zu nennen.
- **SKILL.md Bauteil-Check:** Punkt 1 „nur in einem Teil der Abschnitte“; neuer Punkt 8
  (Abschnitts-Check, „Beschriftung belegt nur die Spitze der Hinweislinie“) und Punkt 9
  (Unterkanten- und Rand-Check, Maßkette endet an Unterkante); Positiv-Liste für
  Schichtenfolgen erst nach dem Abschnitts-Check.
- **SO-04:** Sauberkeitsschicht unter **allen** erdberührten Betonbauteilen; fehlt sie (ganz
  oder in einem Abschnitt) → **klarer Aufbaufehler** (Entscheidung des Nutzers 19.11.);
  Kies-/Schotterschicht als gleichwertige Variante. Quelle: Bauprofessor Sauberkeitsschicht.
- `00_uebersicht.md` (Vorgehen), ZQ-04 (Verweis auf KO-08), DT-W1 Sockel ergänzt.
- Zeichenwerkzeug `platte` mit neuer Schraffur `kreuz` (Magerbeton/Sauberkeitsschicht).

## Lokaler Nachtest

Abschnitts-Check mit `linien.py` am Testdetail: unter dem Fundament Kreuzschraffur
(y ≈ 80,9–83,2 %), unter der Sohle (y ≈ 63,8 % bis Bildrand) nur Kote und Bruchlinie →
Lücke eindeutig. Testbericht `tests/befunde_test_sauberkeitsschicht.json` →
`tests/ausgabe/sks_test_bericht.pdf`: Befund B1 klarer Aufbaufehler, Korrekturskizze zeigt die
Sauberkeitsschicht in Kreuzschraffur unter der ganzen Sohle wie die Musterlösung.
**Noch offen:** vollständiger Lauf in claude.ai mit v12 (neuer Chat).

## Lehren

- Eine Beschriftung belegt eine Schicht nur an der Spitze ihrer Hinweislinie.
- Vollständigkeit einer Schichtenfolge nie aus der Legende ableiten, sondern je Abschnitt.
- Unterkanten gegen Erdreich und Bereiche bis zum Bildrand gezielt ansehen.
