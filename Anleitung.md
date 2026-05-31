
# Solera Zeit-Manager – Bedienungsanleitung

## Einführung

Der Solera Zeit-Manager wertet PDF‑Zeitkalender aus, berechnet Ihre Arbeitszeit und erfasst Überstunden. Abwesenheiten wie Urlaub, Krankheit, Feiertage und Arzttermine werden automatisch berücksichtigt und korrigieren das Soll. Die Anwendung läuft lokal auf Ihrem Rechner – es werden keine Daten in die Cloud übertragen oder auf Servern gespeichert.

---

## Starten des Programms

Laden Sie die bereitgestellte `.exe`‑Datei herunter und legen Sie sie in einem eigenen Ordner ab (zum Beispiel `D:\Zeiterfassung`). Ein Doppelklick auf `Solera_Zeit_Manager.exe` startet das Programm sofort – eine separate Installation von Python oder zusätzlichen Paketen ist nicht erforderlich. Beim ersten Start legt die Anwendung automatisch eine `config.json` und eine `abwesenheiten.json` an. In diesen beiden Dateien werden Ihre Einstellungen und Abwesenheiten dauerhaft gespeichert.

---

## Erste Schritte

Nach dem Start sehen Sie die Hauptoberfläche mit einem Einstellungsbereich und mehreren Registerkarten (Wochenübersicht, Urlaub, Krankheit, Arzttermine, Arbeitszeitmodelle).

**PDF-Ordner wählen**  
Klicken Sie auf die Schaltfläche „Ordner wählen“ und navigieren Sie zu dem Verzeichnis, in dem Ihre PDF‑Zeitkalender liegen. Bestätigen Sie mit „Ordner auswählen“. Der Pfad erscheint danach im Eingabefeld.

**Start-Montag setzen**  
Im Feld „Start-Montag“ tragen Sie das Datum des ersten auszuwertenden Montags ein, zum Beispiel `07.07.2025`. Alternativ können Sie über die Jahres‑Auswahlliste direkt das gewünschte Jahr wählen – der Start-Montag springt dann automatisch auf den ersten Montag dieses Jahres.

**Soll‑Wochenstunden und Saldo‑Vortrag**  
Unter „Soll-Stunden/Woche“ geben Sie Ihre vertragliche Wochenarbeitszeit an, üblicherweise `40.0`. Das Feld „Saldo-Vortrag“ ist nur im ersten Jahr relevant, falls Sie bereits einen Überstunden‑Saldo aus der Zeit vor der Nutzung des Programms haben. In allen späteren Jahren wird der Vortrag automatisch aus der letzten Woche des Vorjahres berechnet und hier nicht mehr manuell verändert.

**Übernehmen & Speichern**  
Klicken Sie auf „Übernehmen & Speichern“. Die Anwendung speichert Ihre Einstellungen, liest alle PDF‑Dateien im gewählten Ordner ein und zeigt die erste Auswertung an.

---

## Die Wochenübersicht

In der Registerkarte „Wochenübersicht“ sehen Sie für jede Kalenderwoche eine Zeile, die von Montag bis Sonntag reicht. Ganz links steht das Datum des Montags, gefolgt von den tatsächlich gearbeiteten Stunden (Ist) und dem vertraglichen Soll. Die Differenz (Ist minus Soll) wird grün bei Plusstunden und rot bei Minderstunden dargestellt. Ganz rechts sehen Sie den kumulierten Saldo – also die Summe aller Differenzen bis einschließlich dieser Woche.

**Feiertags‑Button (FT+)**  
Wenn Sie an einem Feiertag gearbeitet haben, erscheint ein blauer Knopf mit der Beschriftung `FT+`. Die angezeigte Stundenzahl umfasst sowohl die tatsächlich geleistete Arbeitszeit als auch den konfigurierten Feiertagszuschlag.

Mit einem Klick auf `FT+` zahlen Sie diese Stunden aus – sie werden vom Saldo abgezogen. Der Knopf wird orange und zeigt den ausgezahlten Betrag mit einem Häkchen an. Möchten Sie die Auszahlung rückgängig machen, klicken Sie erneut auf den Knopf. Die Stunden werden dann wieder dem Saldo gutgeschrieben. Der FT+‑Knopf erscheint nur dann, wenn an einem Feiertag tatsächlich gearbeitet wurde; für freie Feiertage wird kein Button angeboten.

---

## Abwesenheiten eintragen

Die Anwendung unterscheidet drei Arten von Abwesenheiten, die Sie in den entsprechenden Registerkarten eintragen können. Alle Abwesenheiten reduzieren das Soll und schonen so Ihren Überstunden‑Saldo.

**Urlaub**  
In der Registerkarte „Urlaub“ geben Sie das Start‑ und das Enddatum Ihres Urlaubs ein und klicken auf „Urlaub speichern“. Der Zeitraum wird in der Liste darunter angezeigt und kann dort auch wieder gelöscht werden. Urlaubstage erhalten kein Soll und kein Ist – es entsteht keine künstliche Überzeit.

**Krankheit**  
In der Registerkarte „Krankheit“ erfassen Sie den Zeitraum Ihrer Krankmeldung. Haben Sie an einem Krankheitstag teilweise gearbeitet, können Sie die geleisteten Stunden im Feld „Trotzdem gearbeitet“ eintragen. Die App setzt das Soll für diesen Tag auf die tatsächliche Arbeitszeit, sodass keine zusätzliche Überzeit entsteht. Volle Krankheitstage ohne Arbeitsleistung reduzieren das Soll auf null.

**Arzttermine**  
In der Registerkarte „Arzttermine“ tragen Sie das Datum des Arztbesuchs und die voraussichtliche Dauer in Stunden ein (zum Beispiel `2.5` für zweieinhalb Stunden). Das Tagesoll wird um diese Dauer reduziert, jedoch nie unter null. Auch hier können Sie Einträge über den „Löschen“‑Knopf entfernen.

---

## Arbeitszeitmodelle verwalten

Die Registerkarte „Arbeitszeit‑Modelle“ erlaubt es Ihnen, verschiedene Arbeitszeitmodelle für unterschiedliche Zeiträume zu hinterlegen. Das ist vor allem bei Teilzeit oder geänderten Arbeitszeiten nützlich.

Wählen Sie ein Startdatum im Format `JJJJ‑MM‑TT`, das Bundesland für die Feiertagsberechnung und die täglichen Soll‑Stunden für jeden Wochentag. Klicken Sie auf „Neues Modell speichern“. Die Anwendung verwendet für jeden berechneten Tag automatisch das passende Modell, sodass auch rückwirkende Änderungen korrekt berücksichtigt werden. Gespeicherte Modelle erscheinen in der Liste unterhalb der Eingabe und können dort auch wieder gelöscht werden.

---

## Jahreswechsel und automatischer Saldo‑Vortrag

Die App wertet alle PDFs im angegebenen Ordner aus, auch wenn sie mehrere Jahre umfassen. Mit der Jahres‑Auswahlliste im oberen Bereich wechseln Sie das Anzeigejahr.

Sobald Sie ein neues Jahr auswählen, springt das Start‑Montag‑Feld automatisch auf den ersten Montag dieses Jahres. Gleichzeitig berechnet die Anwendung den Saldo aus der letzten Woche des Vorjahres und trägt ihn als Saldo‑Vortrag ein – Sie müssen also nichts manuell übertragen. Wenn Sie dennoch ein anderes Startdatum wünschen, können Sie es von Hand ändern und mit „Übernehmen & Speichern“ bestätigen. Der Vortrag wird dann entsprechend neu berechnet.

---

## Feiertage und Zuschläge

Über die Bibliothek `holidays` kennt die App die gesetzlichen Feiertage aller Bundesländer. Die Zuordnung erfolgt über das im Arbeitszeitmodell angegebene Bundesland. Zusätzlich können Sie in der Datei `abwesenheiten.json` manuelle Feiertage hinterlegen, beispielsweise Betriebsruhetage.

Den Feiertagszuschlag konfigurieren Sie zentral in der Datei `config.json` unter dem Abschnitt `zuschlaege` und dem Schlüssel `feiertag`. Der Standardwert `1.25` bedeutet einen Zuschlag von 25 Prozent auf die tatsächlich gearbeiteten Stunden. Möchten Sie einen höheren oder niedrigeren Zuschlag, passen Sie diesen Wert einfach an.

An einem freien Feiertag erhalten Sie kein Soll und keine zusätzliche Gutschrift – der Saldo bleibt unverändert. An einem gearbeiteten Feiertag hingegen wird das Soll auf null gesetzt, die geleistete Arbeitszeit zuzüglich des Zuschlags gutgeschrieben und als FT+ ausgewiesen. Nur diese tatsächliche Feiertagsarbeit ist auszahlbar.

---

## Hinweise für den Alltag

Neue PDF‑Dateien, die Sie in den Zeiterfassungsordner legen, werden beim nächsten Klick auf „Aktualisieren“ (der blaue Knopf neben den Einstellungen) oder auf „Übernehmen & Speichern“ eingelesen. Sie müssen das Programm dafür nicht neu starten.

Alle Einstellungen mit Ausnahme der Abwesenheiten speichert die App in der Datei `config.json`. Ihre Abwesenheiten (Urlaub, Krankheit, Arzttermine) werden in der Datei `abwesenheiten.json` abgelegt. Beide Dateien befinden sich im selben Ordner wie die `.exe`‑Datei und sollten nicht manuell gelöscht werden.

---

## Verknüpfungen erstellen (Desktop, Taskleiste, Startmenü)  

Da das Programm ohne Installation auskommt, müssen Sie Verknüpfungen manuell anlegen. Das ist in wenigen Schritten erledigt.

## Desktop-Verknüpfung  

Klicken Sie mit der rechten Maustaste auf die .exe-Datei.
Wählen Sie Senden an → Desktop (Verknüpfung erstellen).
Auf Ihrem Desktop erscheint ein Symbol, mit dem Sie das Programm direkt starten können.

## Taskleiste  

Starten Sie das Programm mit einem Doppelklick auf die .exe-Datei.
Sobald das Programmfenster geöffnet ist, klicken Sie mit der rechten Maustaste auf das Programmsymbol in der Taskleiste.
Wählen Sie An Taskleiste anheften.
Das Symbol bleibt nun dauerhaft in der Taskleiste – auch nachdem Sie das Programm beendet haben.

## Startmenü (optional)  

Drücken Sie Windows + R, geben Sie shell:start menu ein und bestätigen Sie mit Enter.
Der Ordner „Startmenü“ öffnet sich. Ziehen Sie mit der rechten Maustaste die .exe-Datei in diesen Ordner und wählen Sie Verknüpfung hier erstellen.
Alternativ können Sie die zuvor erstellte Desktop-Verknüpfung in diesen Ordner kopieren.
Das Programm erscheint nun im Startmenü unter „Alle Apps“ und kann von dort gestartet werden.

**Hinweis:** Wenn Sie das Programm später an einen anderen Ort verschieben, müssen Sie die Verknüpfungen erneut anlegen, da sie sonst ins Leere zeigen.

## Fehlerbehebung

Sollte die App nach dem Start keine Daten anzeigen, überprüfen Sie bitte, ob der eingestellte PDF‑Ordner existiert und tatsächlich `.pdf`‑Dateien enthält. Klicken Sie dann auf „Aktualisieren“. In der Konsole (das schwarze Fenster, das sich zusammen mit der App öffnet) können Sie sehen, ob PDFs gefunden werden und ob Stunden extrahiert werden konnten.

Zeigt die Wochenübersicht ein falsches Soll an, kontrollieren Sie Ihre Arbeitszeitmodelle und das eingestellte Startdatum. Oft sind für den betroffenen Zeitraum noch Abwesenheiten eingetragen, die das Soll reduzieren.

Wenn der FT+‑Knopf nicht erscheint, obwohl Sie an einem Feiertag gearbeitet haben, prüfen Sie, ob der Feiertag korrekt erkannt wurde. Die App zeigt in der Zeile jeder Woche die erkannten Feiertage mit Datum und Name an. Fehlt ein Feiertag, können Sie ihn manuell in der `abwesenheiten.json` ergänzen.

---

## Lizenz

Dieses Programm ist Open Source und steht unter der MIT‑Lizenz. Den vollständigen Lizenztext finden Sie in der Datei `LICENSE`. Die Lizenzen der verwendeten Bibliotheken sind in der Datei `LICENSE_INFO.txt` aufgeführt.

---

## Kontakt

Gerald Günther – <graffiter.prog@gmail.com>  
