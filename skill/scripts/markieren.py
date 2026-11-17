"""Zeichnet Befunde als farbige Kreise mit Nummern-Badge und Führungslinie in eine PDF-Zeichnung.

Die Originalzeichnung bleibt als Vektor-PDF erhalten; die Markierungen liegen als eigene Ebene darüber.

Aufruf:
    python markieren.py <zeichnung.pdf> <befunde.json> <ausgabe.pdf>

Koordinaten sind Prozentwerte: x = 0 (links) … 100 (rechts), y = 0 (oben) … 100 (unten),
r in % der Blattbreite.

Einstufung → Farbe und Linienart (passend zur Übersicht im Bericht):
    aufbaufehler    = Rot,    durchgezogen
    auffaelligkeit  = Orange, gestrichelt
    hinweis         = Blau,   gepunktet
    nicht_pruefbar  = keine Markierung

Je Befund:
    "kreis":  {"x", "y", "r"}           Kreis um die Stelle (r mindestens 1,5 %)
    "badge":  {"x", "y"}                Position des Nummern-Badges im freien Bereich
                                        neben der Zeichnung; Führungslinie wird gezogen.
                                        Ohne Angabe: automatisch schräg außerhalb des Kreises.
    "schraffur": [[x, y], …]            optionale Fläche (schwache Schraffur in der Befundfarbe)
Zusätzlich auf oberster Ebene:
    "beschriftungen": [{"text": "Wand A", "x": …, "y": …}]   z. B. Wandbezeichnungen
"""
import io
import json
import math
import sys

from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FARBEN = {
    "aufbaufehler": HexColor("#C62828"),
    "auffaelligkeit": HexColor("#E07B00"),
    "hinweis": HexColor("#1F6FB2"),
    "nicht_pruefbar": HexColor("#6B7280"),
}
GRAU_DUNKEL = HexColor("#1F2937")
R_MIN = 1.5  # Mindestradius in % der Blattbreite


def einstufung_normalisieren(wert):
    """Vereinheitlicht verschiedene Schreibweisen der Einstufung."""
    w = str(wert or "aufbaufehler").lower().replace("ä", "ae").replace("ü", "ue").replace(" ", "_")
    if w.startswith("nicht") or "pruefbar" in w:
        return "nicht_pruefbar"
    if w.startswith("auff") or w.startswith("risiko") or w.startswith("moegl"):
        return "auffaelligkeit"
    if w.startswith("hinweis") or w.startswith("verbess"):
        return "hinweis"
    return "aufbaufehler"


def befunde_lesen(daten):
    """Akzeptiert das aktuelle Format ("befunde") und das alte ("maengel")."""
    return daten.get("befunde") or daten.get("maengel") or []


def befund_kennung(b):
    """Anzeige-Nummer eines Befunds, z. B. 'B3'."""
    nr = str(b.get("nr", "?"))
    return nr if nr.upper().startswith("B") else f"B{nr}"


def strichart(einstufung, linie):
    if einstufung == "auffaelligkeit":
        return [linie * 4, linie * 2.5]
    if einstufung == "hinweis":
        return [linie * 0.1, linie * 2.2]
    return []


def zeichne_befund(c, b, pt, w):
    e = einstufung_normalisieren(b.get("einstufung"))
    farbe = FARBEN[e]
    linie = max(1.3, w * 0.0017)
    k = b["kreis"]
    px, py = pt(k["x"], k["y"])
    r = max(k.get("r", 3), R_MIN) / 100 * w

    # Schraffur (schwach, in Befundfarbe)
    if b.get("schraffur"):
        punkte = [pt(x, y) for x, y in b["schraffur"]]
        c.saveState()
        pfad = c.beginPath()
        pfad.moveTo(*punkte[0])
        for p in punkte[1:]:
            pfad.lineTo(*p)
        pfad.close()
        c.clipPath(pfad, stroke=0, fill=0)
        c.setStrokeColor(Color(farbe.red, farbe.green, farbe.blue, alpha=0.55))
        c.setLineWidth(max(0.5, w * 0.0006))
        xs = [p[0] for p in punkte]
        ys = [p[1] for p in punkte]
        hoehe = max(ys) - min(ys)
        t = -hoehe
        while t <= max(xs) - min(xs):
            c.line(min(xs) + t, min(ys), min(xs) + t + hoehe, max(ys))
            t += max(2.5, w * 0.0035)
        c.restoreState()

    # Kreis ohne Füllung
    c.setStrokeColor(farbe)
    c.setLineWidth(linie)
    c.setLineCap(1)
    c.setDash(strichart(e, linie))
    c.circle(px, py, r, stroke=1, fill=0)
    c.setDash([])

    # Badge-Position: vorgegeben oder automatisch schräg nach außen
    br = max(8.0, w * 0.0105)
    if b.get("badge"):
        bx, by = pt(b["badge"]["x"], b["badge"]["y"])
    else:
        richtung = {"oben-rechts": (1, 1), "oben-links": (-1, 1), "unten-rechts": (1, -1),
                    "unten-links": (-1, -1)}.get(b.get("nummer_position", "oben-rechts"), (1, 1))
        abstand = r + w * 0.045
        bx = px + richtung[0] * abstand * 0.707
        by = py + richtung[1] * abstand * 0.707

    # Führungslinie vom Kreisrand zum Badge
    winkel = math.atan2(by - py, bx - px)
    sx, sy = px + r * math.cos(winkel), py + r * math.sin(winkel)
    dist = math.hypot(bx - sx, by - sy)
    if dist > br:
        ex, ey = bx - br * math.cos(winkel), by - br * math.sin(winkel)
        c.setStrokeColor(farbe)
        c.setLineWidth(linie * 0.7)
        c.line(sx, sy, ex, ey)

    # Badge: weißer Grund, farbiger Rand, farbige Schrift
    text = befund_kennung(b)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setStrokeColor(farbe)
    c.setLineWidth(linie)
    breite = br * (1.2 if len(text) <= 2 else 1.55)
    c.roundRect(bx - breite, by - br * 0.8, 2 * breite, 1.6 * br, br * 0.5, stroke=1, fill=1)
    c.setFillColor(farbe)
    gr = br * 1.0
    c.setFont("Helvetica-Bold", gr)
    c.drawCentredString(bx, by - gr * 0.36, text)


def zeichne_beschriftung(c, s, pt, w):
    x, y = pt(s["x"], s["y"])
    gr = max(9.0, w * 0.0115)
    c.setFont("Helvetica-Bold", gr)
    breite = c.stringWidth(s["text"], "Helvetica-Bold", gr)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setStrokeColor(GRAU_DUNKEL)
    c.setLineWidth(0.8)
    c.rect(x - breite / 2 - gr * 0.4, y - gr * 0.45, breite + gr * 0.8, gr * 1.35, stroke=1, fill=1)
    c.setFillColor(GRAU_DUNKEL)
    c.drawCentredString(x, y - gr * 0.05, s["text"])


GRUEN = HexColor("#15803D")  # Farbe der Korrekturskizze (Ergänzungen / Korrekturen)


def zeichne_korrektur(c, k, pt, w, h):
    """Zeichnet ein Element der Korrekturskizze in Grün.

    Typen (Koordinaten in Prozent):
      holz          {"rechteck": [x1, y1, x2, y2]}            Kantholz/Latte im Schnitt (Rechteck mit Kreuz)
      platte        {"rechteck": [...], "richtung": "auto"}   Plattenwerkstoff mit Querstrich-Schraffur
      abklebung     {"punkte": [[x, y], …]}                   dicke gestrichelte Linie (Klebeband)
      linie         {"punkte": [[x, y], …]}                   durchgezogene Linie
      durchstreichen{"von": [x, y], "bis": [x, y]}            falschen Wert/Text durchstreichen
      text          {"text": "…", "x", "y", "ziel": [x, y]}   Beschriftung, optional mit Hinweislinie
    """
    typ = k.get("typ")
    linie = max(1.0, w * 0.0013)
    c.saveState()
    c.setStrokeColor(GRUEN)
    c.setFillColor(GRUEN)
    c.setLineCap(1)
    if typ in ("holz", "platte"):
        x1, y1, x2, y2 = k["rechteck"]
        (ax, ay), (bx, by) = pt(x1, y1), pt(x2, y2)
        lx, ux = min(ax, bx), max(ax, bx)
        ly, uy = min(ay, by), max(ay, by)
        c.setFillColor(HexColor("#FFFFFF"))
        c.rect(lx, ly, ux - lx, uy - ly, stroke=0, fill=1)  # darunterliegende Linien abdecken
        c.setStrokeColor(GRUEN)
        c.setLineWidth(linie)
        c.rect(lx, ly, ux - lx, uy - ly, stroke=1, fill=0)
        if typ == "holz":
            c.line(lx, ly, ux, uy)
            c.line(lx, uy, ux, ly)
        else:
            abstand = max(2.0, w * 0.0045)
            senkrecht = (uy - ly) > (ux - lx) if k.get("richtung", "auto") == "auto" else k["richtung"] == "quer"
            c.setLineWidth(linie * 0.7)
            if senkrecht:  # lange Seite vertikal → waagerechte Querstriche
                yy = ly + abstand / 2
                while yy < uy:
                    c.line(lx, yy, ux, yy)
                    yy += abstand
            else:
                xx = lx + abstand / 2
                while xx < ux:
                    c.line(xx, ly, xx, uy)
                    xx += abstand
    elif typ == "daemmung":
        # fehlende Dämmung: Fläche (Polygon) mit grüner Wellen-/Kreuzschraffur
        punkte = [pt(x, y) for x, y in k["punkte"]]
        pfad = c.beginPath()
        pfad.moveTo(*punkte[0])
        for p in punkte[1:]:
            pfad.lineTo(*p)
        pfad.close()
        c.setFillColor(HexColor("#FFFFFF"))
        c.drawPath(pfad, stroke=0, fill=1)
        c.saveState()
        c.clipPath(pfad, stroke=0, fill=0)
        c.setStrokeColor(GRUEN)
        c.setLineWidth(linie * 0.6)
        xs = [p[0] for p in punkte]
        ys = [p[1] for p in punkte]
        hoehe = max(ys) - min(ys)
        abstand = max(3.0, w * 0.004)
        t = -hoehe
        while t <= max(xs) - min(xs):
            c.line(min(xs) + t, min(ys), min(xs) + t + hoehe, max(ys))
            c.line(min(xs) + t, max(ys), min(xs) + t + hoehe, min(ys))
            t += abstand * 1.6
        c.restoreState()
        c.setStrokeColor(GRUEN)
        c.setLineWidth(linie)
        c.drawPath(pfad, stroke=1, fill=0)
    elif typ in ("abklebung", "linie"):
        punkte = [pt(x, y) for x, y in k["punkte"]]
        c.setLineWidth(linie * (2.2 if typ == "abklebung" else 1.0))
        if typ == "abklebung":
            c.setDash([linie * 4, linie * 2.5])
        pfad = c.beginPath()
        pfad.moveTo(*punkte[0])
        for p in punkte[1:]:
            pfad.lineTo(*p)
        c.drawPath(pfad, stroke=1, fill=0)
    elif typ == "durchstreichen":
        (ax, ay), (bx, by) = pt(*k["von"]), pt(*k["bis"])
        c.setLineWidth(linie * 1.3)
        c.line(ax, ay, bx, by)
    elif typ == "text":
        gr = k.get("groesse", max(7.5, w * 0.0075))
        x, y = pt(k["x"], k["y"])
        zeilen = str(k["text"]).split("\n")
        schrift = "Helvetica-Bold" if k.get("fett", True) else "Helvetica"
        breite = max(c.stringWidth(z, schrift, gr) for z in zeilen)
        hoehe = gr * 1.2 * len(zeilen)
        if k.get("ziel"):
            zx, zy = pt(*k["ziel"])
            c.setLineWidth(linie * 0.8)
            ax = x if zx < x else x + breite
            c.line(ax, y - hoehe / 2 + gr * 0.35, zx, zy)
            c.circle(zx, zy, linie * 1.2, stroke=0, fill=1)
        if k.get("rahmen", True):
            c.setFillColor(HexColor("#FFFFFF"))
            c.setLineWidth(linie * 0.6)
            c.rect(x - gr * 0.3, y - hoehe + gr * 0.85, breite + gr * 0.6, hoehe + gr * 0.1, stroke=1, fill=1)
        c.setFillColor(GRUEN)
        c.setFont(schrift, gr)
        for i, z in enumerate(zeilen):
            c.drawString(x, y - i * gr * 1.2, z)
    c.restoreState()


def korrigierte_seite(pdf_ein, daten):
    """Gibt (PdfWriter mit Korrekturskizze, Seitennummer, Anzahl Elemente) zurück."""
    seitennr = int(daten.get("seite", 1))
    reader = PdfReader(pdf_ein)
    writer = PdfWriter(clone_from=reader)
    seite = writer.pages[seitennr - 1]
    mb = seite.mediabox
    w, h = float(mb.width), float(mb.height)
    x0, y0 = float(mb.left), float(mb.bottom)

    def pt(x, y):
        return x / 100 * w, h - y / 100 * h

    puffer = io.BytesIO()
    c = canvas.Canvas(puffer, pagesize=(w, h))
    elemente = [k for b in befunde_lesen(daten) for k in b.get("korrektur", [])]
    # Flächen zuerst, Texte zuletzt
    for k in sorted(elemente, key=lambda k: {"daemmung": 0, "holz": 0, "platte": 0, "abklebung": 1, "linie": 1,
                                              "durchstreichen": 2, "text": 3}.get(k.get("typ"), 1)):
        zeichne_korrektur(c, k, pt, w, h)
    for s in daten.get("beschriftungen", []):
        zeichne_beschriftung(c, s, pt, w)
    c.save()
    puffer.seek(0)
    seite.merge_transformed_page(PdfReader(puffer).pages[0], Transformation().translate(x0, y0))
    return writer, seitennr, len(elemente)


def markierte_seite(pdf_ein, daten):
    """Gibt (PdfWriter mit markierter Zeichnung, Seitennummer, Anzahl Markierungen) zurück."""
    seitennr = int(daten.get("seite", 1))
    befunde = befunde_lesen(daten)

    reader = PdfReader(pdf_ein)
    writer = PdfWriter(clone_from=reader)
    seite = writer.pages[seitennr - 1]
    if seite.rotation % 360:
        print(f"Warnung: Seite ist um {seite.rotation}° gedreht – Markierungen könnten verschoben sein.")

    mb = seite.mediabox
    w, h = float(mb.width), float(mb.height)
    x0, y0 = float(mb.left), float(mb.bottom)

    def pt(x, y):  # Prozent (oben-links) -> PDF-Punkte (unten-links)
        return x / 100 * w, h - y / 100 * h

    puffer = io.BytesIO()
    c = canvas.Canvas(puffer, pagesize=(w, h))
    sichtbar = [b for b in befunde if b.get("kreis")
                and einstufung_normalisieren(b.get("einstufung")) != "nicht_pruefbar"]
    # Hinweise zuerst, Aufbaufehler zuletzt (liegen oben)
    reihenfolge = {"hinweis": 0, "auffaelligkeit": 1, "aufbaufehler": 2}
    for b in sorted(sichtbar, key=lambda b: reihenfolge[einstufung_normalisieren(b.get("einstufung"))]):
        zeichne_befund(c, b, pt, w)
    for s in daten.get("beschriftungen", []):
        zeichne_beschriftung(c, s, pt, w)
    c.save()
    puffer.seek(0)

    ebene = PdfReader(puffer).pages[0]
    seite.merge_transformed_page(ebene, Transformation().translate(x0, y0))
    return writer, seitennr, len(sichtbar)


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    pdf_ein, json_datei, pdf_aus = sys.argv[1:4]
    with open(json_datei, encoding="utf-8") as f:
        daten = json.load(f)
    writer, _, anzahl = markierte_seite(pdf_ein, daten)
    with open(pdf_aus, "wb") as f:
        writer.write(f)
    print(f"{anzahl} Markierung(en) gesetzt → {pdf_aus}")


if __name__ == "__main__":
    main()
