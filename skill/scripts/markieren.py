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


def korrektur_grenzen(daten, w, h):
    """Umrandendes Rechteck aller Korrekturelemente (inkl. Hinweistexte) in Prozent – damit der
    Bericht beim Zuschneiden nichts abschneidet. None, wenn es keine Elemente gibt."""
    xs, ys = [], []

    def pt(x, y):
        return x / 100 * w, h - y / 100 * h

    for b in befunde_lesen(daten):
        for k in b.get("korrektur", []):
            if k.get("typ") == "text":
                x, y, _, _, gr, breite, hoehe = text_box(k, pt, w, h)
                xs += [x - gr * 0.3, x + breite + gr * 0.3]
                ys += [y + gr, y - hoehe + gr * 0.85]
                if k.get("ziel"):
                    zx, zy = pt(*k["ziel"])
                    xs.append(zx)
                    ys.append(zy)
            else:
                for p in (k.get("punkte") or ([k["rechteck"][:2], k["rechteck"][2:]] if k.get("rechteck")
                                               else [k.get("von"), k.get("bis")])):
                    if p:
                        px, py = pt(*p)
                        xs.append(px)
                        ys.append(py)
    if not xs:
        return None
    return [min(xs) / w * 100, 100 - max(ys) / h * 100, max(xs) / w * 100, 100 - min(ys) / h * 100]


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
      holz          {"rechteck": [x1, y1, x2, y2]}                    Kantholz/Latte im Schnitt (Kreuz)
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
        x1, y1, x2, y2 = k["rechteck"]
        (ax, ay), (bx, by) = pt(x1, y1), pt(x2, y2)
        lx, ux = min(ax, bx), max(ax, bx)
        ly, uy = min(ay, by), max(ay, by)
        c.setFillColor(WEISS)
        c.rect(lx, ly, ux - lx, uy - ly, stroke=0, fill=1)  # darunterliegende Linien abdecken
        c.setStrokeColor(GRUEN)
        c.setLineWidth(linie)
        c.rect(lx, ly, ux - lx, uy - ly, stroke=1, fill=0)
        c.line(lx, ly, ux, uy)
        c.line(lx, uy, ux, ly)
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
    elemente = [k for b in befunde_lesen(daten) for k in b.get("korrektur", [])]
    if not hinweistexte:
        elemente = [k for k in elemente if k.get("typ") != "text" or k.get("rahmen") is False]
    # Entfernen zuerst, dann Flächen, Linien, Texte zuletzt
    for k in sorted(elemente, key=lambda k: {"entfernen": -1, "daemmung": 0, "platte": 0.5, "holz": 0.6,
                                              "abklebung": 1, "linie": 1, "durchstreichen": 2,
                                              "text": 3}.get(k.get("typ"), 1)):
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
