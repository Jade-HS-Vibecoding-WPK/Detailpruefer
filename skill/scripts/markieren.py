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
WEISS = HexColor("#FFFFFF")
TEXT_MAX_BREITE = 0.26  # Hinweistexte werden ab ca. 26 % der Blattbreite umbrochen


def _pfad(c, punkte):
    pfad = c.beginPath()
    pfad.moveTo(*punkte[0])
    for p in punkte[1:]:
        pfad.lineTo(*p)
    pfad.close()
    return pfad


def _flaeche(k, pt):
    """Punkte einer Fläche in PDF-Punkten – aus "punkte" (Polygon) oder "rechteck"."""
    if k.get("punkte"):
        return [pt(x, y) for x, y in k["punkte"]]
    x1, y1, x2, y2 = k["rechteck"]
    return [pt(x1, y1), pt(x2, y1), pt(x2, y2), pt(x1, y2)]


def _band(k, punkte, pt):
    """Schichtrichtung einer Fläche: Ursprung A, Einheitsvektor u (längs), n (quer), Dicke H.

    "band": [[x, y], [x, y], [x, y]] = zwei Punkte auf einer Schichtgrenze + ein Punkt auf der
    gegenüberliegenden Grenze. Ohne Angabe: erste Kante des Polygons + letzter Punkt.
    """
    if k.get("band"):
        a, b, gegen = (pt(x, y) for x, y in k["band"])
    else:
        a, b, gegen = punkte[0], punkte[1], punkte[-1]
    ux, uy = b[0] - a[0], b[1] - a[1]
    laenge = math.hypot(ux, uy) or 1.0
    ux, uy = ux / laenge, uy / laenge
    cx, cy = gegen[0] - a[0], gegen[1] - a[1]
    s = cx * ux + cy * uy
    nx, ny = cx - s * ux, cy - s * uy
    dicke = math.hypot(nx, ny) or 1.0
    return a, (ux, uy), (nx / dicke, ny / dicke), dicke


def _schlaufen(c, k, punkte, pt, linie):
    """Dämmstoff-Schraffur (weich) wie in CAD-Zeichnungen: Schlaufen über die ganze Schichtdicke,
    abwechselnd oben/unten, in Schichtrichtung. Größe richtet sich nach der Schichtdicke."""
    a, (ux, uy), (nx, ny), dicke = _band(k, punkte, pt)
    # Geometrie in Schichtkoordinaten: s = längs, q = quer (0 … dicke).
    # Kreise (Radius R) liegen abwechselnd an der einen und der anderen Schichtgrenze und sind
    # über innere Tangenten verbunden → tropfenförmige Schlaufen wie die CAD-Schraffur „Dämmung weich“.
    R = 0.24 * dicke
    d = k.get("teilung", 0.25) * dicke          # Versatz zwischen gegenüberliegenden Schlaufen
    proj = [(px - a[0]) * ux + (py - a[1]) * uy for px, py in punkte]
    i0, i1 = int(math.floor(min(proj) / d)) - 2, int(math.ceil(max(proj) / d)) + 2
    zentren = [(i * d, R if i % 2 == 0 else dicke - R) for i in range(i0, i1 + 1)]

    def tangente(p, q):
        vx, vy = q[0] - p[0], q[1] - p[1]
        dist = math.hypot(vx, vy)
        vx, vy = vx / dist, vy / dist
        w = -(1 if p[1] < dicke / 2 else -1) * math.acos(min(1.0, R / (dist / 2)))

        def drehen(x, y):
            return x * math.cos(w) - y * math.sin(w), x * math.sin(w) + y * math.cos(w)
        tx, ty = drehen(vx, vy)
        gx, gy = drehen(-vx, -vy)
        return (p[0] + R * tx, p[1] + R * ty), (q[0] + R * gx, q[1] + R * gy)

    tg = [tangente(zentren[i], zentren[i + 1]) for i in range(len(zentren) - 1)]
    lokal = []
    for i in range(1, len(zentren) - 1):
        p = zentren[i]
        ein, aus = tg[i - 1][1], tg[i][0]
        w1 = math.atan2(ein[1] - p[1], ein[0] - p[0])
        w2 = math.atan2(aus[1] - p[1], aus[0] - p[0])
        rand = -math.pi / 2 if p[1] < dicke / 2 else math.pi / 2  # Bogen läuft über die Schichtgrenze
        if (rand - w1) % (2 * math.pi) <= (w2 - w1) % (2 * math.pi):
            bogen = (w2 - w1) % (2 * math.pi)
        else:
            bogen = -((w1 - w2) % (2 * math.pi))
        teile = max(10, int(abs(bogen) / 0.08))
        lokal += [ein] + [(p[0] + R * math.cos(w1 + bogen * j / teile),
                           p[1] + R * math.sin(w1 + bogen * j / teile)) for j in range(teile + 1)] + [aus]
    weg = c.beginPath()
    for j, (s, q) in enumerate(lokal):
        x, y = a[0] + s * ux + q * nx, a[1] + s * uy + q * ny
        if j == 0:
            weg.moveTo(x, y)
        else:
            weg.lineTo(x, y)
    c.setLineWidth(linie * 0.6)
    c.drawPath(weg, stroke=1, fill=0)


def _zickzack(c, k, punkte, pt, linie, doppelt=False):
    """Dämmung hart (Dämmplatten): Zickzack über die ganze Schichtdicke; doppelt = gekreuzt (Rauten)."""
    a, (ux, uy), (nx, ny), dicke = _band(k, punkte, pt)
    teilung = k.get("teilung", 1.0) * dicke   # Länge eines Zacks (hin und zurück)
    proj = [(px - a[0]) * ux + (py - a[1]) * uy for px, py in punkte]
    s0, s1 = min(proj) - teilung, max(proj) + teilung
    c.setLineWidth(linie * 0.6)
    for start_oben in ([True, False] if doppelt else [True]):
        weg = c.beginPath()
        s, oben = s0, start_oben
        weg.moveTo(a[0] + s * ux + (dicke if oben else 0) * nx, a[1] + s * uy + (dicke if oben else 0) * ny)
        while s <= s1:
            s += teilung / 2
            oben = not oben
            q = dicke if oben else 0
            weg.lineTo(a[0] + s * ux + q * nx, a[1] + s * uy + q * ny)
        c.drawPath(weg, stroke=1, fill=0)


def _welle(c, k, punkte, pt, linie):
    """Dämmung geschlängelt: weiche Wellenlinie über die ganze Schichtdicke (ohne Schlaufen)."""
    a, (ux, uy), (nx, ny), dicke = _band(k, punkte, pt)
    teilung = k.get("teilung", 0.9) * dicke   # Wellenlänge
    proj = [(px - a[0]) * ux + (py - a[1]) * uy for px, py in punkte]
    s, s1 = min(proj) - teilung, max(proj) + teilung
    weg = c.beginPath()
    erster = True
    while s <= s1:
        q = dicke / 2 + dicke * 0.46 * math.sin(2 * math.pi * s / teilung)
        x, y = a[0] + s * ux + q * nx, a[1] + s * uy + q * ny
        if erster:
            weg.moveTo(x, y)
            erster = False
        else:
            weg.lineTo(x, y)
        s += teilung / 48
    c.setLineWidth(linie * 0.6)
    c.drawPath(weg, stroke=1, fill=0)


DAEMM_ARTEN = ("weich", "hart", "hart_doppelt", "geschlaengelt")


def _plattenschraffur(c, art, punkte, k, pt, w, linie):
    """Schraffur von Plattenwerkstoffen – wie dieselbe Schicht in der Zeichnung:
    striche (OSB/Holzwerkstoff), zickzack (MDF/Holzfaser), punkte (Gipskarton), diagonal (Brett/Holz)."""
    a, (ux, uy), (nx, ny), dicke = _band(k, punkte, pt)
    proj = [(px - a[0]) * ux + (py - a[1]) * uy for px, py in punkte]
    s0, s1 = min(proj), max(proj)
    c.setLineWidth(linie * 0.6)
    if art == "punkte":
        abstand = max(1.6, w * 0.0018)
        s = s0
        reihe = 0
        while s <= s1:
            q = abstand / 2 + (abstand / 2 if reihe % 2 else 0)
            while q < dicke:
                c.circle(a[0] + s * ux + q * nx, a[1] + s * uy + q * ny, linie * 0.35, stroke=0, fill=1)
                q += abstand
            s += abstand * 0.8
            reihe += 1
        return
    if art == "zickzack":
        teilung = max(dicke * 1.1, 3.0)
        weg = c.beginPath()
        s = s0 - teilung
        weg.moveTo(a[0] + s * ux, a[1] + s * uy)
        oben = True
        while s <= s1 + teilung:
            s += teilung / 2
            q = dicke if oben else 0
            weg.lineTo(a[0] + s * ux + q * nx, a[1] + s * uy + q * ny)
            oben = not oben
        c.drawPath(weg, stroke=1, fill=0)
        return
    abstand = max(2.0, w * 0.0045) if art == "striche" else max(2.5, dicke * 0.6)
    s = s0 + abstand / 2
    while s <= s1:
        versatz = dicke * 0.8 if art == "diagonal" else 0
        x0, y0 = a[0] + s * ux, a[1] + s * uy
        c.line(x0, y0, x0 + versatz * ux + dicke * nx, y0 + versatz * uy + dicke * ny)
        s += abstand


def text_zeilen(k, w):
    """Zeilen eines Hinweistexts – lange Zeilen werden automatisch umbrochen."""
    from reportlab.lib.utils import simpleSplit
    gr = k.get("groesse", max(7.5, w * 0.0075))
    schrift = "Helvetica-Bold" if k.get("fett", True) else "Helvetica"
    zeilen = []
    for z in str(k["text"]).split("\n"):
        zeilen += simpleSplit(z, schrift, gr, w * TEXT_MAX_BREITE) or [""]
    breite = max(stringbreite(z, schrift, gr) for z in zeilen)
    return zeilen, schrift, gr, breite


def stringbreite(text, schrift, gr):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    return stringWidth(text, schrift, gr)


def text_box(k, pt, w, h):
    """Position (x, y der ersten Grundlinie), Zeilen, Schrift, Größe, Breite, Höhe – auf dem Blatt gehalten."""
    zeilen, schrift, gr, breite = text_zeilen(k, w)
    hoehe = gr * 1.2 * len(zeilen)
    x, y = pt(k["x"], k["y"])
    rand = gr * 0.6
    x = min(max(x, rand), w - breite - rand)
    y = min(max(y, hoehe - gr * 0.85 + rand), h - gr - rand)
    return x, y, zeilen, schrift, gr, breite, hoehe


# ---------------------------------------------------------------- Maßstab und Geometrie
# Bauteile können in echten Maßen (cm) angegeben werden; der Maßstab der Zeichnung
# (detail.massstab, z. B. "1:5") rechnet sie in Punkte auf dem Blatt um.
MASSSTAB = {"pt_cm": None, "text": None}


def massstab_setzen(daten):
    """Liest den Maßstab aus befunde.json ("detail": {"massstab": "1:5"} oder "massstab")."""
    text = str((daten.get("detail") or {}).get("massstab") or daten.get("massstab") or "").replace(" ", "")
    MASSSTAB["text"] = text or None
    MASSSTAB["pt_cm"] = None
    if ":" in text:
        try:
            m = float(text.split(":")[1].replace(",", "."))
            MASSSTAB["pt_cm"] = 72 / 2.54 / m   # 1 cm in Wirklichkeit = so viele Punkte auf dem Blatt
        except ValueError:
            pass


def _cm(wert):
    if MASSSTAB["pt_cm"] is None:
        raise ValueError("Maße in cm brauchen den Maßstab der Zeichnung: \"detail\": {\"massstab\": \"1:5\"}")
    return float(wert) * MASSSTAB["pt_cm"]


def _einheit(vx, vy):
    laenge = math.hypot(vx, vy) or 1.0
    return vx / laenge, vy / laenge


def _richtung(k, pt, schluessel="richtung"):
    """Richtung (Einheitsvektor auf dem Blatt). "richtung": [[x,y],[x,y]] = zwei Punkte auf
    einer Linie der Zeichnung (z. B. Dachfläche) – oder "winkel" in Grad (0 = waagerecht,
    positiv = nach rechts ansteigend)."""
    if k.get(schluessel):
        (ax, ay), (bx, by) = (pt(*p) for p in k[schluessel])
        return _einheit(bx - ax, by - ay)
    w = math.radians(float(k.get("winkel", 0)))
    return math.cos(w), math.sin(w)


def _normale(u, seite="oben"):
    """Senkrechte zu u, zeigt zur gewünschten Seite (oben/unten/links/rechts auf dem Blatt)."""
    nx, ny = -u[1], u[0]
    if seite == "unten":
        nx, ny = (nx, ny) if ny < 0 else (-nx, -ny)
    elif seite == "links":
        nx, ny = (nx, ny) if nx < 0 else (-nx, -ny)
    elif seite == "rechts":
        nx, ny = (nx, ny) if nx > 0 else (-nx, -ny)
    else:  # oben
        nx, ny = (nx, ny) if ny > 0 or (ny == 0 and nx > 0) else (-nx, -ny)
    return nx, ny


def _rechteck(mitte, u, n, b, hoehe):
    mx, my = mitte
    return [(mx + s * u[0] * b / 2 + t * n[0] * hoehe / 2, my + s * u[1] * b / 2 + t * n[1] * hoehe / 2)
            for s, t in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def _versatz_linie(punkte, abstand):
    """Parallele zu einem Linienzug im Abstand (links der Laufrichtung, Gehrung an Ecken)."""
    neu = []
    for i, (x, y) in enumerate(punkte):
        normalen = []
        if i > 0:
            ux, uy = _einheit(x - punkte[i - 1][0], y - punkte[i - 1][1])
            normalen.append((-uy, ux))
        if i < len(punkte) - 1:
            ux, uy = _einheit(punkte[i + 1][0] - x, punkte[i + 1][1] - y)
            normalen.append((-uy, ux))
        nx, ny = _einheit(sum(n[0] for n in normalen), sum(n[1] for n in normalen))
        cosw = max(0.3, sum(nx * n[0] + ny * n[1] for n in normalen) / len(normalen))
        neu.append((x + nx * abstand / cosw, y + ny * abstand / cosw))
    return neu


def _holz_ecken(k, pt):
    """Ecken eines Holzquerschnitts (Pfette, Latte, Sparren …) in Punkten.
    Varianten: "rechteck" [x1,y1,x2,y2] (achsparallel) · "punkte" (4 Ecken) ·
    "mitte"/"auf" [x,y] + "querschnitt_cm" [b, h] + "richtung"/"winkel" (+ "seite")."""
    if k.get("rechteck"):
        x1, y1, x2, y2 = k["rechteck"]
        (ax, ay), (bx, by) = pt(x1, y1), pt(x2, y2)
        return [(ax, ay), (bx, ay), (bx, by), (ax, by)]
    if k.get("punkte"):
        return [pt(x, y) for x, y in k["punkte"]]
    b, hoehe = (_cm(v) for v in k.get("querschnitt_cm", [6, 6]))
    u = _richtung(k, pt)
    n = _normale(u, k.get("seite", "oben"))
    if k.get("auf"):  # sitzt auf einer Linie: Unterseite mittig auf dem Punkt
        ax, ay = pt(*k["auf"])
        mitte = (ax + n[0] * hoehe / 2, ay + n[1] * hoehe / 2)
    else:
        mitte = pt(*k["mitte"])
    return _rechteck(mitte, u, n, b, hoehe)


def _firstlatte_teile(k, pt):
    """Firstlatte (aufrecht, Standard 3/5 cm) und Firstlattenhalter bis "halter_bis"."""
    teile = {"latte": _holz_ecken(dict(k, querschnitt_cm=k.get("querschnitt_cm", [3, 5]),
                                         winkel=k.get("winkel", 0)), pt), "halter": []}
    if k.get("halter_bis"):
        ecken = teile["latte"]
        unten = ((ecken[0][0] + ecken[1][0]) / 2, (ecken[0][1] + ecken[1][1]) / 2)
        ziel = pt(*k["halter_bis"])
        u = _einheit(ziel[0] - unten[0], ziel[1] - unten[1])
        n = (-u[1], u[0])
        d = _cm(0.25)
        fuss = _cm(k.get("fuss_cm", 4)) / 2
        teile["halter"] = [
            [(unten[0] + n[0] * d, unten[1] + n[1] * d), (ziel[0] + n[0] * d, ziel[1] + n[1] * d)],
            [(unten[0] - n[0] * d, unten[1] - n[1] * d), (ziel[0] - n[0] * d, ziel[1] - n[1] * d)],
            [(ziel[0] + n[0] * fuss, ziel[1] + n[1] * fuss), (ziel[0] - n[0] * fuss, ziel[1] - n[1] * fuss)]]
    return teile


def _firstziegel_umriss(k, pt):
    """Außenkontur eines Firstziegels (Kappe über dem First) als Linienzug in Punkten.
    "first" = Firstpunkt auf der Oberseite der Dachdeckung (Schnittpunkt beider Deckungslinien),
    Neigungen aus "richtung_links"/"richtung_rechts" (je 2 Punkte auf der Deckung) oder
    "neigung" in Grad (symmetrisch). Maße: "breite_cm" (gesamt), "hoehe_cm" (über dem Firstpunkt)."""
    fx, fy = pt(*k["first"])

    def abwaerts(schluessel, vorzeichen):
        if k.get(schluessel):
            ux, uy = _richtung(k, pt, schluessel)
        else:
            a = math.radians(float(k.get("neigung", 30)))
            ux, uy = vorzeichen * math.cos(a), -math.sin(a)
        if ux * vorzeichen < 0:   # Richtung vom First weg nach außen/unten
            ux, uy = -ux, -uy
        return ux, uy

    dl, dr = abwaerts("richtung_links", -1), abwaerts("richtung_rechts", 1)
    halb = _cm(k.get("breite_cm", 24)) / 2
    hoehe = _cm(k.get("hoehe_cm", 7))
    lippe = _cm(k.get("lippe_cm", 1.5))
    punkte = []
    for d, seite in ((dl, -1), (dr, 1)):
        a = halb / max(0.2, abs(d[0]))
        ende = (fx + d[0] * a, fy + d[1] * a + _cm(0.6))            # liegt knapp auf der Deckung
        auslauf = (ende[0] + d[0] * lippe, ende[1] + d[1] * lippe - lippe * 0.4)
        schulter = (fx + seite * halb * 0.55, fy + hoehe * 0.72)
        punkte.append((auslauf, ende, schulter))
    (aus_l, ende_l, sch_l), (aus_r, ende_r, sch_r) = punkte
    return [aus_l, ende_l, sch_l, (fx, fy + hoehe), sch_r, ende_r, aus_r]


def _lattenreihe_ecken(k, pt):
    """Querschnitte gleicher Latten entlang einer Linie ("von" → "bis"), Abstand in cm."""
    (ax, ay), (bx, by) = pt(*k["von"]), pt(*k["bis"])
    u = _einheit(bx - ax, by - ay)
    n = _normale(u, k.get("seite", "oben"))
    b, hoehe = (_cm(v) for v in k.get("querschnitt_cm", [5, 3]))
    abstand = _cm(k.get("abstand_cm", 33))
    laenge = math.hypot(bx - ax, by - ay)
    s = _cm(k.get("start_cm", 0)) + b / 2
    reihe = []
    while s <= laenge - b / 2 + 1e-6:
        mitte = (ax + u[0] * s + n[0] * hoehe / 2, ay + u[1] * s + n[1] * hoehe / 2)
        reihe.append(_rechteck(mitte, u, n, b, hoehe))
        s += abstand
    return reihe


def element_punkte(k, pt):
    """Alle Punkte (in PDF-Punkten), die ein Korrekturelement belegt – für Zuschnitt und Zoom.
    Texte liefern nur ihren Zielpunkt."""
    typ = k.get("typ")
    try:
        if typ == "holz":
            return _holz_ecken(k, pt)
        if typ == "firstlatte":
            t = _firstlatte_teile(k, pt)
            return t["latte"] + [p for linie in t["halter"] for p in linie]
        if typ == "firstziegel":
            return _firstziegel_umriss(k, pt)
        if typ == "lattenreihe":
            return [p for ecken in _lattenreihe_ecken(k, pt) for p in ecken]
        if typ == "text":
            return [pt(*k["ziel"])] if k.get("ziel") else []
        if k.get("rechteck"):
            return [pt(*k["rechteck"][:2]), pt(*k["rechteck"][2:])]
        if k.get("punkte"):
            return [pt(x, y) for x, y in k["punkte"]]
        return [pt(*p) for p in (k.get("von"), k.get("bis")) if p]
    except (KeyError, ValueError, TypeError) as fehler:
        print(f"Warnung: Korrekturelement „{typ}“ unvollständig ({fehler}).")
        return []


def korrektur_zoom(daten, b, w, h, rand=4.0):
    """Zoom-Ausschnitt (Prozent) um die zeichnenden Korrekturelemente eines Befunds."""
    massstab_setzen(daten)

    def pt(x, y):
        return x / 100 * w, h - y / 100 * h
    pkt = [p for k in b.get("korrektur", []) if k.get("typ") != "text" for p in element_punkte(k, pt)]
    if not pkt:
        return None
    xs = [p[0] / w * 100 for p in pkt]
    ys = [100 - p[1] / h * 100 for p in pkt]
    return [min(xs) - rand, min(ys) - rand, max(xs) + rand, max(ys) + rand]


def korrektur_grenzen(daten, w, h):
    """Umrandendes Rechteck aller Korrekturelemente (inkl. Hinweistexte) in Prozent – damit der
    Bericht beim Zuschneiden nichts abschneidet. None, wenn es keine Elemente gibt."""
    massstab_setzen(daten)
    xs, ys = [], []

    def pt(x, y):
        return x / 100 * w, h - y / 100 * h

    for b in befunde_lesen(daten):
        for k in b.get("korrektur", []):
            if k.get("typ") == "text":
                x, y, _, _, gr, breite, hoehe = text_box(k, pt, w, h)
                xs += [x - gr * 0.3, x + breite + gr * 0.3]
                ys += [y + gr, y - hoehe + gr * 0.85]
            for px, py in element_punkte(k, pt):
                xs.append(px)
                ys.append(py)
    if not xs:
        return None
    return [min(xs) / w * 100, 100 - max(ys) / h * 100, max(xs) / w * 100, 100 - min(ys) / h * 100]


def _holz_zeichnen(c, ecken, linie, schnitt="quer"):
    c.setFillColor(WEISS)
    c.drawPath(_pfad(c, ecken), stroke=0, fill=1)   # darunterliegende Linien abdecken
    c.setStrokeColor(GRUEN)
    c.setLineWidth(linie)
    c.drawPath(_pfad(c, ecken), stroke=1, fill=0)
    if schnitt == "laengs":   # Holz längs geschnitten: Faserlinien
        c.setLineWidth(linie * 0.5)
        (a, b, cc, d) = ecken[:4]
        for f in (0.3, 0.55, 0.8):
            p = (a[0] + (d[0] - a[0]) * f, a[1] + (d[1] - a[1]) * f)
            q = (b[0] + (cc[0] - b[0]) * f, b[1] + (cc[1] - b[1]) * f)
            c.line(p[0] + (q[0] - p[0]) * 0.08, p[1] + (q[1] - p[1]) * 0.08,
                   p[0] + (q[0] - p[0]) * (0.55 + 0.3 * f), p[1] + (q[1] - p[1]) * (0.55 + 0.3 * f))
    else:                     # Querschnitt: Kreuz
        c.line(ecken[0][0], ecken[0][1], ecken[2][0], ecken[2][1])
        c.line(ecken[1][0], ecken[1][1], ecken[3][0], ecken[3][1])


BAHN_ARTEN = ("luftdicht", "winddicht", "abdichtung", "unterdeckbahn", "lueftungsband")


def _bahn_zeichnen(c, punkte, art, linie):
    """Folie/Bahn als Linienzug: luftdicht (Strich-Punkt), winddicht (gestrichelt),
    abdichtung/unterdeckbahn (kräftig), lueftungsband (feiner Zickzack)."""
    if art == "lueftungsband":
        weg = c.beginPath()
        weg.moveTo(*punkte[0])
        amp, schritt = linie * 1.6, linie * 2.4
        for (ax, ay), (bx, by) in zip(punkte, punkte[1:]):
            ux, uy = _einheit(bx - ax, by - ay)
            laenge, s, oben = math.hypot(bx - ax, by - ay), 0.0, True
            while s < laenge:
                s = min(laenge, s + schritt)
                q = amp if oben else -amp
                weg.lineTo(ax + ux * s - uy * q, ay + uy * s + ux * q)
                oben = not oben
        c.setLineWidth(linie * 0.6)
        c.drawPath(weg, stroke=1, fill=0)
        return
    stil = {"luftdicht": (1.8, [linie * 6, linie * 2, linie * 1, linie * 2]),
            "winddicht": (1.6, [linie * 4, linie * 2.5]),
            "abdichtung": (2.6, []), "unterdeckbahn": (2.0, [])}.get(art, (1.6, []))
    c.setLineWidth(linie * stil[0])
    c.setDash(stil[1])
    weg = c.beginPath()
    weg.moveTo(*punkte[0])
    for p in punkte[1:]:
        weg.lineTo(*p)
    c.drawPath(weg, stroke=1, fill=0)
    c.setDash([])


def _profil_zeichnen(c, punkte, linie, dicke=None, geschlossen=False, fuellen=True):
    """Freie Form: Linienzug, geschlossene Fläche oder Band mit Dicke (z. B. Blech, Ziegel)."""
    if dicke:
        innen = _versatz_linie(punkte, -dicke)
        flaeche = list(punkte) + list(reversed(innen))
        c.setFillColor(WEISS)
        c.drawPath(_pfad(c, flaeche), stroke=0, fill=1)
        c.setStrokeColor(GRUEN)
        c.setLineWidth(linie)
        c.drawPath(_pfad(c, flaeche), stroke=1, fill=0)
        return
    if geschlossen:
        if fuellen:
            c.setFillColor(WEISS)
            c.drawPath(_pfad(c, punkte), stroke=0, fill=1)
        c.setStrokeColor(GRUEN)
        c.setLineWidth(linie)
        c.drawPath(_pfad(c, punkte), stroke=1, fill=0)
        return
    weg = c.beginPath()
    weg.moveTo(*punkte[0])
    for p in punkte[1:]:
        weg.lineTo(*p)
    c.setLineWidth(linie)
    c.drawPath(weg, stroke=1, fill=0)


def zeichne_korrektur(c, k, pt, w, h):
    """Zeichnet ein Element der Korrekturskizze in Grün.

    Grundsatz: Die Skizze zeigt den KORRIGIERTEN ZUSTAND wie eine überarbeitete Zeichnung –
    falsch gezeichnete Teile werden entfernt (weiß abgedeckt), fehlende oder fortzuführende
    Schichten werden mit DERSELBEN Schraffur wie in der Zeichnung eingezeichnet.

    Typen (Koordinaten in Prozent):
      entfernen     {"punkte": [[x, y], …]} oder {"rechteck": […]}   falsch gezeichnetes Teil weiß abdecken
      daemmung      {"punkte": […], "band": [[x,y],[x,y],[x,y]],     Dämmung in Schichtdicke und -richtung;
                     "art": "weich"}                                 "band" = 2 Punkte auf einer Schichtgrenze
                                                                     + 1 Punkt auf der anderen. "art":
                                                                     weich (Schlaufen: Faserdämmstoffe),
                                                                     hart (Zickzack: Dämmplatten),
                                                                     hart_doppelt (gekreuzter Zickzack),
                                                                     geschlaengelt (Wellenlinie: dünne
                                                                     weiche Lagen, z. B. Trittschall)
      holz          {"rechteck": [x1, y1, x2, y2]} oder                Kantholz/Latte/Pfette/Sparren; Kreuz im
                    {"mitte"|"auf": [x,y], "querschnitt_cm": [b,h],   Querschnitt, Faserlinien bei
                     "richtung": [[x,y],[x,y]] | "winkel": Grad,      "schnitt": "laengs"; "auf" = sitzt auf
                     "seite": "oben", "schnitt": "quer"}               einer Linie (Unterseite mittig)
      lattenreihe   {"von", "bis", "querschnitt_cm", "abstand_cm",    Latten gleichen Abstands auf einer Linie
                     "seite", "start_cm"}                            (z. B. Traglatten auf Konterlatten)
      firstlatte    {"mitte", "querschnitt_cm": [3,5],                Firstlatte + Firstlattenhalter
                     "halter_bis": [x,y]}
      firstziegel   {"first": [x,y], "richtung_links", "richtung_rechts" | "neigung",
                     "breite_cm": 24, "hoehe_cm": 7, "dicke_cm": 1.2, "lueftung": true}
                                                                     Firstziegel/-pfanne als Kappe über
                                                                     dem First, mit Lüftungselement
      profil        {"punkte": […], "dicke_cm": d, "geschlossen"}    freie Form (Blech, Halter, Formteil)
      bahn          {"punkte": […], "art": "luftdicht"}              Folie/Bahn: luftdicht | winddicht |
                                                                     abdichtung | unterdeckbahn | lueftungsband
    Maße in cm brauchen den Maßstab: "detail": {"massstab": "1:5"}.
      platte        {"rechteck"|"punkte", "schraffur": "striche"}    Plattenwerkstoff; Schraffur wie in der
                                                                     Zeichnung: striche | zickzack | punkte | diagonal
      abklebung     {"punkte": [[x, y], …]}                          dicke gestrichelte Linie (Klebeband)
      linie         {"punkte": [[x, y], …]}                          durchgezogene Linie
      durchstreichen{"von": [x, y], "bis": [x, y]}                   falschen Wert/Text durchstreichen
      text          {"text": "…", "x", "y", "ziel": [x, y]}          Beschriftung (wird umbrochen und auf
                                                                     dem Blatt gehalten), optional Hinweislinie
    """
    typ = k.get("typ")
    linie = max(1.0, w * 0.0013)
    c.saveState()
    c.setStrokeColor(GRUEN)
    c.setFillColor(GRUEN)
    c.setLineCap(1)
    if typ == "entfernen":
        c.setFillColor(WEISS)
        c.drawPath(_pfad(c, _flaeche(k, pt)), stroke=0, fill=1)
    elif typ == "holz":
        _holz_zeichnen(c, _holz_ecken(k, pt), linie, k.get("schnitt", "quer"))
    elif typ == "lattenreihe":
        for ecken in _lattenreihe_ecken(k, pt):
            _holz_zeichnen(c, ecken, linie)
    elif typ == "firstlatte":
        teile = _firstlatte_teile(k, pt)
        c.setLineWidth(linie * 0.8)
        for (a, b) in teile["halter"]:
            c.line(a[0], a[1], b[0], b[1])
        _holz_zeichnen(c, teile["latte"], linie)
    elif typ == "firstziegel":
        umriss = _firstziegel_umriss(k, pt)
        dicke = _cm(k.get("dicke_cm", 1.2))
        # Linienzug läuft links→rechts über den First; innen liegt rechts der Laufrichtung
        _profil_zeichnen(c, umriss, linie, dicke=dicke)
        if k.get("lueftung", True):   # Lüftungselement/Firstrolle: unter dem Ziegelrand auf der Deckung
            for ende, auslauf in ((umriss[1], umriss[0]), (umriss[5], umriss[6])):
                ux, uy = _einheit(ende[0] - auslauf[0], ende[1] - auslauf[1])   # Richtung zum First
                fuss = (ende[0] - ux * _cm(1.0), ende[1] - _cm(0.6) - uy * _cm(1.0))
                kopf = (fuss[0] + ux * _cm(5), fuss[1] + uy * _cm(5))
                c.setStrokeColor(GRUEN)
                _bahn_zeichnen(c, [fuss, kopf], "lueftungsband", linie)
    elif typ == "profil":
        punkte = [pt(x, y) for x, y in k["punkte"]]
        dicke = _cm(k["dicke_cm"]) if k.get("dicke_cm") else None
        _profil_zeichnen(c, punkte, linie, dicke=dicke, geschlossen=k.get("geschlossen", False),
                         fuellen=k.get("fuellung", "weiss") == "weiss")
    elif typ == "bahn":
        art = str(k.get("art", "luftdicht")).lower().replace("ü", "ue")
        if art not in BAHN_ARTEN:
            print(f"Warnung: unbekannte Bahn-Art „{art}“ ({', '.join(BAHN_ARTEN)}).")
        _bahn_zeichnen(c, [pt(x, y) for x, y in k["punkte"]], art, linie)
    elif typ == "platte":
        punkte = _flaeche(k, pt)
        if not k.get("punkte") and not k.get("band"):
            # Rechteck: Schichtrichtung = lange Seite (oder "richtung": "laengs"/"quer")
            lx, ux = min(p[0] for p in punkte), max(p[0] for p in punkte)
            ly, uy = min(p[1] for p in punkte), max(p[1] for p in punkte)
            senkrecht = (uy - ly) > (ux - lx)
            if k.get("richtung") in ("laengs", "quer"):
                senkrecht = k["richtung"] == "quer"
            punkte = ([(lx, uy), (lx, ly), (ux, ly), (ux, uy)] if senkrecht
                      else [(lx, uy), (ux, uy), (ux, ly), (lx, ly)])
        pfad = _pfad(c, punkte)
        c.setFillColor(WEISS)
        c.drawPath(pfad, stroke=0, fill=1)
        c.saveState()
        c.clipPath(_pfad(c, punkte), stroke=0, fill=0)
        c.setStrokeColor(GRUEN)
        c.setFillColor(GRUEN)
        _plattenschraffur(c, k.get("schraffur", "striche"), punkte, k, pt, w, linie)
        c.restoreState()
        c.setStrokeColor(GRUEN)
        c.setLineWidth(linie)
        c.drawPath(_pfad(c, punkte), stroke=1, fill=0)
    elif typ == "daemmung":
        punkte = _flaeche(k, pt)
        c.setFillColor(WEISS)
        c.drawPath(_pfad(c, punkte), stroke=0, fill=1)
        c.saveState()
        c.clipPath(_pfad(c, punkte), stroke=0, fill=0)
        c.setStrokeColor(GRUEN)
        art = str(k.get("art", "weich")).lower().replace("ä", "ae")
        if art not in DAEMM_ARTEN and k.get("schraffur") != "kreuz":
            print(f"Warnung: unbekannte Dämmstoff-Art „{art}“ – verwende „weich“ ({', '.join(DAEMM_ARTEN)}).")
            art = "weich"
        if art == "hart":
            _zickzack(c, k, punkte, pt, linie)
        elif art == "hart_doppelt":
            _zickzack(c, k, punkte, pt, linie, doppelt=True)
        elif art == "geschlaengelt":
            _welle(c, k, punkte, pt, linie)
        elif k.get("schraffur") == "kreuz":  # alte Darstellung, nur auf Wunsch
            xs, ys = [p[0] for p in punkte], [p[1] for p in punkte]
            hoehe, abstand = max(ys) - min(ys), max(3.0, w * 0.004)
            c.setLineWidth(linie * 0.6)
            t = -hoehe
            while t <= max(xs) - min(xs):
                c.line(min(xs) + t, min(ys), min(xs) + t + hoehe, max(ys))
                c.line(min(xs) + t, max(ys), min(xs) + t + hoehe, min(ys))
                t += abstand * 1.6
        else:
            _schlaufen(c, k, punkte, pt, linie)
        c.restoreState()
        if k.get("umriss"):
            c.setStrokeColor(GRUEN)
            c.setLineWidth(linie * 0.8)
            c.drawPath(_pfad(c, punkte), stroke=1, fill=0)
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
        x, y, zeilen, schrift, gr, breite, hoehe = text_box(k, pt, w, h)
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


def korrigierte_seite(pdf_ein, daten, hinweistexte=True):
    """Gibt (PdfWriter mit Korrekturskizze, Seitennummer, Anzahl Elemente) zurück.

    hinweistexte=False lässt Beschriftungen mit Rahmen/Hinweislinie weg (für die kleinen
    Ausschnitte in den Befundkarten – dort steht der Text ohnehin in der Karte).
    Ersatzwerte direkt im Text ("rahmen": false) bleiben immer sichtbar."""
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
    massstab_setzen(daten)
    elemente = [k for b in befunde_lesen(daten) for k in b.get("korrektur", [])]
    if not hinweistexte:
        elemente = [k for k in elemente if k.get("typ") != "text" or k.get("rahmen") is False]
    # Entfernen zuerst, dann Flächen, Bauteile, Linien, Texte zuletzt
    reihenfolge = {"entfernen": -1, "daemmung": 0, "platte": 0.5, "bahn": 0.55, "holz": 0.6,
                   "lattenreihe": 0.6, "profil": 0.7, "firstlatte": 0.8, "firstziegel": 0.9,
                   "abklebung": 1, "linie": 1, "durchstreichen": 2, "text": 3}
    for k in sorted(elemente, key=lambda k: reihenfolge.get(k.get("typ"), 1)):
        try:
            zeichne_korrektur(c, k, pt, w, h)
        except (KeyError, ValueError, TypeError) as fehler:
            print(f"Warnung: Korrekturelement „{k.get('typ')}“ übersprungen – {fehler}")
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
