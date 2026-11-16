# Prüfkatalog – Übersicht

Der Prüfkatalog enthält die Regeln, nach denen ein Detail geprüft wird.
**Maßstab sind deutsche Regeln (DIN, GEG).** Alle Regeln sind in eigenen Worten
zusammengefasst; Normtexte werden nicht wiedergegeben.

## Dateien

| Datei | Bereich | Kürzel | Stand |
|---|---|---|---|
| `01_luftdichtheit.md` | Luftdichtheit | LD | ✅ Teil 1 |
| `02_feuchteschutz.md` | Feuchteschutz, Diffusion, Tauwasser | FS | ✅ Teil 1 |
| `03_waermeschutz_waermebruecken.md` | Wärmeschutz und Wärmebrücken | WB | ✅ Teil 1 |
| `04_winddichtheit_hinterlueftung.md` | Winddichtheit, Hinterlüftung, Schlagregen | WH | ✅ Teil 2 |
| `05_holzschutz.md` | Konstruktiver Holzschutz | HS | ✅ Teil 2 |
| `06_konstruktion_holzrahmenbau.md` | Konstruktion (Plausibilität) | KO | ✅ Teil 2 |
| `07_zeichnungsqualitaet.md` | Legende ↔ Zeichnung ↔ Maßketten | ZQ | ✅ Teil 2 |

Brandschutz und Schallschutz: nur Abfrage über `checkliste.md` (C7, C8), keine Prüfung.

## So wird eine Regel angewendet

Jede Regel hat dasselbe Schema:

- **Prüfe** – was genau geprüft wird
- **So erkennst du es in der Zeichnung** – woran man es im Plan sieht
- **Fehlerbild** – wie ein Verstoß typischerweise aussieht
- **Warum ist das ein Fehler?** – die bauphysikalische/konstruktive Begründung
- **Mögliche Folgen** – welcher Bauschaden droht
- **Verbesserung** – wie man es richtig macht
- **Quelle** – Norm bzw. Regelwerk
- **Einstufung** – welche der vier Einstufungen (siehe unten) typischerweise passt

## Grundsätze der Prüfung

- **Qualitative Plausibilitätsprüfung – keine Berechnungen.** Es werden **keine** sd-, R-
  oder U-Werte, **kein** Temperaturfaktor f_Rsi und **kein** Tauwasser berechnet.
  Wenn ein Problem nur rechnerisch sicher beurteilt werden kann: das erklären, trotzdem einen
  passenden Hinweis geben, aber nichts rechnen. (Einfaches Aufaddieren von Maßketten zur
  Kontrolle der Zeichnung ist erlaubt – das ist keine bauphysikalische Berechnung.)
- **Nichts erfinden:** keine Schichten, Maße, Materialwerte oder Normanforderungen
  ergänzen oder schätzen. Normwerte nur nennen, wenn sie in diesem Katalog stehen.
- **Fehlende Zeichnungsangabe ≠ baulicher Mangel.** Fehlt eine Angabe, ist das in der Regel
  „nicht beurteilbar“ oder „Klärungsbedarf“ – außer das Fehlen ist selbst ein
  Planungsmangel (z. B. Luftdichtheitsschicht nirgends festgelegt).
- **Keine Pauschalaussagen** wie „Die Konstruktion ist sicher/normgerecht“.
- **Jeder Befund wird begründet:** Woran ist er in der Datei zu erkennen (Stelle, Linie,
  Symbol, Beschriftung, Legende)?

## Die vier Einstufungen

| Einstufung | Wann? | Was wird angegeben? | Markierung in der Zeichnung |
|---|---|---|---|
| **Aufbaufehler** | In der Zeichnung **klar erkennbar** falsch oder fehlend | Stelle, Begründung, Folgen, Verbesserung, Quelle | roter Kreis, **durchgezogen** (+ ggf. Schraffur) |
| **Risiko / Klärungsbedarf** | Fraglich; Darstellung mehrdeutig oder Information fehlt, die für ein Urteil nötig ist | Was ist fraglich? Welche Information/Prüfung fehlt? | roter Kreis, **gestrichelt** |
| **Verbesserungshinweis** | Kein klarer Mangel, aber eine sinnvolle Optimierung | Mögliche Verbesserung | roter Kreis, **gepunktet** (nur wenn ortsbezogen) |
| **Nicht beurteilbar** | Prüfung mit den vorhandenen Angaben nicht möglich | Welche Angabe bzw. welches Detail fehlt genau | keine Markierung |

## Vorgehen

1. Gehe **jede** Regel aller Bereichsdateien durch – auch wenn das Detail auf den ersten
   Blick korrekt wirkt.
2. Notiere zu jeder Regel: `erfüllt` oder eine der vier Einstufungen – mit Regel-Kürzel.
3. Jede Regel enthält einen Abschnitt **Einstufung** mit Hinweisen, welche Einstufung typisch ist.
4. Vergleiche die **Zeichnung mit der Legende**: Was die Legende verspricht, muss auch
   gezeichnet sein – und umgekehrt.
5. Erfüllte Regeln, die für das Detail wichtig sind, kurz als positiv erwähnen
   (aber ohne Pauschalurteil über die Gesamtkonstruktion).

## Quellen und Normausgaben

| Kurzbezeichnung | Inhalt |
|---|---|
| GEG | Gebäudeenergiegesetz (u. a. § 26 Luftdichtheit, Anlage 1 Referenzgebäude, Anlage 7 Bestand) |
| DIN 4108-2 | Mindestanforderungen an den Wärmeschutz (u. a. Mindestwärmeschutz an Wärmebrücken) |
| DIN 4108-3 | Klimabedingter Feuchteschutz (Tauwasser, Schlagregen, nachweisfreie Bauteile) |
| DIN 4108-7 | Luftdichtheit von Gebäuden – Planungs- und Ausführungsempfehlungen |
| DIN 4108 Beiblatt 2 | Wärmebrücken – Planungs- und Ausführungsbeispiele |
| DIN EN ISO 10456 | Bemessungswerte von Baustoffen (λ, μ) |
| DIN EN 15026 | Hygrothermische Simulation (Alternative zum Glaser-Verfahren) |
| DIN 68800-1/-2 | Holzschutz – Allgemeines; vorbeugende bauliche Maßnahmen |
| DIN 18516-1 | Hinterlüftete Außenwandbekleidungen |
| DIN EN 1995-1-1 | Eurocode 5 – Bemessung von Holzbauten (nur Verweis; Statik wird nicht geprüft) |

> Vor fachlicher Verwendung immer die **aktuell gültige Ausgabe** der Norm prüfen.
> Regeln mit dem Zusatz **(Faustregel)** stammen aus der Baupraxis und sind keine Normanforderung.
