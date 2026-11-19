# 12 – Detailtypen: Aufbau verstehen und richtig ergänzen (DT)

**Zweck:** Der Skill soll **jedes** fachgerechte Detail prüfen können – nicht nur Beispiele, die
den Testzeichnungen ähneln. Dafür beschreibt dieser Katalog die **üblichen Detailtypen** im
Holzbau: woran man sie erkennt, welche Bauteile **in welcher Lage zueinander** dazugehören,
welche Varianten **gleichwertig richtig** sind und **wie fehlende Teile geometrisch richtig**
eingezeichnet werden. Zu jedem Typ gibt es eine **eigene Referenzskizze** (`referenz/*.png`,
schematisch, nicht maßstäblich) zum Anschauen.

> Regeln in eigenen Worten nach den angegebenen Quellen; keine fremden Zeichnungen kopiert.
> Die Skizzen zeigen **eine** richtige Lösung – andere Ausführungen mit denselben Funktionen
> sind ebenfalls richtig (Grundsatz 7). Maße sind übliche Werte bzw. „nach Tragwerksplanung“.

## DT-00 So wird ein Detail einem Typ zugeordnet

1. **Detailart** bestimmen (First, Traufe, Ortgang, Sockel, Ecke, Decke, Fenster, Attika …) –
   aus Titel, Lage der Schichten, Dachneigung, Gelände-/Fußbodenlinien.
2. **Konstruktion/Tragsystem** bestimmen – über die **Erkennungsmerkmale** der Typen unten
   (z. B. Firstpfette im Querschnitt sichtbar → Pfettendach; Sparren stoßen im First
   aneinander → Sparrendach; Kehlbalken → Kehlbalkendach; Dämmung über den Sparren →
   Aufsparrendämmung).
3. **Spuren fehlender Bauteile lesen:** Maße, Höhenkoten, Schraubenachsen oder Hinweislinien,
   die **ins Leere** laufen (an ihrem Ende ist kein Bauteil gezeichnet), zeigen fast immer auf ein
   **fehlendes Bauteil** – z. B. ein Höhenmaß in der Firstachse, das in der Dämmung endet
   (= Oberkante der fehlenden Firstpfette), oder Schrauben, die schräg aus den Sparren nach
   unten in den Raum laufen (= Sparren-Pfetten-Verschraubung ohne Pfette). Das fehlende Bauteil
   **genau dort** einzeichnen, wo diese Spuren enden.
4. **Sparrendach erst, wenn die Firstverbindung eindeutig ist:** Fehlt am First eine Pfette, gilt
   das Dach nur dann als Sparren-/Kehlbalkendach, wenn eine **Firstverbindung als Bauteil
   gezeichnet und beschriftet** ist (Laschen, Zange, Scherzapfen, Blatt) oder Legende/Titel es
   nennen. **Schrauben allein, ein stumpfer Sparrenstoß oder eine Fuge reichen nicht** – dann ist
   die Konstruktion **nicht eindeutig** → Rückfrage K0 (mit den gefundenen Spuren als Hinweis,
   z. B. „Ein Höhenmaß in der Firstachse endet ohne Bauteil – Pfettendach mit Firstpfette?“).
5. **Lässt sich die Konstruktion nicht eindeutig zuordnen** (z. B. am First weder Pfette noch
   Sparrenverbindung, unklar ob Dachraum beheizt), **immer vor der Prüfung nachfragen**
   (Checkliste K1) – nicht raten (Entscheidung Nutzer 18.11.2026). Erst nach der Antwort
   prüfen und die Korrekturskizze nach dem passenden Typ zeichnen.
6. Weicht das Detail von allen Typen ab, aber erfüllt es die **Funktionen** (Lastabtrag,
   Regensicherheit, Wind-/Luftdichtheit, Dämmung, Belüftung, Holzschutz) erkennbar, ist es
   **kein Befund** – nach den Funktionsregeln (Kataloge 01–07) prüfen.
7. **Geometrie nie schätzen:** Kanten, Neigungen und Schnittpunkte mit
   `python scripts/linien.py` aus der Vektorzeichnung lesen (siehe SKILL.md, Schritt 1).

---

## Teil A – Steildach

### DT-D1 First, Pfettendach, Zwischensparrendämmung (Raum bis unter den First beheizt)

- **Erkennen:** Firstpfette (Kantholz/BSH, im Querschnitt mit Kreuz) unter den Sparren in der
  Firstachse; Sparren liegen links und rechts auf der Pfette auf (stumpf gestoßen, oft mit Fuge).
- **Hinweise auf eine fehlende Firstpfette:** Sparren stoßen im First stumpf oder mit Fuge
  aneinander, ohne gezeichnete Firstverbindung; schräge Schraubenachsen (z. B. Tellerkopf- bzw.
  Vollgewindeschrauben) laufen aus den Sparren nach unten ins Leere; ein Höhenmaß in der
  Firstachse endet ohne Bauteil; die Firstfuge läuft bis in den Raum.
- **Bauteile von außen nach innen:** Firstziegel auf Firstlatte mit Firstlattenhaltern,
  Lüftungselement mit Insektenschutz (Abluft mind. 0,5 ‰ der Dachfläche, mind. 50 cm²/m
  [[IDH-HOLZSCHUTZ]]) · Deckung · Trag-/Konterlattung · Unterdeckung bis über den First ·
  Sparren mit Volldämmung **bis an die Pfette** (keine Hohlräume) · **Firstpfette** · luftdichte
  Ebene/Dampfbremse **an die Pfette luftdicht angeschlossen** (abgeklebt) oder unter der Pfette
  durchgeführt · Installationsebene · Bekleidung.
- **Geometrie (so einzeichnen):**
  - Pfettenmitte **auf der Firstachse** (Schnittpunkt der Dachflächen, mit `linien.py
    --schnitt` aus den beiden Deckungs- oder Unterdeckungslinien).
  - **Oberkante Pfette – in dieser Reihenfolge bestimmen:**
    1. **Maß oder Kote der Zeichnung**, das in der Firstachse endet (z. B. Höhenmaß von der
       Firstspitze nach unten, das ohne Bauteil in der Dämmung endet) → Oberkante genau am
       Maßende (mit `linien.py` die Maßlinie und ihr Ende auslesen).
    2. Angabe in Legende/Text (z. B. „Sparren aufgekervt“, Kervtiefe).
    3. Sonst: Schnittpunkt der beiden Sparren-Unterkanten in der Firstachse (`linien.py
       --schnitt`); die Sparren liegen dann mit einer Kerve auf (Kervtiefe nach
       Tragwerksplanung) [[BAUNETZ-PFETTENDACH]].
    Die Pfettenoberkante liegt damit **innerhalb der Sparrenhöhe** (Sparren aufgekervt), die
    Pfette reicht nach unten **unter** den Innenaufbau.
  - Querschnitt aus Legende/Bemaßung, sonst „nach Tragwerksplanung“ (Praxis z. B. 14/28,
    hochkant) [[PRAXIS]]. Die Pfette **hängt nach unten** aus dem Innenaufbau (Sichtpfette)
    oder wird bekleidet – **nie** oben in der Dämmebene oder in der Unterdeckung.
  - Innenaufbau (Dampfbremse, Installationsebene, Bekleidung) endet seitlich an der Pfette:
    Teile, die in die Pfette laufen, mit `entfernen` abdecken; Dampfbremse mit `abklebung` an
    die Pfettenflanke anschließen.
  - Firstabdeckung nach DA-02 (`firstziegel`, `firstlatte` mit `halter_bis`).
- **Varianten (richtig):** Pfette bekleidet (Bekleidung läuft unter der Pfette durch, Dampfbremse
  über die Pfette geführt); Firstpfette mit Firstsäulen (einfach stehender Stuhl) bzw. zusätzlich
  Mittelpfetten (zweifach stehend) [[BAUNETZ-PFETTENDACH]].
- **Typische Fehler:** Pfette fehlt (Lastabtrag, DA-01); Pfette in der Dämmebene gezeichnet;
  Dämmlücke über der Pfette; Dampfbremse endet ohne Anschluss an der Pfette (LD-02).
- **Referenzskizze:** `referenz/first_pfettendach.png`

### DT-D2 First, Sparrendach bzw. Kehlbalkendach (ohne Firstpfette)

- **Erkennen:** Keine Firstpfette; die Sparren eines Paars stoßen in der Firstachse aneinander
  und stützen sich gegenseitig (Sparrendach); oft ein waagerechter Kehlbalken zwischen den
  Sparren (Kehlbalkendach) [[BAUNETZ-SPARRENDACH]], [[BAUNETZ-KEHLBALKENDACH]].
- **Bauteile:** wie DT-D1 außen; **Firstverbindung** der Sparren (z. B. Scherzapfen, Blatt
  oder beidseitige Laschen – Art nach Tragwerksplanung) [[PRAXIS]]; Volldämmung zwischen
  den Sparren bis in den First; luftdichte Ebene **unter den Sparren durchgehend über den
  First** (am Firstpunkt geknickt, nicht unterbrochen).
- **Geometrie:** Sparren-Oberkanten und -Unterkanten treffen sich in der Firstachse; die
  Firstverbindung liegt **innerhalb der Sparrenhöhe** (zwischen Unterdeckung und luftdichter
  Ebene). Bei Laschen: zwei Laschen im Längsschnitt als `holz` mit `schnitt: laengs`
  beiderseits der Achse, Höhe ≈ Sparrenhöhe. Fußpunkt zugfest (Deckenbalken/Decke) – im
  Firstdetail nur im Text.
- **Kehlbalkendach mit Spitzboden:** Dämmung und luftdichte Ebene laufen **in der
  Kehlbalkenlage** waagerecht durch, der Spitzboden darüber ist kalt und belüftet (DT-D3).
- **Typische Fehler:** keine Firstverbindung erkennbar (DA-01); luftdichte Ebene am First offen.
- **Referenzskizze:** `referenz/first_sparrendach.png`

### DT-D3 First über kaltem, nicht ausgebautem Dachraum / Spitzboden

- **Erkennen:** Dämmebene liegt tiefer (oberste Geschossdecke bzw. Kehlbalkenlage); im First
  nur Sparren, Firstpfette (falls Pfettendach), Unterdeckung, Lattung, Deckung.
- **Pflicht:** Unterdeckung am First mit **Lüftungsschlitz ca. 10 cm**, gegen Flugschnee und
  Insekten geschützt, ohne den Lüftungsquerschnitt einzuschränken; alternativ Querlüftung von
  Giebel zu Giebel [[IDH-HOLZSCHUTZ]].
- **Typischer Fehler:** Unterdeckung über den First geschlossen bei kaltem Dachraum.

### DT-D4 Traufe, Pfettendach (Fußpfette/Rähm auf der Wand)

- **Erkennen:** Sparren liegen auf einer Fußpfette bzw. auf dem Rähm der Außenwand;
  Dachüberstand mit Sparrenköpfen oder Kastengesims.
- **Bauteile:** Rinne mit Traufblech/Einlaufblech · Traufbohle · Lüftungsgitter (Zuluft mind.
  2 ‰ der Dachfläche, mind. 200 cm²/m ≈ 2 cm Spalt) · Unterdeckung auf das Traufblech
  geführt · Sparrenkopf „unter Dach“ (innerhalb der 60°-Linie) · Fußpfette/Rähm nach Statik ·
  Stellbrett/Randholz zwischen den Sparren als Dämmabschluss · Dämmung von Wand und Dach
  ohne Lücke verbunden · **luftdichter Anschluss** Dachfolie ↔ Wand (Folie/Klebeband)
  [[IDH-HOLZSCHUTZ]], [[BAUNETZ-TRAUFE]].
- **Geometrie:** Fußpfette/Rähm sitzt **auf der Wandkrone** (Oberkante Wand = Unterkante
  Pfette), Sparren-Unterkante liegt auf der Pfette (Kerve); Stellbrett **zwischen** den Sparren
  in Flucht der Wand-Außenkante; Dachüberstand-Untersicht mit Überdämmung ≥ 30 mm bei
  Holzwerkstoffplatten empfohlen [[IDH-HOLZSCHUTZ]].
- **Varianten:** freiliegende Sparrenköpfe; Kastengesims; Aufschiebling; Dachüberstand aus
  Massivholzplatte.
- **Referenzskizze:** `referenz/traufe_pfettendach.png`

### DT-D5 Traufe, Sparrendach (Sparrenfuß auf Deckenbalken/Decke)

- **Erkennen:** Sparrenfuß steht auf einem Deckenbalken bzw. einer Schwelle auf der Decke;
  kein Pfettenauflager.
- **Pflicht:** **zugfeste** Verbindung Sparrenfuß ↔ Deckenbalken/Decke (unverschiebliches
  Dreieck) [[BAUNETZ-SPARRENDACH]]; sonst wie DT-D4 (Belüftung, Unterdeckung, Luftdichtheit).
- **Typischer Fehler:** Sparrenfuß ohne Auflager/Zugverbindung (DA-01, KO-06).

### DT-D6 Ortgang (Giebelwand)

- **Erkennen:** Schnitt parallel zur Traufe; Dachfläche endet seitlich über einer Giebelwand.
- **Bauteile:** seitlicher Abschluss der Deckung (Ortgangziegel oder Ortgangbrett mit
  Abdeckung) · Unterdeckung bis zur Außenkante · Rähm auf dem Ständerwerk der Giebelwand ·
  Dachplatte/Dach-OSB liegt **auf** dem Rähm · Dämmung des Daches bis an die Wand ·
  Abluft der Fassaden-Hinterlüftung unter dem Überstand · oberste Befestigungslatte der
  Fassade · luftdichter Anschluss Wand ↔ Dach (DA-05) [[BAUNETZ-UNTERDECKUNG-RAND]],
  [[BAUNETZ-HOLZRAHMENBAU]].
- **Geometrie:** Rähm in Tiefe des Ständerwerks unmittelbar unter der Dachplatte; Überstand als
  Flugsparren/Ortgangleiter oder auskragende Platte (Pfetten-/Sparrenköpfe außerhalb „unter
  Dach“ abdecken) [[IDH-HOLZSCHUTZ]].
- **Referenzskizze:** `referenz/ortgang.png`

### DT-D7 Aufsparrendämmung (Variante für First, Traufe, Ortgang)

- **Erkennen:** durchgehende druckfeste Dämmplatten **über** den Sparren; Sparren sichtbar
  oder unter Sichtschalung.
- **Bauteile (von außen):** Deckung · Lattung · **tragende** Konterlattung (z. B. 40/60) ·
  Unterdeckbahn falls erforderlich · Aufdachdämmung (druckfest, z. B. Holzfaser Typ DAD) ·
  Dampfbremse/luftdichte Ebene auf der Schalung · Schalung bzw. Massivholzplatte · Sparren
  [[IDH-HOLZSCHUTZ]].
- **Geometrie:** Luftdichte Ebene liegt **auf** der Schalung (nicht unter den Sparren); am
  First läuft sie über den First, an der Traufe an die Wand angeschlossen. Holzbauteile liegen
  raumseitig der Dämmung.
- **Typischer Fehler:** Dampfbremse unter den Sparren und zusätzlich Aufdachdämmung ohne
  Nachweis (Doppel-Dampfbremse).

---

## Teil B – Außenwand Holzrahmenbau

### DT-W1 Sockel

- **Pflicht:** Abstand Unterkante Holz (Schwelle, Bekleidung) – Gelände **≥ 30 cm**; ≥ 15 cm
  mit Kiesbett (16/32, Breite ≥ 30 cm) oder wasserableitendem Belag mit ≥ 2 % Gefälle; ≥ 5 cm
  nur mit zusätzlicher Abdichtung nach DIN 18533 [[IDH-HOLZSCHUTZ]], [[DIN-68800-2]].
  Schwelle als trockenes Vollholz auf **kraftschlüssiger Unterfütterung** (schwindarmer Mörtel),
  **Horizontalabdichtung** unter der Schwelle, **luftdichter Anschluss** Wand ↔ Bodenplatte,
  Perimeterdämmung mit Sockelputz im Spritzwasserbereich [[IDH-HOLZSCHUTZ]].
- **Geometrie:** Schwelle in Breite des Ständerwerks unmittelbar auf Unterfütterung/Abdichtung;
  Bekleidung endet mit Abstand über Gelände; Bodenaufbau innen nach SO-04;
  **Sauberkeitsschicht unter Fundament und ganzer Sohle** – Abschnitte einzeln prüfen (KO-08)
  [[BAUPROFESSOR-SAUBERKEITSSCHICHT]].
- **Varianten:** Betonaufkantung (GOK ≤ OKFF), Rinne mit Gitterrost an Türen
  [[IDH-HOLZSCHUTZ]].
- **Referenzskizze:** `referenz/sockel.png`

### DT-W2 Außen- und Innenecke

- **Pflicht:** Ständerwerk an der Ecke so, dass **beide** Beplankungen innen ein Auflager haben
  (Eckständer/Zulage); Dämmung bis in die Ecke; luftdichte Ebene an der Innenecke geschlossen
  (Plattenstoß abgeklebt); Unterkonstruktion der Fassade an der Ecke; Eckausbildung der
  Bekleidung nach Fachregel 01 [[FACHREGEL-01]], [[DATAHOLZ-AW]] (siehe KO-01, KO-02, KO-05, LD-02).
- **Erkennen:** Horizontalschnitt mit zwei Wänden im rechten Winkel. Eine Wand läuft bis zur
  Außenecke durch (Endständer über die volle Gefachtiefe), die andere stößt **stumpf** gegen deren
  Ständerebene (ihr Endständer liegt dort an).
- **Geometrie (Prinzip, KO-09):** Der Plattenrand der raumseitigen Beplankung der durchlaufenden
  Wand endet dort, wo die stoßende Wand beginnt – **direkt dahinter** liegt ein Zusatzstiel/eine
  Zulage im Gefach, **raumseitig bündig** mit der Ständerebene und **am Endständer der stoßenden
  Wand** anliegend (Anschluss nach Statik). **Außen vor dem Zusatzstiel läuft die Dämmung weiter.**
  Der Plattenrand der stoßenden Wand liegt auf deren Endständer. Luftdichte Ebene: OSB der einen
  Wand → Eckstoß abgeklebt → OSB der anderen Wand. Fassadenlatten beidseits unmittelbar an der
  Außenecke; winddichte Platte bis zur Ecke.
- **Varianten:** versetzter Endständer, Eckausbildung aus drei Ständern, gespiegelte Lösung
  (die andere Wand läuft durch) – richtig, wenn KO-01, KO-09 und LD-02 erfüllt sind.
- **Referenzskizze:** `referenz/ecke_aussen.png`

### DT-W3 Geschossdecke an Außenwand

- **Pflicht:** Deckenbalken bzw. Deckenplatte auf Rähm/Wand oder in Balkenschuh; **Randbohle**
  als Dämmabschluss; Dämmung am Deckenrand durchgehend; **luftdichte Ebene über die
  Deckenebene hinweg** geschlossen (z. B. Folienstreifen um die Randbohle oder
  durchlaufende Beplankung) [[BAUNETZ-LUFTDICHT]], [[DIN-4108-7]]; Fassade mit Hinterlüftung
  läuft durch.

---

## Teil C – Fenster und Türen im Holzrahmenbau

### DT-F1 Fensteranschluss (seitlich, oben, unten)

- **Grundsatz:** Anschlussfuge **innen luftdicht** (und dampfbremsend), **außen schlagregen- und
  winddicht**, die Windsperre umlaufend und nicht unterbrochen; die Fuge nimmt Bewegungen auf
  und muss Tauwasser vermeiden [[BAUNETZ-ANSCHLUSSFUGEN]], [[RAL-FENSTER]].
- **Bauteile:** Fenster in der **Dämmebene** (Flucht Ständerwerk) auf Montagezarge/Unterfütterung ·
  innen luftdichtes Anschlussband an die innere Beplankung (OSB) · Fuge gedämmt · außen
  Anschluss an die Fassadenbahn/Winddichtung (Band oder Folie) · **unten:** Fensterbank mit
  Gefälle nach außen, Tropfkante, seitliche Aufkantung; darunter zweite wasserführende Ebene
  (Abdichtung unter der Fensterbank, ins Fenster eingebunden) · **oben:** Sturz bzw. Rähm/
  Sturzholz im Ständerwerk; Hinterlüftung über dem Sturz mit Zu-/Abluft und Insektenschutz
  (WH-03) · Laibung innen bekleidet [[RAL-FENSTER]], [[PRAXIS]].
- **Typische Fehler:** Fenster vor der Dämmebene ohne Dämmung der Laibung; keine Abdichtung
  unter der Fensterbank; luftdichter Anschluss fehlt; Hinterlüftung über dem Fenster geschlossen.
- **Referenzskizze:** `referenz/fenster_unten.png`

---

## Teil D – Flachdach und Pultdach

### DT-FD0 Flachdach-Typ erkennen [[IDH-HOLZSCHUTZ]], [[IDH-FLACHDACH]]

| Typ | Aufbau | Hinweis |
|---|---|---|
| I | Dämmung **über** der Tragebene (Aufdachdämmung), darunter Dampfbremse auf der Schalung | robust; Luftdichtheitsebene oberhalb der Balkenlage, nicht auskragen lassen |
| II | Volldämmung zwischen den Balken **plus Überdämmung** und Behelfsabdichtung auf der Schalung | Überdämmung bauphysikalisch bemessen (Nachweis) |
| III | Volldämmung **nur** zwischen den Balken, eine Abdichtung | **Sonderkonstruktion**, nur kleinflächig mit Nachweis → mögliche Auffälligkeit, Nachweis erforderlich |
| IV | Volldämmung + **separate Belüftungsebene** über der Dämmung, Unterdeckung | Belüftungsweg ≤ 15 m, Lüftungshöhe nach Tabelle |
| V | Belüftung im Dachraum (flach geneigt) | nur bei funktionierender Belüftung |

### DT-FD1 Attika (Typ I, Aufdachdämmung)

- **Bauteile (von oben):** Abdichtung **über die Attika** geführt · Blechabdeckung auf Trennlage
  mit Gefälle nach innen · Gefälledämmung druckfest (DAA) · Behelfsabdichtung **bis OK Attika**
  hochgeführt · Dachschalung (Scheibe) · Balkenlage · Randbohle/Lagerholz · Luftdichtung mit
  Folienstreifen an die Wand ergänzt · Entwässerung (Attikaablauf + Notablauf) [[IDH-FLACHDACH]].
- **Referenzskizze:** `referenz/attika.png`

### DT-FD2 Dachrand mit Überstand (Typ II) und belüftetes Flachdach (Typ IV)

- **Typ II:** Behelfsabdichtung am Rand durchlaufend; tragende Massivholzplatte oder auskragende
  Sparren; Randbohle als Gurt; Dampfbremse luftdicht an die Wand angeschlossen
  [[IDH-FLACHDACH]].
- **Typ IV:** Lückenschalung mit Belüftungsschlitzen (Gaze) am Rand; Unterkonstruktion der
  Belüftungsebene; diffusionsoffene Unterdeckung über der Volldämmung; Dampfbremse
  sd ≥ 2 m, luftdicht [[IDH-FLACHDACH]].

### DT-P1 Pultdach – oberer Abschluss (Pultdachfirst)

- **Pflicht:** wie Traufe/First des belüfteten Steildachs: Abluftöffnung am oberen Rand
  (bei belüfteter Deckung Pultdachabschluss mind. 2 ‰ der Dachfläche, mind. 200 cm²/m)
  [[IDH-HOLZSCHUTZ]]; Abschlussblech mit Tropfkante; Unterdeckung über den Rand; Rähm/Pfette
  als Auflager; luftdichter Anschluss an die Wand.

---

## Grundlagen dieses Katalogs

[[IDH-HOLZSCHUTZ]] · [[IDH-FLACHDACH]] · [[BAUNETZ-PFETTENDACH]] · [[BAUNETZ-SPARRENDACH]] ·
[[BAUNETZ-KEHLBALKENDACH]] · [[BAUNETZ-BELUEFTET]] · [[BAUNETZ-LUFTDICHT]] ·
[[BAUNETZ-ANSCHLUSSFUGEN]] · [[RAL-FENSTER]] · [[BAUNETZ-HOLZRAHMENBAU]] · [[DIN-68800-2]] ·
[[DIN-4108-7]]. Wo eine Zeichnungs- oder Maßregel nur aus der Baupraxis stammt, ist sie mit
[[PRAXIS]] gekennzeichnet.
