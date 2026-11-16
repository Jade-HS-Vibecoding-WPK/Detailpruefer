"""Rendert eine PDF-Seite als Bild und legt ein Prozent-Raster darüber.

Damit kann Claude Positionen in der Zeichnung ablesen:
x = 0 (links) … 100 (rechts), y = 0 (oben) … 100 (unten).

Aufruf:
    python raster.py <zeichnung.pdf> <ausgabe.png> [--seite 1] [--dpi 150] [--ausschnitt x1 y1 x2 y2]

Mit --ausschnitt (in Prozent) wird nur ein Teil gezeigt – nützlich zum Hineinzoomen.
"""
import argparse
import sys

import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

RASTER_FEIN = (0, 150, 220, 70)     # hellblau, transparent – alle 5 %
RASTER_GROB = (0, 110, 200, 150)    # kräftiger – alle 10 %
SCHRIFT = (0, 80, 170, 255)


def schrift(groesse):
    try:
        return ImageFont.load_default(size=groesse)
    except TypeError:  # ältere Pillow-Versionen
        return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser(description="PDF-Seite mit Prozent-Raster als PNG ausgeben")
    ap.add_argument("pdf")
    ap.add_argument("png")
    ap.add_argument("--seite", type=int, default=1)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--ausschnitt", type=float, nargs=4, metavar=("X1", "Y1", "X2", "Y2"))
    a = ap.parse_args()

    doc = pdfium.PdfDocument(a.pdf)
    seite = doc[a.seite - 1]
    bild = seite.render(scale=a.dpi / 72).to_pil().convert("RGBA")
    W, H = bild.size

    # Bereich, der gezeigt wird (in Prozent)
    x1, y1, x2, y2 = a.ausschnitt if a.ausschnitt else (0, 0, 100, 100)
    bild = bild.crop((int(x1 / 100 * W), int(y1 / 100 * H), int(x2 / 100 * W), int(y2 / 100 * H)))
    bw, bh = bild.size

    # Rand für Beschriftung
    rand = 40
    leinwand = Image.new("RGBA", (bw + 2 * rand, bh + 2 * rand), (255, 255, 255, 255))
    leinwand.paste(bild, (rand, rand))
    ebene = Image.new("RGBA", leinwand.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ebene)
    f = schrift(14)

    # Rasterweite: im Ausschnitt feiner
    spanne = max(x2 - x1, y2 - y1)
    schritt = 5 if spanne > 40 else 1 if spanne <= 10 else 2.5 if spanne <= 25 else 5
    grob = schritt * 2

    def px_x(p):
        return rand + (p - x1) / (x2 - x1) * bw

    def px_y(p):
        return rand + (p - y1) / (y2 - y1) * bh

    def werte(von, bis):
        start = (int(von / schritt) + (0 if von % schritt == 0 else 1)) * schritt
        v = start
        while v <= bis + 1e-9:
            yield round(v, 2)
            v += schritt

    for v in werte(x1, x2):
        ist_grob = abs(v / grob - round(v / grob)) < 1e-6
        X = px_x(v)
        d.line([(X, rand), (X, rand + bh)], fill=RASTER_GROB if ist_grob else RASTER_FEIN, width=1)
        if ist_grob:
            t = f"{v:g}"
            d.text((X, rand - 4), t, fill=SCHRIFT, font=f, anchor="mb")
            d.text((X, rand + bh + 4), t, fill=SCHRIFT, font=f, anchor="mt")
    for v in werte(y1, y2):
        ist_grob = abs(v / grob - round(v / grob)) < 1e-6
        Y = px_y(v)
        d.line([(rand, Y), (rand + bw, Y)], fill=RASTER_GROB if ist_grob else RASTER_FEIN, width=1)
        if ist_grob:
            t = f"{v:g}"
            d.text((rand - 4, Y), t, fill=SCHRIFT, font=f, anchor="rm")
            d.text((rand + bw + 4, Y), t, fill=SCHRIFT, font=f, anchor="lm")

    Image.alpha_composite(leinwand, ebene).convert("RGB").save(a.png)
    print(f"Rasterbild gespeichert: {a.png}  (Ausschnitt x {x1:g}–{x2:g} %, y {y1:g}–{y2:g} %, Raster {schritt:g} %)")


if __name__ == "__main__":
    main()
