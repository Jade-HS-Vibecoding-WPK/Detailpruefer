# Prüfkatalog – Übersicht

**Ziel:** Eine hochgeladene Bauzeichnung oder ein Baudetail wird **qualitativ** geprüft.
Zuerst wird der dargestellte Schichtenaufbau erkannt – nummeriert **wie die Legende der
Zeichnung, von außen nach innen (S1 = außen)**. Dann werden sichtbare Konstruktionsfehler
und mögliche Risiken benannt und konkrete, zum dargestellten Aufbau passende
Verbesserungsvorschläge gegeben.

Maßstab sind deutsche Regeln. Ausgaben und Status der Normen: **`quellen.md`**
(Erläuterung) und **`quellen.json`** (Quellenverzeichnis mit Links, Stand 16./17.11.2026).

## Quellenpflicht

Jede Nennung einer **Norm, eines Gesetzes oder Paragraphen** und jeder Grenzwert im Bericht
wird mit einer Quelle aus `quellen.json` belegt: im Text **`[[ID]]`** direkt hinter der
Aussage (z. B. „GModG § 13 [[GMODG-13]]“). Der Bericht macht daraus eine hochgestellte,
verlinkte Fußnote und listet die Quelle im Quellenverzeichnis. Fehlt eine passende Quelle:
erst recherchieren und in `quellen.json` ergänzen (mit Link) – sonst die Aussage weglassen.
Praxisempfehlungen werden mit `[[PRAXIS]]`, Herstellerangaben mit `[[HERSTELLER]]` gekennzeichnet.

## Dateien

| Datei | Bereich | Kürzel |
|---|---|---|
| `01_luftdichtheit.md` | Luftdichtheit (Raumluft soll nicht in die Konstruktion strömen) | LD |
| `02_feuchteschutz.md` | Feuchteschutz: Dampfbremse, Diffusion, Tauwasser, Austrocknung | FS |
| `03_waermeschutz_waermebruecken.md` | Wärmeschutz und Wärmebrücken | WB |
| `04_winddichtheit_hinterlueftung.md` | Winddichtheit · Hinterlüftung · Schlagregenschutz · geneigtes Dach (Teile A–D) | WH |
| `05_holzschutz.md` | Baulicher Holzschutz | HS |
| `06_konstruktion_holzrahmenbau.md` | Konstruktion – qualitative Plausibilität, keine Statik | KO |
| `07_zeichnungsqualitaet.md` | Zeichnungsqualität | ZQ |
| `08_dach_steildach.md` | **Bauteil-Katalog** Steildach: Tragsystem, First, Traufe, Ortgang, Lattung | DA |
| `09_wand_sockel.md` | **Bauteil-Katalog** Außenwand Holzrahmenbau, Sockel, Bodenaufbau | SO |
| `10_bauteildicken.md` | **Übliche Bauteildicken** (Praxis-Richtwerte aus Standardaufbauten) | RW |
| `07_zeichnungsqualitaet.md` → ZQ-06 | **Rechtschreibung** der Beschriftungen (Korrektur auch in der Skizze) | ZQ |
| `11_baustoffe.md` | **Geeignete Baustoffe je Einbaulage** (Empfehlung bei fehlender Materialangabe oder nicht funktionsfähiger Schicht) | BS |
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
5. **Fehlende Bauteile nach ihrer Funktion werten.** Das Detail wird geprüft, **wie es
   gezeichnet ist** – ein Ausführungsdetail muss vollständig sein.
   - Fehlt ein **funktional notwendiges Bauteil** (ohne das Regensicherheit, Lastabtrag,
     Luft-/Winddichtheit, Dämmebene oder Belüftung nicht funktionieren – z. B. Firstziegel
     und Firstlatte am First, Auflager einer Pfette, Unterkonstruktion einer Bekleidung),
     ist das ein **klarer Aufbaufehler** – auch wenn es „vielleicht geplant“ ist.
   - Fehlt **Zubehör** mit Schutzfunktion (z. B. Insektenschutz, Tropfkante), ist das eine
     **mögliche Auffälligkeit**.
   - Fehlen nur **Angaben** (Material, Produkt, Maß, Benennung), ist das ein
     **Verbesserungshinweis** oder „aus der Datei nicht prüfbar“.
   Welche Bauteile je Detailart notwendig sind, steht in den Bauteil-Katalogen (`08_…` ff.).
6. **Geltungsbereich beachten:** Jede Regel sagt unter **„Gilt für“**, für welche Bauart bzw.
   welches Fassadensystem sie gilt. Passt sie nicht zum Detail → nicht anwenden.
7. **Mehrere richtige Ausführungen anerkennen:** Es gibt für fast jedes Detail mehrere
   fachgerechte Lösungen (z. B. Trocken- oder Mörtelfirst, Pfetten- oder Sparrendach,
   Holzfaser- oder Bahnenunterdeckung). Geprüft wird, ob die **gezeichnete** Lösung die
   Funktionen erfüllt – nicht, ob sie einer bestimmten Musterlösung gleicht. Eine
   abweichende, aber funktionierende Ausführung ist **kein** Befund.
   **Verbesserung:** die für das gezeichnete Detail **am besten geeignete** Lösung vorschlagen
   und in die Korrekturskizze zeichnen (passend zu Tragsystem, Deckung, Schichtenfolge und
   vorhandenen Bauteilen – möglichst wenig ändern); sinnvolle Alternativen im Text nennen.
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

**Aussagesicherheit** je Befund: **hoch** (eindeutig dargestellt) · **mittel** (naheliegende
Deutung, andere möglich) · **gering** (mehrere Deutungen möglich) – mit kurzem Grund.

**Priorität** in der Maßnahmenliste (automatisch): hoch = klarer Aufbaufehler oder mögliche
Auffälligkeit bei LD/FS · mittel = übrige mögliche Auffälligkeiten · niedrig = Hinweise.

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

0. **Detailart und Tragsystem bestimmen** (z. B. First eines Pfettendachs, Traufe mit
   Fußpfette, Sockel einer Holzrahmenwand) und den passenden Bauteil-Katalog (`08_…` ff.)
   öffnen: **Welche Bauteile und Funktionen muss dieses Detail haben?** Jedes davon in der
   Zeichnung suchen – fehlt eines, Grundsatz 5 anwenden.
1. Schichtenaufbau von innen nach außen erkennen (Zeichnung **und** Legende); unklare
   Schichten als „unklar“ markieren. Bei Ecken beide Wände Schicht für Schicht vergleichen
   (ZQ-01) und Unterkonstruktionen bis zur Ecke verfolgen (KO-01, KO-05). An Anschlüssen
   jede Platte und Bahn bis zu ihrem tatsächlichen Ende verfolgen: Endet sie dort, wo ihre
   Funktion übergeben wird, oder läuft sie in das Nachbarbauteil hinein (KO-07)?
2. Jede Regel aller Bereiche durchgehen; Geltungsbereich prüfen.
3. Je Regel notieren: `erfüllt`, `nicht anwendbar` oder eine Einstufung – mit Kürzel.
4. Doppelbefunde zusammenführen (Grundsatz 8).
5. Für wichtige erfüllte Regeln kurz festhalten, was positiv ist – ohne Pauschalurteil.
