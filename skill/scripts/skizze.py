"""Erzeugt die Korrekturskizze: Originalzeichnung + grün eingezeichnete Ergänzungen.

Aufruf:
    python skizze.py <zeichnung.pdf> <befunde.json> <korrektur.pdf>

Die Ergänzungen stehen je Befund im Feld "korrektur" (siehe markieren.zeichne_korrektur):
holz, platte, abklebung, linie, durchstreichen, text – Koordinaten in Prozent.
Die Originalzeichnung bleibt als Vektor-PDF erhalten.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from markieren import korrigierte_seite  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    pdf_ein, json_datei, pdf_aus = sys.argv[1:4]
    with open(json_datei, encoding="utf-8") as f:
        daten = json.load(f)
    writer, _, anzahl = korrigierte_seite(pdf_ein, daten)
    with open(pdf_aus, "wb") as f:
        writer.write(f)
    print(f"Korrekturskizze mit {anzahl} Element(en) erstellt → {pdf_aus}")


if __name__ == "__main__":
    main()
