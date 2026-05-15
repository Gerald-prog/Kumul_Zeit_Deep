from pathlib import Path
from datetime import date
from collections import defaultdict

from pdf_parser import lade_pdf_text, baue_tages_ist_aus_pdf_text


from pathlib import Path
from datetime import date
from collections import defaultdict

from pdf_parser import lade_pdf_text, baue_tages_ist_aus_pdf_text


def lade_tages_ist_aus_pdf_ordner(pfad: Path) -> dict[date, float]:
    print(f"\n🔍 Suche PDFs in: {pfad}")
    if not pfad.exists():
        raise FileNotFoundError(f"Ordner existiert nicht: {pfad}")
    if not pfad.is_dir():
        raise ValueError(f"Pfad ist kein Ordner: {pfad}")

    pdf_dateien = sorted(pfad.glob("*.pdf"))
    print(f"📄 Gefundene PDFs: {len(pdf_dateien)}")

    tages_ist: dict[date, float] = defaultdict(float)

    for pdf_path in pdf_dateien:
        try:
            text = lade_pdf_text(pdf_path)
            daten = baue_tages_ist_aus_pdf_text(text)
            for tag, stunden in daten.items():
                tages_ist[tag] += stunden
        except Exception as e:
            print(f"❌ Fehler bei {pdf_path.name}: {e}")

    # --- HIER KOMMT DIE NEUE AUSGABE ---
    print("\n📋 ENDGÜLTIGE TAGESLISTE (sortiert):")
    for tag in sorted(tages_ist.keys()):
        print(f"   {tag}  ->  {tages_ist[tag]} h")

    print(f"\n✅ Gesamttage nach Zusammenführung: {len(tages_ist)}")
    return dict(tages_ist)


# DEBUG-VERSION
# def lade_tages_ist_aus_pdf_ordner(pfad: Path) -> dict[date, float]:
#     print(f"\n🔍 Suche PDFs in: {pfad}")
#     if not pfad.exists():
#         print("❌ Ordner existiert nicht!")
#         raise FileNotFoundError(f"Ordner existiert nicht: {pfad}")
#     if not pfad.is_dir():
#         print("❌ Pfad ist kein Ordner!")
#         raise ValueError(f"Pfad ist kein Ordner: {pfad}")

#     pdf_dateien = sorted(pfad.glob("*.pdf"))
#     print(f"📄 Gefundene PDFs: {len(pdf_dateien)}")
#     for i, p in enumerate(pdf_dateien):
#         print(f"   {i+1}. {p.name}")

#     if not pdf_dateien:
#         print("⚠️ Keine PDF-Dateien vorhanden – Abbruch.")
#         return {}

#     tages_ist: dict[date, float] = defaultdict(float)

#     for pdf_path in pdf_dateien:
#         try:
#             print(f"\n📥 Lese: {pdf_path.name}")
#             text = lade_pdf_text(pdf_path)
#             print(f"   Textlänge: {len(text)} Zeichen")
#             daten = baue_tages_ist_aus_pdf_text(text)
#             print(f"   Gefundene Tage: {len(daten)}")
#             for tag, stunden in daten.items():
#                 print(f"      {tag}  ->  {stunden} h")
#                 tages_ist[tag] += stunden
#         except Exception as e:
#             print(f"❌ Fehler bei {pdf_path.name}: {e}")

#     print(f"\n✅ Gesamttage nach Zusammenführung: {len(tages_ist)}")
#     return dict(tages_ist)

# ORIGINAL VERSION
# def lade_tages_ist_aus_pdf_ordner(pfad: Path) -> dict[date, float]:
#     if not pfad.exists():
#         raise FileNotFoundError(f"Ordner existiert nicht: {pfad}")
#     if not pfad.is_dir():
#         raise ValueError(f"Pfad ist kein Ordner: {pfad}")
#     tages_ist: dict[date, float] = defaultdict(float)
#     pdf_dateien = sorted(pfad.glob("*.pdf"))
#     for pdf_path in pdf_dateien:
#         try:
#             text = lade_pdf_text(pdf_path)
#             daten = baue_tages_ist_aus_pdf_text(text)
#             for tag, stunden in daten.items():
#                 tages_ist[tag] += stunden
#         except Exception as e:
#             print(f"Fehler beim Verarbeiten von {pdf_path.name}: {e}")
#     return dict(tages_ist)
