"""Zeichnet die eigenen Referenzskizzen der Detailtypen (pruefkatalog/12_detailtypen.md).

Schematische Prinzipskizzen (nicht maßstäblich genau, Maße in cm als übliche Werte), damit
der Skill die LAGE der Bauteile zueinander nachschlagen kann. Selbst gezeichnet nach den
im Katalog genannten Quellen – keine fremden Zeichnungen.

Aufruf:  python referenz.py <zielordner>      → <zielordner>/<name>.png und .pdf
"""
import io
import math
import os
import sys

import pypdfium2 as pdfium
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCHWARZ = HexColor("#111111")
GRAU = HexColor("#6B7280")
ROT = HexColor("#C62828")      # luftdichte Ebene
BLAU = HexColor("#1F6FB2")     # Wind-/Wasserführung


class Skizze:
    """Weltkoordinaten in cm (x nach rechts, y nach oben)."""

    def __init__(self, titel, untertitel, breite=842, hoehe=595, mass=3.2, ursprung=(300, 300)):
        self.puffer = io.BytesIO()
        self.c = canvas.Canvas(self.puffer, pagesize=(breite, hoehe))
        self.b, self.h, self.s = breite, hoehe, mass
        self.o = ursprung
        self.legende = []
        self.c.setFont("Helvetica-Bold", 13)
        self.c.drawString(30, hoehe - 34, titel)
        self.c.setFont("Helvetica", 8.5)
        self.c.setFillColor(GRAU)
        self.c.drawString(30, hoehe - 48, untertitel)
        self.c.setFillColor(SCHWARZ)

    def p(self, x, y):
        return self.o[0] + x * self.s, self.o[1] + y * self.s

    # ---------------------------------------------------------------- Grundformen
    def _pfad(self, pkt):
        pf = self.c.beginPath()
        pf.moveTo(*self.p(*pkt[0]))
        for q in pkt[1:]:
            pf.lineTo(*self.p(*q))
        pf.close()
        return pf

    def flaeche(self, pkt, schraffur=None, linie=0.7, fuellen=True, farbe=SCHWARZ, richtung=None):
        c = self.c
        c.saveState()
        if fuellen:
            c.setFillColor(white)
            c.drawPath(self._pfad(pkt), stroke=0, fill=1)
        if schraffur:
            c.saveState()
            c.clipPath(self._pfad(pkt), stroke=0, fill=0)
            self._schraffur(pkt, schraffur, richtung)
            c.restoreState()
        c.setStrokeColor(farbe)
        c.setLineWidth(linie)
        c.drawPath(self._pfad(pkt), stroke=1, fill=0)
        c.restoreState()

    def _schraffur(self, pkt, art, richtung):
        c = self.c
        xs = [self.p(*q)[0] for q in pkt]
        ys = [self.p(*q)[1] for q in pkt]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        c.setStrokeColor(SCHWARZ)
        c.setLineWidth(0.35)
        if art == "diagonal":        # Holzwerkstoffplatte, Ziegel
            d = 4
            for k in range(int((x1 - x0 + y1 - y0) / d) + 2):
                c.line(x0 + k * d, y0, x0 + k * d - (y1 - y0), y1)
        elif art == "punkte":         # Gipskarton, Mörtel
            c.setFillColor(SCHWARZ)
            for i, x in enumerate(range(int(x0), int(x1), 4)):
                for j, y in enumerate(range(int(y0), int(y1), 4)):
                    c.circle(x + (j % 2) * 2, y, 0.35, stroke=0, fill=1)
        elif art == "beton":
            c.setFillColor(SCHWARZ)
            n = 0
            for x in range(int(x0), int(x1), 6):
                for y in range(int(y0), int(y1), 6):
                    n += 1
                    c.circle(x + (n * 7) % 5, y + (n * 3) % 5, 0.5, stroke=0, fill=1)
        elif art == "kies":
            for x in range(int(x0), int(x1), 7):
                for y in range(int(y0), int(y1), 6):
                    c.circle(x + (y % 3), y, 2.0, stroke=1, fill=0)
        elif art == "zickzack" and richtung:  # Holzfaser-/Hartschaumplatte
            self._zickzack(richtung)
        elif art == "weich" and richtung:     # Faserdämmstoff
            self._weich(richtung)

    def _band_punkte(self, richtung):
        (ax, ay), (bx, by), dicke = richtung     # Grundlinie a→b, Dicke nach links (cm)
        ux, uy = bx - ax, by - ay
        lang = math.hypot(ux, uy)
        ux, uy = ux / lang, uy / lang
        return (ax, ay), (ux, uy), (-uy, ux), lang, dicke

    def _zickzack(self, richtung):
        (ax, ay), (ux, uy), (nx, ny), lang, dicke = self._band_punkte(richtung)
        schritt = max(dicke * 0.5, 1.2)
        pf = self.c.beginPath()
        pf.moveTo(*self.p(ax, ay))
        t, oben = 0.0, True
        while t <= lang + schritt:
            t += schritt
            d = dicke if oben else 0
            pf.lineTo(*self.p(ax + ux * t + nx * d, ay + uy * t + ny * d))
            oben = not oben
        self.c.drawPath(pf, stroke=1, fill=0)

    def _weich(self, richtung):
        """Weiche Dämmung als gleichmäßige Schlaufen zwischen beiden Schichtgrenzen."""
        (ax, ay), (ux, uy), (nx, ny), lang, dicke = self._band_punkte(richtung)
        c_ = dicke / 2
        a_ = dicke * 0.16
        b_ = dicke * 0.42
        pf = self.c.beginPath()
        th, erster = -math.pi, True
        while True:
            t = a_ * th - b_ * math.sin(th)
            d = c_ - c_ * math.cos(th)
            q = self.p(ax + ux * t + nx * d, ay + uy * t + ny * d)
            if erster:
                pf.moveTo(*q)
                erster = False
            else:
                pf.lineTo(*q)
            if t > lang + dicke:
                break
            th += 0.12
        self.c.setLineWidth(0.4)
        self.c.drawPath(pf, stroke=1, fill=0)

    def band(self, a, b, d1, d2, schraffur=None, linie=0.7):
        """Schicht entlang der Linie a→b zwischen den Abständen d1 < d2 (cm, links der Richtung)."""
        ux, uy = b[0] - a[0], b[1] - a[1]
        lang = math.hypot(ux, uy)
        nx, ny = -uy / lang, ux / lang
        q = lambda pkt, d: (pkt[0] + nx * d, pkt[1] + ny * d)
        pkt = [q(a, d1), q(b, d1), q(b, d2), q(a, d2)]
        self.flaeche(pkt, schraffur, linie, richtung=(q(a, d1), q(b, d1), d2 - d1))
        return pkt

    def holz(self, x0, y0, x1, y1, laengs=False, winkel=0, gestrichelt=False):
        """Kantholz im Querschnitt (Kreuz) bzw. längs (Faserlinien); winkel dreht um die Mitte."""
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        w = math.radians(winkel)
        def r(x, y):
            dx, dy = x - mx, y - my
            return mx + dx * math.cos(w) - dy * math.sin(w), my + dx * math.sin(w) + dy * math.cos(w)
        e = [r(x0, y0), r(x1, y0), r(x1, y1), r(x0, y1)]
        c = self.c
        c.saveState()
        if gestrichelt:
            c.setDash([3, 2])
        self.flaeche(e, linie=0.9)
        c.setLineWidth(0.5)
        if gestrichelt:
            c.setDash([3, 2])
        if laengs:
            for k in (0.3, 0.55, 0.8):
                a, b = r(x0 + (x1 - x0) * 0.05, y0 + (y1 - y0) * k), r(x1 - (x1 - x0) * 0.05, y0 + (y1 - y0) * k)
                c.line(*self.p(*a), *self.p(*b))
        else:
            c.line(*self.p(*e[0]), *self.p(*e[2]))
            c.line(*self.p(*e[1]), *self.p(*e[3]))
        c.restoreState()
        return e

    def linie(self, pkt, farbe=SCHWARZ, breite=0.8, strich=None):
        c = self.c
        c.saveState()
        c.setStrokeColor(farbe)
        c.setLineWidth(breite)
        if strich:
            c.setDash(strich)
        pf = c.beginPath()
        pf.moveTo(*self.p(*pkt[0]))
        for q in pkt[1:]:
            pf.lineTo(*self.p(*q))
        c.drawPath(pf, stroke=1, fill=0)
        c.restoreState()

    def luftdicht(self, pkt):
        self.linie(pkt, ROT, 1.6, [5, 1.5, 1, 1.5])

    def winddicht(self, pkt):
        self.linie(pkt, BLAU, 1.4, [4, 2])

    def nr(self, n, ziel, pos, text):
        """Nummer mit Hinweislinie; Text in die Legende."""
        c = self.c
        zx, zy = self.p(*ziel)
        px, py = self.p(*pos)
        px = min(max(px, 22), self.b - 268)
        py = min(max(py, 40), self.h - 70)
        c.saveState()
        c.setStrokeColor(GRAU)
        c.setLineWidth(0.5)
        c.line(px, py, zx, zy)
        c.setFillColor(SCHWARZ)
        c.circle(zx, zy, 1.1, stroke=0, fill=1)
        c.setFillColor(white)
        c.setStrokeColor(SCHWARZ)
        c.circle(px, py, 6.5, stroke=1, fill=1)
        c.setFillColor(SCHWARZ)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(px, py - 2.6, str(n))
        c.restoreState()
        self.legende.append((n, text))

    def text(self, x, y, t, groesse=7.5, farbe=GRAU):
        self.c.setFont("Helvetica", groesse)
        self.c.setFillColor(farbe)
        self.c.drawString(*self.p(x, y), t)
        self.c.setFillColor(SCHWARZ)

    def fertig(self, ziel, name, quellen):
        c = self.c
        x, y = self.b - 250, self.h - 80
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x, y, "Bauteile")
        y -= 14
        c.setFont("Helvetica", 7.6)
        for n, t in sorted(self.legende):
            zeilen = _umbrechen(t, 44)
            c.drawString(x, y, f"{n:>2}  {zeilen[0]}")
            for z in zeilen[1:]:
                y -= 9.5
                c.drawString(x + 13, y, z)
            y -= 11.5
        y -= 6
        c.setStrokeColor(ROT); c.setLineWidth(1.6); c.setDash([5, 1.5, 1, 1.5])
        c.line(x, y + 3, x + 22, y + 3); c.setDash()
        c.drawString(x + 28, y, "luftdichte Ebene / Dampfbremse")
        y -= 12
        c.setStrokeColor(BLAU); c.setLineWidth(1.4); c.setDash([4, 2])
        c.line(x, y + 3, x + 22, y + 3); c.setDash()
        c.drawString(x + 28, y, "Wind-/Wasserführung (Unterdeckung, Bahn)")
        c.setStrokeColor(SCHWARZ)
        c.setFont("Helvetica", 6.8)
        c.setFillColor(GRAU)
        c.drawString(30, 22, "Eigene schematische Prinzipskizze (Detailprüfer Architektur), nicht maßstäblich – eine richtige "
                     "Lösung von mehreren. Grundlagen: " + quellen)
        c.save()
        os.makedirs(ziel, exist_ok=True)
        png = os.path.join(ziel, name + ".png")
        bild = pdfium.PdfDocument(self.puffer.getvalue())[0].render(scale=1.6).to_pil()
        bild.convert("RGB").quantize(24).save(png, optimize=True)   # wenige Farben, klein für den Skill
        return png


def _umbrechen(t, n):
    w, z = t.split(), [""]
    for x in w:
        if len(z[-1]) + len(x) + 1 > n:
            z.append(x)
        else:
            z[-1] = (z[-1] + " " + x).strip()
    return z


def _hang(winkel, seite):
    """Einheitsvektor entlang der Dachfläche vom First nach außen (seite -1 links, +1 rechts)."""
    a = math.radians(winkel)
    return seite * math.cos(a), -math.sin(a)


def _versatz(seite, a_deg, t, d):
    """Punkt auf der Schichtgrenze mit Abstand d (cm, + = nach außen, 0 = Sparren-Unterkante):
    die Grenze trifft die Firstachse bei y = d / cos(a); t = Weg entlang der Dachfläche ab dort."""
    a = math.radians(a_deg)
    ux, uy = _hang(a_deg, seite)
    return (ux * t, d / math.cos(a) + uy * t)


def _t_bei_x(a_deg, x):
    """Weg entlang der Dachfläche bis zum waagerechten Abstand x von der Firstachse."""
    return abs(x) / math.cos(math.radians(a_deg))


def _dachband(sk, seite, a_deg, d1, d2, t0, t1, art=None, linie=0.7):
    pkt = [_versatz(seite, a_deg, t0, d1), _versatz(seite, a_deg, t1, d1),
           _versatz(seite, a_deg, t1, d2), _versatz(seite, a_deg, t0, d2)]
    # Dicke senkrecht zur Fläche = d2 - d1; Richtung so, dass „links“ nach außen zeigt
    richtung = (pkt[0], pkt[1], d2 - d1) if seite == 1 else (pkt[1], pkt[0], d2 - d1)
    sk.flaeche(pkt, art, linie, richtung=richtung)
    return pkt


def _dachschichten(sk, a_deg, laenge, innen_ab=0.0, mit_innen=True, offset0=0.0):
    """Schichten beidseits des Firsts. Abstand 0 = Sparren-Unterkante; innen_ab = waagerechter
    Abstand zur Firstachse, ab dem die Innenschichten beginnen (z. B. Pfettenflanke)."""
    for seite in (-1, 1):
        _dachband(sk, seite, a_deg, 0, 20, 0, laenge, "weich")
        _dachband(sk, seite, a_deg, 20, 22.2, 0, laenge, "zickzack")
        if mit_innen:
            t0 = _t_bei_x(a_deg, innen_ab) if innen_ab else 0
            # Grenzlinien unterhalb: bei Start an der Pfettenflanke den Weg je Grenze anpassen
            for d1, d2, art in ((-4.0, 0.0, "weich"), (-5.25, -4.0, "punkte")):
                if innen_ab:
                    a = math.radians(a_deg)
                    ta = (innen_ab - 0) / math.cos(a)
                    pkt = [_versatz(seite, a_deg, ta, d1), _versatz(seite, a_deg, laenge, d1),
                           _versatz(seite, a_deg, laenge, d2), _versatz(seite, a_deg, ta, d2)]
                    richtung = (pkt[0], pkt[1], d2 - d1) if seite == 1 else (pkt[1], pkt[0], d2 - d1)
                    sk.flaeche(pkt, art, 0.7, richtung=richtung)
                else:
                    _dachband(sk, seite, a_deg, d1, d2, 0, laenge, art)


def _deckung(sk, a_deg, laenge, d0=22.2, first=True):
    """Konterlattung (Band), Traglatten (Querschnitt), Deckung (Band) und Firstabdeckung."""
    a = math.radians(a_deg)
    for seite in (-1, 1):
        # Konterlattung als Band (längs geschnitten)
        p = [_versatz(seite, a_deg, t, d) for t, d in ((0, d0), (laenge, d0), (laenge, d0 + 4), (0, d0 + 4))]
        sk.flaeche(p, linie=0.5)
        # Traglatten 3/5 im Querschnitt
        t = 12
        while t < laenge - 3:
            m = _versatz(seite, a_deg, t, d0 + 4 + 1.5)
            sk.holz(m[0] - 2.5, m[1] - 1.5, m[0] + 2.5, m[1] + 1.5, winkel=-seite * a_deg)
            t += 33
        # Deckung als Band
        p = [_versatz(seite, a_deg, t, d) for t, d in ((12, d0 + 7), (laenge + 6, d0 + 7), (laenge + 6, d0 + 10), (12, d0 + 10))]
        sk.flaeche(p, "diagonal", 0.6)
    sk.winddicht([_versatz(-1, a_deg, laenge, d0 + 0.3), _versatz(-1, a_deg, 0, d0 + 0.3),
                  _versatz(1, a_deg, laenge, d0 + 0.3)])
    if first:
        y_kl = d0 / math.cos(a)
        ziegel = lambda x: (d0 + 10) / math.cos(a) - abs(x) * math.tan(a)   # Oberseite Deckung
        # Firstlatte 4/6 hochkant auf Haltern
        sk.linie([(0, y_kl + 0.5), (0, y_kl + 6)], SCHWARZ, 0.9)
        sk.holz(-2, y_kl + 6, 2, y_kl + 12)
        # Firstziegel als Kappe über den obersten Ziegeln, Lüftungselement darunter
        top = max(ziegel(0) + 4, y_kl + 15)
        kappe = [(-22, ziegel(22) + 0.8), (-8, top), (8, top), (22, ziegel(22) + 0.8)]
        sk.linie(kappe, SCHWARZ, 2.2)
        sk.linie([(-20, ziegel(20) + 0.3), (-8, ziegel(8) + 1.5)], BLAU, 1.0, [1.5, 1.5])
        sk.linie([(20, ziegel(20) + 0.3), (8, ziegel(8) + 1.5)], BLAU, 1.0, [1.5, 1.5])


def first_pfettendach(ziel):
    a = 30
    sk = Skizze("Referenz DT-D1 · First, Pfettendach, Zwischensparrendämmung",
                "Firstpfette UNTER den Sparren (Sparren aufgekervt); Oberkante nach Maß der Zeichnung, sonst im Schnittpunkt der Sparren-Unterkanten;"
                " Innenaufbau endet an der Pfette, Dampfbremse luftdicht angeschlossen.",
                ursprung=(285, 330), mass=2.6)
    L = 85
    _dachschichten(sk, a, L, innen_ab=7.0)
    # Firstpfette 14/28 – Oberkante im Schnittpunkt der Sparren-Unterkanten (0,0)
    sk.holz(-7, -28, 7, 0)
    # Dampfbremse unter den Sparren, an die Pfettenflanken angeschlossen
    for seite in (-1, 1):
        t0 = 7 / math.cos(math.radians(a))
        p0 = _versatz(seite, a, t0, 0)
        sk.luftdicht([_versatz(seite, a, L, 0), p0, (seite * 7, p0[1] - 5)])
    _deckung(sk, a, L)
    # Sparren-Pfetten-Verschraubung: schräge Schrauben aus den Sparren in die Pfette
    for seite in (-1, 1):
        sk.linie([_versatz(seite, a, 30, 21), (-seite * 3, -14)], GRAU, 0.8, [6, 2, 1, 2])
    sk.nr(11, _versatz(1, a, 18, 14), (70, 62), "Schrauben (z. B. Tellerkopf-/Vollgewindeschrauben) schräg durch die Sparren IN die Pfette – laufen sie ins Leere, fehlt die Pfette")
    sk.nr(1, (0, 31), (-60, 60), "Firstziegel auf Firstlatte, Lüftungselement mit Insektenschutz (Abluft ≥ 0,5 ‰, ≥ 50 cm²/m)")
    sk.nr(2, (0, 22), (-45, 72), "Firstlatte (z. B. 4/6 hochkant) auf Firstlattenhaltern")
    sk.nr(3, _versatz(-1, a, 45, 30), (-95, 40), "Deckung auf Traglattung 3/5")
    sk.nr(4, _versatz(-1, a, 55, 24), (-110, 20), "Konterlattung = Belüftungsebene ≥ 20 mm")
    sk.nr(5, _versatz(-1, a, 60, 21), (-115, 2), "Unterdeckplatte/-bahn, über den First geführt (2. wasserführende Ebene)")
    sk.nr(6, _versatz(-1, a, 40, 10), (-110, -18), "Sparren mit Volldämmung bis an die Pfette, ohne Hohlraum")
    sk.nr(7, (0, -14), (40, -55), "Firstpfette (Querschnitt nach Statik, z. B. 14/28) – Sparren liegen mit Kerve auf")
    sk.nr(8, _versatz(1, a, 30, -0.3), (75, -30), "Dampfbremse/luftdichte Ebene, an der Pfette luftdicht abgeklebt")
    sk.nr(9, _versatz(1, a, 50, -3), (95, -10), "Installationsebene, endet an der Pfette")
    sk.nr(10, _versatz(1, a, 70, -5.5), (110, 8), "Bekleidung (z. B. Gipsplatte)")
    sk.text(-10, -36, "Firstachse")
    sk.linie([(0, -34), (0, 45)], GRAU, 0.4, [6, 2, 1, 2])
    return sk.fertig(ziel, "first_pfettendach", "Informationsdienst Holz, holzbau handbuch R5/T2/F2 (2023); BauNetz Wissen Pfettendach, First.")


def first_sparrendach(ziel):
    a = 35
    sk = Skizze("Referenz DT-D2 · First, Sparrendach (ohne Firstpfette)",
                "Sparrenpaar stützt sich im First gegenseitig (Firstverbindung innerhalb der Sparrenhöhe);"
                " luftdichte Ebene läuft ohne Unterbrechung über den First.", ursprung=(285, 320), mass=2.6)
    L = 85
    _dachschichten(sk, a, L, innen_ab=0.0)
    for seite in (-1, 1):
        sk.luftdicht([_versatz(seite, a, L, 0), (0, 0)])
    # Sparren in Ansicht (gestrichelt) mit Laschen als Firstverbindung
    for seite in (-1, 1):
        sk.linie([_versatz(seite, a, 0, 0), _versatz(seite, a, L, 0), _versatz(seite, a, L, 20), _versatz(seite, a, 0, 20)],
                 GRAU, 0.6, [3, 2])
    sk.holz(-14, 2, 14, 14, laengs=True, gestrichelt=True)
    _deckung(sk, a, L)
    sk.nr(1, (0, 34), (-60, 62), "Firstabdeckung wie DT-D1 (Firstziegel, Lüftung, Firstlatte, Halter)")
    sk.nr(2, (8, 8), (55, 55), "Firstverbindung des Sparrenpaars (z. B. Laschen, Blatt, Scherzapfen) – nach Statik; Sparren in Ansicht")
    sk.nr(3, _versatz(-1, a, 40, 10), (-110, -10), "Volldämmung zwischen den Sparren bis in den First")
    sk.nr(4, (0, 0), (40, -40), "luftdichte Ebene unter den Sparren, über den First durchgehend")
    sk.nr(5, _versatz(1, a, 60, -5.5), (100, -15), "Installationsebene und Bekleidung, im First zusammengeführt")
    sk.nr(6, _versatz(-1, a, 60, 21), (-115, 15), "Unterdeckung über den First (bei kaltem Dachraum mit Lüftungsschlitz ~10 cm)")
    sk.linie([(0, -20), (0, 50)], GRAU, 0.4, [6, 2, 1, 2])
    sk.text(-60, -70, "Firstachse; Fußpunkt zugfest mit Deckenbalken/Decke verbunden (nicht dargestellt)")
    return sk.fertig(ziel, "first_sparrendach", "BauNetz Wissen Sparrendach, Kehlbalkendach; Informationsdienst Holz R5/T2/F2 (2023).")


def _wand_vertikal(sk, x_aussen, y0, y1, mit_fassade=True):
    """Holzrahmenwand von außen (x_aussen) nach innen (+x): Fassade, Lattung, Platte, Gefach, OSB, Install., GK."""
    x = x_aussen
    teile = []
    if mit_fassade:
        teile += [(2.4, "diagonal", "Fassade"), (3.0, None, "Lattung"), ]
    teile += [(1.6, "zickzack", "Holzfaser/MDF"), (24.0, "weich", "Gefach"), (1.5, "diagonal", "OSB"),
              (4.0, "weich", "Inst."), (1.25, "punkte", "GK")]
    lagen = {}
    for d, art, name in teile:
        p = [(x, y0), (x + d, y0), (x + d, y1), (x, y1)]
        richtung = ((x + d, y0), (x + d, y1), d) if art in ("weich", "zickzack") else None
        if art in ("weich", "zickzack"):
            sk.flaeche(p, art, richtung=((x, y1), (x, y0), d))
        else:
            sk.flaeche(p, art, linie=0.6 if art else 0.4)
        lagen[name] = (x, x + d)
        x += d
    return lagen


def ortgang(ziel):
    sk = Skizze("Referenz DT-D6 · Ortgang (Giebelwand Holzrahmenbau, Schnitt parallel zur Traufe)",
                "Rähm auf dem Ständerwerk unter der Dachplatte; Dachdämmung bis an die Wand; Fassaden-Hinterlüftung"
                " oben offen mit Insektenschutz; luftdichter Anschluss Wand–Dach.", ursprung=(160, 150), mass=2.8)
    lagen = _wand_vertikal(sk, 0, 0, 70)
    xg0, xg1 = lagen["Gefach"]
    # Rähm 10 × Wanddicke Ständerwerk unter der Dachplatte
    sk.holz(xg0, 70, xg1, 80)
    for name in ("Holzfaser/MDF", "OSB", "Inst.", "GK"):
        x0, x1 = lagen[name]
        if name in ("Holzfaser/MDF",):
            sk.flaeche([(x0, 70), (x1, 70), (x1, 80), (x0, 80)], "zickzack", richtung=((x0, 80), (x0, 70), x1 - x0))
    xi = lagen["GK"][1]
    # Dachaufbau waagerecht: Dach-OSB auf Rähm, Sparren mit Dämmung, Unterdeckplatte, Lattung, Deckung
    yd = 80
    sk.flaeche([(xg0, yd), (125, yd), (125, yd + 1.5), (xg0, yd + 1.5)], "diagonal")          # Dach-OSB
    sk.flaeche([(xg0, yd + 1.5), (125, yd + 1.5), (125, yd + 25.5), (xg0, yd + 25.5)], "weich",
               richtung=((xg0, yd + 1.5), (125, yd + 1.5), 24))
    for xs in (xg1 + 10, xg1 + 90):
        sk.holz(xs, yd + 1.5, xs + 8, yd + 25.5)
    sk.flaeche([(-30, yd + 25.5), (125, yd + 25.5), (125, yd + 29.5), (-30, yd + 29.5)], "diagonal")   # Überstand/Platte
    sk.winddicht([(-30, yd + 29.7), (125, yd + 29.7)])
    for xl in (-25, 15, 55, 95):
        sk.holz(xl, yd + 29.5, xl + 5, yd + 32.5)                   # Konterlatten (quer geschnitten)
    sk.flaeche([(-27, yd + 32.5), (125, yd + 32.5), (125, yd + 35.5), (-27, yd + 35.5)], linie=0.5)  # Traglattung längs
    sk.flaeche([(-33, yd + 35.5), (125, yd + 35.5), (125, yd + 39), (-33, yd + 39)], "diagonal")
    sk.flaeche([(-36, yd + 22), (-33, yd + 22), (-33, yd + 39), (-36, yd + 39)], "diagonal")   # Ortgangziegel-Schenkel
    # Innen: Installationsebene und GK unter der Dach-OSB, ab Innenkante Wand
    sk.flaeche([(lagen["OSB"][0], yd - 4), (125, yd - 4), (125, yd), (lagen["OSB"][0], yd)], "weich",
               richtung=((lagen["OSB"][0], yd - 4), (125, yd - 4), 4))
    sk.flaeche([(xi, yd - 5.25), (125, yd - 5.25), (125, yd - 4), (xi, yd - 4)], "punkte")
    sk.luftdicht([(lagen["OSB"][1], 40), (lagen["OSB"][1], yd), (125, yd)])
    # Fassade endet unter dem Überstand mit Abluftspalt, oberste Latte
    sk.holz(2.4, 60, 5.4, 65)
    sk.linie([(1.0, 66), (1.0, 69)], BLAU, 1.2, [1, 1])
    sk.nr(1, (-34, yd + 30), (-55, 120), "seitlicher Abschluss: Ortgangziegel (oder Ortgangbrett mit Abdeckung), befestigt")
    sk.nr(2, (40, yd + 29.7), (40, 135), "Unterdeckung bis zur Außenkante")
    sk.nr(3, (20, yd + 27), (-60, 100), "Dachüberstand (z. B. Holzplatte, bindet ins Dach ein)")
    sk.nr(4, ((xg0 + xg1) / 2, 75), (70, 50), "Rähm auf dem Ständerwerk (Querschnitt nach Statik), Dachplatte liegt auf")
    sk.nr(5, (80, yd + 14), (120, 135), "Dachdämmung in voller Sparrenhöhe bis an die Wand")
    sk.nr(6, (lagen["OSB"][1], yd), (100, 55), "luftdichte Ebene Wand–Dach durchgehend (Stoß abgeklebt)")
    sk.nr(7, (1.0, 67), (-45, 70), "Abluft der Hinterlüftung mit Insektenschutz")
    sk.nr(8, (3.9, 62.5), (-45, 50), "oberste Fassadenlatte nahe der Oberkante")
    return sk.fertig(ziel, "ortgang", "Informationsdienst Holz R5/T2/F2 (2023); BauNetz Wissen Unterdeckung Außenränder, Tafelbau/Rahmenbau.")


def traufe_pfettendach(ziel):
    a = 30
    ar = math.radians(a)
    sk = Skizze("Referenz DT-D4 · Traufe, Sparren auf Rähm/Fußpfette (Holzrahmenbau)",
                "Sparren liegen auf dem Rähm (bzw. Fußpfette) der Wand; Stellbrett als Dämmabschluss; Zuluft mit"
                " Insektenschutz; Unterdeckung auf das Traufblech; luftdichte Ebene Dach–Wand verbunden.",
                ursprung=(300, 70), mass=2.3)
    lagen = _wand_vertikal(sk, 0, 0, 80)
    xg0, xg1 = lagen["Gefach"]
    sk.holz(xg0, 80, xg1, 90)                                   # Rähm 10 × Ständerwerk
    u = (math.cos(ar), math.sin(ar))
    n = (-math.sin(ar), math.cos(ar))
    p0 = (xg1, 90)                                              # Sparren-Unterkante liegt innen auf dem Rähm
    def q(t, d):
        return p0[0] + u[0] * t + n[0] * d, p0[1] + u[1] * t + n[1] * d
    t0, t1 = -85, 55
    # Sparren im Überstand (Ansicht), Dämmung im beheizten Bereich
    sk.flaeche([q(t0, 0), q(-36, 0), q(-36, 20), q(t0, 20)], linie=0.9)
    sk.linie([q(t0 + 4, 10), q(-38, 10)], SCHWARZ, 0.4)
    sk.flaeche([q(-36, 0), q(t1, 0), q(t1, 20), q(-36, 20)], "weich", richtung=(q(-36, 0), q(t1, 0), 20))
    # Stellbrett in Flucht der Wand-Außenseite
    xs = lagen["Holzfaser/MDF"][0]
    ts = (xs - p0[0]) / u[0]
    sk.flaeche([q(ts - 2.4, 0), q(ts, 0), q(ts, 20), q(ts - 2.4, 20)], linie=0.9)
    # Unterdeckplatte, Konterlattung, Traglatten, Deckung
    sk.flaeche([q(t0, 20), q(t1, 20), q(t1, 22.2), q(t0, 22.2)], "zickzack", richtung=(q(t0, 20), q(t1, 20), 2.2))
    sk.winddicht([q(t0 - 8, 22.5), q(t1, 22.5)])
    sk.flaeche([q(t0, 22.2), q(t1, 22.2), q(t1, 26.2), q(t0, 26.2)], linie=0.5)
    t = t0 + 12
    while t < t1:
        m = q(t, 27.7)
        sk.holz(m[0] - 2.5, m[1] - 1.5, m[0] + 2.5, m[1] + 1.5, winkel=a)
        t += 33
    sk.flaeche([q(t0 - 6, 30), q(t1, 30), q(t1, 33), q(t0 - 6, 33)], "diagonal", 0.6)
    # Traufbohle, Traufblech, Rinne, Lüftungsgitter
    tb = q(t0, 22.2)
    sk.holz(tb[0] - 1, tb[1], tb[0] + 7, tb[1] + 4)
    sk.linie([q(t0 - 8, 22.5), (tb[0] - 10, tb[1] - 6)], BLAU, 1.6)
    sk.c.saveState(); sk.c.setLineWidth(1.1)
    cx, cy = sk.p(tb[0] - 14, tb[1] - 12); sk.c.circle(cx, cy, 7 * sk.s, stroke=1, fill=0); sk.c.restoreState()
    g = q(ts - 1.2, 21)
    sk.linie([q(t0 + 8, 23.5), q(t0 + 8, 25.5)], BLAU, 1.2, [1, 1])
    # Innen: Dachfolie unter den Sparren an die Wand-OSB, Installationsebene und GK
    xo = lagen["OSB"][1]
    to = (xo - p0[0]) / u[0]
    sk.flaeche([q(to, -4.3), q(t1, -4.3), q(t1, -0.3), q(to, -0.3)], "weich", richtung=(q(to, -4.3), q(t1, -4.3), 4))
    sk.flaeche([q(to + 4, -5.55), q(t1, -5.55), q(t1, -4.3), q(to + 4, -4.3)], "punkte")
    sk.luftdicht([q(t1, -0.3), q(to, -0.3), (xo, 60)])
    sk.nr(1, (tb[0] - 14, tb[1] - 12), (-150, 30), "Rinne mit Traufblech / Einlaufblech")
    sk.nr(2, (tb[0] + 3, tb[1] + 2), (-150, 60), "Traufbohle")
    sk.nr(3, q(-60, 22.5), (-150, 95), "Unterdeckung bis auf das Traufblech (kein Wassersack)")
    sk.nr(4, q(t0 + 8, 24.5), (-150, 130), "Zuluft unter der Deckung mit Insektenschutz (≥ 2 ‰, ≥ 200 cm²/m)")
    sk.nr(5, q(-60, 10), (-150, 5), "Sparrenkopf unter Dach (innerhalb der 60°-Linie)")
    sk.nr(6, q(ts - 1.2, 10), (-60, 150), "Stellbrett zwischen den Sparren als Dämmabschluss")
    sk.nr(7, ((xg0 + xg1) / 2, 85), (85, 40), "Rähm / Fußpfette nach Statik, Sparren liegen auf (Kerve)")
    sk.nr(8, (xo, 65), (85, 15), "luftdichte Ebene Dach–Wand verbunden")
    sk.nr(9, q(30, 10), (85, 150), "Dämmung Dach und Wand ohne Lücke verbunden")
    return sk.fertig(ziel, "traufe_pfettendach", "Informationsdienst Holz R5/T2/F2 (2023), Traufdetails; BauNetz Wissen Traufe, Pfettendach.")


def sockel(ziel):
    sk = Skizze("Referenz DT-W1 · Sockel Holzrahmenbau (Abstand Holz–Gelände ≥ 30 cm)",
                "Schwelle auf Unterfütterung und Horizontalabdichtung; Holz ≥ 30 cm über Gelände (≥ 15 cm mit Kiesbett,"
                " ≥ 5 cm nur mit Abdichtung nach DIN 18533); luftdichter Anschluss an die Bodenplatte.",
                ursprung=(260, 110), mass=3.0)
    gok = 0
    # Bodenplatte mit Perimeterdämmung, Fundament schematisch
    sk.flaeche([(10, gok + 10), (120, gok + 10), (120, gok + 30), (10, gok + 30)], "beton")
    sk.flaeche([(-2, gok - 30), (10, gok - 30), (10, gok + 30), (-2, gok + 30)], "zickzack",
               richtung=((-2, gok + 30), (-2, gok - 30), 12))
    sk.flaeche([(10, gok - 30), (34, gok - 30), (34, gok + 10), (10, gok + 10)], "beton")
    sk.linie([(-60, gok), (-2, gok)], SCHWARZ, 1.2)
    sk.flaeche([(-40, gok - 6), (-2, gok - 6), (-2, gok), (-40, gok)], "kies", 0.4)
    # Unterfütterung + Abdichtung + Schwelle
    yb = gok + 30
    sk.flaeche([(13, yb), (40, yb), (40, yb + 2), (13, yb + 2)], "punkte")
    sk.linie([(12, yb + 2.3), (41, yb + 2.3)], SCHWARZ, 2.0)
    sk.holz(13.6, yb + 2.5, 37.6, yb + 12.5)
    lagen = _wand_vertikal(sk, 7.0 - 0.2, yb + 12.5, yb + 75)
    sk.flaeche([(12, yb + 2.5), (13.6, yb + 2.5), (13.6, yb + 12.5), (12, yb + 12.5)], "zickzack",
               richtung=((12, yb + 12.5), (12, yb + 2.5), 1.6))
    # Fassade beginnt ≥ 30 cm über GOK
    sk.luftdicht([(lagen["OSB"][1], yb + 50), (lagen["OSB"][1], yb + 13), (lagen["OSB"][1] + 6, yb + 10)])
    # Fußboden innen
    sk.flaeche([(42, yb), (120, yb), (120, yb + 6), (42, yb + 6)], "zickzack", richtung=((42, yb), (120, yb), 6))
    sk.flaeche([(42, yb + 6), (120, yb + 6), (120, yb + 12), (42, yb + 12)], "punkte")
    sk.linie([(-55, gok), (-55, yb + 2.5)], GRAU, 0.5)
    sk.linie([(-58, yb + 2.5), (13.6, yb + 2.5)], GRAU, 0.3, [2, 2])
    sk.text(-75, (gok + yb) / 2, "≥ 30 cm", 8, SCHWARZ)
    sk.nr(1, (25, yb + 7), (90, 80), "Schwelle (trockenes Vollholz) in Breite des Ständerwerks")
    sk.nr(2, (30, yb + 2.3), (90, 55), "Horizontalabdichtung unter der Schwelle")
    sk.nr(3, (30, yb + 1), (90, 30), "kraftschlüssige Unterfütterung (schwindarmer Mörtel)")
    sk.nr(4, (4, gok + 5), (-90, 40), "Perimeterdämmung (XPS) mit Sockelputz im Spritzwasserbereich")
    sk.nr(5, (-20, gok - 3), (-90, 15), "Kiesstreifen 16/32, b ≥ 30 cm (bei Abstand ≥ 15 cm)")
    sk.nr(6, (lagen["OSB"][1], yb + 20), (90, 105), "luftdichter Anschluss Wand–Bodenplatte")
    sk.nr(7, (lagen["Fassade"][0] + 1, yb + 40), (-90, 90), "Fassadenbekleidung, Unterkante ≥ 30 cm über Gelände (bzw. 15/5 cm s. o.)")
    sk.nr(8, (80, yb + 9), (100, 130), "Fußbodenaufbau innen (siehe SO-04)")
    return sk.fertig(ziel, "sockel", "Informationsdienst Holz R5/T2/F2 (2023), Kap. 5.6; DIN 68800-2.")


def fenster_unten(ziel):
    sk = Skizze("Referenz DT-F1 · Fensteranschluss unten (Brüstung, Holzrahmenbau, hinterlüftete Fassade)",
                "Fenster in der Dämmebene; innen luftdichter Anschluss an die OSB; außen schlagregendicht, Abdichtung"
                " unter der Fensterbank als 2. wasserführende Ebene; Fensterbank mit Gefälle und Tropfkante.",
                ursprung=(260, 70), mass=3.4)
    lagen = _wand_vertikal(sk, 0, 0, 70)
    xg0, xg1 = lagen["Gefach"]
    sk.holz(xg0, 70, xg1, 76)                                  # Brüstungsriegel
    # Fensterrahmen auf Unterfütterung in der Dämmebene
    sk.flaeche([(xg0 + 4, 76), (xg0 + 20, 76), (xg0 + 20, 79), (xg0 + 4, 79)], "punkte")
    sk.holz(xg0 + 4, 79, xg0 + 20, 90)
    sk.flaeche([(xg0 + 8, 90), (xg0 + 11, 90), (xg0 + 11, 130), (xg0 + 8, 130)], linie=0.6)   # Glas
    sk.luftdicht([(lagen["OSB"][1], 60), (lagen["OSB"][1], 77), (xg0 + 20, 80)])
    sk.linie([(lagen["Holzfaser/MDF"][0], 66), (lagen["Holzfaser/MDF"][0], 76), (xg0 + 4, 78)], BLAU, 1.8)
    # Fensterbank außen mit Gefälle und Tropfkante
    sk.linie([(xg0 + 4, 80.5), (-8, 77), (-8, 73.5)], SCHWARZ, 1.8)
    sk.nr(1, (xg0 + 12, 85), (80, 120), "Fensterrahmen in der Dämmebene (auf Unterfütterung/Montagezarge)")
    sk.nr(2, (lagen["OSB"][1], 70), (90, 60), "innen luftdichter Anschluss Fenster–OSB (Anschlussband)")
    sk.nr(3, (lagen["Holzfaser/MDF"][0], 72), (-80, 100), "Abdichtung unter der Fensterbank, an Fenster und Fassadenbahn angeschlossen")
    sk.nr(4, (-4, 77.5), (-80, 70), "Fensterbank mit Gefälle nach außen, Tropfkante, seitliche Aufkantung")
    sk.nr(5, ((xg0 + xg1) / 2, 73), (90, 35), "Brüstungsriegel im Ständerwerk; Fuge gedämmt")
    sk.nr(6, (2.4, 40), (-80, 40), "Hinterlüftung unter der Fensterbank offen (Zuluft) mit Insektenschutz")
    return sk.fertig(ziel, "fenster_unten", "BauNetz Wissen Anschlussfugen; RAL-Leitfaden Fenstermontage (2024); Informationsdienst Holz R5/T2/F2.")


def attika(ziel):
    sk = Skizze("Referenz DT-FD1 · Attika, Flachdach Typ I (Aufdachdämmung)",
                "Behelfsabdichtung bis OK Attika hochgeführt; Abdichtung über die Attika; Blechabdeckung mit Gefälle nach"
                " innen; Luftdichtheitsebene oberhalb der Balkenlage, an die Wand angeschlossen.",
                ursprung=(150, 280), mass=2.8)
    lagen = _wand_vertikal(sk, 0, -60, 0)
    # Balkenlage, Schalung, OSB
    yb = 0
    sk.holz(lagen["Gefach"][0], yb, lagen["Gefach"][1] + 0, yb + 24)            # Randbohle
    sk.flaeche([(lagen["Gefach"][1], yb), (150, yb), (150, yb + 24), (lagen["Gefach"][1], yb + 24)], linie=0.4)
    sk.holz(80, yb, 92, yb + 24, laengs=True)
    sk.flaeche([(lagen["Holzfaser/MDF"][0], yb + 24), (150, yb + 24), (150, yb + 26.2), (lagen["Holzfaser/MDF"][0], yb + 26.2)], "diagonal")
    sk.luftdicht([(lagen["Holzfaser/MDF"][0] + 1, yb + 26.6), (150, yb + 26.6)])
    sk.flaeche([(40, yb + 27), (150, yb + 27), (150, yb + 47), (40, yb + 41)], "zickzack",
               richtung=((40, yb + 27), (150, yb + 27), 14))
    sk.linie([(40, yb + 41.3), (150, yb + 47.3)], SCHWARZ, 2.0)
    # Attika-Aufbau
    sk.holz(lagen["Holzfaser/MDF"][0], yb + 26.2, 38, yb + 60, laengs=True)
    sk.luftdicht([(39, yb + 27), (39, yb + 60)])
    sk.linie([(-3, yb + 63), (lagen["Holzfaser/MDF"][0], yb + 61), (40, yb + 62.5), (40, yb + 41.3)], SCHWARZ, 2.0)
    sk.linie([(-5, yb + 50), (-5, yb + 65), (42, yb + 63), (42, yb + 58)], GRAU, 1.6)
    sk.nr(1, (20, yb + 64), (60, 110), "Blechabdeckung auf Trennlage, Gefälle ≥ 2 % nach innen")
    sk.nr(2, (40, yb + 50), (90, 95), "Abdichtung über die Attika geführt")
    sk.nr(3, (39, yb + 40), (110, 75), "Behelfsabdichtung/Dampfsperre bis OK Attika hochgeführt")
    sk.nr(4, (100, yb + 35), (130, 100), "Gefälledämmung druckfest (Typ DAA)")
    sk.nr(5, (120, yb + 25), (140, 60), "Dachschalung (Scheibe), darunter Balkenlage")
    sk.nr(6, (lagen["Gefach"][0] + 12, yb + 12), (-60, 30), "Randbohle/Lagerholz am Dachrand")
    sk.nr(7, (lagen["OSB"][1], -20), (-60, -40), "luftdichter Anschluss Wand–Dach (Folienstreifen)")
    return sk.fertig(ziel, "attika", "Informationsdienst Holz, holzbau handbuch R3/T2/F1 Flachdächer (2019), Abb. 8.1; R5/T2/F2 (2023).")


ALLE = [first_pfettendach, first_sparrendach, traufe_pfettendach, ortgang, sockel, fenster_unten, attika]

if __name__ == "__main__":
    ziel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "referenz")
    for f in ALLE:
        print("erstellt:", f(ziel))
