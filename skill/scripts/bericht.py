"""Erzeugt den PDF-Prüfbericht des Detailprüfers.

Aufruf:
    python bericht.py <zeichnung.pdf> <befunde.json> <pruefbericht.pdf>

Gliederung (wichtiges zuerst):
    Seite 1   Berichtskopf, Hinweis, Kurzfazit mit kompakter Befundliste
              Maßnahmenliste zum Abhaken
    Querformat  Markierte Zeichnung (mit Legende)
    1  Befunde im Detail (Karten mit Zeichnungsausschnitt)
    2  Nicht prüfbar und offene Fragen
    3  Positiv festgestellt
    Anhang  A1 Methode und Einstufungen · A2 Annahmen · A3 Code-Legende · A4 Quellenverzeichnis

Quellen: Im Text von befunde.json mit [[ID]] zitieren (IDs aus pruefkatalog/quellen.json).
Der Bericht setzt daraus hochgestellte, verlinkte Fußnoten und listet nur zitierte Quellen.
Befundnummern (B1, B2 …) im Text werden automatisch zur Befundkarte verlinkt.
"""
import datetime
import hashlib
import io
import json
import os
import re
import sys
from xml.sax.saxutils import escape

import pypdfium2 as pdfium
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
from markieren import (FARBEN, befund_kennung, befunde_lesen,  # noqa: E402
                       einstufung_normalisieren, markierte_seite)

KATALOG = os.path.join(HIER, "..", "pruefkatalog")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------- Konstanten
HINWEIS = ("Dieser Bericht ist eine KI-gestützte Hilfestellung auf Grundlage einer qualitativen "
           "Plausibilitätsprüfung der Zeichnung. Er ersetzt keine fachliche Prüfung und keinen "
           "Nachweis. Die Ergebnisse können Fehler enthalten und sind fachlich zu überprüfen.")
HINWEIS_KURZ = "KI-gestützte Hilfestellung – ersetzt keine fachliche Prüfung und keinen Nachweis."

EINSTUFUNGEN = [  # Schlüssel, Bezeichnung, Linienart
    ("aufbaufehler", "Klarer Aufbaufehler", "durchgezogen"),
    ("auffaelligkeit", "Mögliche Auffälligkeit", "gestrichelt"),
    ("hinweis", "Verbesserungshinweis", "gepunktet"),
    ("nicht_pruefbar", "Aus der Datei nicht prüfbar", "keine"),
]
NAME = {k: n for k, n, _ in EINSTUFUNGEN}
ART = {k: a for k, _, a in EINSTUFUNGEN}
BEREICHE = {"LD": "Luftdichtheit", "FS": "Feuchteschutz / Dampfbremse",
            "WB": "Wärmeschutz / Wärmebrücken",
            "WH": "Winddichtheit / Hinterlüftung / Schlagregenschutz",
            "HS": "Holzschutz", "KO": "Konstruktion", "ZQ": "Zeichnungsqualität"}
FELDER = [("fundstelle", "Fundstelle"), ("erkennbar", "Woran erkennbar"),
          ("begruendung", "Warum relevant"), ("risiko", "Mögliches Risiko"),
          ("zu_klaeren", "Zu klären"), ("verbesserung", "Verbesserung"),
          ("grundlage", "Grundlage"), ("verweise", "Verweis")]
PRIO_NAME = {1: "hoch", 2: "mittel", 3: "niedrig"}

TEXT = colors.HexColor("#111827")
GRAU = colors.HexColor("#6B7280")
GRAU_MITTEL = colors.HexColor("#9CA3AF")
LINIE = colors.HexColor("#D1D5DB")
HINTERGRUND = colors.HexColor("#F3F4F6")
KOPF = colors.HexColor("#374151")
LINK = colors.HexColor("#1F6FB2")


# ---------------------------------------------------------------- Schriften
def schriften_registrieren():
    kandidaten = [
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/ariali.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"),
        ("/usr/share/fonts/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/dejavu/DejaVuSans-Oblique.ttf"),
        ("/System/Library/Fonts/Supplemental/Arial.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
         "/System/Library/Fonts/Supplemental/Arial Italic.ttf"),
    ]
    try:
        import matplotlib
        d = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
        kandidaten.append((os.path.join(d, "DejaVuSans.ttf"), os.path.join(d, "DejaVuSans-Bold.ttf"),
                           os.path.join(d, "DejaVuSans-Oblique.ttf")))
    except Exception:
        pass
    for normal, fett, kursiv in kandidaten:
        if all(os.path.exists(p) for p in (normal, fett, kursiv)):
            pdfmetrics.registerFont(TTFont("Bericht", normal))
            pdfmetrics.registerFont(TTFont("Bericht-Fett", fett))
            pdfmetrics.registerFont(TTFont("Bericht-Kursiv", kursiv))
            pdfmetrics.registerFontFamily("Bericht", normal="Bericht", bold="Bericht-Fett",
                                          italic="Bericht-Kursiv", boldItalic="Bericht-Fett")
            return "Bericht", "Bericht-Fett", True
    return "Helvetica", "Helvetica-Bold", False


SCHRIFT, FETT, UNICODE = schriften_registrieren()
ERSATZ = {"≥": ">=", "≤": "<=", "→": "->", "↔": "<->", "≠": "!=", "≈": "~", "●": "*"}


def t(text):
    text = "" if text is None else str(text)
    if not UNICODE:
        for a, b in ERSATZ.items():
            text = text.replace(a, b)
    return text


def stil(name, **kw):
    basis = dict(fontName=SCHRIFT, fontSize=9, leading=12.2, textColor=TEXT)
    basis.update(kw)
    return ParagraphStyle(name, **basis)


S_TITEL = stil("titel", fontName=FETT, fontSize=19, leading=23)
S_UNTER = stil("unter", fontSize=10, leading=13, textColor=GRAU)
S_H1 = stil("h1", fontName=FETT, fontSize=13, leading=16, spaceBefore=6 * mm, spaceAfter=2.5 * mm,
            keepWithNext=1)
S_H2 = stil("h2", fontName=FETT, fontSize=10.5, leading=13, spaceBefore=3.5 * mm, spaceAfter=1.5 * mm,
            keepWithNext=1)
S_TEXT = stil("text")
S_KLEIN = stil("klein", fontSize=8.3, leading=10.8)
S_GRAU = stil("grau", fontSize=7.5, leading=9.5, textColor=GRAU)
S_LABEL = stil("label", fontName=FETT, fontSize=8.3, leading=10.8, textColor=KOPF)
S_KOPF = stil("kopf", fontName=FETT, fontSize=8.3, leading=10.5, textColor=colors.white)
S_KARTE_TITEL = stil("kartentitel", fontName=FETT, fontSize=10.5, leading=13.5)
S_HINWEIS = stil("hinweis", fontSize=8.8, leading=12, textColor=KOPF)


# ---------------------------------------------------------------- Textaufbereitung
class Zitate:
    """Nummeriert zitierte Quellen in der Reihenfolge ihres ersten Auftretens."""

    def __init__(self, quellen, fest=None):
        self.quellen = quellen
        self.fest = fest or {}      # feste Nummern (nach Gruppen sortiert) aus dem ersten Durchlauf
        self.nummern = {}
        self.reihenfolge = []       # Reihenfolge des ersten Auftretens

    def nummer(self, qid):
        if qid not in self.quellen:
            raise SystemExit(f"Unbekannte Quellen-ID [[{qid}]] – bitte in pruefkatalog/quellen.json ergänzen.")
        if qid not in self.reihenfolge:
            self.reihenfolge.append(qid)
        if qid not in self.nummern:
            self.nummern[qid] = self.fest.get(qid, len(self.nummern) + 1)
        return self.nummern[qid]


def feste_nummern(reihenfolge, quellen):
    """Nummeriert Quellen nach Gruppe (Gesetze, Normen, …) und darin nach erstem Auftreten."""
    gruppen = quellen.get("gruppen", [])
    sortiert = sorted(reihenfolge, key=lambda q: (gruppen.index(quellen["quellen"][q]["gruppe"]),
                                                  reihenfolge.index(q)))
    return {q: i + 1 for i, q in enumerate(sortiert)}


ZITATE = None
CODES = set()
BEFUND_IDS = set()
ANKER_ZIEL = {}  # Befundkennung → Sprungziel (Karte oder Abschnitt „nicht prüfbar“)


def mt(text):
    """Text → Paragraph-Markup: escapen, [[ID]] → Fußnote, B-Nummern → Link, Codes sammeln."""
    roh = t(text)
    for m in re.finditer(r"\b([A-Z]{2})-(\d{2})\b", roh):
        if m.group(1) in BEREICHE:
            CODES.add(m.group(0))
    s = escape(roh)

    def fussnote(m):
        teile = [x.strip() for x in m.group(1).split(",")]
        links = []
        for qid in teile:
            n = ZITATE.nummer(qid)
            links.append(f'<a href="#quelle{n}" color="{LINK.hexval().replace("0x", "#")}">{n}</a>')
        return "<super>" + ",".join(links) + "</super>"

    s = re.sub(r"\[\[([A-Z0-9,\- ]+)\]\]", fussnote, s)

    def befundlink(m):
        kennung = "B" + m.group(1)
        if kennung in ANKER_ZIEL:
            return f'<a href="#{ANKER_ZIEL[kennung]}" color="{LINK.hexval().replace("0x", "#")}">{kennung}</a>'
        return m.group(0)

    s = re.sub(r"\bB(\d{1,2})\b", befundlink, s)
    return s.replace("\n", "<br/>")


def P(text, s=S_TEXT):
    return Paragraph(mt(text), s)


def farbe_hex(e):
    return FARBEN[e].hexval().replace("0x", "#")


# ---------------------------------------------------------------- Kleine Grafiken
class Anker(Flowable):
    """Unsichtbarer Sprungpunkt; merkt sich die Seitennummer."""

    def __init__(self, name, seiten):
        super().__init__()
        self.name, self.seiten = name, seiten
        self.width = self.height = 0

    def draw(self):
        self.seiten[self.name] = self.canv.getPageNumber()
        self.canv.bookmarkPage(self.name)


class Kreissymbol(Flowable):
    def __init__(self, e, g=4.2 * mm):
        super().__init__()
        self.e, self.g = e, g
        self.width, self.height = g, g

    def draw(self):
        c = self.canv
        if self.e == "nicht_pruefbar":
            c.setFillColor(GRAU)
            c.setFont(SCHRIFT, 8)
            c.drawCentredString(self.g / 2, self.g * 0.3, "–")
            return
        c.setStrokeColor(FARBEN[self.e])
        c.setLineWidth(1.3)
        c.setLineCap(1)
        c.setDash({"auffaelligkeit": [2.6, 1.6], "hinweis": [0.1, 2.3]}.get(self.e, []))
        c.circle(self.g / 2, self.g / 2, self.g / 2 - 0.8, stroke=1, fill=0)


class Status(Flowable):
    """Statussymbol für die Schichttabelle: ok = Haken, unklar = ?, fehler = Kreuz."""

    def __init__(self, status, g=3.6 * mm):
        super().__init__()
        self.status, self.g = status, g
        self.width, self.height = g, g

    def draw(self):
        c, g = self.canv, self.g
        c.setLineWidth(1.3)
        c.setLineCap(1)
        if self.status == "ok":
            c.setStrokeColor(colors.HexColor("#2F6B3A"))
            c.line(g * 0.12, g * 0.5, g * 0.4, g * 0.2)
            c.line(g * 0.4, g * 0.2, g * 0.9, g * 0.85)
        elif self.status == "fehler":
            c.setStrokeColor(FARBEN["aufbaufehler"])
            c.line(g * 0.15, g * 0.15, g * 0.85, g * 0.85)
            c.line(g * 0.15, g * 0.85, g * 0.85, g * 0.15)
        else:
            c.setFillColor(FARBEN["auffaelligkeit"])
            c.setFont(FETT, g * 1.05)
            c.drawCentredString(g / 2, g * 0.12, "?")


class Kaestchen(Flowable):
    def __init__(self, g=3.6 * mm):
        super().__init__()
        self.g = g
        self.width = self.height = g

    def draw(self):
        self.canv.setStrokeColor(KOPF)
        self.canv.setLineWidth(0.8)
        self.canv.rect(0, 0, self.g, self.g, stroke=1, fill=0)


def einstufung_marke(e, kurz=False):
    name = NAME[e] if not kurz else {"aufbaufehler": "Aufbaufehler", "auffaelligkeit": "Auffälligkeit",
                                     "hinweis": "Hinweis", "nicht_pruefbar": "nicht prüfbar"}[e]
    return Paragraph(f'<font color="{farbe_hex(e)}">●</font> {escape(t(name))}'
                     if UNICODE else escape(name), S_KLEIN)


# ---------------------------------------------------------------- Tabellen
def tabelle(zeilen, breiten, kopf=True, zebra=False):
    tab = Table(zeilen, colWidths=breiten, repeatRows=1 if kopf else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINIE),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if kopf:
        st.append(("BACKGROUND", (0, 0), (-1, 0), KOPF))
    if zebra:
        for i in range(1 if kopf else 0, len(zeilen), 2):
            st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#FAFAFA")))
    tab.setStyle(TableStyle(st))
    return tab


def kopfzeile_tab(titel_liste):
    return [P(x, S_KOPF) for x in titel_liste]


# ---------------------------------------------------------------- Bilder
class Zeichnungsbilder:
    """Rendert die markierte Zeichnung einmal und liefert Gesamtbild und Ausschnitte."""

    def __init__(self, pdf_bytes, seitennr, dpi=200):
        doc = pdfium.PdfDocument(pdf_bytes)
        seite = doc[seitennr - 1]
        self.bild = seite.render(scale=dpi / 72).to_pil().convert("RGB")
        self.W, self.H = self.bild.size
        self.verhaeltnis = seite.get_width() / seite.get_height()  # Breite/Höhe

    def ausschnitt(self, x1, y1, x2, y2, breite_mm):
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(100, x2), min(100, y2)
        crop = self.bild.crop((int(x1 / 100 * self.W), int(y1 / 100 * self.H),
                               int(x2 / 100 * self.W), int(y2 / 100 * self.H)))
        puffer = io.BytesIO()
        crop.save(puffer, "PNG", optimize=True)
        puffer.seek(0)
        hoehe_mm = breite_mm * crop.size[1] / crop.size[0]
        return Image(puffer, width=breite_mm * mm, height=hoehe_mm * mm), hoehe_mm

    def zoom_fuer(self, b, breite_mm=56, hoehe_max_mm=48):
        if b.get("zoom"):
            x1, y1, x2, y2 = b["zoom"]
        else:
            k = b["kreis"]
            halb_x = max(4.0 * max(k.get("r", 2), 1.5), 6.0)
            halb_y = halb_x * self.verhaeltnis * (hoehe_max_mm / breite_mm)
            x1, x2 = k["x"] - halb_x, k["x"] + halb_x
            y1, y2 = k["y"] - halb_y, k["y"] + halb_y
        bild, h = self.ausschnitt(x1, y1, x2, y2, breite_mm)
        if h > hoehe_max_mm:  # zu hoch → schmaler skalieren
            faktor = hoehe_max_mm / h
            bild, _ = self.ausschnitt(x1, y1, x2, y2, breite_mm * faktor)
        return bild


# ---------------------------------------------------------------- Logik
def prioritaet(b):
    if b.get("prioritaet") in ("hoch", "mittel", "niedrig"):
        return {"hoch": 1, "mittel": 2, "niedrig": 3}[b["prioritaet"]]
    e = b["_e"]
    bereich = str(b.get("regel", ""))[:2].upper()
    if e == "aufbaufehler":
        return 1
    if e == "auffaelligkeit":
        return 1 if bereich in ("LD", "FS") else 2
    return 3


def regel_titel():
    """Liest Regel-Titel (z. B. 'LD-02 …') aus den Katalogdateien für die Code-Legende."""
    titel = {}
    if not os.path.isdir(KATALOG):
        return titel
    for datei in sorted(os.listdir(KATALOG)):
        if datei.endswith(".md"):
            with open(os.path.join(KATALOG, datei), encoding="utf-8") as f:
                for zeile in f:
                    m = re.match(r"^#{2,3}\s+([A-Z]{2}-\d{2})\s+(.+)$", zeile.strip())
                    if m:
                        titel[m.group(1)] = m.group(2).strip()
    return titel


def koordinaten_text(b):
    k = b.get("kreis")
    if not k:
        return ""
    return f"Rasterposition auf dem Blatt: x ≈ {k['x']:.0f} %, y ≈ {k['y']:.0f} %"


# ---------------------------------------------------------------- Inhalt
def inhalt_erzeugen(daten, quellen, bilder, seiten, fest=None):
    global ZITATE
    ZITATE = Zitate(quellen["quellen"], fest)
    CODES.clear()

    d = daten.get("detail", {})
    bericht = daten.get("bericht", {})
    befunde = befunde_lesen(daten)
    for b in befunde:
        b["_e"] = einstufung_normalisieren(b.get("einstufung"))
        b["_id"] = befund_kennung(b)
        BEFUND_IDS.add(b["_id"])
        ANKER_ZIEL[b["_id"]] = b["_id"] if b["_e"] != "nicht_pruefbar" else "abschnitt_offen"
    anzahl = {k: sum(1 for b in befunde if b["_e"] == k) for k, *_ in EINSTUFUNGEN}
    karten = [b for b in befunde if b["_e"] != "nicht_pruefbar"]
    nicht_pruefbar = [b for b in befunde if b["_e"] == "nicht_pruefbar"]
    BREITE = 174 * mm

    def seite_von(name):
        n = seiten.get(name)
        return f'<a href="#{name}" color="{LINK.hexval().replace("0x", "#")}">{n}</a>' if n else "–"

    # ---------- Seite 1: Kopf
    f = [P("Prüfbericht Baudetail", S_TITEL),
         P("Qualitative Plausibilitätsprüfung einer Detailzeichnung – Detailprüfer Architektur", S_UNTER),
         Spacer(1, 4 * mm)]
    pruefer = "Fachlich geprüft von: __________________  Datum: _________"
    felder = [("Projekt", d.get("projekt") or "nicht angegeben"), ("Detail", d.get("titel")),
              ("Datei", d.get("datei")), ("Bauart", d.get("bauart")),
              ("Schnitt / Maßstab", " · ".join(x for x in (d.get("schnitt"), d.get("massstab")) if x)),
              ("Fassadensystem", d.get("fassade")),
              ("Prüfdatum", d.get("pruefdatum")),
              ("Normstand", f"gemäß Quellenverzeichnis (Anhang A4), abgefragt am {quellen.get('abgerufen', '–')}"),
              ("Berichts-ID", bericht.get("id")), ("Version", bericht.get("version", "1.0"))]
    zeilen = []
    for i in range(0, len(felder), 2):
        zeile = []
        for k, v in felder[i:i + 2]:
            zeile += [P(k, S_LABEL), P(v or "–", S_KLEIN)]
        while len(zeile) < 4:
            zeile += ["", ""]
        zeilen.append(zeile)
    zeilen.append([P("Erstellt", S_LABEL), P("Detailprüfer Architektur (KI-gestützt)", S_KLEIN),
                   P(pruefer, S_KLEIN), ""])
    kopf = Table(zeilen, colWidths=[27 * mm, 60 * mm, 27 * mm, 60 * mm])
    kopf.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINIE),
                              ("SPAN", (2, -1), (3, -1)),
                              ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                              ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    f += [kopf, Spacer(1, 4 * mm)]

    hinweis = Table([[P(HINWEIS, S_HINWEIS)]], colWidths=[BREITE])
    hinweis.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, KOPF),
                                 ("BACKGROUND", (0, 0), (-1, -1), HINTERGRUND),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                                 ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    f += [hinweis]

    # ---------- Kurzfazit
    f.append(P("Kurzfazit", S_H1))
    zahlen = (f"{anzahl['aufbaufehler']} klare(r) Aufbaufehler · {anzahl['auffaelligkeit']} mögliche "
              f"Auffälligkeit(en) · {anzahl['hinweis']} Verbesserungshinweis(e) · "
              f"{anzahl['nicht_pruefbar']} Punkt(e) aus der Datei nicht prüfbar.")
    if daten.get("kurzfazit"):
        f.append(P(daten["kurzfazit"], S_TEXT))
        f.append(Spacer(1, 1.5 * mm))
    f.append(P(zahlen, S_KLEIN))
    f.append(Spacer(1, 2 * mm))
    z = [kopfzeile_tab(["Nr.", "Einstufung", "Befund", "Kurzmaßnahme", "S."])]
    for b in befunde:
        anker = b["_id"] if b["_e"] != "nicht_pruefbar" else "abschnitt_offen"
        z.append([Paragraph(f'<a href="#{anker}" color="{LINK.hexval().replace("0x", "#")}"><b>{b["_id"]}</b></a>', S_KLEIN),
                  einstufung_marke(b["_e"], kurz=True), P(b.get("titel"), S_KLEIN),
                  P(b.get("massnahme") or "–", S_KLEIN),
                  Paragraph(seite_von(anker), S_KLEIN)])
    f.append(tabelle(z, [10 * mm, 27 * mm, 68 * mm, 61 * mm, 8 * mm], zebra=True))

    # ---------- Maßnahmenliste
    massnahmen = sorted([b for b in karten if b.get("massnahme")],
                        key=lambda b: (prioritaet(b), int(re.sub(r"\D", "", b["_id"]) or 0)))
    z = [kopfzeile_tab(["Nr.", "Was ändern", "Wo in der Zeichnung", "Priorität", "erl."])]
    for b in massnahmen:
        z.append([P(b["_id"], S_KLEIN), P(b["massnahme"], S_KLEIN), P(b.get("wo") or b.get("fundstelle"), S_KLEIN),
                  P(PRIO_NAME[prioritaet(b)], S_LABEL if prioritaet(b) == 1 else S_KLEIN), Kaestchen()])
    if len(z) == 1:
        z.append(["", P("Keine Maßnahmen.", S_KLEIN), "", "", ""])
    f.append(KeepTogether([P("Maßnahmenliste zum Abhaken", S_H1),
                           P("Sortiert nach Priorität. Regel für die Priorität: siehe Anhang A1.", S_GRAU),
                           Spacer(1, 1.5 * mm),
                           tabelle(z, [10 * mm, 76 * mm, 60 * mm, 17 * mm, 11 * mm], zebra=True)]))

    # ---------- Markierte Zeichnung (im Fluss, ohne erzwungenen Seitenumbruch)
    lz = []
    for k, name, art in EINSTUFUNGEN[:3]:
        lz += [Kreissymbol(k), Paragraph(f'<font color="{farbe_hex(k)}"><b>{escape(name)}</b></font> ({art})', S_KLEIN)]
    leg = Table([lz], colWidths=[5 * mm, 53 * mm, 5 * mm, 56 * mm, 5 * mm, 50 * mm])
    leg.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 1)]))
    x1, y1, x2, y2 = daten.get("zeichnung_ausschnitt", [0, 0, 100, 100])
    bild, h = bilder.ausschnitt(x1, y1, x2, y2, 174)
    if h > 150:
        bild, h = bilder.ausschnitt(x1, y1, x2, y2, 174 * 150 / h)
    f.append(KeepTogether([Anker("zeichnung", SEITEN_AKTUELL), P("Markierte Zeichnung", S_H1), leg,
                           P("Badges B1 … = Befundnummer mit Führungslinie zur Stelle. "
                             "„Wand A“ / „Wand B“ = Bezeichnung der Wände in diesem Bericht.", S_GRAU),
                           Spacer(1, 2 * mm), bild]))

    # ---------- Schichtenaufbau
    f.append(KeepTogether([P("Erkannter Schichtenaufbau", S_H1),
                           P("Nummerierung wie die Legende der Zeichnung: S1 = außen. "
                             "Status: Haken = eindeutig, ? = unklar, Kreuz = fehlerhaft.", S_GRAU),
                           Spacer(1, 1.5 * mm), schichten_tabelle(daten)]))

    # ---------- 1 Befunde im Detail
    f.append(P("1  Befunde im Detail", S_H1))
    f.append(P("Feldreihenfolge in jeder Karte: Fundstelle → Woran erkennbar → Warum relevant → "
               "Mögliches Risiko → Zu klären → Verbesserung → Grundlage → Verweis.", S_GRAU))
    f.append(Spacer(1, 2 * mm))
    for b in karten:
        f.append(befund_karte(b, bilder))

    # ---------- 2 Nicht prüfbar und offene Fragen
    f += [Anker("abschnitt_offen", SEITEN_AKTUELL), P("2  Nicht prüfbar und offene Fragen", S_H1),
          P("2.1  Aus der Datei nicht prüfbar", S_H2)]
    z = [kopfzeile_tab(["Nr.", "Thema", "Was fehlt bzw. ist zu klären", "Nachweis"])]
    for b in nicht_pruefbar:
        code = b.get("regel", "")
        thema = mt(b.get("titel")) + (f'<br/><font color="#6B7280" size="7">{mt(code)}</font>' if code else "")
        z.append([P(b["_id"], S_KLEIN), Paragraph(thema, S_KLEIN),
                  P(b.get("zu_klaeren") or b.get("fehlt"), S_KLEIN),
                  P("erforderlich" if b.get("nachweis_erforderlich") else "–", S_KLEIN)])
    if len(z) == 1:
        z.append(["", P("Keine.", S_KLEIN), "", ""])
    f.append(tabelle(z, [10 * mm, 50 * mm, 94 * mm, 20 * mm], zebra=True))

    f.append(P("2.2  Offene Fragen an die Planung", S_H2))
    fragen = daten.get("offene_fragen", [])
    z = [kopfzeile_tab(["Nr.", "Frage", "Warum wichtig", "Annahme in diesem Bericht"])]
    for i, q in enumerate(fragen, 1):
        z.append([P(q.get("nr", f"F{i}"), S_KLEIN), P(q.get("frage"), S_KLEIN),
                  P(q.get("warum"), S_KLEIN), P(q.get("annahme"), S_KLEIN)])
    if len(z) == 1:
        z.append(["", P("Keine offenen Fragen.", S_KLEIN), "", ""])
    f.append(tabelle(z, [10 * mm, 62 * mm, 52 * mm, 50 * mm], zebra=True))

    # ---------- 3 Positiv festgestellt
    f.append(P("3  Positiv festgestellt", S_H1))
    f.append(P("Einzelfeststellungen ohne Gesamturteil über die Konstruktion.", S_GRAU))
    f.append(Spacer(1, 1.5 * mm))
    z = [kopfzeile_tab(["Thema", "Feststellung"])]
    for p in daten.get("positiv", []):
        if isinstance(p, dict):
            z.append([Paragraph(f'<font color="#6B7280">{mt(p.get("regel", ""))}</font><br/>{mt(p.get("thema", ""))}',
                                S_KLEIN), P(p.get("text"), S_KLEIN)])
        else:
            z.append(["", P(p, S_KLEIN)])
    f.append(tabelle(z, [40 * mm, 134 * mm], zebra=True))

    # ---------- Anhang
    f.append(P("Anhang", S_H1))
    f.append(P("A1  Methode, Einstufungen und Priorität", S_H2))
    f.append(P("Qualitative Plausibilitätsprüfung anhand der Zeichnung und ihrer Legende. Es wurden keine "
               "bauphysikalischen oder statischen Berechnungen durchgeführt (keine sd-, U- oder R-Werte, "
               "kein Tauwasser, kein Temperaturfaktor f_Rsi, keine Tragfähigkeit oder Schraubenbemessung). "
               "Punkte, die nur rechnerisch sicher beurteilt werden können, sind mit „Nachweis erforderlich“ "
               "gekennzeichnet. Faustregeln sind als Praxisempfehlung gekennzeichnet und keine Normpflicht. "
               "Längen wurden höchstens im Maßstab abgelesen. Der Schichtenaufbau ist wie die Legende der "
               "Zeichnung von außen nach innen nummeriert (S1 = außen).", S_KLEIN))
    f.append(Spacer(1, 2 * mm))
    z = [kopfzeile_tab(["Einstufung", "Markierung", "Bedeutung"])]
    bedeutung = {
        "aufbaufehler": "Nur wenn eindeutig aus der Zeichnung erkennbar.",
        "auffaelligkeit": "Fraglich; die Darstellung ist mehrdeutig oder für ein Urteil fehlen Informationen.",
        "hinweis": "Kein Mangel erkennbar, aber sinnvolle Verbesserung – auch fehlende oder unklare Angaben.",
        "nicht_pruefbar": "Mit den vorhandenen Angaben nicht beurteilbar; benannt wird, was fehlt.",
    }
    for k, name, art in EINSTUFUNGEN:
        z.append([einstufung_marke(k), P(art, S_KLEIN), P(bedeutung[k], S_KLEIN)])
    f.append(tabelle(z, [44 * mm, 26 * mm, 104 * mm]))
    f.append(Spacer(1, 2 * mm))
    f.append(P("Priorität in der Maßnahmenliste: hoch = klarer Aufbaufehler oder mögliche Auffälligkeit "
               "bei Luftdichtheit bzw. Feuchteschutz; mittel = übrige mögliche Auffälligkeiten; niedrig = "
               "Verbesserungshinweise. Aussagesicherheit je Befund: hoch = eindeutig dargestellt; mittel = "
               "naheliegende Deutung, andere Deutung möglich; gering = Darstellung lässt mehrere Deutungen zu.",
               S_KLEIN))

    f.append(P("A2  Annahmen", S_H2))
    z = [kopfzeile_tab(["Nr.", "Annahme"])]
    for i, a in enumerate(daten.get("annahmen", []), 1):
        z.append([P(f"A2.{i}", S_KLEIN), P(a, S_KLEIN)])
    if len(z) == 1:
        z.append(["", P("Keine.", S_KLEIN)])
    f.append(tabelle(z, [14 * mm, 160 * mm], zebra=True))

    # Code-Legende erst nach allen Texten (damit alle Codes gesammelt sind)
    titel = regel_titel()
    f.append(P("A3  Code-Legende", S_H2))
    f.append(P("Die kleinen grauen Codes verweisen auf die Prüfregeln des Detailprüfers. "
               "Aufgeführt sind alle Codes, die in diesem Bericht vorkommen.", S_GRAU))
    f.append(Spacer(1, 1.5 * mm))
    z = [kopfzeile_tab(["Code", "Bereich", "Prüfregel"])]
    for code in sorted(CODES):
        z.append([P(code, S_KLEIN), P(BEREICHE.get(code[:2], ""), S_KLEIN),
                  P(titel.get(code, "–"), S_KLEIN)])
    f.append(tabelle(z, [16 * mm, 58 * mm, 100 * mm], zebra=True))

    # Quellenverzeichnis
    f.append(P("A4  Quellenverzeichnis", S_H2))
    f.append(P(f"Nur im Bericht zitierte Quellen. Hochgestellte Zahlen im Text verweisen hierher. "
               f"Links aufgerufen am {quellen.get('abgerufen', '–')}. Norminhalte sind sinngemäß "
               f"wiedergegeben; Normtexte sind in der Regel kostenpflichtig über DIN Media erhältlich.",
               S_GRAU))
    nach_nummer = sorted(ZITATE.nummern.items(), key=lambda kv: kv[1])
    for gruppe in quellen.get("gruppen", []):
        eintraege = [(qid, n) for qid, n in nach_nummer if quellen["quellen"][qid]["gruppe"] == gruppe]
        if not eintraege:
            continue
        f.append(P(gruppe, S_LABEL))
        z = []
        for qid, n in eintraege:
            q = quellen["quellen"][qid]
            text = f'<a name="quelle{n}"/>{escape(t(q["titel"]))}'
            if q.get("url"):
                url = escape(q["url"])
                text += f'<br/><a href="{url}" color="{LINK.hexval().replace("0x", "#")}">{url}</a>'
            z.append([Paragraph(f"[{n}]", S_KLEIN), Paragraph(text, S_KLEIN)])
        tab = Table(z, colWidths=[10 * mm, 164 * mm])
        tab.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 3),
                                 ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
        f += [tab, Spacer(1, 1.5 * mm)]
    return f


def befund_karte(b, bilder):
    e = b["_e"]
    farbe = FARBEN[e]
    breite_inhalt = 169 * mm

    meta = [f'<font color="{farbe_hex(e)}"><b>{escape(NAME[e])}</b></font>']
    if b.get("regel"):
        meta.append(f'<font color="#6B7280">{mt(b["regel"])}</font>')
    if b.get("sicherheit"):
        s = f"Aussagesicherheit: {escape(t(b['sicherheit']))}"
        if b.get("sicherheit_grund"):
            s += f" – {mt(b['sicherheit_grund'])}"
        meta.append(f'<font color="#374151">{s}</font>')
    if b.get("nachweis_erforderlich"):
        meta.append('<font color="#374151"><b>Nachweis erforderlich</b></font>')
    kopf = [Paragraph(f'<b>{b["_id"]}</b>  {mt(b.get("titel"))}', S_KARTE_TITEL), Spacer(1, 1 * mm),
            Paragraph("  ·  ".join(meta), S_KLEIN)]

    zeilen = []
    for feld, label in FELDER:
        wert = b.get(feld) or (b.get("fehlt") if feld == "zu_klaeren" else None)
        if not wert:
            continue
        inhalt = mt(wert)
        if feld == "fundstelle" and b.get("kreis"):
            inhalt += f'<br/><font color="#6B7280" size="7">{escape(t(koordinaten_text(b)))}</font>'
        zeilen.append([P(label, S_LABEL), Paragraph(inhalt, S_KLEIN)])

    if b.get("kreis"):
        bild = bilder.zoom_fuer(b)
        oben = Table([[kopf, bild]], colWidths=[breite_inhalt - 60 * mm, 60 * mm])
    else:
        oben = Table([[kopf]], colWidths=[breite_inhalt])
    oben.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    felder = Table(zeilen, colWidths=[32 * mm, breite_inhalt - 32 * mm])
    felder.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LINEABOVE", (0, 0), (-1, -1), 0.3, LINIE),
                                ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                                ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    innen = Table([[oben], [Spacer(1, 1.5 * mm)], [felder]], colWidths=[breite_inhalt])
    innen.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    karte = Table([["", innen]], colWidths=[2.2 * mm, 171.8 * mm])
    karte.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), farbe),
                               ("BOX", (0, 0), (-1, -1), 0.5, LINIE),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LEFTPADDING", (1, 0), (1, 0), 6), ("RIGHTPADDING", (1, 0), (1, 0), 6),
                               ("TOPPADDING", (1, 0), (1, 0), 6), ("BOTTOMPADDING", (1, 0), (1, 0), 5),
                               ("LEFTPADDING", (0, 0), (0, 0), 0), ("RIGHTPADDING", (0, 0), (0, 0), 0)]))
    return KeepTogether([Anker(b["_id"], SEITEN_AKTUELL), karte, Spacer(1, 4 * mm)])


SEITEN_AKTUELL = {}


def schichten_tabelle(daten):
    z = [kopfzeile_tab(["Nr.", "Schicht (von außen nach innen)", "Dicke", "", "Anmerkung"])]
    for i, s in enumerate(daten.get("schichtenaufbau", []), 1):
        z.append([P(s.get("nr", f"S{i}"), S_KLEIN), P(s.get("schicht"), S_KLEIN), P(s.get("dicke"), S_KLEIN),
                  Status(s.get("status", "ok")), P(s.get("anmerkung") or "", S_KLEIN)])
    return tabelle(z, [10 * mm, 58 * mm, 26 * mm, 8 * mm, 72 * mm], zebra=True)


# ---------------------------------------------------------------- Aufbau
def baue(pdf_ziel, daten, quellen, bilder, seiten, gesamt, fest=None):
    d = daten.get("detail", {})
    bericht = daten.get("bericht", {})
    kopf_links = t(f"Projekt: {d.get('projekt') or 'nicht angegeben'} · {d.get('titel', '')}")
    kopf_rechts = t(f"Bericht {bericht.get('id', '')} · Version {bericht.get('version', '1.0')}")

    def kopf_fuss(c, doc):
        breite, hoehe = c._pagesize
        rand = 18 * mm
        c.saveState()
        c.setFont(SCHRIFT, 7)
        c.setFillColor(GRAU)
        c.drawString(rand, hoehe - 10 * mm, kopf_links[:110])
        c.drawRightString(breite - rand, hoehe - 10 * mm, kopf_rechts)
        c.setStrokeColor(LINIE)
        c.setLineWidth(0.4)
        c.line(rand, hoehe - 11.5 * mm, breite - rand, hoehe - 11.5 * mm)
        c.line(rand, 12.5 * mm, breite - rand, 12.5 * mm)
        c.drawString(rand, 8.5 * mm, t(HINWEIS_KURZ))
        c.drawRightString(breite - rand, 8.5 * mm, f"Seite {doc.page} von {gesamt or '–'}")
        c.restoreState()

    doc = BaseDocTemplate(pdf_ziel, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                          topMargin=16 * mm, bottomMargin=17 * mm,
                          title=t(f"Prüfbericht {d.get('titel', '')}"),
                          author="Detailprüfer Architektur (KI-gestützt)",
                          subject="Qualitative Plausibilitätsprüfung – kein Nachweis")
    hoch = Frame(18 * mm, 17 * mm, A4[0] - 36 * mm, A4[1] - 33 * mm, id="hoch", leftPadding=0,
                 rightPadding=0, topPadding=0, bottomPadding=0)
    qb, qh = landscape(A4)
    quer = Frame(15 * mm, 15 * mm, qb - 30 * mm, qh - 30 * mm, id="quer", leftPadding=0,
                 rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="hoch", frames=[hoch], onPage=kopf_fuss, pagesize=A4),
                          PageTemplate(id="quer", frames=[quer], onPage=kopf_fuss, pagesize=landscape(A4))])

    global SEITEN_AKTUELL
    SEITEN_AKTUELL = {}
    inhalt = inhalt_erzeugen(daten, quellen, bilder, seiten, fest)
    doc.build(inhalt)
    neue_seiten = dict(SEITEN_AKTUELL)
    neue_seiten.update({k: v for k, v in seiten.items() if k not in neue_seiten})
    return neue_seiten, doc.page, feste_nummern(ZITATE.reihenfolge, quellen)


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    pdf_ein, json_datei, pdf_aus = sys.argv[1:4]
    with open(json_datei, encoding="utf-8") as f:
        daten = json.load(f)
    with open(os.path.join(KATALOG, "quellen.json"), encoding="utf-8") as f:
        quellen = json.load(f)
    daten.setdefault("bericht", {})
    if not daten["bericht"].get("id"):
        heute = datetime.date.today().strftime("%Y%m%d")
        kurz = hashlib.sha1(os.path.basename(pdf_ein).encode("utf-8")).hexdigest()[:4].upper()
        daten["bericht"]["id"] = f"DPA-{heute}-{kurz}"

    writer, seitennr, anzahl = markierte_seite(pdf_ein, daten)
    puffer = io.BytesIO()
    writer.write(puffer)
    bilder = Zeichnungsbilder(puffer.getvalue(), seitennr)

    # Zwei Durchläufe: erst Seitenzahlen sammeln, dann mit Seitenverweisen setzen
    seiten, gesamt, fest = baue(io.BytesIO(), daten, quellen, bilder, {}, None)
    seiten, gesamt2, _ = baue(pdf_aus, daten, quellen, bilder, seiten, gesamt, fest)
    if gesamt2 != gesamt:  # Seitenzahl hat sich verschoben → noch einmal setzen
        seiten, gesamt2, _ = baue(pdf_aus, daten, quellen, bilder, seiten, gesamt2, fest)
    print(f"Prüfbericht erstellt: {pdf_aus}  ({gesamt2} Seiten, {anzahl} Markierungen, "
          f"{len(ZITATE.nummern)} Quellen, Schrift: {'Unicode' if UNICODE else 'Helvetica'})")


if __name__ == "__main__":
    main()
