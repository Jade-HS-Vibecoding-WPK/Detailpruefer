# 09 – Bauteil-Katalog Außenwand Holzrahmenbau und Sockel (SO)

**Zweck:** „Bauteil-Datenbank“ für Außenwände im Holzrahmenbau (Regelquerschnitt, Ecke,
Sockel). Sie nennt die **Pflichtbauteile und Funktionen**, **anerkannte Varianten**, typische
Fehler und die **beste Korrektur** samt Zeichenwerkzeug. Detailregeln stehen in den
Funktionskatalogen (LD, FS, WB, WH, HS, KO) – hier wird darauf verwiesen.

> **So benutzen:** wie `08_dach_steildach.md` – Pflichtbauteile einzeln suchen; andere
> anerkannte Variante ist **kein** Befund; fehlendes funktional notwendiges Bauteil →
> klarer Aufbaufehler (Grundsatz 5). Keine Bemessung, keine Berechnungen.

---

## SO-01 Außenwand: vollständige Schichtenfolge

- **Gilt für:** hinterlüftete Holzrahmenbau-Außenwände (Regelquerschnitt, Ecke, Anschlüsse).
- **Pflichtbauteile von außen nach innen (Funktion):**
  1. **Bekleidung** (Regenschutz) mit **Unterkonstruktion** (Lattung/Konterlattung) –
     auch an Ecken und Rändern → KO-05.
  2. **Hinterlüftungsebene** mit Zu- und Abluft und Insektenschutz → WH-02, WH-03.
  3. **Winddichte Ebene** außen auf der Dämmung (z. B. Holzfaserdämmplatte, Unterdeck-/
     Fassadenbahn), Stöße und Anschlüsse geschlossen → WH-01.
  4. **Tragendes Ständerwerk** mit Schwelle und Rähm; **Dämmung** im Gefach lückenlos → WB-01.
  5. **Aussteifende/luftdichte Ebene** raumseitig (z. B. OSB mit verklebten Stößen oder
     Dampfbremsbahn) → LD-01 bis LD-03, FS-01.
  6. **Installationsebene** (empfohlen) → LD-04.
  7. **Innenbekleidung**.
- **Anerkannte Varianten:** Beplankung außen (statt innen) aussteifend; Dampfbremsbahn statt
  OSB; WDVS auf Holzfaserplatte statt hinterlüfteter Bekleidung (dann andere WH-Regeln);
  ohne Installationsebene (dann Durchdringungen besonders beachten).
- **Typische Auffälligkeit:** Schicht fehlt in einer Wand der Ecke; winddichte Ebene endet vor
  der Ecke; Bekleidung ohne Unterkonstruktion an der Ecke; luftdichte Ebene nicht
  angeschlossen.
- **Beste Korrektur:** fehlende Platte mit `platte` und passender `schraffur`, fehlende
  Latten/Stiele mit `holz` bzw. `lattenreihe`, Dämmung mit `daemmung` (`art` nach Dämmstoff),
  Anschlüsse mit `abklebung`/`bahn`.
- **Grundlage:** siehe die verwiesenen Regeln; [[DIN-4108-7]]; [[DIN-68800-2]].
- **Einstufung:** funktional notwendige Schicht fehlt → **klarer Aufbaufehler**; nur in der
  Legende fehlend → **Verbesserungshinweis** (ZQ-03).

## SO-02 Sockel: Abstand des Holzes zum Gelände (Spritzwasser)

- **Gilt für:** Sockel von Holzrahmenbau-Wänden (Vertikalschnitt mit Gelände bzw. Belag).
- **Prüfe:** Liegt die **Unterkante der Holzkonstruktion** (Schwelle, unterste Bekleidung,
  Lattung) ausreichend hoch über der **Geländeoberkante bzw. Belagsoberkante**?
- **Regelwert:** Holzbauteile sollen **30 cm** Abstand zum Gelände haben (Spritzschutz)
  [[BAUNETZ-HOLZFASSADE]]. Geringere Abstände nur unter den in DIN 68800-2 genannten
  zusätzlichen Bedingungen (z. B. Kiesbett, Belag mit Gefälle, zusätzliche Abdichtung)
  [[DIN-68800-2]] – Bedingungen **nicht** aus dem Gedächtnis ergänzen, sondern als
  „zu prüfen“ benennen.
- **So erkennst du es in der Zeichnung:** Geländelinie/OK Gelände, Höhenkoten, Maßketten;
  Abstand im Maßstab ablesen (Zeichnungsprüfung, keine Berechnung).
- **Typische Auffälligkeit:** Schwelle bzw. Bekleidung reicht bis nahe ans Gelände; keine
  Geländelinie dargestellt.
- **Warum relevant?** Spritzwasser und Schnee befeuchten das Holz wiederholt.
- **Mögliches Risiko:** dauerhaft erhöhte Holzfeuchte kann Pilzbefall begünstigen.
- **Beste Korrektur:** Sockel erhöhen (z. B. Betonsockel/Aufkantung) oder Gelände absenken;
  unterste Bekleidung mit Abstand und Tropfkante; Kiesstreifen als Hinweis. Zeichnung:
  `entfernen` + `platte`/`profil` für Sockel, `text` mit Hinweislinie für den Abstand.
- **Grundlage:** [[BAUNETZ-HOLZFASSADE]]; [[DIN-68800-2]].
- **Einstufung:** Abstand eindeutig deutlich unter 30 cm ohne erkennbare Zusatzmaßnahme →
  **mögliche Auffälligkeit** (Zusatzbedingungen könnten erfüllt sein) + Hinweis; Holz im
  Erdreich bzw. auf Geländehöhe → **klarer Aufbaufehler**; keine Geländelinie →
  **aus der Datei nicht prüfbar**.

## SO-03 Sockel: Schwelle und Feuchteschutz gegen den Untergrund

- **Gilt für:** Anschluss Holzrahmenwand an Bodenplatte bzw. Sockel.
- **Pflichtbauteile und Funktionen:**
  - **Schwelle** auf ebenem Auflager (Ausgleich/Untermörtelung), **Trennlage bzw.
    Abdichtung** zwischen Beton und Holz gegen aufsteigende Feuchte (Praxisempfehlung
    [[PRAXIS]]; baulicher Holzschutz [[DIN-68800-2]]).
  - **Luftdichter Anschluss** der raumseitigen Ebene an die Bodenplatte → LD-02.
  - **Wärmebrücke** Sockel: Dämmung von Wand und Bodenplatte/Perimeter schließt an
    (Perimeterdämmung als `daemmung` `art` `hart`) → WB-01.
  - **Unterer Abschluss der Hinterlüftung** mit Insektenschutz und Tropfkante →
    WH-03 [[BAUNETZ-HOLZFASSADE]].
- **Anerkannte Varianten:** Schwelle auf Betonsockel/Aufkantung; Schwelle auf Bodenplatte mit
  Sockelabdichtung; Holzrahmenwand auf Streifenfundament mit Kriechkeller.
- **Typische Auffälligkeit:** Schwelle direkt auf Beton ohne Trennlage; luftdichte Ebene endet
  über der Bodenplatte; Bekleidung unten ohne Lüftungsöffnung/Insektenschutz; Dämmung von Wand
  und Bodenplatte schließt nicht an.
- **Beste Korrektur:** Trennlage/Abdichtung als `bahn` (`abdichtung`) unter der Schwelle und
  ggf. am Sockel hochgeführt; Anschluss der Luftdichtheitsebene als `abklebung`; Lüftungsgitter
  als `bahn` (`lueftungsband`); Perimeterdämmung als `daemmung` (`hart`).
- **Grundlage:** [[DIN-68800-2]]; [[DIN-4108-7]]; [[BAUNETZ-HOLZFASSADE]]; [[PRAXIS]].
- **Einstufung:** Trennlage/Abdichtung fehlt eindeutig → **klarer Aufbaufehler**; nur nicht
  beschriftet → **Verbesserungshinweis**; Insektenschutz fehlt → **mögliche Auffälligkeit**.
