# Auswertung Blindtest 6 – Ortgang (claude.ai, vermutlich noch Skill-Stand v5)

> NICHT Teil des Skills. Testdetail: `tests/details/blindtest_6_ortgang.pdf`, korrektes Detail:
> `tests/details/ortgang_korrekt.pdf`, Musterlösung: `blindtest_6_ortgang_musterloesung.pdf`
> (rot = im Testdetail veränderte Bereiche). Lauf vom Nutzer in claude.ai (18.11.2026),
> ausgewertet am selben Tag.

## Ablauf

- Der Ortgang wurde **im selben Chat wie Blindtest 5 (Sockel, 17.11.)** geprüft („Ich prüfe
  jetzt das Ortgangdetail auf dieselbe Weise“). Der Skill war in diesem Chat schon mit dem
  Stand **v5** geladen. Die v6-Neuerungen (übliche Bauteildicken, interner Bauteil-Check,
  Spalte „üblich“) waren damit sehr wahrscheinlich **nicht aktiv**.
  → **Lehre:** Jeder Blindtest gehört in einen **neuen** Chat, sonst gilt der alte Skill-Stand.
- Keine Fragerunde; Annahmen (Wetterlage, beheiztes DG) als offene Fragen im Bericht.
- Bericht 13 Seiten; 2 klare Aufbaufehler, 5 mögliche Auffälligkeiten, 1 Hinweis, 4 nicht prüfbar.

## Eingebaute Fehler → Ergebnis

| Eingebauter Fehler (rot in der Musterlösung) | Befund in claude.ai | Bewertung |
|---|---|---|
| **Rähm 10/24 fehlt** am Wandkopf | B1 klarer Aufbaufehler, in der Skizze eingezeichnet | ✅ |
| **Sparren und Dachdämmung nur 15 statt 24 cm** (Legende: Sparren 24/8; Gesamtmaß 38 statt 42) | B5 nur „mögliche Auffälligkeit“ (Widerspruch Legende/Zeichnung); kein Abgleich mit dem üblichen Bereich (200–240 mm); Dämmung ohne Materialangabe nicht angesprochen | ⚠️ teilweise |
| **Hinterlüftung oben geschlossen** (Musterlösung: Verkleidung endet unter dem Überstand, Lüftungsgitter) | B2 klarer Aufbaufehler, Abluftspalt mit Insektenschutzgitter | ✅ |
| **Obere Befestigungslatte der Fassade fehlt** (rot an der Oberkante der Verkleidung) | nicht erkannt („Lattung richtig dargestellt“) | ❌ übersehen |
| **Fugenabdichtung Innenecke Wand/Dach fehlt** (an der Schattenfuge) | B4 kein Eckband zwischen Wand- und Dach-OSB | ✅ |
| **Latte der Installationsebene am Wandanschluss** (rot im Dach) | – | ❌ übersehen (Nebenbauteil) |
| **Hinweislinien vertauscht, Fassadenbahn ohne Hinweislinie** (nicht rot, aber verändert) | B6 + B8 | ✅ |

**Trefferquote: 4 von 7 voll, 1 teilweise, 2 übersehen.** Die Deutung der roten Latten
(Fassade oben, Installationsebene) ist noch mit dem Nutzer abzustimmen.

## Fehlalarme / strittige Befunde

- **B3 „Holzplatte statt DWD-Platte“:** In der Musterlösung läuft die mehrschichtige
  Holzplatte genauso weit ins Dach → laut Musterlösung **Fehlalarm** (fachliche Einschätzung
  durch den Nutzer offen).
- B7 Ortgangpfanne (Windsogsicherung, Tropfblech): Hinweis, in der Musterlösung nicht geändert –
  vertretbar als Hinweis nach DA-05.

## Nachfrage „Ist die 15 cm Dämmung ausreichend?“

- claude.ai hat einen **U-Wert überschlagen** (≈ 0,16 W/m²K, λ-Werte angenommen) und
  geantwortet „rechnerisch reichen die 15 cm wahrscheinlich aus“.
- Das **verstößt gegen den Grundsatz „keine Berechnungen“** und führt in die falsche Richtung:
  Laut Musterlösung sind 24 cm richtig. Der Skill regelt bisher nur die Prüfung selbst, nicht
  Nachfragen nach dem Bericht.

## Lehren für den Skill

1. Blindtests immer in einem neuen Chat (Hinweis in README/HANDOFF).
2. **Nachfragen nach dem Bericht** gelten dieselben Regeln: keine U-Werte schätzen, stattdessen
   üblicher Bereich (RW-01) + „Wärmeschutznachweis erforderlich“.
3. **Fehlt die Materialangabe** eines gezeichneten Bauteils (hier: Dachdämmung), geeignete
   Baustoffe für diese Einbaulage vorschlagen (Feature-Wunsch des Nutzers, 18.11.).
4. DA-05 Ortgang um Wandkopf (Rähm), Abluft der Fassaden-Hinterlüftung unter dem Überstand
   und obere Befestigungslatte ergänzen.

---

# Zweiter Lauf – claude.ai v7, neuer Chat (18.11.2026)

Bericht: `blindtest_6_ortgang_bericht_v7.pdf` (18 Seiten; 2 Aufbaufehler, 6 Auffälligkeiten,
1 Hinweis, 4 nicht prüfbar). Spalte „üblich“, Baustoff-Empfehlungen und Empfehlungen im
Schichtenaufbau sind jetzt vorhanden.

| Eingebauter Fehler | v5 | v7 |
|---|---|---|
| Rähm fehlt | ✅ | ✅ B1 – aber Rähm nur 24/6 gezeichnet (Musterlösung 10/24) und Vorschlag „OSB-Streifen entfernen“ (in der Musterlösung bleibt die Platte auf dem Rähm) |
| Sparren/Dämmung 15 statt 24 cm | ⚠️ | ✅ B5 mit „üblich 200–240 mm“ + Baustoff-Empfehlung; in der Skizze nur beschriftet (Höhenversatz) |
| Hinterlüftung oben geschlossen | ✅ | ✅ B2 |
| Oberste Fassadenlatte fehlt | ❌ | ✅ B4 |
| Fugenabdichtung Innenecke | ✅ | ✅ B7 |
| Latte Installationsebene am Wandanschluss | ❌ | ❌ |
| Hinweislinien vertauscht | ✅ | ✅ B3 |

**Trefferquote v7: 6 von 7** (v5: 4 von 7).

## Fehlalarme / Unstimmigkeiten v7

- **B8 Konterlattung 3 cm „zu niedrig“** – Fehlalarm. Regel RW-01 nannte nur den dataholz-
  Standardaufbau (50 mm). Nach Nelskamp/Fachregel genügen 30 mm bei Sparren < 8 m.
- **B9 DWD-Schraffur** – eindeutig beschriftete Schicht; laut Nutzer kein Befund.
- **B6 Windsogsicherung** als Auffälligkeit – laut Nutzer nur Verbesserungshinweis.
- **Schreibfehler „Konerlattung“** erkannt, aber in der Skizze nicht korrigiert.
- **Positiv WB-01** „Dämmung schließt ohne Lücke an, Sparrenfeld voll gedämmt“ widerspricht B1/B5.
- Nachfrage-Regel (keine U-Werte) wurde in diesem Lauf nicht getestet.

## Nachbesserung (18.11.)

- RW-01: Konterlattung mind. 30 mm (Sparren < 8 m) [[NELSKAMP-D13]]; Rähm: Querschnitt der
  Schwelle bzw. 10 cm × Wanddicke (Praxisempfehlung; Vorschlag übernommen, Nutzer ohne Präferenz), Quelle BauNetz Rahmenbau.
- DA-05: Platte über dem Wandkopf bleibt auf dem Rähm (kein KO-07); Latte der
  Installationsebene am Rand; Windsogsicherung = Verbesserungshinweis.
- ZQ-05: beschriftete Schicht mit anderer Schraffur = kein Befund. Neu ZQ-06 Rechtschreibung
  mit Korrektur in der Skizze (entfernen + text ohne Rahmen).
- SKILL.md: Positiv-Liste gegen Befunde abgleichen; Querschnitte fehlender Bauteile nie schätzen.
- Höhenversatz in der Skizze bleibt bekannte Grenze (Entscheidung Nutzer).
