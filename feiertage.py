from datetime import date
import holidays
from typing import Set

BUNDESLAENDER = {
    "Baden-Württemberg": "BW",
    "Bayern": "BY",
    "Berlin": "BE",
    "Brandenburg": "BB",
    "Bremen": "HB",
    "Hamburg": "HH",
    "Hessen": "HE",
    "Mecklenburg-Vorpommern": "MV",
    "Niedersachsen": "NI",
    "Nordrhein-Westfalen": "NW",
    "Rheinland-Pfalz": "RP",
    "Saarland": "SL",
    "Sachsen": "SN",
    "Sachsen-Anhalt": "ST",
    "Schleswig-Holstein": "SH",
    "Thüringen": "TH",
}


def lade_feiertage(jahr: int, bundesland_iso: str) -> set[date]:
    feiertage = holidays.country_holidays("DE", years=jahr, subdiv=bundesland_iso)
    return set(feiertage.keys())


def lade_feiertage_mit_namen(jahr: int, bundesland_iso: str):
    return holidays.country_holidays("DE", years=jahr, subdiv=bundesland_iso)


def lade_feiertage_fuer_zeitraum(
    start: date, ende: date, bundesland_iso: str
) -> Set[date]:
    feiertage: Set[date] = set()
    for jahr in range(start.year, ende.year + 1):
        feiertage.update(lade_feiertage(jahr, bundesland_iso))
    return {d for d in feiertage if start <= d <= ende}


def ist_feiertag(datum: date, feiertage: set[date]) -> bool:
    return datum in feiertage
