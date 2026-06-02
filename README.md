# Solera Zeit-Manager

Eine lokale Anwendung zur Auswertung von PDF-Zeitkalendern und Verwaltung
von Arbeitszeitkonten – entwickelt für Gerald Günther und seine Kollegen.

## Features

- **PDF-Import**: Liest automatisch alle PDF-Zeitkalender in einem Ordner ein.
- **Wochenübersicht**: Zeigt Ist, Soll, Differenz und kumulierten Saldo pro Woche.
- **Feiertagsarbeit**: Erkennt gesetzliche Feiertage (nach Bundesland) und
  bietet einen FT+-Button für tatsächlich gearbeitete Feiertage (inkl. Zuschlag).
- **Abwesenheiten**: Urlaub, Krankheit (mit Teilarbeit), Arzttermine (§616 BGB)
  reduzieren das Soll und schonen den Überstunden-Saldo.
- **Arbeitszeitmodelle**: Historienbasierte Modelle für Teilzeit oder geänderte
  Arbeitszeiten – jedes Modell ist einem Zeitraum zugeordnet.
- **Jahresfilter**: Automatischer Saldo-Vortrag beim Wechsel des Anzeigejahres.
- **Lokal & offline**: Alle Daten bleiben auf dem eigenen Rechner, kein Cloud-Zwang.

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

### Variante A – Quellcode (Entwickler)

```bash
git clone <https://github.com/Gerald-prog/Kumul_Zeit_Deep>
cd KUMUL_ZEIT_DEEP
pip install -r requirements.txt
python ui_desktop.py  
