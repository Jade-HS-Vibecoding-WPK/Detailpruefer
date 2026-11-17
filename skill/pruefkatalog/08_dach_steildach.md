# 08 – Bauteil-Katalog Steildach: Tragsystem, First, Traufe, Ortgang (DA)

**Zweck:** Dieser Katalog ist die „Bauteil-Datenbank“ für geneigte Dächer mit Ziegel- oder
Dachsteindeckung. Er sagt je Detailart, **welche Bauteile und Funktionen vorhanden sein
müssen**, welche **Ausführungsvarianten fachgerecht** sind (mehrere Wege sind richtig!),
woran man **Fehler** erkennt und wie die **am besten geeignete Korrektur** gezeichnet wird.

> **So benutzen:** (1) Detailart und Tragsystem bestimmen. (2) Die Pflichtbauteile der
> Detailart einzeln in der Zeichnung suchen. (3) Ist eine **andere anerkannte Variante**
> gezeichnet, ist das **kein** Befund. (4) Fehlt ein Pflichtbauteil → Grundsatz 5 in
> `00_uebersicht.md` (funktional notwendig → klarer Aufbaufehler). (5) Korrektur so wählen,
> dass sie zur gezeichneten Konstruktion passt und möglichst wenig ändert.
> **Keine Bemessung:** Querschnitte, Abstände, Lüftungsquerschnitte werden nicht berechnet.
> Maße nur aus Beschriftung/Legende übernehmen; fehlt ein Maß → „nach Tragwerksplanung“
> bzw. „nach Herstellerangabe“.

**Nicht hier geprüft (nur Verweis):** Belüftung allgemein → WH-06 · Regeldachneigung → WH-07 ·
Luftdichtheit → LD-02 · Dämmebene → WB-01 · Auflager → KO-06.

---

## DA-01 Tragsystem erkennen – Lastabtrag am First ist dargestellt

- **Gilt für:** First- und Traufdetails geneigter Holzdächer.
- **Prüfe:** Welches Tragsystem ist gezeichnet, und ist der Lastabtrag am First schlüssig?
- **Anerkannte Varianten:**
  - **Pfettendach:** Pfetten parallel zur Traufe tragen die Sparren; am First liegt eine
    **Firstpfette**, auf der die Sparren aufliegen (Kerve gering, Auflagerfläche ausreichend);
    die Pfette wird durch Stützen/Wände getragen [[BAUNETZ-PFETTENDACH]].
  - **Sparrendach:** Die beiden Sparren eines Paares **stützen sich im First gegenseitig**
    (Firstverbindung, z. B. Scherzapfen, Blatt, Laschen/Zange); die Fußpunkte sind über
    Deckenbalken bzw. Decke zugfest verbunden [[BAUNETZ-SPARRENDACH]]. Keine Firstpfette nötig.
  - **Kehlbalkendach:** Sparrendach mit Kehlbalken zwischen den Sparrenpaaren
    [[BAUNETZ-KEHLBALKENDACH]] – der Kehlbalken liegt meist außerhalb des Firstdetails.
- **So erkennst du es in der Zeichnung:** Beschriftung („Firstpfette“, „Zange“, „Laschen“),
  Holzquerschnitte mit Kreuz unter dem First, Verbindung der Sparrenköpfe, Maßangaben.
- **Typische Auffälligkeit:** Sparren enden am First ohne Pfette **und** ohne Verbindung
  untereinander; ein unbenanntes Bauteil in der Firstachse ohne erkennbare Tragfunktion;
  Pfette beschriftet, aber nicht gezeichnet (oder umgekehrt).
- **Warum relevant?** Ohne Auflager oder Firstverbindung ist der Lastweg der Sparren nicht
  ausführbar.
- **Mögliches Risiko:** Durchbiegen oder Abgleiten der Sparren am First; Risse in Bekleidung
  und Luftdichtheitsebene. Ob es trägt, kann nur die Tragwerksplanung beurteilen.
- **Beste Korrektur (wählen nach Zeichnung):**
  - Hinweise auf Pfettendach (Fußpfette im Traufdetail, Stützen, Beschriftung) oder kein
    eindeutiges System → **Firstpfette** unter dem First einzeichnen, Sparren darauf
    aufgelagert; Querschnitt aus Beschriftung, sonst „nach Tragwerksplanung“ –
    Werkzeug `holz` mit `querschnitt_cm`, `winkel` 0, mittig in der Firstachse.
  - Hinweise auf Sparrendach (Sparrenpaare, Decke als Zugband, Kehlbalken) → **Firstverbindung**
    der Sparren (z. B. beidseitige Laschen/Zange) – Werkzeug `holz`/`profil`.
  - Alternative im Text nennen.
- **Grundlage:** [[BAUNETZ-PFETTENDACH]], [[BAUNETZ-SPARRENDACH]], [[BAUNETZ-KEHLBALKENDACH]];
  Bemessung nach Eurocode 5 [[EC5]] (nicht Teil der Prüfung).
- **Einstufung:** Kein Lastabtrag am First erkennbar → **klarer Aufbaufehler** +
  **Nachweis erforderlich**. System erkennbar, Verbindung nur nicht beschriftet →
  **Verbesserungshinweis**. Querschnitt beschriftet ≠ gezeichnet → **mögliche Auffälligkeit**
  (KO-06).

## DA-02 Firstabdeckung: Firstziegel auf Firstlatte – regensicher und befestigt

- **Gilt für:** First (und sinngemäß Grat) von Ziegel- und Dachsteindeckungen.
- **Prüfe:** Ist der First **regensicher geschlossen** – Firstziegel bzw. Firststeine über
  dem First, getragen von einer Firstlatte auf Firstlattenhaltern, befestigt?
- **Pflichtbauteile:** Firstziegel/-steine (Kappe über beide Dachflächen) · Firstlatte
  (hochkant, typisch 30/50 oder 40/60 mm [[NELSKAMP-D13]]) · Firstlattenhalter (verbinden
  Latte mit Sparren bzw. Konterlattung) · Befestigung der Firstziegel (Firstklammern bzw.
  nach Herstellerangabe) · oberste Ziegelreihe beidseits bis unter den Firstziegel.
- **Anerkannte Varianten:** **Trockenfirst** mit Lüftungselement (heute üblich, belüftet) ·
  **Lüfter-Firstziegel** bzw. Formsteine [[BAUNETZ-FIRST]] · **Mörtelfirst** (älter; ohne
  Firstbelüftung – dann Abluft anders lösen, siehe DA-03) · Systemfirst des Herstellers.
- **So erkennst du es in der Zeichnung:** Über dem Schnittpunkt der beiden Deckungsflächen
  liegt eine Kappe; darunter ein kleiner Holzquerschnitt (Firstlatte) mit senkrechtem Halter.
- **Typische Auffälligkeit:** First **offen** – Deckung endet beidseits, dazwischen Lücke;
  Firstlatte ohne Halter „schwebend“; Firstziegel ohne Überdeckung der obersten Reihe.
- **Warum relevant?** Der First ist der wetterfeste Zusammenschluss der Dachflächen
  [[BAUNETZ-FIRST]]; ohne Firstabdeckung kann Regen und Flugschnee ungehindert eindringen.
- **Mögliches Risiko:** Wassereintrag in Konterlattungsebene und Dämmung; Durchfeuchtung.
- **Beste Korrektur:** Werkzeug `firstziegel` (Firstpunkt = Schnittpunkt der beiden
  Deckungsoberseiten, `richtung_links`/`richtung_rechts` je zwei Punkte auf der Deckung,
  `lueftung`: true) + `firstlatte` (Querschnitt aus Beschriftung, sonst [3, 5]; `halter_bis` =
  Oberkante Sparren bzw. Konterlatte in der Firstachse). Beschriftung: „Firstziegel mit
  Lüftungselement, Firstlatte auf Firstlattenhaltern, Befestigung nach Herstellerangabe“.
- **Grundlage:** [[BAUNETZ-FIRST]]; Fachregeln des Dachdeckerhandwerks [[ZVDH]];
  Verlegeanleitung des Ziegelherstellers [[NELSKAMP-D13]] bzw. [[HERSTELLER]].
- **Einstufung:** Firstabdeckung fehlt → **klarer Aufbaufehler** (funktional notwendig –
  auch wenn sie „geplant“ sein mag). Nur Firstlattenhalter oder Befestigung nicht
  dargestellt → **mögliche Auffälligkeit**.

## DA-03 Belüftung und Unterdeckung am First

- **Gilt für:** belüftete Steildächer (Konterlattungsebene unter der Deckung).
- **Prüfe:** Kann die an der Traufe einströmende Luft am First **abströmen**
  [[BAUNETZ-FIRST]] – Lüftungselement bzw. Lüfterziegel mit Insektenschutz? Ist die
  Unterdeckung am First regensicher geschlossen bzw. überlappt?
- **Anerkannte Varianten:** Unterdeckplatte (z. B. Holzfaser/MDF) über den First
  durchlaufend, Abluft aus der Konterlattungsebene über das Lüftungselement des
  Trockenfirsts · Unterdeckbahn je nach System mit Firstöffnung · Lüfterziegel in der Fläche.
- **Typische Auffälligkeit:** Belüftungsebene am First geschlossen (z. B. Mörtelfirst ohne
  andere Abluft); Unterdeckung am First offen ohne Überdeckung; Insektenschutz fehlt.
- **Warum relevant?** Ohne Abluft funktioniert die Belüftung unter der Deckung nicht (WH-06).
- **Mögliches Risiko:** Feuchte unter der Deckung; Tauwasser an der Unterseite der Ziegel.
- **Beste Korrektur:** Lüftungselement im First (`firstziegel` mit `lueftung`), Unterdeckung
  mit `bahn` (`unterdeckbahn`) bzw. `platte` schließen. Lüftungsquerschnitte **nicht**
  berechnen → „nach DIN 4108-3 bzw. Herstellerangabe nachweisen“ [[DIN-4108-3]].
- **Grundlage:** [[BAUNETZ-FIRST]]; [[ZVDH]]; [[DIN-4108-3]].
- **Einstufung:** Abluft eindeutig verschlossen → **mögliche Auffälligkeit**; nicht
  erkennbar → **aus der Datei nicht prüfbar**. Insektenschutz fehlt → **mögliche Auffälligkeit**.
- **Abgrenzung:** Zuluft an der Traufe → DA-04/WH-06.

## DA-04 Traufe: Wasserführung, Zuluft, Auflager

- **Gilt für:** Traufen geneigter Dächer.
- **Pflichtbauteile und Funktionen:**
  - **Unterdeckung bis in die Rinne:** über ein **Traufblech** geführt (kein Wassersack),
    Ende mit Tropf- oder Rinneneinlaufblech; Traufbleche auch bei verklebten/verschweißten
    Unterdeckungen [[BAUNETZ-UNTERDECKUNG-RAND]].
  - **Zuluft** in die Konterlattungsebene mit **Insektenschutz** (Lüftungskamm/-gitter)
    [[BAUNETZ-TRAUFE]].
  - **Anhebung der ersten Ziegelreihe** (Traufbohle, Traufanhebung bzw. Traufkeil), damit die
    erste Reihe in der Dachneigung liegt (Praxisempfehlung [[PRAXIS]], Herstellerangabe).
  - **Rinne** mit Rinnenhaltern; Rinneneinlaufblech.
  - **Auflager der Sparren** (Fußpfette, Rähm, Decke) → KO-06; Sparrenfeld gedämmt bis
    zur Wand → WB-01; Luftdichtheit Dach–Wand → LD-02; Winddichtheit Dach–Wand → WH-01.
- **Anerkannte Varianten:** Traufe mit Überstand, ohne Überstand oder einbezogen
  [[BAUNETZ-TRAUFE]]; Traufkeil oder Traufbohle; Lüftungskamm oder Lüftungsgitter.
- **Typische Auffälligkeit:** Unterdeckung endet vor der Rinne oder unter der Rinnenkante;
  kein Traufblech; Konterlattungsebene an der Traufe geschlossen; Zuluft ohne Insektenschutz.
- **Warum relevant?** Wasser von der Unterdeckung muss sicher in die Rinne geführt werden;
  die Belüftung beginnt an der Traufe.
- **Mögliches Risiko:** Wassersack und Durchfeuchtung der Traufe; Insektenbefall.
- **Beste Korrektur:** Traufblech als `profil` mit `dicke_cm` (z. B. 0,1–0,2) in die Rinne
  geführt; Lüftungsgitter als `bahn` `lueftungsband`; Traufbohle als `holz`.
- **Grundlage:** [[BAUNETZ-UNTERDECKUNG-RAND]]; [[BAUNETZ-TRAUFE]]; [[ZVDH]].
- **Einstufung:** Wasserführung der Unterdeckung in die Rinne fehlt eindeutig → **klarer
  Aufbaufehler**; Zuluft fehlt → **mögliche Auffälligkeit** (WH-06); Insektenschutz fehlt →
  **mögliche Auffälligkeit**.

## DA-05 Ortgang: seitlicher Abschluss regensicher und windsogsicher

- **Gilt für:** Ortgänge (seitlicher Dachrand am Giebel).
- **Pflichtbauteile und Funktionen:**
  - **Unterdeckung bis zur Außenkante** – sinnvoll bis zur Außenkante der Dachfläche,
    mindestens bis zur Außenkante der Wandbekleidung [[BAUNETZ-UNTERDECKUNG-RAND]].
  - **Seitlicher Abschluss der Deckung:** Ortgangziegel (Formziegel) **oder** Ortgangbrett/
    Windbrett mit Abdeckung (z. B. Blech) – je nach System [[NELSKAMP-D13]], [[ZVDH]].
  - **Befestigung/Windsogsicherung** der Randziegel (z. B. Sturmklammern bzw. Schrauben nach
    Fachregel und Hersteller) [[NELSKAMP-D13]].
  - **Konterlattung**, damit eingedrungenes Wasser abfließen kann – kritisch bei
    Sichtschalung am Ortgang [[BAUNETZ-UNTERDECKUNG-RAND]].
  - Abschluss der Dämmebene und Luftdichtheit an der Giebelwand → WB-01, LD-02.
- **Anerkannte Varianten:** Ortgangziegel links/rechts · Ortgangbrett (Windbrett) mit
  Blechabdeckung · Ortgang mit Überstand oder bündig.
- **Typische Auffälligkeit:** Deckung endet ohne seitlichen Abschluss; Unterdeckung endet vor
  der Wand; keine Befestigung der Randziegel dargestellt; Sichtschalung ohne Konterlattung.
- **Warum relevant?** Am Ortgang greift Wind besonders an; Regen darf nicht seitlich unter
  die Deckung gelangen.
- **Mögliches Risiko:** Abheben von Randziegeln bei Sturm; Wassereintrag in die Giebelwand.
- **Beste Korrektur:** Ortgangziegel als `profil` (Kappe mit seitlichem Schenkel) bzw.
  Ortgangbrett als `holz` + Blech als `profil` mit `dicke_cm`; Unterdeckung als `bahn`/`platte`
  bis zur Außenkante; Befestigung als Hinweistext.
- **Grundlage:** [[BAUNETZ-UNTERDECKUNG-RAND]]; [[NELSKAMP-D13]]; [[ZVDH]].
- **Einstufung:** Seitlicher Abschluss fehlt → **klarer Aufbaufehler**; Befestigung nicht
  dargestellt → **mögliche Auffälligkeit**; Unterdeckung endet zu früh → **mögliche
  Auffälligkeit** (eindeutig vor der Wand → klarer Aufbaufehler).

## DA-06 Schichtfolge der Deckung: Traglattung auf Konterlattung

- **Gilt für:** belüftete Ziegel-/Dachsteindeckungen.
- **Prüfe:** Liegt die Konterlattung (in Sparrenrichtung) auf der Unterdeckung und darauf die
  Traglattung (quer, im Lattabstand), darauf die Deckung? Sind die Latten im Schnitt richtig
  dargestellt (Traglatten als einzelne Querschnitte, Konterlatte als durchlaufendes Band)?
- **Typische Auffälligkeit:** Reihenfolge in Legende vertauscht; Traglatten fehlen; Deckung
  liegt direkt auf der Unterdeckung.
- **Beste Korrektur:** `lattenreihe` (Traglatten, `querschnitt_cm` aus Legende, Abstand nach
  Ziegel bzw. aus der Zeichnung) auf der Oberkante der Konterlattung; Konterlattung als `holz`
  mit `schnitt` `laengs`.
- **Grundlage:** [[ZVDH]]; Herstellerangaben [[NELSKAMP-D13]].
- **Einstufung:** Lattung fehlt → **klarer Aufbaufehler**; nur Legende vertauscht →
  **mögliche Auffälligkeit** (ZQ-01).
