import re
from datetime import date, datetime
from typing import Dict
from pathlib import Path
import pdfplumber
from collections import defaultdict


def parse_stunden(text: str) -> float:
    text = text.replace(",", ".")
    return float(text)


def lade_pdf_text(pfad: str | Path) -> str:
    text = []
    with pdfplumber.open(str(pfad)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def baue_tages_ist_aus_pdf_text(pdf_text: str) -> Dict[date, float]:
    # Alleinstehende Datumszeilen vor der eigentlichen Stundenzeile entfernen
    bereinigt = re.sub(
        r"(\d{2}\.\d{2}\.\d{4})\s*\n\s*(\1\s+\d+[.,]?\d*)",
        r"\2",
        pdf_text,
    )

    tages_ist: dict[date, float] = defaultdict(float)

    # Neuer, robuster Regex: Nur Datum + erste Zahl (Stunden) – alles andere ignorieren
    pattern = re.compile(
        r"(\d{2}\.\d{2}\.\d{4})\s+(\d+(?:[.,]\d+)?)\s+(Regular|Holiday Surcharge)",
        re.MULTILINE,
    )

    for match in pattern.finditer(bereinigt):
        datum_str = match.group(1)
        stunden_str = match.group(2)

        d = datetime.strptime(datum_str, "%d.%m.%Y").date()
        stunden = float(stunden_str.replace(",", "."))
        tages_ist[d] += stunden

    return dict(tages_ist)


# def baue_tages_ist_aus_pdf_text(pdf_text: str) -> Dict[date, float]:
#     # Textbereinigung: alleinstehende Datumszeilen vor Berechnungszeile entfernen
#     bereinigt = re.sub(
#         r"(\d{2}\.\d{2}\.\d{4})\s*\n\s*(\1\s+\d+[.,]?\d*\s+(?:Regular|Holiday Surcharge))",
#         r"\2",
#         pdf_text,
#     )
#     tages_ist: dict[date, float] = defaultdict(float)
#     pattern = re.compile(
#         r"(?P<datum>\d{2}\.\d{2}\.\d{4})\s+"
#         r"(?P<stunden>\d+(?:,\d+)?)\s+"
#         r"(?P<zeitart>[A-Za-z ]+)",
#         re.MULTILINE,
#     )
#     for match in pattern.finditer(bereinigt):
#         datum_str = match.group("datum")
#         stunden_str = match.group("stunden")
#         d = datetime.strptime(datum_str, "%d.%m.%Y").date()
#         stunden = float(stunden_str.replace(",", "."))
#         tages_ist[d] += stunden
#     return dict(tages_ist)
