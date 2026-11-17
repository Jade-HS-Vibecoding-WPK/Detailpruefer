# Auswertung Blindtest 3 – Traufe

> NICHT Teil des Skills. Musterlösung: `blindtest_3_traufe_musterloesung.pdf` (rot = im
> Testdetail veränderte Bereiche, richtig dargestellt). Zusätzlich das fertige, richtige
> Ausgangsdetail: `blindtest_3_traufe_korrekt.pdf`. Ausgewertet am 17.11.2026.

## Eingebaute Fehler laut Musterlösung → Ergebnis des Detailprüfers

| Eingebauter Fehler (rot in der Musterlösung) | Befund im Bericht | Einstufung | Gefunden? |
|---|---|---|---|
| Sparrenfeld nur 10 cm gedämmt + 10 cm „Luftsicht“ → richtig: 20 cm Sparren/Dämmung, vollständig gedämmt (Zeichnung und Legende rot) | B1 (+ B3 Legende) | klarer Aufbaufehler | ✅ |
| Fußpfette zu klein, ohne Auflager in der Wanddämmung → richtig: Pfette 16/20 auf dem Wandkopf, unter Füllholz/Sparren | B2 | klarer Aufbaufehler | ✅ |
| Winkelangabe 45° falsch → Musterlösung: 35° | B4 | mögliche Auffälligkeit | ✅ (siehe Anmerkung) |
| **OSB-Platte der Wand läuft über den Wandkopf hinaus durch die Dachdämmung bis unter die Unterdeckplatte** → richtig: OSB endet am Wandkopf (Höhe Folienanschluss), Dachdämmung läuft durch | – | – | ❌ **übersehen** |

**Trefferquote: 3 von 4 eingebauten Fehlern gefunden.**

Anmerkung zum Winkel: Der Detailprüfer hat erkannt, dass die Angabe „45°“ nicht zur
Zeichnung passt, und die gezeichnete Neigung mit etwa 25° abgelesen. Die Musterlösung nennt
35°. Nachgemessen (Unterdeckplatte im Rasterbild): die Zeichnung steigt mit etwa 25° an –
falls 35° gelten soll, müsste auch die Zeichnung angepasst werden. Der Befund (Beschriftung
und Zeichnung widersprechen sich) bleibt richtig.

## Weitere Befunde des Detailprüfers (in der Musterlösung nicht als Fehler markiert)

| Befund | Bewertung |
|---|---|
| B3 Dachlegende: Reihenfolge Konterlattung/Lattung, Maßkette (Gipskarton 1,5 statt 2,5 cm, Summe 39 statt 40 cm) | **Zusatzbefund, kein Fehlalarm** – steht genauso im richtigen Ausgangsdetail. |
| B5 Folie, Funktionen und Dämmstoffe nicht in der Legende; Schreibfehler | **Zusatzbefund** (Hinweis) – ebenfalls im Ausgangsdetail vorhanden. |

Keine Fehlalarme im engeren Sinn: Alle weiteren Befunde betreffen echte Widersprüche, die
schon im Ausgangsdetail stehen.

## Warum wurde der OSB-Fehler übersehen?

- Geprüft wurde nur, **ob** die Dachfolie an die OSB der Wand angeschlossen ist (LD-02,
  „Stift-Regel“) – das war erfüllt und wurde sogar als positiv vermerkt.
- **Nicht** geprüft wurde, **wo die OSB-Platte endet**. Sie läuft im Testdetail etwa 20 cm
  über den Folienanschluss hinaus nach oben, teilt die Dachdämmung und endet erst unter der
  Unterdeckplatte. Der Katalog hatte dafür keine Regel; der Schritt „jede Schicht bis zu
  ihrem Ende verfolgen“ war nur für Ecken (Unterkonstruktion) und Plattenränder (KO-01)
  beschrieben.

## Erkenntnisse und Änderungen am Skill

- **Neue Regel KO-07** „Schichten enden am Anschluss – keine Platte läuft in die Dämmebene
  des Nachbarbauteils“ (`skill/pruefkatalog/06_konstruktion_holzrahmenbau.md`).
- **Vierter Abgleich** in `SKILL.md` Schritt 1 und in `00_uebersicht.md` (Vorgehen):
  Bei Anschlüssen jede Platte und Bahn bis zu ihrem tatsächlichen Ende verfolgen und mit
  der Lage des Anschlusses vergleichen – besonders in Vertikalschnitten.
- Die Erkennung bei Dächern/Vertikalschnitten funktioniert grundsätzlich (3 von 4), ist aber
  erst an einem Detail erprobt.
- Hinweis: KO-07 ist aus diesem Test entstanden – ein erneuter Lauf an der Traufe ist
  deshalb **kein Blindtest** mehr, sondern nur eine Kontrolle, ob die Regel greift.

## Kontrolllauf in claude.ai (17.11.2026)

Skill als ZIP über **Plugins → Hinzufügen → Plugin hochladen** installiert (Skills liegen in
claude.ai inzwischen unter „Plugins“). Zeichnung als `Traufe.pdf` hochgeladen, Modell
Opus 5.5 (Mittel), Code-Ausführung an, ausgehender Netzwerkverkehr aus.

**Technik: läuft.** raster.py, markieren.py, skizze.py und bericht.py laufen ohne
Nachinstallation; Bericht (14 Seiten) + Korrekturskizze als PDF; Umlaute und Schrift korrekt.
Dauer ca. 8 Minuten.

| Eingebauter Fehler | claude.ai | Ergebnis |
|---|---|---|
| OSB läuft durch die Dachdämmung | B1 klarer Aufbaufehler (KO-07) | ✅ – neue Regel greift |
| Fußpfette ohne Auflager / zu klein | B2 klarer Aufbaufehler | ✅ |
| Winkelangabe 45° | B3 mögliche Auffälligkeit (gezeichnet ca. 25°) | ✅ |
| Sparrenfeld nur halb gedämmt | nur in B5 als Legendenwiderspruch („Luftsicht ist als Dämmung gezeichnet – klären“) | ⚠️ **falsch gedeutet** – Dämmlücke nicht als Fehler erkannt |

Zusatzbefund **B4** „Unterdeckung entwässert hinter die Rinne“ (Abtropfblech endet hinter
und unter dem Rinnenrand) – ist im richtigen Ausgangsdetail gleich gezeichnet; fachlich vom
Nutzer zu bewerten.

**Erkenntnisse aus dem claude.ai-Lauf**
- **Checkliste übersprungen:** Es kam keine Fragerunde; Annahmen wurden still getroffen und
  als offene Fragen F1–F5 in den Bericht geschrieben → SKILL.md Schritt 2 muss ausdrücklich
  „anhalten und auf Antwort warten“ verlangen.
- **Dämmschraffur mehrdeutig:** Die großen Dämm-Bögen reichen optisch weit ins Feld; der
  leere Streifen darunter (über der Folie) wurde als gedämmt gelesen. Regel ergänzen: Nennt die Legende eine
  Luftschicht/einen Hohlraum **innerhalb** der Dämmebene, ist das selbst ein Befund nach WB-01
  – unabhängig davon, wie die Schraffur wirkt.
- **Layout:** Überschrift „Befunde im Detail“ steht allein auf einer sonst leeren Seite
  (Seite 4) – Überschrift muss mit der ersten Karte zusammenbleiben.
- Ergebnisse schwanken zwischen Läufen (lokal: OSB übersehen; claude.ai: Dämmung falsch
  gedeutet). Jede Regel hilft nur, wenn sie im Ablauf ausdrücklich abgefragt wird.

## Zweiter Lauf in claude.ai (17.11.2026, Skill-Version v2)

Neue Version über **Plugins → Detailpruefer architektur → ⋯ → Neue Version hochladen** als
`.skill`-Datei (= ZIP mit anderer Endung) eingespielt. Gleiche Zeichnung `Traufe.pdf`,
gleiche Anfrage.

- **Fragerunde funktioniert:** Nach dem Erfassen hält der Skill an und stellt 9 Fragen mit
  Annahmen (u. a. ausdrücklich: „Ist die 10 cm Luftschicht Absicht?“). Antwort neutral:
  „0: nicht angegeben. 7: Standort unbekannt, Gruppe II. Alle anderen Annahmen ok.“
- **Treffer: 4 von 4.** B1 Luftschicht im Sparrenfeld (klarer Aufbaufehler, WB-01), B2 OSB
  läuft ins Dach (klarer Aufbaufehler, KO-07), B3 Fußpfette (klarer Aufbaufehler), B4
  Dachneigung 45°/ca. 25° (mögliche Auffälligkeit). Zusätzlich B5 Traufe/Unterdeckung,
  B6 Maßkette, B7 Legende (wie im Ausgangsdetail vorhanden).
- **Korrekturskizze:** Hinweistexte vollständig (nichts abgeschnitten); Sparrenfeld mit
  weicher Dämmung (Schlaufen) in voller Höhe; Fußpfette 16/20 auf dem Rähm eingezeichnet;
  OSB-Stück entfernt. **Schwäche:** Der frei gewordene Bereich über dem Wandkopf wurde nicht
  bis zum Füllholz mit Dachdämmung gefüllt → KO-07 um eine ausdrückliche Anweisung für die
  Korrekturskizze ergänzt (entfernen + ganzen Bereich mit gleicher `art`/`band` füllen),
  als Version v3 in claude.ai eingespielt (noch nicht erneut getestet).
- Bericht 14 Seiten, Dauer ca. 10 Minuten inkl. Fragerunde.
