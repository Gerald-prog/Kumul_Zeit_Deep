from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional


@dataclass
class Tagesdaten:
    ist: float = 0.0
    soll: float = 0.0
    typ: str = "normal"


@dataclass
class WochenDaten:
    tage: Dict[date, Tagesdaten] = field(default_factory=dict)
    ist_stunden: float = 0.0
    tage_mit_daten: int = 0
    soll_stunden: float = 0.0
    diff: float = 0.0
    saldo: float = 0.0

    # Getrennte Gutschriften-Töpfe
    urlaub_gutschrift: float = 0.0
    krank_gutschrift: float = 0.0
    feiertag_nicht_gearbeitet_gutschrift: float = 0.0
    feiertag_zuschlag_gutschrift: float = 0.0

    # Davon bereits ausgezahlt
    urlaub_ausbezahlt: float = 0.0
    krank_ausbezahlt: float = 0.0
    feiertag_nicht_gearbeitet_ausbezahlt: float = 0.0
    feiertag_zuschlag_ausbezahlt: float = 0.0

    feiertags_namen: List[str] = field(default_factory=list)
    ist_stunden_pdf_original: Optional[float] = None
    hinweis: str = ""


class Arbeitszeitrechner:
    def __init__(self, zeitmodelle_raw: list):
        self.zeitmodelle = sorted(zeitmodelle_raw, key=lambda x: x["gueltig_ab"])
        self._cache = {}

    def get_config_for_date(self, stichtag: date) -> dict:
        if stichtag in self._cache:
            return self._cache[stichtag]
        gewaehltes_modell = (
            self.zeitmodelle[0] if self.zeitmodelle else {"tagessoll": {}}
        )
        for modell in self.zeitmodelle:
            modell_start = date.fromisoformat(modell["gueltig_ab"])
            if stichtag >= modell_start:
                gewaehltes_modell = modell
            else:
                break
        self._cache[stichtag] = gewaehltes_modell
        return gewaehltes_modell
