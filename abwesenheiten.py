import json
from pathlib import Path
from datetime import datetime, date, timedelta
import sys

# Bestimme das Verzeichnis, in dem die JSON gespeichert wird
if getattr(sys, "frozen", False):
    EXE_DIR = Path(sys.executable).parent
else:
    EXE_DIR = Path(__file__).parent

ABWESENHEITEN_DATEI = EXE_DIR / "abwesenheiten.json"


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def expand_range(von: date, bis: date):
    d = von
    while d <= bis:
        yield d
        d += timedelta(days=1)


def lade_abwesenheiten_raw(pfad=None) -> dict:
    if pfad is None:
        p = ABWESENHEITEN_DATEI
    else:
        p = Path(pfad)
    if not p.exists():
        return {
            "urlaub_raw": [],
            "feiertage_raw": [],
            "krankheit_raw": [],
            "arzttermine_raw": [],
            "auszahlungen_raw": {},
        }
    return json.loads(p.read_text(encoding="utf-8"))


def speichere_abwesenheiten_raw(data: dict, pfad=None):
    if pfad is None:
        p = ABWESENHEITEN_DATEI
    else:
        p = Path(pfad)
    p.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def baue_abwesenheiten_core(raw: dict):
    urlaub: set[date] = set()
    feiertage: set[date] = set()
    krankheit: dict[date, float] = {}
    arzttermine: dict[date, float] = {}

    for block in raw.get("urlaub_raw", []):
        von = parse_date(block["von"])
        bis = parse_date(block["bis"])
        urlaub.update(expand_range(von, bis))

    for d in raw.get("feiertage_raw", []):
        feiertage.add(parse_date(d))

    for block in raw.get("krankheit_raw", []):
        von = parse_date(block["von"])
        bis = parse_date(block.get("bis", block["von"]))
        gs = block.get("gearbeitete_stunden", {})
        for tag in expand_range(von, bis):
            krankheit[tag] = float(gs.get(tag.isoformat(), 0.0))

    for a in raw.get("arzttermine_raw", []):
        arzttermine[parse_date(a["datum"])] = float(a["dauer"])

    return urlaub, feiertage, krankheit, arzttermine


def speichere_auszahlung(montag: date, kategorie: str, stunden: float, pfad=None):
    raw = lade_abwesenheiten_raw(pfad)
    if "auszahlungen_raw" not in raw:
        raw["auszahlungen_raw"] = {}
    m_str = montag.isoformat()
    if m_str not in raw["auszahlungen_raw"]:
        raw["auszahlungen_raw"][m_str] = {}
    if stunden <= 0:
        raw["auszahlungen_raw"][m_str].pop(kategorie, None)
    else:
        raw["auszahlungen_raw"][m_str][kategorie] = stunden
    speichere_abwesenheiten_raw(raw, pfad)
