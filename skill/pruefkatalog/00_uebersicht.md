# Prüfkatalog – Übersicht

**Ziel:** Eine hochgeladene Bauzeichnung oder ein Baudetail wird **qualitativ** geprüft.
Zuerst wird der dargestellte Schichtenaufbau von innen nach außen erkannt. Dann werden
sichtbare Konstruktionsfehler und mögliche Risiken benannt und konkrete, zum dargestellten
Aufbau passende Verbesserungsvorschläge gegeben.

Maßstab sind deutsche Regeln. Ausgaben und Status der Normen: **`quellen.md`**
(Stand 16.11.2026).

## Dateien

| Datei | Bereich | Kürzel |
|---|---|---|
| `01_luftdichtheit.md` | Luftdichtheit (Raumluft soll nicht in die Konstruktion strömen) | LD |
| `02_feuchteschutz.md` | Feuchteschutz: Dampfbremse, Diffusion, Tauwasser, Austrocknung | FS |
| `03_waermeschutz_waermebruecken.md` | Wärmeschutz und Wärmebrücken | WB |
| `04_winddichtheit_hinterlueftung.md` | Winddichtheit · Hinterlüftung · Schlagregenschutz (drei getrennte Teile) | WH |
| `05_holzschutz.md` | Baulicher Holzschutz | HS |
| `06_konstruktion_holzrahmenbau.md` | Konstruktion – qualitative Plausibilität, keine Statik | KO |
| `07_zeichnungsqualitaet.md` | Zeichnungsqualität | ZQ |
| `quellen.md` | Normausgaben, Gesetzesstand, Quellen | – |

Brand- und Schallschutz: nur Abfrage über `checkliste.md`, keine Prüfung.

## Funktionen klar trennen

Eine Schicht kann mehrere Funktionen übernehmen (z. B. OSB als Luftdichtheitsschicht **und**
Dampfbremse). Die Funktionen werden trotzdem **getrennt** geprüft und jeder Befund nur dem
**einen** passenden Bereich zugeordnet.

| Funktion | Wovor schützt sie? | Lage (typisch) | Bereich |
|---|---|---|---|
| **Luftdichtheit** | Durchströmung der Konstruktion mit warmer Raumluft (Konvektion) | raumseitig | LD |
| **Dampfbremse** | zu viel Wasserdampf**diffusion** in die Konstruktion | raumseitig | FS |
| **Winddichtheit** | Durchströmung der Dämmung mit kalter Außenluft | außenseitig auf der Dämmung | WH, Teil A |
| **Hinterlüftung** | Feuchtestau hinter der Bekleidung – ermöglicht Abtrocknung | zwischen Bekleidung und winddichter Ebene | WH, Teil B |
| **Schlagregenschutz** | Eindringen von Regenwasser | Bekleidung (+ ggf. zweite wasserführende Ebene) | WH, Teil C |

## Grundsätze der Prüfung

1. **Keine Berechnungen.** Es werden keine sd-, U- oder R-Werte, keine Tauwassermengen,
   kein Temperaturfaktor f_Rsi und keine Tragfähigkeit oder Schraubenbemessung berechnet.
   Wäre eine Berechnung für ein sicheres Urteil nötig, wird der Punkt als
   **„Nachweis erforderlich“** bzw. **„aus der Zeichnung nicht abschließend prüfbar“**
   gekennzeichnet – mit einem qualitativen Hinweis. (Längen aus der Zeichnung ablesen und
   Maßketten aufaddieren ist erlaubt – das ist Zeichnungsprüfung, keine Berechnung.)
2. **Nichts erfinden:** keine Schichten, Maße, Materialwerte, Normklauseln oder Grenzwerte
   ergänzen. Grenzwerte nur, wenn sie in `quellen.md` als verifiziert stehen.
3. **Faustregeln und typische Bauweisen sind keine Normpflichten.** Sie werden als
   **(Praxisempfehlung)** gekennzeichnet.
4. **Risiken vorsichtig formulieren:** Tauwasser, Schimmel, Fäulnis oder Tragfähigkeitsverlust
   folgen **nicht automatisch** aus einer sichtbaren Auffälligkeit. Sie werden als
   **mögliche** Risiken beschrieben („kann … begünstigen“), wenn das fachlich passt.
5. **Fehlende oder unklare Zeichnungsangabe ≠ Baufehler.** Sie wird als Verbesserungshinweis
   oder „aus der Datei nicht prüfbar“ eingeordnet.
6. **Geltungsbereich beachten:** Jede Regel sagt unter **„Gilt für“**, für welche Bauart bzw.
   welches Fassadensystem sie gilt. Passt sie nicht zum Detail → nicht anwenden.
7. **Mehrere Lösungen zulassen:** Verbesserungsvorschläge sind konkret, aber nicht die
   einzig zulässige Ausführung („z. B.“, „eine Möglichkeit ist …“).
8. **Keine Doppelbefunde:** Ein Sachverhalt wird nur **einmal** als Befund aufgeführt – im
   Bereich, in dem seine Hauptursache liegt. Andere Bereiche **verweisen** darauf
   (z. B. „siehe LD-02“).
9. **Keine Pauschalaussagen**, dass die Konstruktion insgesamt sicher oder normgerecht sei.
10. **Klar und verständlich auf Deutsch.** Fachbegriffe beim ersten Auftreten kurz erklären.

## Die Einstufungen

| Einstufung | Wann? | Was wird angegeben? | Markierung |
|---|---|---|---|
| **Klarer Aufbaufehler** | Nur wenn er aus der Zeichnung **eindeutig** hervorgeht | Fundstelle, woran erkennbar, warum relevant, mögliches Risiko, Verbesserungsmöglichkeiten, Grundlage | roter Kreis, durchgezogen |
| **Mögliche Auffälligkeit** | Fraglich: Darstellung mehrdeutig, oder ein Urteil hängt von fehlenden Informationen ab | Was ist fraglich? Welche Information oder Prüfung fehlt? | roter Kreis, gestrichelt |
| **Verbesserungshinweis** | Kein Mangel erkennbar, aber eine sinnvolle Verbesserung – auch fehlende/unklare Zeichnungsangaben | Mögliche Verbesserung | roter Kreis, gepunktet (nur wenn ortsbezogen) |
| **Aus der Datei nicht prüfbar** | Mit den vorhandenen Angaben nicht beurteilbar | Welche Angabe bzw. welches Detail genau fehlt | keine Markierung |

Zusatzkennzeichnung (zu jeder Einstufung möglich): **„Nachweis erforderlich“** – wenn nur
eine Berechnung bzw. ein Nachweis (Tauwasser, Wärmebrücke, Statik, U-Wert) Sicherheit gibt.

## Schema jeder Regel

- **Gilt für** – Bauart / Fassadensystem, für das die Regel gilt
- **Prüfe** – was geprüft wird
- **So erkennst du es in der Zeichnung** – woran man es im Plan sieht
- **Typische Auffälligkeit** – wie ein Problem typischerweise aussieht
- **Warum relevant?** – fachliche Begründung
- **Mögliches Risiko** – was passieren *kann* (nicht: was automatisch passiert)
- **Verbesserungsmöglichkeiten** – eine oder mehrere fachgerechte Lösungen
- **Grundlage** – Norm (mit Ausgabe, siehe `quellen.md`) oder (Praxisempfehlung)
- **Einstufung** – welche Einstufung wann passt
- **Abgrenzung** – wo ein ähnlicher Sachverhalt geprüft wird (gegen Doppelbefunde)

## Vorgehen

1. Schichtenaufbau von innen nach außen erkennen (Zeichnung **und** Legende); unklare
   Schichten als „unklar“ markieren.
2. Jede Regel aller Bereiche durchgehen; Geltungsbereich prüfen.
3. Je Regel notieren: `erfüllt`, `nicht anwendbar` oder eine Einstufung – mit Kürzel.
4. Doppelbefunde zusammenführen (Grundsatz 8).
5. Für wichtige erfüllte Regeln kurz festhalten, was positiv ist – ohne Pauschalurteil.
