from pathlib import Path
from datetime import date, datetime, timedelta
from collections import defaultdict
import re

from pdf_parser import lade_pdf_text, baue_tages_ist_aus_pdf_text


def extract_date_from_filename(filename: str) -> date | None:
    """
    Zieht ein Datum (Jahr, Monat, Tag) aus einem Dateinamen wie
    '..._und_2025 12 22_am_...' heraus.
    """
    match = re.search(r"(\d{4})\s+(\d{2})\s+(\d{2})", filename)
    if match:
        y, m, d = map(int, match.groups())
        try:
            return date(y, m, d)
        except ValueError:
            pass
    return None


def montag_der_woche(d: date) -> date:
    """Gibt den Montag der Woche zurück, in der d liegt."""
    return d - timedelta(days=d.weekday())


def lade_tages_ist_aus_pdf_ordner(pfad: Path) -> dict[date, float]:
    print(f"\n🔍 Suche PDFs in: {pfad}")
    if not pfad.exists():
        raise FileNotFoundError(f"Ordner existiert nicht: {pfad}")
    if not pfad.is_dir():
        raise ValueError(f"Pfad ist kein Ordner: {pfad}")

    pdf_dateien = sorted(pfad.glob("*.pdf"))
    print(f"📄 Gefundene PDFs: {len(pdf_dateien)}")

    # Sortiere absteigend nach dem Datum im Dateinamen (neueste zuerst)
    pdf_dateien.sort(
        key=lambda p: extract_date_from_filename(p.stem) or date.min,
        reverse=True,
    )

    tages_ist: dict[date, float] = {}
    gesehene_tage: set[date] = set()

    for pdf_path in pdf_dateien:
        try:
            text = lade_pdf_text(pdf_path)
            rohdaten = baue_tages_ist_aus_pdf_text(text)

            # Kalenderwoche aus dem Dateinamen bestimmen
            file_datum = extract_date_from_filename(pdf_path.stem)
            if file_datum is None:
                print(
                    f"⚠️ Kein Datum im Dateinamen: {pdf_path.name} – überspringe Filter"
                )
                continue

            week_start = montag_der_woche(file_datum)
            week_end = week_start + timedelta(days=6)

            # Nur Tage innerhalb dieser Woche übernehmen, wenn noch nicht gesehen
            for tag, stunden in rohdaten.items():
                if week_start <= tag <= week_end and tag not in gesehene_tage:
                    gesehene_tage.add(tag)
                    tages_ist[tag] = stunden

            print(
                f"   {pdf_path.name}: {len(rohdaten)} rohe Tage, "
                f"innerhalb der Woche übernommen: {len(tages_ist)} bisher"
            )

        except Exception as e:
            print(f"❌ Fehler bei {pdf_path.name}: {e}")

    print("\n📋 ENDGÜLTIGE TAGESLISTE (sortiert):")
    for tag in sorted(tages_ist.keys()):
        print(f"   {tag}  ->  {tages_ist[tag]} h")

    print(f"\n✅ Gesamttage nach Zusammenführung: {len(tages_ist)}")
    return tages_ist
