# 11 – Geeignete Baustoffe je Einbaulage (Baustoff-Empfehlung, BS)

**Zweck:** Ist ein Bauteil **gezeichnet, aber ohne Material** angegeben (z. B. Dämmung im
Sparrenfeld ohne Beschriftung), oder ist eine Schicht **technisch nicht funktionsfähig**
(z. B. Dämmung viel zu dünn), dann nennt der Bericht **geeignete Baustoffe für genau diese
Einbaulage** – mit Quelle und üblicher Dicke aus `10_bauteildicken.md`.

> **Wichtig:** Das sind **Empfehlungen aus geprüften Standardaufbauten und Fachliteratur**,
> keine Produktwahl und kein Nachweis. Keine λ-, sd-, U- oder R-Werte nennen oder rechnen.
> Nur Baustoffe aus dieser Tabelle empfehlen; was hier fehlt → „Baustoff nach Planung bzw.
> Nachweis festlegen“. Herstellerzulassung/Verwendbarkeit immer als „nach Hersteller“ ergänzen.
> Die Darstellung in der Zeichnung (Schraffur) hat Vorrang: Eine weiche Dämmschraffur
> (Schlaufen) spricht für Faserdämmstoffe, eine harte (Zickzack) für Dämmplatten.

## BS-01 Fehlende Materialangabe → geeignete Baustoffe nennen

1. Im **Bauteil-Check** (SKILL.md, Schritt 1) je Schicht festhalten: **Material angegeben?**
   (Legende, Beschriftung, Schraffur eindeutig?).
2. Fehlt die Materialangabe, die **Einbaulage** bestimmen (Tabelle unten) und 2–4 geeignete
   Baustoffe aus derselben Zeile nennen. Mit der Schraffur abgleichen und Unpassendes
   weglassen (z. B. bei weicher Schraffur keine Hartschaumplatten).
3. **Wo im Bericht** (Entscheidung Nutzer 18.11.2026):
   - **Detail funktioniert technisch** (nur die Angabe fehlt) → kurze Empfehlung im
     Schichtenaufbau, Feld `empfehlung` der Schicht; dazu ein **Verbesserungshinweis**
     „Material nicht angegeben“ (ZQ-01).
   - **Detail funktioniert technisch nicht** (die Schicht gehört zu einem **klaren
     Aufbaufehler** oder ist **deutlich außerhalb des üblichen Bereichs**, z. B. Dämmung nur
     halb so dick wie üblich, oder ein Pflichtbauteil fehlt) → **eigener Abschnitt
     „Baustoff-Empfehlungen“** (Feld `baustoff_empfehlungen` in `befunde.json`), mit Bezug
     auf den Befund; im Schichtenaufbau nur „→ siehe Baustoff-Empfehlungen“.
4. Die **Einstufung** des Befunds richtet sich weiter nach den übrigen Regeln (z. B. RW-01:
   Dicke deutlich außerhalb üblich = mögliche Auffälligkeit). Die Empfehlung ändert die
   Einstufung nicht.
- **Grundlage:** [[DATAHOLZ-AW]], [[DATAHOLZ-SD]], [[DATAHOLZ-GD]], [[BAUNETZ-HOLZFASERDAEMMUNG]],
  [[BAUNETZ-PERIMETERDAEMMUNG]], [[DIN-4108-10]] (Anwendungsgebiete, z. B. DZ = Zwischensparrendämmung,
  DAD = Außendämmung Dach unter Deckung, WAB = Außendämmung Wand hinter Bekleidung, PB = unter
  Bodenplatte; Kurzzeichen erläutert in [[BAUNETZ-DAEMMSTOFF-ANWENDUNG]]).
- **Einstufung:** Material fehlt, Detail funktioniert → **Verbesserungshinweis**.

## Dämmstoffe

| Einbaulage | geeignete Baustoffe (Auswahl) | Hinweise | Quelle |
|---|---|---|---|
| **Sparrenfeld** (Zwischensparrendämmung, Anwendungsgebiet DZ) | Mineralwolle (Glas-/Steinwolle) als Klemmfilz/Matte · Zellulosefaser (eingeblasen) · Schafwolle · Holzfaser-Dämmmatte (flexibel) | **volle Sparrenhöhe** ausfüllen; weiche Schraffur = Faserdämmstoff; innen Dampfbremse/luftdichte Ebene (LD/FS) | [[DATAHOLZ-SD]], [[BAUNETZ-HOLZFASERDAEMMUNG]], [[DIN-4108-10]] |
| **Gefach Holzrahmenwand** | Mineralwolle · Zellulosefaser (eingeblasen) · Schafwolle · Holzfaserdämmung | Gefach vollständig füllen (Ständerbreite) | [[DATAHOLZ-AW]], [[BAUNETZ-HOLZFASERDAEMMUNG]] |
| **Installationsebene** (Wand/Dach) | Mineralwolle · Zellulosefaser · Schafwolle · Holzfaserdämmung · oder ungedämmt (Luftschicht) | gedämmt oder leer – beides üblich; Dämmung innen der Dampfbremse → FS-05 | [[DATAHOLZ-AW]], [[DATAHOLZ-SD]] |
| **Über den Sparren** (Unterdeckplatte / Aufsparrendämmung, DAD) | Holzfaserdämmplatte (Unterdeckplatte, druckfest) | harte Schraffur (Zickzack); regensichere Ausführung nach Hersteller | [[DATAHOLZ-SD]], [[BAUNETZ-HOLZFASERDAEMMUNG]] |
| **Außendämmung Wand** unter Putz (WDVS) | Holzfaserdämmplatte (WDVS-geeignet) | nur als System nach Hersteller/Zulassung [[HERSTELLER]] | [[BAUNETZ-HOLZFASERDAEMMUNG]] |
| **Trittschalldämmung** unter schwimmendem Estrich | Mineralwolle-Trittschalldämmplatte (MW-T) · Holzfaser-Trittschalldämmung | geschlängelte Schraffur bei dünnen weichen Lagen | [[DATAHOLZ-GD]], [[BAUNETZ-HOLZFASERDAEMMUNG]] |
| **Perimeter / unter Bodenplatte / erdberührt** (PB) | XPS · Schaumglas · EPS nur mit bauaufsichtlicher Zulassung als Perimeterdämmung (nicht bei drückendem Wasser) | feuchtebeständig, verrottungsfest, frostbeständig, druckstabil; **keine** Faserdämmstoffe | [[BAUNETZ-PERIMETERDAEMMUNG]] |
| **Dämmung unter Estrich auf Bodenplatte** | kein belegter Katalog – nach Wärmeschutznachweis und Hersteller | – | – |

## Plattenwerkstoffe

| Einbaulage | geeignete Baustoffe | Hinweise | Quelle |
|---|---|---|---|
| Außenbeplankung Holzrahmenwand (hinter Hinterlüftung) | MDF-Platte (diffusionsoffen) · Gipsfaserplatte | außen diffusionsoffener als innen (FS-01) | [[DATAHOLZ-AW]] |
| Innenbeplankung, aussteifend/luftdicht | OSB-Platte (Stöße luftdicht verklebt) | luftdichte Ebene → LD | [[DATAHOLZ-AW]] |
| Innenbekleidung | Gipsplatte (GKF/Typ DF) · Gipsfaserplatte | – | [[DATAHOLZ-AW]], [[DATAHOLZ-SD]] |
| Unterdeckung Dach | Holzfaser-Unterdeckplatte · Unterdeckbahn | bis zur Außenkante (DA-05) | [[DATAHOLZ-SD]], [[BAUNETZ-UNTERDECKUNG-RAND]] |

## Bahnen, Hölzer und sonstige Bauteile

| Einbaulage | Empfehlung | Quelle |
|---|---|---|
| Luftdichte Ebene / Dampfbremse | OSB mit verklebten Stößen **oder** Dampfbremsbahn; Anschlüsse mit Klebeband nach Hersteller | [[DATAHOLZ-SD]], [[DIN-4108-7]], [[HERSTELLER]] |
| Winddichtung hinter offener Fassade | Fassadenbahn nach Hersteller (bei offenen Fugen UV-beständig) | [[HERSTELLER]] |
| Lattung/Konterlattung, Sparren, Rähm, Schwelle | Nadelholz; Querschnitte siehe `10_bauteildicken.md`, tragende Querschnitte nach Tragwerksplanung | [[DATAHOLZ-AW]], [[DATAHOLZ-SD]], [[EC5]] |
