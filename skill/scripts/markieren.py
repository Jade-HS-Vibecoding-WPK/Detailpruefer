"""Zeichnet Befunde als rote Kreise, Nummern und Schraffuren in eine PDF-Zeichnung.

Die Originalzeichnung bleibt als Vektor-PDF erhalten (scharf beim Zoomen);
die Markierungen werden als eigene Ebene darübergelegt.

Aufruf:
    python markieren.py <zeichnung.pdf> <befunde.json> <ausgabe.pdf>

Koordinaten sind Prozentwerte:
x = 0 (links) … 100 (rechts), y = 0 (oben) … 100 (unten), r in % der Blattbreite.

Einstufung → Linienart:
    aufbaufehler    = durchgezogen
    auffaelligkeit  = gestrichelt   (früher: risiko)
    hinweis         = gepunktet
    nicht_pruefbar  = keine Markierung
"""
import io
import json
import sys

from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROT = Color(0.80, 0.08, 0.08)
ROT_TRANSPARENT = Color(0.80, 0.08, 0.08, alpha=0.08)

RICHTUNGEN = {  # wo die Nummer am Kreis sitzt (x-, y-Richtung in PDF-Koordinaten)
    "oben-rechts": (1, 1), "oben-links": (-1, 1),
    "unten-rechts": (1, -1), "unten-links": (-1, -1),
}


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
    """Akzeptiert das neue Format ("befunde") und das alte ("maengel")."""
    return daten.get("befunde") or daten.get("maengel") or []


def strichart(einstufung, linie):
    if einstufung == "auffaelligkeit":
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
    c.setStrokeColor(ROT)
    c.setLineWidth(linie * 1.5)
    pfad = c.beginPath()
    pfad.moveTo(*punkte[0])
    for p in punkte[1:]:
        pfad.lineTo(*p)
    pfad.close()
    c.drawPath(pfad, stroke=1, fill=0)


def markierte_seite(pdf_ein, daten):
    """Gibt (PdfWriter mit markierter Zeichnung, Anzahl Markierungen) zurück."""
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
    anzahl = 0
    sichtbar = [b for b in befunde
                if einstufung_normalisieren(b.get("einstufung")) != "nicht_pruefbar"]
    for b in sichtbar:
        if b.get("schraffur"):
            schraffur(c, [pt(x, y) for x, y in b["schraffur"]], w)
    for b in sichtbar:
        k = b.get("kreis")
        if k:
            px, py = pt(k["x"], k["y"])
            kreis_und_nummer(c, px, py, k.get("r", 3) / 100 * w, b["nr"], w,
                             einstufung_normalisieren(b.get("einstufung")),
                             b.get("nummer_position", "oben-rechts"))
            anzahl += 1
    c.save()
    puffer.seek(0)

    ebene = PdfReader(puffer).pages[0]
    seite.merge_transformed_page(ebene, Transformation().translate(x0, y0))
    return writer, seitennr, anzahl


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
