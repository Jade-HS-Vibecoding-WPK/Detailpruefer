"""Erzeugt den PDF-Prüfbericht des Detailprüfers.

Aufruf:
    python bericht.py <zeichnung.pdf> <befunde.json> <pruefbericht.pdf>

Aufbau des Berichts:
    1. Deckblatt (Angaben zum Detail, Pflichthinweis, Übersicht, Legende)
    2. Markierte Zeichnung (Original als Vektor-PDF + rote Markierungen)
    3. Schichtenaufbau, Befunde nach Einstufung, nicht Prüfbares, Positives,
       Annahmen, Grundlagen, Pflichthinweis
Jede Seite erhält eine Fußzeile mit Hinweis und Seitenzahl.
"""
import io
import json
import os
import sys
from xml.sax.saxutils import escape

from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (Flowable, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from markieren import befunde_lesen, einstufung_normalisieren, markierte_seite  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PFLICHTHINWEIS = ("Dieses Ergebnis ist eine Hilfestellung. Es ersetzt keine fachliche Prüfung "
                  "und keinen Nachweis. Die KI kann sich irren – alle Ergebnisse sind fachlich "
                  "zu überprüfen.")
METHODE = ("Qualitative Plausibilitätsprüfung anhand der Zeichnung. Es wurden keine "
           "bauphysikalischen oder statischen Berechnungen durchgeführt (keine sd-, U- oder "
           "R-Werte, kein Tauwasser, kein f_Rsi, keine Tragfähigkeit). Punkte, die nur "
           "rechnerisch sicher beurteilt werden können, sind als „Nachweis erforderlich“ "
           "gekennzeichnet. Faustregeln sind als Praxisempfehlung gekennzeichnet und keine "
           "Normpflicht.")

EINSTUFUNGEN = [  # Schlüssel, Bezeichnung, Farbe, Strichart der Markierung
    ("aufbaufehler", "Klarer Aufbaufehler", colors.HexColor("#B71C1C"), "durchgezogen"),
    ("auffaelligkeit", "Mögliche Auffälligkeit", colors.HexColor("#B45309"), "gestrichelt"),
    ("hinweis", "Verbesserungshinweis", colors.HexColor("#1F5F8B"), "gepunktet"),
    ("nicht_pruefbar", "Aus der Datei nicht prüfbar", colors.HexColor("#555555"), "keine"),
]
EINSTUFUNG = {k: (name, farbe, art) for k, name, farbe, art in EINSTUFUNGEN}
BEREICHE = [("LD", "Luftdichtheit"), ("FS", "Feuchteschutz / Dampfbremse"),
            ("WB", "Wärmeschutz / Wärmebrücken"),
            ("WH", "Winddichtheit / Hinterlüftung / Schlagregenschutz"),
            ("HS", "Holzschutz"), ("KO", "Konstruktion"), ("ZQ", "Zeichnungsqualität")]
FELDER = [("fundstelle", "Fundstelle"), ("erkennbar", "Woran erkennbar"),
          ("begruendung", "Warum relevant"), ("risiko", "Mögliches Risiko"),
          ("fehlt", "Was fehlt / zu klären"), ("verbesserung", "Verbesserung"),
          ("grundlage", "Grundlage"), ("verweise", "Verweis")]
ROT = colors.HexColor("#CC1414")
GRAU_HELL = colors.HexColor("#F3F4F6")
LINIE = colors.HexColor("#D1D5DB")


# ---------------------------------------------------------------- Schriften
def schriften_registrieren():
    """Sucht eine Unicode-Schrift (für Umlaute, ≥, → …); sonst Helvetica."""
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
    try:  # matplotlib bringt DejaVu mit (häufig in Cloud-Umgebungen vorhanden)
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
            return "Bericht", "Bericht-Fett", "Bericht-Kursiv", True
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", False


SCHRIFT, SCHRIFT_FETT, SCHRIFT_KURSIV, UNICODE = schriften_registrieren()
ERSATZ = {"≥": ">=", "≤": "<=", "→": "->", "↔": "<->", "≠": "!=", "≈": "~", "⚠": "!"}


def t(text):
    """Text vorbereiten: None → '', Sonderzeichen ersetzen, falls keine Unicode-Schrift."""
    text = "" if text is None else str(text)
    if not UNICODE:
        for a, b in ERSATZ.items():
            text = text.replace(a, b)
    return text


# ---------------------------------------------------------------- Stile
def stil(name, **kw):
    basis = dict(fontName=SCHRIFT, fontSize=9.5, leading=13, textColor=colors.HexColor("#111827"))
    basis.update(kw)
    return ParagraphStyle(name, **basis)


S_TITEL = stil("titel", fontName=SCHRIFT_FETT, fontSize=22, leading=27, spaceAfter=2 * mm)
S_UNTERTITEL = stil("untertitel", fontSize=11, leading=15, textColor=colors.HexColor("#4B5563"))
S_H1 = stil("h1", fontName=SCHRIFT_FETT, fontSize=14, leading=18, spaceBefore=5 * mm, spaceAfter=2.5 * mm,
            keepWithNext=1)
S_H2 = stil("h2", fontName=SCHRIFT_FETT, fontSize=11, leading=14, spaceBefore=3 * mm, spaceAfter=1.5 * mm,
            keepWithNext=1)
S_TEXT = stil("text")
S_KLEIN = stil("klein", fontSize=8.5, leading=11.5, textColor=colors.HexColor("#374151"))
S_LABEL = stil("label", fontName=SCHRIFT_FETT, fontSize=8.5, leading=11.5, textColor=colors.HexColor("#374151"))
S_KOPF = stil("kopf", fontName=SCHRIFT_FETT, fontSize=10, leading=13, textColor=colors.white)
S_HINWEIS = stil("hinweis", fontName=SCHRIFT_FETT, fontSize=10, leading=14, textColor=colors.HexColor("#7F1D1D"))


def P(text, s=S_TEXT):
    return Paragraph(escape(t(text)).replace("\n", "<br/>"), s)


class Kreissymbol(Flowable):
    """Kleines Legendensymbol: Kreis mit Linienart der Markierung."""

    def __init__(self, art, groesse=5 * mm):
        super().__init__()
        self.art, self.g = art, groesse
        self.width, self.height = groesse * 1.6, groesse

    def draw(self):
        c = self.canv
        if self.art == "keine":
            c.setFont(SCHRIFT, 8)
            c.setFillColor(colors.HexColor("#6B7280"))
            c.drawString(0, self.g * 0.3, "–")
            return
        c.setStrokeColor(ROT)
        c.setLineWidth(1.3)
        c.setLineCap(1)
        c.setDash({"gestrichelt": [3, 2], "gepunktet": [0.1, 2.6]}.get(self.art, []))
        c.circle(self.g / 2, self.g / 2, self.g / 2 - 1, stroke=1, fill=0)


# ---------------------------------------------------------------- Bausteine
def tabelle(daten, breiten, kopf=True, kopf_farbe=colors.HexColor("#374151")):
    tab = Table(daten, colWidths=breiten, repeatRows=1 if kopf else 0)
    stil_liste = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINIE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if kopf:
        stil_liste += [("BACKGROUND", (0, 0), (-1, 0), kopf_farbe)]
    tab.setStyle(TableStyle(stil_liste))
    return tab


def befund_block(b):
    """Ein Befund als Tabelle mit farbigem Kopf."""
    e = einstufung_normalisieren(b.get("einstufung"))
    name, farbe, _ = EINSTUFUNG[e]
    kopf = f"Nr. {b.get('nr', '–')}  ·  {b.get('regel', '')}  ·  {b.get('titel', '')}"
    zusatz = name + ("  ·  Nachweis erforderlich" if b.get("nachweis_erforderlich") else "")
    zeilen = [[P(kopf, S_KOPF), ""], [P(zusatz, S_LABEL), ""]]
    for feld, label in FELDER:
        if b.get(feld):
            zeilen.append([P(label, S_LABEL), P(b[feld], S_KLEIN)])
    # Darf über Seitenwechsel laufen; die Kopfzeile wird dann wiederholt.
    tab = Table(zeilen, colWidths=[38 * mm, 136 * mm], repeatRows=1)
    tab.setStyle(TableStyle([
        ("SPAN", (0, 0), (1, 0)), ("SPAN", (0, 1), (1, 1)),
        ("BACKGROUND", (0, 0), (1, 0), farbe),
        ("BACKGROUND", (0, 1), (1, 1), GRAU_HELL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.6, farbe),
        ("LINEBELOW", (0, 1), (-1, -2), 0.3, LINIE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [tab, Spacer(1, 4 * mm)]


def hinweisbox(text):
    tab = Table([[P(text, S_HINWEIS)]], colWidths=[174 * mm])
    tab.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.4, ROT),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FEF2F2")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return tab


def aufzaehlung(eintraege):
    if not eintraege:
        return [P("Keine.", S_KLEIN)]
    return [P("•  " + str(e), S_TEXT) for e in eintraege]


# ---------------------------------------------------------------- Inhalt
def textseiten(daten):
    detail = daten.get("detail", {})
    befunde = befunde_lesen(daten)
    for b in befunde:
        b["_e"] = einstufung_normalisieren(b.get("einstufung"))
    gruppen = {k: [b for b in befunde if b["_e"] == k] for k, *_ in EINSTUFUNGEN}
    n_nachweis = sum(1 for b in befunde if b.get("nachweis_erforderlich"))

    inhalt = [P("Prüfbericht", S_TITEL),
              P("Detailprüfer Architektur – qualitative Plausibilitätsprüfung eines Baudetails",
                S_UNTERTITEL), Spacer(1, 6 * mm)]

    angaben = [("Detail", detail.get("titel")), ("Datei", detail.get("datei")),
               ("Bauart", detail.get("bauart")), ("Fassadensystem", detail.get("fassade")),
               ("Schnitt / Maßstab", " · ".join(x for x in (detail.get("schnitt"), detail.get("massstab")) if x)),
               ("Prüfdatum", detail.get("pruefdatum")),
               ("Normstand", detail.get("normstand", "16.11.2026 (siehe Abschnitt Grundlagen)"))]
    inhalt.append(tabelle([[P(k, S_LABEL), P(v, S_TEXT)] for k, v in angaben if v],
                          [42 * mm, 132 * mm], kopf=False))
    inhalt += [Spacer(1, 6 * mm), hinweisbox("Wichtiger Hinweis: " + PFLICHTHINWEIS), Spacer(1, 6 * mm)]

    inhalt.append(P("Übersicht der Befunde", S_H2))
    zeilen = [[P("Einstufung", S_KOPF), P("Anzahl", S_KOPF), P("Markierung in der Zeichnung", S_KOPF)]]
    for k, name, farbe, art in EINSTUFUNGEN:
        farbcode = farbe.hexval().replace("0x", "#")
        zeilen.append([Paragraph(f'<font color="{farbcode}"><b>{escape(t(name))}</b></font>', S_TEXT),
                       P(str(len(gruppen[k])), S_TEXT),
                       Table([[Kreissymbol(art), P(art if art != "keine" else "keine Markierung", S_KLEIN)]],
                             colWidths=[11 * mm, 50 * mm],
                             style=[("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                    ("LEFTPADDING", (0, 0), (-1, -1), 0)])])
    inhalt.append(tabelle(zeilen, [70 * mm, 22 * mm, 82 * mm]))
    inhalt.append(Spacer(1, 2 * mm))
    inhalt.append(P(f"Davon mit Zusatz „Nachweis erforderlich“: {n_nachweis}. "
                    "Die Nummern in der Zeichnung entsprechen den Nummern der Befundliste.", S_KLEIN))
    inhalt += [Spacer(1, 5 * mm), P("Methode", S_H2), P(METHODE, S_KLEIN), PageBreak()]

    # 1. Schichtenaufbau
    inhalt.append(P("1. Erkannter Schichtenaufbau (von innen nach außen)", S_H1))
    schichten = daten.get("schichtenaufbau", [])
    if schichten:
        z = [[P("Nr.", S_KOPF), P("Schicht", S_KOPF), P("Dicke", S_KOPF), P("Anmerkung", S_KOPF)]]
        for i, s in enumerate(schichten, 1):
            anm = s.get("anmerkung", "")
            if s.get("unklar"):
                anm = "unklar – " + anm if anm else "unklar"
            z.append([P(str(i), S_KLEIN), P(s.get("schicht"), S_KLEIN), P(s.get("dicke"), S_KLEIN),
                      P(anm, S_LABEL if s.get("unklar") else S_KLEIN)])
        inhalt.append(tabelle(z, [10 * mm, 62 * mm, 20 * mm, 82 * mm]))
    else:
        inhalt.append(P("Kein Schichtenaufbau angegeben.", S_KLEIN))

    # 2.–4. Befunde
    abschnitte = [("2. Klare Aufbaufehler", "aufbaufehler"),
                  ("3. Mögliche Auffälligkeiten und Klärungsbedarf", "auffaelligkeit")]
    for titel, k in abschnitte:
        inhalt.append(P(titel, S_H1))
        if not gruppen[k]:
            inhalt.append(P("Keine.", S_KLEIN))
        for b in gruppen[k]:
            inhalt += befund_block(b)

    inhalt.append(P("4. Weitere Verbesserungshinweise", S_H1))
    if not gruppen["hinweis"]:
        inhalt.append(P("Keine.", S_KLEIN))
    for kuerzel, bereich in BEREICHE + [("", "Sonstige")]:
        if kuerzel:
            teil = [b for b in gruppen["hinweis"] if str(b.get("regel", "")).upper().startswith(kuerzel)]
        else:
            bekannte = tuple(k for k, _ in BEREICHE)
            teil = [b for b in gruppen["hinweis"] if not str(b.get("regel", "")).upper().startswith(bekannte)]
        if teil:
            inhalt.append(P(f"{kuerzel} – {bereich}" if kuerzel else bereich, S_H2))
            for b in teil:
                inhalt += befund_block(b)

    # 5. Nicht prüfbar
    inhalt.append(P("5. Aus der Datei nicht prüfbar", S_H1))
    if gruppen["nicht_pruefbar"]:
        z = [[P("Nr.", S_KOPF), P("Regel", S_KOPF), P("Thema", S_KOPF), P("Was fehlt", S_KOPF)]]
        for b in gruppen["nicht_pruefbar"]:
            fehlt = b.get("fehlt") or b.get("begruendung") or ""
            if b.get("nachweis_erforderlich"):
                fehlt += " (Nachweis erforderlich)"
            z.append([P(b.get("nr"), S_KLEIN), P(b.get("regel"), S_KLEIN),
                      P(b.get("titel"), S_KLEIN), P(fehlt, S_KLEIN)])
        inhalt.append(tabelle(z, [10 * mm, 18 * mm, 56 * mm, 90 * mm]))
    else:
        inhalt.append(P("Keine.", S_KLEIN))

    # 6.–8.
    inhalt.append(P("6. Positiv festgestellt (ohne Gesamturteil)", S_H1))
    inhalt += aufzaehlung(daten.get("positiv"))
    inhalt.append(P("7. Annahmen", S_H1))
    inhalt += aufzaehlung(daten.get("annahmen"))

    inhalt.append(P("8. Grundlagen und Normstand", S_H1))
    grundlagen = []
    for b in befunde:
        for g in str(b.get("grundlage", "")).split(";"):
            g = g.strip()
            if g and g not in grundlagen:
                grundlagen.append(g)
    inhalt += aufzaehlung(grundlagen)
    inhalt.append(Spacer(1, 2 * mm))
    inhalt.append(P("Normausgaben und Gesetzesstand laut Quellenliste des Skills "
                    "(pruefkatalog/quellen.md), Stand 16.11.2026. Norminhalte sind sinngemäß "
                    "wiedergegeben. Vor fachlicher Verwendung den aktuellen Status und die "
                    "bauaufsichtliche Einführung prüfen.", S_KLEIN))

    inhalt += [Spacer(1, 6 * mm), KeepTogether([hinweisbox(PFLICHTHINWEIS)])]
    return inhalt


# ---------------------------------------------------------------- Zusammenbau
def fusszeile(breite, hoehe, nr, gesamt, titel, beschriftung=None):
    puffer = io.BytesIO()
    c = canvas.Canvas(puffer, pagesize=(breite, hoehe))
    rand = 18 * mm if breite < 700 else 12 * mm
    c.setStrokeColor(LINIE)
    c.setLineWidth(0.5)
    c.line(rand, 14 * mm, breite - rand, 14 * mm)
    c.setFont(SCHRIFT, 7.5)
    c.setFillColor(colors.HexColor("#4B5563"))
    c.drawString(rand, 10 * mm, t(f"Detailprüfer Architektur · Prüfbericht {titel}"))
    c.drawRightString(breite - rand, 10 * mm, t(f"Seite {nr} von {gesamt}"))
    c.setFillColor(colors.HexColor("#7F1D1D"))
    c.drawString(rand, 6.5 * mm, t("Hilfestellung – ersetzt keine fachliche Prüfung und keinen Nachweis."))
    if beschriftung:  # Kopfzeile für die Zeichnungsseite
        c.setFillColor(colors.HexColor("#111827"))
        c.setFont(SCHRIFT_FETT, 10)
        c.drawString(rand, hoehe - 10 * mm, t(beschriftung[0]))
        c.setFont(SCHRIFT, 8)
        c.drawString(rand, hoehe - 14.5 * mm, t(beschriftung[1]))
    c.save()
    puffer.seek(0)
    return PdfReader(puffer).pages[0]


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    pdf_ein, json_datei, pdf_aus = sys.argv[1:4]
    with open(json_datei, encoding="utf-8") as f:
        daten = json.load(f)
    titel = daten.get("detail", {}).get("titel", "")

    # Textteil
    puffer = io.BytesIO()
    doc = SimpleDocTemplate(puffer, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=20 * mm,
                            title=t(f"Prüfbericht {titel}"), author="Detailprüfer Architektur")
    doc.build(textseiten(daten))
    puffer.seek(0)
    text = PdfReader(puffer)

    # Markierte Zeichnung
    zw, seitennr, anzahl = markierte_seite(pdf_ein, daten)
    zp = io.BytesIO()
    zw.write(zp)
    zp.seek(0)
    zeichnung = PdfReader(zp).pages[seitennr - 1]

    out = PdfWriter()
    out.add_page(text.pages[0])
    out.add_page(zeichnung)
    for p in text.pages[1:]:
        out.add_page(p)

    gesamt = len(out.pages)
    for i, seite in enumerate(out.pages, 1):
        mb = seite.mediabox
        kopf = None
        if i == 2:
            kopf = ("Markierte Zeichnung – Nummern entsprechen der Befundliste",
                    "Rot durchgezogen = klarer Aufbaufehler · gestrichelt = mögliche Auffälligkeit · "
                    "gepunktet = Verbesserungshinweis")
        ebene = fusszeile(float(mb.width), float(mb.height), i, gesamt, titel, kopf)
        seite.merge_transformed_page(ebene, Transformation().translate(float(mb.left), float(mb.bottom)))

    out.add_metadata({"/Title": t(f"Prüfbericht {titel}"),
                      "/Author": "Detailprüfer Architektur (KI-Hilfestellung)",
                      "/Subject": "Qualitative Plausibilitätsprüfung – kein Nachweis"})
    with open(pdf_aus, "wb") as f:
        out.write(f)
    print(f"Prüfbericht erstellt: {pdf_aus}  ({gesamt} Seiten, {anzahl} Markierungen, "
          f"Schrift: {'Unicode' if UNICODE else 'Helvetica (Ersatzzeichen)'})")


if __name__ == "__main__":
    main()
