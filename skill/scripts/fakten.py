"""Liest die festen Fakten einer PDF-Zeichnung aus – bei jedem Lauf identisch.

Zweck: Gleiche Zeichnung → gleiche Grundlage. Alles, was als Text in der PDF steht
(Legende, Maßzahlen, Winkel, Beschriftungen, Maßstab), wird hier exakt ausgelesen statt
aus dem Bild geschätzt. Befunde zu Legende, Maßkette, Beschriftung und Winkel werden nur
aus diesen Fakten abgeleitet.

Aufruf:
    python fakten.py <zeichnung.pdf> fakten.json [--seite 1]

Ausgabe (fakten.json):
    datei, pruefsumme (SHA-256, erste 12 Zeichen), seiten, blatt_mm,
    massstab (gefundene Angaben „1:5“ …), texte (jede Textzeile mit Position in Prozent),
    legende (Zeilen der Form „2,0 cm  Holzverkleidung …“, sortiert wie in der Zeichnung),
    zahlen (alleinstehende Zahlen, z. B. Maßketten), winkel (Angaben mit „°“).
Koordinaten: x = 0 links … 100 rechts, y = 0 oben … 100 unten (wie raster.py / befunde.json).
"""
import argparse
import hashlib
import json
import os
import re
import sys

from pypdf import PdfReader

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def pruefsumme(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()[:12].upper()


def texte_lesen(seite):
    """Alle Textstücke mit Position (Prozent) – in fester Reihenfolge."""
    w, h = float(seite.mediabox.width), float(seite.mediabox.height)
    stuecke = []

    def besucher(text, cm, tm, _fd, groesse):
        s = text.strip()
        if not s:
            return
        x, y = tm[4], tm[5]
        X = cm[0] * x + cm[2] * y + cm[4]
        Y = cm[1] * x + cm[3] * y + cm[5]
        gr = abs(groesse * tm[0] * cm[0]) or groesse
        stuecke.append({"text": s, "x": round(X / w * 100, 2), "y": round(100 - Y / h * 100, 2),
                        "groesse_pt": round(gr, 1)})

    seite.extract_text(visitor_text=besucher)
    return stuecke, w, h


def zeilen_bilden(stuecke, toleranz=0.35, max_luecke=4.0):
    """Textstücke mit (fast) gleicher Grundlinie und kleiner Lücke zu Zeilen zusammenfassen.
    max_luecke (Prozent der Blattbreite) trennt z. B. Legende und weiter rechts stehende Beschriftungen."""
    zeilen = []
    for s in sorted(stuecke, key=lambda s: (round(s["y"], 1), s["x"])):
        for z in zeilen:
            if abs(z["y"] - s["y"]) <= toleranz and -1.0 <= s["x"] - z["x_ende"] <= max_luecke:
                z["teile"].append(s)
                z["x_ende"] = s["x"] + 0.6 * len(s["text"])
                break
        else:
            zeilen.append({"y": s["y"], "x": s["x"], "x_ende": s["x"] + 0.6 * len(s["text"]),
                           "teile": [s]})
    ergebnis = []
    for z in sorted(zeilen, key=lambda z: (round(z["y"], 1), z["x"])):
        teile = sorted(z["teile"], key=lambda s: s["x"])
        ergebnis.append({"text": " ".join(t["text"] for t in teile), "x": teile[0]["x"],
                         "y": z["y"], "teile": [{"text": t["text"], "x": t["x"]} for t in teile]})
    return ergebnis


# Zahl darf in mehrere Textstücke zerfallen sein („1 ,0 cm“) – Leerzeichen werden toleriert
DICKE = re.compile(r"^\s*(\d+(?:\s?[,.]\s?\d+)?)\s*(cm|mm)\b\s*(.*)$", re.IGNORECASE)


def legende_finden(zeilen):
    """Zeilen, die mit einer Dicke beginnen („2,0 cm Holzverkleidung“) – in Blöcken."""
    eintraege = []
    for z in zeilen:
        m = DICKE.match(z["text"])
        if m and m.group(3).strip():
            zahl = re.sub(r"\s", "", m.group(1))
            eintraege.append({"dicke": f"{zahl} {m.group(2)}", "bezeichnung": m.group(3).strip(),
                              "x": z["x"], "y": z["y"]})
    # in Blöcke gruppieren (gleiche x-Spalte, Zeilen nah untereinander)
    bloecke = []
    for e in sorted(eintraege, key=lambda e: (round(e["x"]), e["y"])):
        for b in bloecke:
            letzte = b[-1]
            if abs(letzte["x"] - e["x"]) < 1.5 and 0 < e["y"] - letzte["y"] < 3.0:
                b.append(e)
                break
        else:
            bloecke.append([e])
    return [b for b in bloecke if len(b) >= 2]


def main():
    ap = argparse.ArgumentParser(description="Feste Fakten (Texte, Legende, Maße) aus einer PDF lesen")
    ap.add_argument("pdf")
    ap.add_argument("json")
    ap.add_argument("--seite", type=int, default=1)
    a = ap.parse_args()

    reader = PdfReader(a.pdf)
    seite = reader.pages[a.seite - 1]
    stuecke, w, h = texte_lesen(seite)
    zeilen = zeilen_bilden(stuecke)
    alle_texte = " ".join(z["text"] for z in zeilen)

    fakten = {
        "datei": os.path.basename(a.pdf),
        "pruefsumme": pruefsumme(a.pdf),
        "seiten": len(reader.pages),
        "blatt_mm": [round(w / 72 * 25.4), round(h / 72 * 25.4)],
        "massstab": sorted(set(re.findall(r"\b1\s?:\s?\d+\b", alle_texte))),
        "legende": legende_finden(zeilen),
        "zahlen": [{"text": s["text"], "x": s["x"], "y": s["y"]} for s in stuecke
                   if re.fullmatch(r"\d+(?:[,.]\d+)?", s["text"])],
        "winkel": [{"text": z["text"], "x": z["x"], "y": z["y"]} for z in zeilen if "°" in z["text"]],
        "texte": zeilen,
    }
    with open(a.json, "w", encoding="utf-8") as f:
        json.dump(fakten, f, ensure_ascii=False, indent=1)

    print(f"Datei: {fakten['datei']}  Prüfsumme: {fakten['pruefsumme']}  Blatt: "
          f"{fakten['blatt_mm'][0]} × {fakten['blatt_mm'][1]} mm  Maßstab: {', '.join(fakten['massstab']) or '–'}")
    for i, block in enumerate(fakten["legende"], 1):
        print(f"Legende {i} (x ≈ {block[0]['x']:.0f} %, y ≈ {block[0]['y']:.0f} %):")
        for e in block:
            print(f"   {e['dicke']:>8}  {e['bezeichnung']}")
    if fakten["winkel"]:
        print("Winkelangaben: " + "; ".join(f"{w_['text']} (x {w_['x']:.0f} %, y {w_['y']:.0f} %)"
                                              for w_ in fakten["winkel"]))
    print(f"{len(zeilen)} Textzeilen, {len(fakten['zahlen'])} Einzelzahlen → {a.json}")


if __name__ == "__main__":
    main()
