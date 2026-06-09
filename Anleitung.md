# Solera Zeit-Manager – Bedienungsanleitung

## Einführung

Der Solera Zeit-Manager wertet PDF‑Zeitkalender aus, berechnet Ihre Arbeitszeit und erfasst Überstunden.
Abwesenheiten wie Urlaub, Krankheit, Feiertage und Arzttermine werden automatisch berücksichtigt
und korrigieren das Soll. Die Anwendung läuft lokal auf Ihrem Rechner – es werden keine Daten
in die Cloud übertragen oder auf Servern gespeichert.

---

## Programmstart

Laden Sie die bereitgestellte `.exe`‑Datei herunter und legen Sie sie in einem eigenen Ordner ab
(zum Beispiel `D:\Zeiterfassung`). Ein Doppelklick auf `Solera_Zeit_Manager.exe` startet das Programm
sofort – eine Installation ist nicht erforderlich. Beim ersten Start werden automatisch die
erforderlichen Konfigurationsdateien angelegt.

---

## Erste Schritte

Nach dem Start sehen Sie die Hauptoberfläche. Im oberen Bereich befinden sich die **Einstellungen**,
darunter die Registerkarten (**Wochenübersicht**, **Urlaub**, **Krankheit**, **Arzttermine**,
**Arbeitszeit-Modelle**). Ganz unten im Fenster wird der aktuelle Gesamtsaldo angezeigt,
rechts unten Ihr Copyright‑Hinweis.

### PDF‑Ordner wählen

Klicken Sie auf die Schaltfläche **Ordner wählen** (untereinander mit den anderen Buttons in der
rechten Spalte). Navigieren Sie zu dem Verzeichnis, in dem Ihre PDF‑Zeitkalender liegen,
und bestätigen Sie mit **Ordner auswählen**. Der Pfad erscheint dann im Eingabefeld.
Solange noch kein Ordner gewählt wurde, steht dort als Platzhalter **„Bitte Ordner wählen“**.

### Start‑Montag setzen

Das Feld **Start‑Montag** zeigt den ersten auszuwertenden Montag an. Wenn Sie das Programm zum
ersten Mal starten, wird automatisch der erste Montag des aktuellen Jahres eingetragen.
Sie können das Datum auch manuell ändern (Format `TT.MM.JJJJ`) oder über die
**Jahres‑Auswahlliste** das gewünschte Jahr wählen – der Start‑Montag springt dann automatisch
auf den ersten Montag dieses Jahres.

### Name eintragen

Rechts neben der Jahres‑Auswahlliste finden Sie das Feld **Name**. Tragen Sie hier Ihren
Namen ein – er wird in der Copyright‑Anzeige und in exportierten PDFs verwendet.

### Soll‑Wochenstunden und Saldo‑Vortrag

Unter **Soll-Stunden/Woche** geben Sie Ihre vertragliche Wochenarbeitszeit an, üblicherweise `40.0`.
Das Feld **Saldo-Vortrag** wird automatisch aus der letzten Woche des Vorjahres berechnet;
eine manuelle Eingabe ist im ersten Jahr oder bei Sonderfällen möglich.

### Übernehmen & Speichern

Klicken Sie auf **Übernehmen & Speichern**, um Ihre Einstellungen zu sichern und die erste
Auswertung zu starten. Die Wochenliste wird jetzt gefüllt.

---

## Die Wochenübersicht

In der Registerkarte **Wochenübersicht** sehen Sie für jede Kalenderwoche eine Zeile.
Links steht das Datum des Montags, gefolgt von den tatsächlich gearbeiteten Stunden (Ist),
dem vertraglichen Soll, der Differenz (grün bei Plusstunden, rot bei Minderstunden) und
ganz rechts dem kumulierten Saldo.

In Zeilen mit erkannten Feiertagen sehen Sie ein kleines Kalender‑Icon und die Namen der
Feiertage. Wenn Sie an einem Feiertag **tatsächlich gearbeitet** haben, erscheint zusätzlich
ein blauer **FT+‑Button**. Er zeigt die gesamte Feiertagsarbeit inklusive des Zuschlags an.

- **Auszahlung:** Klick auf den FT+‑Button zieht die Stunden vom Saldo ab (Button wird orange).
- **Rücknahme:** Ein erneuter Klick bucht die Stunden wieder ein (Button wird wieder blau).

Der FT+‑Button erscheint nur für gearbeitete Feiertage; für freie Feiertage gibt es keine
auszahlbaren Stunden.

---

## Abwesenheiten eintragen

In den Registerkarten **Urlaub**, **Krankheit** und **Arzttermine** können Sie Ihre
Abwesenheiten erfassen. Alle Einträge reduzieren das Soll und schonen so Ihren
Überstunden‑Saldo.

### Urlaub

- Tragen Sie Von‑ und Bis‑Datum ein (Bis ist optional, für einzelne Tage einfach Von ausfüllen).
- Klicken Sie auf **Urlaub speichern**.
- Urlaubstage bekommen Soll = 0 und Ist = 0 – es entsteht keine künstliche Überzeit.

### Krankheit

- Erfassen Sie den Zeitraum mit Von‑ und Bis‑Datum.
- Falls Sie an einem Krankheitstag teilweise gearbeitet haben, geben Sie die tatsächlichen
  Stunden im Feld **Trotzdem gearbeitet (h)** ein.
- Die App setzt das Soll für diesen Tag auf die tatsächliche Arbeitszeit, sodass keine
  zusätzliche Überzeit entsteht.

### Arzttermine

- Geben Sie das Datum und die Dauer in Stunden ein (z. B. `2.5` für zweieinhalb Stunden).
- Das Tagesoll wird um diese Dauer reduziert (mindestens 0 h).

Alle Einträge können Sie in der jeweiligen Liste durch Klick auf **Löschen** wieder entfernen.

---

## Arbeitszeitmodelle

In der Registerkarte **Arbeitszeit‑Modelle** können Sie unterschiedliche Wochenmodelle
hinterlegen – sinnvoll bei Teilzeit oder geänderten Arbeitszeiten.

- **Ab Datum:** Legt den Gültigkeitsbeginn des Modells fest (Format `JJJJ-MM-TT`).
- **Bundesland:** Wählen Sie Ihr Bundesland für die Feiertagsberechnung.
- **Tägliche Soll‑Stunden:** Geben Sie für jeden Wochentag die vertragliche Arbeitszeit ein.
- Klicken Sie auf **Neues Modell speichern**. Das Modell erscheint in der Liste und wird
  automatisch für alle Berechnungen ab dem Startdatum verwendet.

Gespeicherte Modelle lassen sich über den **Löschen**‑Button entfernen.

---

## Jahreswechsel und Saldo‑Vortrag

Die App wertet **alle** PDFs im gewählten Ordner aus, auch über mehrere Jahre hinweg.
Über die **Jahres‑Auswahlliste** wechseln Sie das Anzeigejahr.

- Der **Start‑Montag** wird automatisch auf den ersten Montag des Jahres gesetzt.
- Das Feld **Saldo‑Vortrag** wird automatisch mit dem Saldo aus der letzten Woche des
  Vorjahres gefüllt (wenn vorhanden). Ein manueller Eintrag ist nur im allerersten Jahr nötig.

Wenn Sie ein bestimmtes Startdatum wünschen, können Sie es von Hand ändern und mit
**Übernehmen & Speichern** bestätigen.

---

## Feiertage und Zuschläge

Die App erkennt die gesetzlichen Feiertage aller Bundesländer (via `holidays`).  
Das verwendete Bundesland bestimmt das im Arbeitszeitmodell hinterlegte Land.

Der Feiertagszuschlag wird in der Datei `config.json` unter `zuschlaege` → `feiertag` konfiguriert
(Standard: `2.25` = 125 % Zuschlag). Diese Einstellung kann bei Bedarf angepasst werden.

- **Freier Feiertag:** Soll = 0, keine Gutschrift → Saldo bleibt unverändert.
- **Gearbeiteter Feiertag:** Soll = 0, Ist aus PDF + Zuschlag werden als FT+ ausgewiesen
  und sind auszahlbar.

---

## PDF-Export für das Arbeitszeitkonto

Unter dem Button **Übernehmen & Speichern** finden Sie die Schaltfläche **PDF erstellen**.
Ein Klick erzeugt eine druckbare Tabelle mit allen Wochen des aktuell angezeigten Jahres
(inklusive Ist, Soll, Differenz, Saldo und Feiertagen). Das PDF wird automatisch geöffnet
und kann gespeichert oder ausgedruckt werden – ideal für Ihre Papierakte.

---

## Tipps für den Alltag

- **Neue PDFs** hinzufügen? Legen Sie die Dateien einfach in den PDF‑Ordner und klicken Sie
  erneut auf **Übernehmen & Speichern**. Die App liest alle PDFs neu ein und aktualisiert die
  Anzeige.
- Das Programm muss nicht neu gestartet werden – nach dem Speichern ist die Anzeige sofort aktuell.
- Ihre Einstellungen werden in der Datei `config.json` gespeichert, Abwesenheiten in
  `abwesenheiten.json`. Beide Dateien liegen im Programmordner und sollten nicht manuell gelöscht werden.

---

## Fehlerbehebung

**Die App zeigt „Bitte zuerst einen PDF-Ordner wählen“ an?**  
Wählen Sie einen gültigen Ordner mit Ihren PDF‑Zeitkalendern aus.

**Keine Daten sichtbar?**  
Prüfen Sie, ob der gewählte Ordner `.pdf`‑Dateien enthält und klicken Sie auf
**Übernehmen & Speichern**.

**Soll‑Stunden falsch?**  
Kontrollieren Sie die Arbeitszeitmodelle und eingetragene Abwesenheiten für den Zeitraum.

**FT+‑Button fehlt trotz Feiertag?**  
Der Button erscheint nur, wenn an dem Feiertag tatsächlich gearbeitet wurde (laut PDF).
Feiertage, an denen Sie frei hatten, zeigen kein FT+.

---

## Lizenz

Dieses Programm ist Open Source und steht unter der **MIT‑Lizenz**.  
Den vollständigen Lizenztext finden Sie in der Datei `LICENSE`.  
Die Lizenzen der verwendeten Bibliotheken sind in `LICENSE_INFO.txt` aufgeführt.

---

## Kontakt

Gerald Günther – <graffiter.prog@gmail.com>  
