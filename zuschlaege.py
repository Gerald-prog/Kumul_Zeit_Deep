"""
Zentrale Berechnungslogik für alle Zuschläge.
Die konkreten Werte (Faktoren) kommen aus der config.json,
die Regeln (z.B. Ist × Faktor) stehen hier.
"""


def berechne_feiertags_zuschlag(ist_stunden: float, faktor: float) -> float:
    """
    Feiertagszuschlag: Ist-Stunden × Faktor.
    Beispiel: 8h × 1,25 = 10h
    """
    return round(ist_stunden * faktor, 4)


# Hier kannst du später weitere Funktionen ergänzen, z. B.:
# def berechne_nacht_zuschlag(ist_stunden, beginn, ende, faktor):
#     ...
