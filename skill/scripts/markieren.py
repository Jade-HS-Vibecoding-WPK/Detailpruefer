"""Zeichnet Mängel als rote Kreise, Nummern und Schraffuren in eine PDF-Zeichnung.

Die Originalzeichnung bleibt als Vektor-PDF erhalten (scharf beim Zoomen);
die Markierungen werden als eigene Ebene darübergelegt.

Aufruf:
    python markieren.py <zeichnung.pdf> <maengel.json> <ausgabe.pdf>

Koordinaten in maengel.json sind Prozentwerte:
x = 0 (links) … 100 (rechts), y = 0 (oben) … 100 (unten), r in % der Blattbreite.

Einstufung → Linienart: aufbaufehler = durchgezogen, risiko = gestrichelt,
hinweis = gepunktet, nicht beurteilbar = keine Markierung.
"""
import io
import json
import sys

from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding="utf-8")

ROT = Color(0.85, 0.05, 0.05)
ROT_TRANSPARENT = Color(0.85, 0.05, 0.05, alpha=0.08)


RICHTUNGEN = {  # wo die Nummer am Kreis sitzt (x-, y-Richtung in PDF-Koordinaten)
    "oben-rechts": (1, 1), "oben-links": (-1, 1),
    "unten-rechts": (1, -1), "unten-links": (-1, -1),
}


def strichart(einstufung, linie):
    """aufbaufehler = durchgezogen, risiko = gestrichelt, hinweis = gepunktet."""
    if einstufung == "risiko":
        return [linie * 4, linie * 3]
    if einstufung == "hinweis":
        return [linie * 0.1, linie * 2.2]
    return []


def kreis_und_nummer(c, px, py, r, nr, w, einstufung, richtung="oben-rechts"):
    linie = max(1.2, w * 0.0016)
    c.setStrokeColor(ROT)
    c.setLineWidth(linie)
    c.setLineCap(1)  # runde Enden – nötig für gepunktete Linien
    c.setDash(strichart(einstufung, linie))
    c.setFillColor(ROT_TRANSPARENT)
    c.circle(px, py, r, stroke=1, fill=1)
    c.setDash([])

    # Nummern-Plakette an der gewählten Ecke des Kreises
    sx, sy = RICHTUNGEN.get(richtung, (1, 1))
    br = max(7.0, w * 0.009)
    bx = px + sx * (r * 0.707 + br * 0.7)
    by = py + sy * (r * 0.707 + br * 0.7)
    c.setFillColor(ROT)
    c.circle(bx, by, br, stroke=0, fill=1)
    c.setFillColor(Color(1, 1, 1))
    gr = br * 1.15
    c.setFont("Helvetica-Bold", gr)
    c.drawCentredString(bx, by - gr * 0.36, str(nr))


def schraffur(c, punkte, w):
    """Rote 45°-Schraffur innerhalb eines Polygons."""
    linie = max(0.6, w * 0.0007)
    abstand = max(2.5, w * 0.0035)
    xs = [p[0] for p in punkte]
    ys = [p[1] for p in punkte]
    c.saveState()
    pfad = c.beginPath()
    pfad.moveTo(*punkte[0])
    for p in punkte[1:]:
        pfad.lineTo(*p)
    pfad.close()
    c.clipPath(pfad, stroke=0, fill=0)
    c.setStrokeColor(ROT)
    c.setLineWidth(linie)
    breite = max(xs) - min(xs)
    hoehe = max(ys) - min(ys)
    t = -hoehe
    while t <= breite:
        x0 = min(xs) + t
        c.line(x0, min(ys), x0 + hoehe, max(ys))
        t += abstand
    c.restoreState()
    # Umriss
    c.setStrokeColor(ROT)
    c.setLineWidth(linie * 1.5)
    pfad = c.beginPath()
    pfad.moveTo(*punkte[0])
    for p in punkte[1:]:
        pfad.lineTo(*p)
    pfad.close()
    c.drawPath(pfad, stroke=1, fill=0)


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    pdf_ein, json_datei, pdf_aus = sys.argv[1:4]

    with open(json_datei, encoding="utf-8") as f:
        daten = json.load(f)
    seitennr = int(daten.get("seite", 1))
    maengel = daten.get("maengel", [])

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
    for m in maengel:
        if m.get("schraffur"):
            schraffur(c, [pt(x, y) for x, y in m["schraffur"]], w)
    for m in maengel:
        k = m.get("kreis")
        einstufung = str(m.get("einstufung", "aufbaufehler")).lower()
        if einstufung.startswith("nicht"):  # „nicht beurteilbar“ wird nicht markiert
            continue
        if k:
            px, py = pt(k["x"], k["y"])
            kreis_und_nummer(c, px, py, k.get("r", 3) / 100 * w, m["nr"], w,
                             einstufung, m.get("nummer_position", "oben-rechts"))
    c.save()
    puffer.seek(0)

    ebene = PdfReader(puffer).pages[0]
    seite.merge_transformed_page(ebene, Transformation().translate(x0, y0))
    with open(pdf_aus, "wb") as f:
        writer.write(f)
    print(f"{len(maengel)} Mangel/Mängel markiert → {pdf_aus}")


if __name__ == "__main__":
    main()
