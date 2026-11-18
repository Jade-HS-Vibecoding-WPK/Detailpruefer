"""Liest die Linien (Vektorpfade) einer PDF-Zeichnung exakt aus – für genaue Koordinaten.

Das Rasterbild (raster.py) eignet sich zum Überblick; Lage und Neigung von Bauteilkanten
(z. B. Sparren-Unterkante, Oberkante Wand, Schichtgrenzen) lassen sich damit aber nur
schätzen. Dieses Skript liefert die Linien direkt aus der Vektorzeichnung in Prozent-
Koordinaten (x = 0 links … 100 rechts, y = 0 oben … 100 unten) – dieselben Koordinaten,
die befunde.json verwendet.

Aufruf:
    python linien.py <zeichnung.pdf> --ausschnitt x1 y1 x2 y2 [--min 1.0] [--seite 1]
        Alle Linien im Ausschnitt, mindestens --min Prozent lang (Standard 1,0), sortiert
        nach Länge. Schraffurlinien sind meist kurz und fallen so heraus.
    python linien.py <zeichnung.pdf> --punkt x y [--radius 0.6] [--min 0.5]
        Linien, die nahe an einem Punkt vorbeilaufen (z. B. „welche Kante liegt hier?“).
    python linien.py <zeichnung.pdf> --schnitt x1 y1 x2 y2 x3 y3 x4 y4
        Schnittpunkt zweier (verlängerter) Linien, z. B. der beiden Sparren-Unterkanten in
        der Firstachse oder Wand-Außenkante mit Dach-Unterseite. Rechnet nur mit Koordinaten.
    python linien.py <zeichnung.pdf> --parallel x1 y1 x2 y2 --abstand_cm d --massstab 1:5
        Parallele zu einer Linie im Abstand d (cm, Wirklichkeit; + = links der Laufrichtung).

Ausgabe je Linie: x1 y1 x2 y2 | Länge % | Winkel ° (0 = waagerecht, + = steigend nach rechts)
"""
import argparse
import ctypes
import math
import sys

import pypdfium2 as pdfium
import pypdfium2.raw as raw

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _mal(m1, m2):
    """Matrix-Produkt (a, b, c, d, e, f) – erst m2, dann m1."""
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return (a2 * a1 + b2 * c1, a2 * b1 + b2 * d1,
            c2 * a1 + d2 * c1, c2 * b1 + d2 * d1,
            e2 * a1 + f2 * c1 + e1, e2 * b1 + f2 * d1 + f1)


def _matrix(obj):
    m = raw.FS_MATRIX()
    if not raw.FPDFPageObj_GetMatrix(obj, ctypes.byref(m)):
        return (1, 0, 0, 1, 0, 0)
    return (m.a, m.b, m.c, m.d, m.e, m.f)


def _anwenden(m, x, y):
    a, b, c, d, e, f = m
    return a * x + c * y + e, b * x + d * y + f


def _pfad_segmente(obj, m):
    n = raw.FPDFPath_CountSegments(obj)
    start = letzter = None
    segmente = []
    for i in range(n):
        seg = raw.FPDFPath_GetPathSegment(obj, i)
        x, y = ctypes.c_float(), ctypes.c_float()
        raw.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
        p = _anwenden(m, x.value, y.value)
        typ = raw.FPDFPathSegment_GetType(seg)
        if typ == raw.FPDF_SEGMENT_MOVETO:
            start = letzter = p
        else:  # LINETO bzw. BEZIERTO (Kurven werden über ihre Stützpunkte angenähert)
            if letzter is not None:
                segmente.append((letzter, p))
            letzter = p
        if raw.FPDFPathSegment_GetClose(seg) and start is not None and letzter != start:
            segmente.append((letzter, start))
            letzter = start
    return segmente


def _sammeln(objekte_zaehlen, objekt_holen, m_eltern, ausgabe):
    for i in range(objekte_zaehlen()):
        obj = objekt_holen(i)
        m = _mal(m_eltern, _matrix(obj))
        typ = raw.FPDFPageObj_GetType(obj)
        if typ == raw.FPDF_PAGEOBJ_PATH:
            ausgabe += _pfad_segmente(obj, m)
        elif typ == raw.FPDF_PAGEOBJ_FORM:
            _sammeln(lambda o=obj: raw.FPDFFormObj_CountObjects(o),
                     lambda j, o=obj: raw.FPDFFormObj_GetObject(o, j), m, ausgabe)


def linien(pdf_pfad, seite=1):
    """Alle Liniensegmente der Seite in Prozent-Koordinaten (oben-links)."""
    dok = pdfium.PdfDocument(pdf_pfad)
    page = dok[seite - 1]
    w, h = page.get_size()
    roh = []
    _sammeln(lambda: raw.FPDFPage_CountObjects(page.raw),
             lambda i: raw.FPDFPage_GetObject(page.raw, i), (1, 0, 0, 1, 0, 0), roh)
    ergebnis, gesehen = [], set()
    for (x1, y1), (x2, y2) in roh:
        a = (round(x1 / w * 100, 3), round(100 - y1 / h * 100, 3))
        b = (round(x2 / w * 100, 3), round(100 - y2 / h * 100, 3))
        if a == b:
            continue
        schluessel = tuple(sorted((a, b)))
        if schluessel in gesehen:
            continue
        gesehen.add(schluessel)
        ergebnis.append((a, b))
    return ergebnis, (w, h)


def laenge(seg):
    (x1, y1), (x2, y2) = seg
    return math.hypot(x2 - x1, y2 - y1)


def winkel(seg, w, h):
    """Winkel auf dem Blatt in Grad (Prozent → Punkte umgerechnet, + = steigend nach rechts)."""
    (x1, y1), (x2, y2) = seg
    dx, dy = (x2 - x1) * w / 100, -(y2 - y1) * h / 100
    if dx < 0:
        dx, dy = -dx, -dy
    return math.degrees(math.atan2(dy, dx))


def abstand_punkt(seg, px, py):
    (x1, y1), (x2, y2) = seg
    vx, vy = x2 - x1, y2 - y1
    t = max(0.0, min(1.0, ((px - x1) * vx + (py - y1) * vy) / (vx * vx + vy * vy or 1)))
    return math.hypot(px - (x1 + t * vx), py - (y1 + t * vy))


def im_ausschnitt(seg, x1, y1, x2, y2):
    return any(x1 <= x <= x2 and y1 <= y <= y2 for x, y in seg)


def schnittpunkt(p1, p2, p3, p4, w, h):
    """Schnittpunkt der Geraden p1-p2 und p3-p4 (Prozent), gerechnet in Blattpunkten."""
    def pt(p):
        return p[0] * w / 100, p[1] * h / 100
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = map(pt, (p1, p2, p3, p4))
    nenner = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(nenner) < 1e-9:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / nenner
    x, y = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
    return x / w * 100, y / h * 100


def ausgeben(segmente, w, h, maximal=80):
    segmente = sorted(segmente, key=laenge, reverse=True)
    for seg in segmente[:maximal]:
        (x1, y1), (x2, y2) = seg
        print(f"{x1:7.3f} {y1:7.3f} {x2:7.3f} {y2:7.3f} | {laenge(seg):6.2f} % | {winkel(seg, w, h):7.2f}°")
    if len(segmente) > maximal:
        print(f"… {len(segmente) - maximal} weitere (Ausschnitt verkleinern oder --min erhöhen)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--seite", type=int, default=1)
    ap.add_argument("--ausschnitt", type=float, nargs=4, metavar=("X1", "Y1", "X2", "Y2"))
    ap.add_argument("--punkt", type=float, nargs=2, metavar=("X", "Y"))
    ap.add_argument("--radius", type=float, default=0.6)
    ap.add_argument("--min", type=float, default=None, help="Mindestlänge in %% (Standard 1,0 bzw. 0,5 bei --punkt)")
    ap.add_argument("--schnitt", type=float, nargs=8)
    ap.add_argument("--parallel", type=float, nargs=4)
    ap.add_argument("--abstand_cm", type=float)
    ap.add_argument("--massstab")
    ap.add_argument("--max", type=int, default=80)
    a = ap.parse_args()

    segmente, (w, h) = linien(a.pdf, a.seite)
    if a.schnitt:
        s = a.schnitt
        p = schnittpunkt(s[0:2], s[2:4], s[4:6], s[6:8], w, h)
        print("Linien sind parallel – kein Schnittpunkt." if p is None
              else f"Schnittpunkt: x = {p[0]:.3f} %, y = {p[1]:.3f} %")
        return
    if a.parallel:
        if not (a.abstand_cm and a.massstab):
            sys.exit("--parallel braucht --abstand_cm und --massstab (z. B. 1:5)")
        x1, y1, x2, y2 = a.parallel
        pt_cm = 72 / 2.54 / float(a.massstab.split(":")[1].replace(",", "."))
        dx, dy = (x2 - x1) * w / 100, (y2 - y1) * h / 100
        n = math.hypot(dx, dy) or 1
        nx, ny = dy / n, -dx / n          # links der Laufrichtung (Blatt, y nach unten)
        d = a.abstand_cm * pt_cm
        ox, oy = nx * d / w * 100, ny * d / h * 100
        print(f"Parallele: {x1 + ox:.3f} {y1 + oy:.3f} {x2 + ox:.3f} {y2 + oy:.3f}")
        return
    if a.punkt:
        mindest = 0.5 if a.min is None else a.min
        px, py = a.punkt
        treffer = [s for s in segmente if laenge(s) >= mindest and abstand_punkt(s, px, py) <= a.radius]
        print(f"{len(treffer)} Linie(n) im Umkreis {a.radius} % um ({px}, {py}):")
        ausgeben(treffer, w, h, a.max)
        return
    mindest = 1.0 if a.min is None else a.min
    x1, y1, x2, y2 = a.ausschnitt or (0, 0, 100, 100)
    treffer = [s for s in segmente if laenge(s) >= mindest and im_ausschnitt(s, x1, y1, x2, y2)]
    print(f"{len(treffer)} Linie(n) ≥ {mindest} % im Ausschnitt x {x1}–{x2}, y {y1}–{y2}:")
    ausgeben(treffer, w, h, a.max)


if __name__ == "__main__":
    main()
