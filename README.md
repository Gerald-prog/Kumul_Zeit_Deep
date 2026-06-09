# Zeit-Manager

Eine lokale Anwendung zur Auswertung von PDF-Zeitkalendern und Verwaltung
von Arbeitszeitkonten.

## Features

- **PDF‑Import**: Liest automatisch alle PDF‑Zeitkalender in einem Ordner ein
  (unterstützt gespiegelte Texte).
- **Wochenübersicht**: Zeigt Ist, Soll, Differenz und kumulierten Saldo pro Woche.
- **Feiertagsarbeit**: Erkennt gesetzliche Feiertage (nach Bundesland) und
  bietet einen FT+‑Button für tatsächlich gearbeitete Feiertage (inkl. Zuschlag).
- **Abwesenheiten**: Urlaub, Krankheit (mit Teilarbeit), Arzttermine (§616 BGB)
  reduzieren das Soll und schonen den Überstunden‑Saldo.
- **Arbeitszeitmodelle**: Historienbasierte Modelle für Teilzeit oder geänderte
  Arbeitszeiten – jedes Modell ist einem Zeitraum zugeordnet.
- **Jahresfilter**: Automatischer Saldo‑Vortrag beim Wechsel des Anzeigejahres.
- **PDF‑Export**: Erzeugt eine druckbare Tabelle des aktuellen Jahres.
- **Dunkles Design**: Durchgängiges dunkles Farbschema für angenehmes Arbeiten.
- **Lokal & offline**: Alle Daten bleiben auf dem eigenen Rechner, kein Cloud‑Zwang.

## Technische Basis

- Python 3.13
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) für die GUI
- [pdfplumber](https://github.com/jsvine/pdfplumber) für PDF‑Extraktion
- [holidays](https://github.com/vacanza/python-holidays) für Feiertage
- [tkcalendar](https://github.com/j4321/tkcalendar) für Datumsauswahl
- [Pillow](https://python-pillow.org/) für Icon‑Einbindung
- [fpdf2](https://pyfpdf.github.io/fpdf2/) für PDF‑Export
- Datenhaltung in lokalen JSON‑Dateien (`config.json`, `abwesenheiten.json`)
- Berechnungslogik komplett in Python, wochenbasiert mit Gutschriften‑System

## Keine Features (bewusste Einschränkungen)

- Keine Mehrbenutzerverwaltung (ein Programm = ein Arbeitszeitkonto).
- Keine automatische Synchronisation mit Zeiterfassungssystemen.
- Keine Gehaltsabrechnung – reines Arbeitszeitkonto.

## Geplante Erweiterungen

- Mitarbeiter-Pool mit SQLite-Datenbank (für Teamleiter).
- Weitere Zuschlagsarten (Nacht, Sonntag, …).
- Grafische Auswertung (Stunden-Visualisierung).
- Export als Excel/CSV.

## Installation & Start

```bash
git clone https://github.com/Gerald-prog/Kumul_Zeit_Deep
cd KUMUL_ZEIT_DEEP
pip install -r requirements.txt
python ui_desktop.py  
