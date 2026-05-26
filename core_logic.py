from datetime import date, datetime, timedelta
from pathlib import Path
import holidays
import re

from abwesenheiten import (
    lade_abwesenheiten_raw,
    baue_abwesenheiten_core,
)
from feiertage import lade_feiertage
from pdf_ordner_loader import lade_tages_ist_aus_pdf_ordner
from models import Tagesdaten, WochenDaten, Arbeitszeitrechner


def parse_date_ddmmYYYY(s: str) -> date:
    return datetime.strptime(s, "%d.%m.%Y").date()


def montag_von_datum(d: date) -> date:
    return d - timedelta(days=d.weekday())


def baue_wochen_aus_tagen(tages_ist: dict[date, float]) -> dict[date, WochenDaten]:
    wochen: dict[date, WochenDaten] = {}
    for tag, stunden in tages_ist.items():
        montag = tag - timedelta(days=tag.weekday())
        if montag not in wochen:
            wochen[montag] = WochenDaten()
        w = wochen[montag]
        w.tage[tag] = Tagesdaten(ist=stunden, soll=0.0, typ="Arbeit")
        w.ist_stunden += stunden
        w.tage_mit_daten += 1
    return wochen


def ergaenze_fehlende_wochen(
    wochen: dict[date, WochenDaten],
    start_montag: date,
    end_datum: date,
) -> dict[date, WochenDaten]:
    m = start_montag
    while m <= end_datum:
        if m not in wochen:
            wochen[m] = WochenDaten()
        m += timedelta(days=7)
    return wochen


def ergaenze_wochen_um_soll_und_gutschriften(
    wochen: dict[date, WochenDaten],
    soll_wochenstunden: float,
    urlaub: set[date],
    feiertage: set[date],
    krankheit: dict[date, float],
    arzttermine: dict[date, float],
    zeitmodelle_liste: list | None = None,
    feiertags_zuschlag_faktor: float = 1.0,
):
    rechner = Arbeitszeitrechner(zeitmodelle_liste) if zeitmodelle_liste else None
    feiertags_cache: dict[tuple[int, str], set[date]] = {}
    soll_pro_tag_fallback = soll_wochenstunden / 5
    manuelle_feiertage = feiertage

    for montag, woche in wochen.items():
        if woche.ist_stunden_pdf_original is None:
            woche.ist_stunden_pdf_original = woche.ist_stunden
        pdf_ist = woche.ist_stunden_pdf_original
        gutschriften = {
            "urlaub": 0.0,
            "krank": 0.0,
            "feiertag_nicht_gearbeitet": 0.0,
            "feiertag_zuschlag": 0.0,
        }
        feiertags_ist_summe = 0.0  # gearbeitete Feiertagsstunden (für Umbuchung)

        for i in range(7):
            tag = montag + timedelta(days=i)

            # Basis-Soll für diesen Tag (ohne Abwesenheiten)
            if rechner:
                config = rechner.get_config_for_date(tag)
                tagessoll_basis = float(
                    config["tagessoll"].get(str(tag.weekday()), 0.0)
                )
                land = config.get("bundesland", "SN")
            else:
                tagessoll_basis = soll_pro_tag_fallback if tag.weekday() < 5 else 0.0
                land = "SN"

            # Feiertage laden (mit Cache)
            jahr = tag.year
            if (jahr, land) not in feiertags_cache:
                feiertags_cache[(jahr, land)] = lade_feiertage(jahr, land)
            aktuelle_feiertage = feiertags_cache[(jahr, land)] | manuelle_feiertage

            # Feiertagsnamen für die Anzeige sammeln
            if tag in aktuelle_feiertage:
                feiertage_obj = holidays.country_holidays(
                    "DE", years=tag.year, subdiv=land
                )
                name = feiertage_obj.get(tag)
                if name:
                    eintrag = f"{tag.strftime('%d.%m.')}: {name}"
                    if eintrag not in woche.feiertags_namen:
                        woche.feiertags_namen.append(eintrag)

            # --- 1. Urlaub ---
            if tag in urlaub:
                woche.tage[tag] = Tagesdaten(ist=0.0, soll=0.0, typ="urlaub")
                continue

            # --- 2. Krankheit ---
            if tag in krankheit:
                gearb = krankheit[tag]
                woche.tage[tag] = Tagesdaten(ist=gearb, soll=gearb, typ="krankheit")
                continue

            # --- 3. Feiertag (arbeitend oder nicht) ---
            if tag in aktuelle_feiertage:
                if tag in woche.tage:  # am Feiertag gearbeitet
                    ist_std = woche.tage[tag].ist
                    zuschlag = 0.0
                    if feiertags_zuschlag_faktor > 1.0:
                        zuschlag = ist_std * (feiertags_zuschlag_faktor - 1.0)
                    gutschriften["feiertag_zuschlag"] += ist_std + zuschlag
                    feiertags_ist_summe += ist_std
                    woche.tage[tag].typ = "feiertag_gearbeitet"
                    woche.tage[tag].soll = 0.0
                else:  # nicht gearbeitet
                    woche.tage[tag] = Tagesdaten(ist=0.0, soll=0.0, typ="feiertag_frei")
                continue

            # --- 4. Arzttermin ---
            effektives_soll = tagessoll_basis
            if tag in arzttermine:
                reduz = min(arzttermine[tag], tagessoll_basis)
                effektives_soll = max(tagessoll_basis - reduz, 0.0)

            # --- Normaltag: Eintrag anlegen oder Soll setzen ---
            if tag not in woche.tage:
                woche.tage[tag] = Tagesdaten(
                    ist=0.0, soll=effektives_soll, typ="normal"
                )
            else:
                # Tag aus PDF: Ist bereits gesetzt, nur Soll nachtragen
                woche.tage[tag].soll = effektives_soll
                if tag in arzttermine:
                    woche.tage[tag].typ = "arzttermin"

        # --- Wochenwerte aus ALLEN 7 Tagen aggregieren ---
        wochen_soll_summe = 0.0
        for i in range(7):
            tag = montag + timedelta(days=i)
            if tag in woche.tage:
                wochen_soll_summe += woche.tage[tag].soll
            else:
                # Tag wurde bisher in keinem Zweig angelegt → Basis-Soll verwenden
                if rechner:
                    config = rechner.get_config_for_date(tag)
                    tagessoll = float(config["tagessoll"].get(str(tag.weekday()), 0.0))
                else:
                    tagessoll = soll_pro_tag_fallback if tag.weekday() < 5 else 0.0
                wochen_soll_summe += tagessoll

        woche.soll_stunden = round(wochen_soll_summe, 2)
        woche.urlaub_gutschrift = round(gutschriften["urlaub"], 2)
        woche.krank_gutschrift = round(gutschriften["krank"], 2)
        woche.feiertag_nicht_gearbeitet_gutschrift = round(
            gutschriften["feiertag_nicht_gearbeitet"], 2
        )
        woche.feiertag_zuschlag_gutschrift = round(gutschriften["feiertag_zuschlag"], 2)

        gesamte_gutschrift = sum(gutschriften.values())
        woche.ist_stunden = round(pdf_ist - feiertags_ist_summe + gesamte_gutschrift, 2)
        woche.diff = round(woche.ist_stunden - woche.soll_stunden, 2)


def wende_auszahlung_an(
    wochen: dict[date, WochenDaten],
    auszahlungen: dict[date, dict[str, float]],
):
    for montag, kat_dict in auszahlungen.items():
        if montag not in wochen:
            continue
        w = wochen[montag]
        for kategorie, betrag in kat_dict.items():
            if kategorie == "urlaub":
                verfuegbar = w.urlaub_gutschrift - w.urlaub_ausbezahlt
                if verfuegbar <= 0:
                    continue
                abzug = min(verfuegbar, betrag)
                w.urlaub_ausbezahlt += abzug
                w.diff -= abzug
            elif kategorie == "krank":
                verfuegbar = w.krank_gutschrift - w.krank_ausbezahlt
                if verfuegbar <= 0:
                    continue
                abzug = min(verfuegbar, betrag)
                w.krank_ausbezahlt += abzug
                w.diff -= abzug
            elif kategorie == "feiertag_nicht_gearbeitet":
                verfuegbar = (
                    w.feiertag_nicht_gearbeitet_gutschrift
                    - w.feiertag_nicht_gearbeitet_ausbezahlt
                )
                if verfuegbar <= 0:
                    continue
                abzug = min(verfuegbar, betrag)
                w.feiertag_nicht_gearbeitet_ausbezahlt += abzug
                w.diff -= abzug
            elif kategorie == "feiertag_zuschlag":
                verfuegbar = (
                    w.feiertag_zuschlag_gutschrift - w.feiertag_zuschlag_ausbezahlt
                )
                if verfuegbar <= 0:
                    continue
                abzug = min(verfuegbar, betrag)
                w.feiertag_zuschlag_ausbezahlt += abzug
                w.diff -= abzug


def berechne_saldo(wochen: dict[date, WochenDaten], start_saldo: float = 0.0):
    saldo = start_saldo
    for montag in sorted(wochen.keys()):
        saldo += wochen[montag].diff
        wochen[montag].saldo = round(saldo, 5)
    return wochen


def run_auswertung(
    *,
    pdf_datei: str,
    startdatum: str,
    sollstunden: float,
    start_saldo: float,
    zeitmodelle_liste=None,
    feiertags_zuschlag_faktor: float = 1.0,
) -> dict:
    pdf_path = Path(pdf_datei)
    if not pdf_path.exists():
        raise FileNotFoundError("PDF-Ordner nicht gefunden.")
    start = parse_date_ddmmYYYY(startdatum)
    if start.weekday() != 0:
        raise ValueError("Startdatum muss ein Montag sein.")

    tages_ist = lade_tages_ist_aus_pdf_ordner(pdf_path)
    raw = lade_abwesenheiten_raw()
    urlaub, feiertage, krankheit, arzttermine = baue_abwesenheiten_core(raw)
    auszahlungen_raw = raw.get("auszahlungen_raw", {})

    start_montag = start - timedelta(days=start.weekday())
    wochen = baue_wochen_aus_tagen(tages_ist)

    max_pdf_datum = max(tages_ist.keys()) if tages_ist else start_montag
    for pdf_file in sorted(Path(pdf_datei).glob("*.pdf")):
        match = re.search(r"(\d{4})\s+(\d{2})\s+(\d{2})", pdf_file.stem)
        if match:
            y, m, d = map(int, match.groups())
            try:
                dat = date(y, m, d)
                if dat > max_pdf_datum:
                    max_pdf_datum = dat
            except ValueError:
                pass

    wochen = ergaenze_fehlende_wochen(wochen, start_montag, max_pdf_datum)

    # wochen = ergaenze_fehlende_wochen(
    #     wochen, start_montag, max(tages_ist.keys()) if tages_ist else start_montag
    # )

    ergaenze_wochen_um_soll_und_gutschriften(
        wochen=wochen,
        soll_wochenstunden=float(sollstunden),
        urlaub=urlaub,
        feiertage=feiertage,
        krankheit=krankheit,
        arzttermine=arzttermine,
        zeitmodelle_liste=zeitmodelle_liste,
        feiertags_zuschlag_faktor=feiertags_zuschlag_faktor,  # <-- nur dieser Parameter wird verwendet!
    )

    # Auszahlungen anwenden
    auszahlungen_pro_woche: dict[date, dict[str, float]] = {}
    for iso, kat_dict in auszahlungen_raw.items():
        montag_von_iso = datetime.strptime(iso, "%Y-%m-%d").date()
        montag_von_iso = montag_von_iso - timedelta(days=montag_von_iso.weekday())
        auszahlungen_pro_woche[montag_von_iso] = kat_dict
    wende_auszahlung_an(wochen, auszahlungen_pro_woche)

    berechne_saldo(wochen, start_saldo)

    # Saldo der letzten Woche zurückgeben
    if wochen:
        letzter_montag = max(wochen.keys())
        gesamt_saldo = wochen[letzter_montag].saldo
    else:
        gesamt_saldo = start_saldo

    return {
        "wochen": wochen,
        "saldo": gesamt_saldo,
        "auszahlungen": auszahlungen_pro_woche,
    }
