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
    gesamter_text = "\n".join(text)

    # Prüfe, ob der Text normale Datumsangaben enthält
    if not re.search(r"\d{2}\.\d{2}\.\d{4}", gesamter_text):
        # Wenn nicht, ist er wahrscheinlich gespiegelt → umdrehen
        gesamter_text = gesamter_text[::-1]

    return gesamter_text


def baue_tages_ist_aus_pdf_text(pdf_text: str) -> Dict[date, float]:
    tages_ist: dict[date, float] = defaultdict(float)

    # Direkt nach Datum, Zahl und "Regular" oder "Holiday Surcharge" suchen
    pattern = re.compile(
        r"(\d{2}\.\d{2}\.\d{4})\s+(\d+(?:[.,]\d+)?)\s+(Regular|Holiday Surcharge)"
    )

    for match in pattern.finditer(pdf_text):
        datum_str = match.group(1)
        stunden_str = match.group(2)
        d = datetime.strptime(datum_str, "%d.%m.%Y").date()
        stunden = float(stunden_str.replace(",", "."))
        tages_ist[d] += stunden

    return dict(tages_ist)
