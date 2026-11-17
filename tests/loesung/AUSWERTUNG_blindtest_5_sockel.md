# Auswertung Blindtest 5 – Sockel (claude.ai, Skill-Version v5)

> NICHT Teil des Skills. Testdetail: `tests/details/blindtest_5_sockel.pdf`, Musterlösung:
> `blindtest_5_sockel_musterloesung.pdf` (rot = im Testdetail veränderte Bereiche).
> Lauf vom Nutzer in claude.ai (17.11.2026), ausgewertet am selben Tag.

## Ablauf

- **Keine Fragerunde** – richtig nach neuer Checkliste: Es gab keine konstruktiv
  entscheidende Frage. Annahmen (normale Wetterlage, Fassade mit offenen Fugen) stehen als
  offene Fragen im Bericht.
- Bericht 14 Seiten; 1 klarer Aufbaufehler, 6 mögliche Auffälligkeiten, 1 Hinweis,
  3 nicht prüfbar.

## Eingebaute Fehler → Ergebnis

| Eingebauter Fehler (rot in der Musterlösung) | Befund in claude.ai | Korrekturskizze | Bewertung |
|---|---|---|---|
| **Schwelle 24/10 fehlt** (beschriftet, nicht gezeichnet) | B1 klarer Aufbaufehler | Schwelle als Holzquerschnitt eingezeichnet | ✅ |
| **XPS-Dämmung 10 statt 16 cm** (Höhen 39,5 statt 49 cm) | B7 „Höhen widersprechen sich“ (Koten 24 cm, Maßkette 19,5 cm) – Widerspruch erkannt, aber nicht der Dämmschicht zugeordnet | keine Korrektur der Dämmdicke | ⚠️ teilweise |
| **Sauberkeitsschicht 5 cm fehlt** unter der Bodenplatte | – | – | ❌ übersehen |
| **Randdämmstreifen fehlt** | B6 mögliche Auffälligkeit | als geschlängelte Dämmung eingezeichnet (sinngemäß richtig) | ✅ |
| **Fußleiste fehlt** | – | – | ❌ übersehen (Nebenbauteil) |

**Trefferquote: 2 von 5 voll, 1 teilweise, 2 übersehen** (Fußleiste ist ein Nebenbauteil).

## Weitere Befunde (in der Musterlösung nicht rot)

- B2 Lastabtrag „Isokorb“ unter der Innenschale (Bezeichnung eher für Balkonanschlüsse;
  Schwelle teilweise über Kerndämmung) – steht genauso in der Musterlösung; fachlich
  vom Nutzer zu bewerten.
- B3 Anschlussband OSB/Beton, B4 Insektenschutz unten, B5 Abdichtung unterbrochen –
  Zusatzbefunde, im Ausgangsdetail ebenfalls so gezeichnet.
- B8 DWD-Platte wie weiche Dämmung schraffiert statt Zickzack – die neue Regel ZQ-05
  (Dämmschraffur passend zur Dämmstoffart) greift.

## Verbesserungsbedarf (umgesetzt am 17.11., siehe PLAN.md)

1. **Höhen-Abgleich bis zur Schicht:** Widersprechen sich Höhenkoten, Maßkette und
   Schichtdicken, muss der Skill die **verursachende Schicht** bestimmen (hier XPS 10 statt
   16 cm) und sie in der Korrekturskizze **in richtiger Dicke** zeichnen – nicht nur den
   Widerspruch nennen.
2. **Bodenaufbau als Pflichtbauteile** (Sockel und Decken): Sauberkeitsschicht unter der
   Bodenplatte, Abdichtung, Dämmung, Trennlage, Estrich mit **Randdämmstreifen**, Belag,
   **Fußleiste**.
3. **Verdeckte Beschriftungen:** Wird eine Höhenkote oder Beschriftung durch ein
   eingezeichnetes Bauteil verdeckt (hier „+0,30 m“ durch die Schwelle), muss sie neben
   dem Bauteil neu gesetzt werden (`text` mit `"farbe": "original"`).
