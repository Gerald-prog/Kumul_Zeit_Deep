import sys
from pathlib import Path
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import date, datetime, timedelta
import json
import logging

from abwesenheiten import (
    lade_abwesenheiten_raw,
    speichere_abwesenheiten_raw,
    speichere_auszahlung,
)
from core_logic import run_auswertung
from config import lade_config, speichere_config
from models import WochenDaten
from feiertage import BUNDESLAENDER
from tkcalendar import DateEntry
import ctypes

logging.basicConfig(level=logging.INFO)


class WochenZeile(ctk.CTkFrame):
    def __init__(
        self, master, montag, daten: WochenDaten, on_update_callback, **kwargs
    ):
        super().__init__(master, **kwargs)
        self.montag = montag
        self.on_update_callback = on_update_callback

        # --- Datum/KW ---
        self.lbl_datum = ctk.CTkLabel(
            self, text=f"KW ab {montag.strftime('%d.%m.%Y')}", width=140
        )
        self.lbl_datum.pack(side="left", padx=10)

        # --- Ist/Soll ---
        ist = daten.ist_stunden
        soll = daten.soll_stunden
        self.lbl_werte = ctk.CTkLabel(
            self, text=f"Ist: {ist:.2f}h | Soll: {soll:.2f}h", width=220
        )
        self.lbl_werte.pack(side="left", padx=10)

        # --- Differenz ---
        diff = daten.diff
        color = "#4ADE80" if diff >= 0 else "#F87171"
        self.lbl_diff = ctk.CTkLabel(
            self,
            text=f"Diff: {diff:+.2f}",
            text_color=color,
            font=("Roboto", 12, "bold"),
            width=90,
        )
        self.lbl_diff.pack(side="left", padx=10)

        # --- Feiertagsanzeige (zwischen Diff und rechten Elementen) ---
        if daten.feiertags_namen:
            feiertags_text = "  📅 " + ",  ".join(daten.feiertags_namen)
            self.lbl_feiertage = ctk.CTkLabel(
                self,
                text=feiertags_text,
                font=("Roboto", 12),
                text_color="gray70",
                anchor="w",
            )
            self.lbl_feiertage.pack(side="left", padx=10)

        # --- Saldo (ganz rechts) ---
        self.lbl_saldo = ctk.CTkLabel(
            self, text=f"Σ {daten.saldo:.2f}", width=100, anchor="e"
        )
        self.lbl_saldo.pack(side="right", padx=(0, 15))

        # --- Nur FT+ Button, wenn an Feiertag gearbeitet wurde ---
        if daten.feiertag_zuschlag_gutschrift > 0:
            bereits_ausgezahlt = daten.feiertag_zuschlag_ausbezahlt
            if bereits_ausgezahlt > 0:
                btn_text = f"FT+ ✓ -{bereits_ausgezahlt:.1f}"
                btn_color = "#F59E0B"
                hover_color = "#D97706"
                command = lambda: on_update_callback(montag, 0.0, "feiertag_zuschlag")
            else:
                btn_text = f"FT+ {daten.feiertag_zuschlag_gutschrift:.1f}"
                btn_color = "#3B82F6"
                hover_color = "#2563EB"
                command = lambda: on_update_callback(
                    montag, daten.feiertag_zuschlag_gutschrift, "feiertag_zuschlag"
                )

            btn = ctk.CTkButton(
                self,
                text=btn_text,
                width=80,
                fg_color=btn_color,
                hover_color=hover_color,
                command=command,
            )
            btn.pack(side="right", padx=3)


class ZeiterfassungApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Solera Zeit-Manager")
        self.geometry("900x800")
        self.cfg = lade_config()

        # --- Icon setzen (Taskleiste + Fenster) ---
        try:
            # Basisverzeichnis (Entwicklung oder PyInstaller)
            if getattr(sys, "frozen", False):
                base_dir = Path(getattr(sys, "_MEIPASS"))
            else:
                base_dir = Path(__file__).parent

            # Icon-Dateiname aus config.json, Fallback auf "mein_icon.ico"
            icon_name = self.cfg.get("icon", "mein_icon.ico") or "mein_icon.ico"

            # Automatische Endung, falls keine angegeben
            if not icon_name.lower().endswith((".ico", ".png")):
                icon_name += ".ico" if sys.platform.startswith("win") else ".png"

            ico_path = base_dir / icon_name

            # 1. Für Windows: AppUserModelID setzen (wichtig für Taskleiste)
            if sys.platform.startswith("win"):
                # Eindeutige ID – du kannst "SoleraZeitManager" durch deinen Wunschnamen ersetzen
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "SoleraZeitManager"
                )

            # 2. Icon-Datei laden und sowohl in der Titelleiste als auch Taskleiste setzen
            if ico_path.exists():
                # a) .ico für Windows-Titelleiste setzen
                if sys.platform.startswith("win") and icon_name.endswith(".ico"):
                    self.iconbitmap(default=str(ico_path))

                # b) Zusätzlich als PhotoImage für die Taskleiste (funktioniert plattformübergreifend)
                pil_img = Image.open(str(ico_path))
                # Für .ico-Dateien nehmen wir das erste eingebettete Bild
                if icon_name.endswith(".ico"):
                    pil_img = pil_img.resize((64, 64))  # Größe anpassen, falls nötig
                photo = ImageTk.PhotoImage(Image=pil_img)
                self.iconphoto(
                    True, photo  # type: ignore[reportArgumentType] <- Kommentierung notwendig
                )
                # True = setzt es als Standard-Icon für alle Fenster
                # photo-> type: ignore[reportArgumentType] Inkombatilität zwischen tkinter und pillow

                print(f"✅ Icon erfolgreich geladen: {ico_path}")
            else:
                print(f"⚠️ Icon nicht gefunden: {ico_path}")

        except Exception as e:
            print(f"❌ Fehler beim Laden des Icons: {e}")

        self.aktuelles_jahr = self.cfg.get("aktuelles_jahr", date.today().year)
        self.setup_ui()
        self.setze_jahr(self.aktuelles_jahr)  # Startet mit dem gespeicherten Jahr
        self.focus_set()
        self.bind("<F5>", lambda event: self.load_and_refresh)

    def create_date_entry(self, master, initial_date=None, **kwargs):
        """Erstellt ein DateEntry-Widget mit einheitlichem Format."""
        if initial_date is None:
            initial_date = date.today()
        elif isinstance(initial_date, str):
            initial_date = datetime.strptime(initial_date, "%d.%m.%Y").date()

        de = DateEntry(
            master,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd.MM.yyyy",  # Deutsches Format
            year=initial_date.year,
            month=initial_date.month,
            day=initial_date.day,
            **kwargs,
        )
        return de

    def setup_ui(self):
        # Einstellungsbereich
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(fill="x", padx=20, pady=10)
        self.settings_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.settings_frame, text="PDF-Ordner:", font=("Roboto", 12, "bold")
        ).grid(row=0, column=0, padx=10, pady=10)
        self.entry_ordner = ctk.CTkEntry(self.settings_frame, width=400)
        self.entry_ordner.insert(0, self.cfg.get("ordner", ""))
        self.entry_ordner.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        ctk.CTkButton(
            self.settings_frame, text="Ordner wählen", command=self.choose_folder
        ).grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkLabel(
            self.settings_frame, text="Start-Montag:", font=("Roboto", 12, "bold")
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_start = self.create_date_entry(  # ctk.CTkEntry(self.settings_frame)
            self.settings_frame,
            initial_date=self.cfg.get("start_montag", f"01.01.{date.today().year}"),
        )

        # self.entry_start.insert(
        #     0, self.cfg.get("start_montag", f"01.01.{date.today().year}")
        # )
        self.entry_start.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(
            self.settings_frame, text="Jahr:", font=("Roboto", 12, "bold")
        ).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.combo_jahr = ctk.CTkComboBox(
            self.settings_frame, values=[str(y) for y in range(2025, 2031)]
        )
        self.combo_jahr.set(str(self.aktuelles_jahr))
        self.combo_jahr.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.combo_jahr.configure(command=self.on_jahr_changed)

        ctk.CTkLabel(
            self.settings_frame, text="Soll-Stunden/Woche:", font=("Roboto", 12, "bold")
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_soll = ctk.CTkEntry(self.settings_frame, width=60)
        self.entry_soll.insert(0, str(self.cfg.get("soll_wochenstunden", 40)))
        self.entry_soll.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(
            self.settings_frame, text="Saldo-Vortrag (h):", font=("Roboto", 12, "bold")
        ).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_vortrag = ctk.CTkEntry(self.settings_frame, width=60)
        self.entry_vortrag.insert(0, str(self.cfg.get("start_saldo", 0.0)))
        self.entry_vortrag.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.btn_save_settings = ctk.CTkButton(
            self.settings_frame,
            text="Übernehmen & Speichern",
            fg_color="green",
            command=self.save_and_reload,
        )
        self.btn_save_settings.grid(row=1, column=2, padx=10, pady=10)

        # Footer
        self.footer = ctk.CTkFrame(self, height=60)
        self.footer.pack(fill="x", side="bottom", padx=20, pady=20)
        self.lbl_gesamt_saldo = ctk.CTkLabel(
            self.footer, text="Gesamt-Saldo: --", font=("Roboto", 18, "bold")
        )
        self.lbl_gesamt_saldo.pack(side="left", padx=20)

        # Tabs
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        self.tab_uebersicht = self.tabs.add("Wochenübersicht")
        self.tab_urlaub = self.tabs.add("Urlaub")
        self.tab_krank = self.tabs.add("Krankheit")
        self.tab_arzt = self.tabs.add("Arzttermine")
        self.tab_modelle = self.tabs.add("Arbeitszeit-Modelle")

        self.scroll_frame = ctk.CTkScrollableFrame(
            self.tab_uebersicht, width=1050, height=450
        )
        self.scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.setup_urlaub_tab()
        self.setup_krankheit_tab()
        self.setup_arzt_tab()
        self.setup_modelle_tab()
        self.bind("<Return>", lambda event: self.save_and_reload())

    def setup_urlaub_tab(self):
        input_frame = ctk.CTkFrame(self.tab_urlaub)
        input_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(input_frame, text="Von:").grid(row=0, column=0, padx=5, pady=10)
        self.entry_u_von = self.create_date_entry(input_frame)
        self.entry_u_von.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(input_frame, text="Bis:").grid(row=0, column=2, padx=5, pady=10)
        self.entry_u_bis = self.create_date_entry(input_frame)
        self.entry_u_bis.grid(row=0, column=3, padx=5)
        ctk.CTkButton(
            input_frame, text="Urlaub speichern", command=self.add_urlaub
        ).grid(row=0, column=4, padx=20)
        self.u_list_frame = ctk.CTkScrollableFrame(
            self.tab_urlaub, label_text="Geplanter Urlaub"
        )
        self.u_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_urlaub_list()

    def add_urlaub(self):
        try:
            von_dt = datetime.strptime(self.entry_u_von.get(), "%d.%m.%Y")
            bis_str = self.entry_u_bis.get()
            bis_dt = datetime.strptime(bis_str, "%d.%m.%Y") if bis_str else von_dt
            raw = lade_abwesenheiten_raw()
            raw["urlaub_raw"].append(
                {"von": von_dt.strftime("%Y-%m-%d"), "bis": bis_dt.strftime("%Y-%m-%d")}
            )
            raw["urlaub_raw"].sort(key=lambda x: x["von"])
            speichere_abwesenheiten_raw(raw)
            self.refresh_urlaub_list()
            self.load_and_refresh()
            self.entry_u_von.delete(0, "end")
            self.entry_u_bis.delete(0, "end")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte Datum im Format TT.MM.JJJJ eingeben!")

    def refresh_urlaub_list(self):
        for child in self.u_list_frame.winfo_children():
            child.destroy()

        raw = lade_abwesenheiten_raw()
        urlaube = raw.get("urlaub_raw", [])
        jahr = self.aktuelles_jahr

        gefiltert = []
        for index, u in enumerate(urlaube):
            von = datetime.strptime(u["von"], "%Y-%m-%d").date()
            bis = datetime.strptime(u["bis"], "%Y-%m-%d").date()
            if von.year <= jahr <= bis.year:
                gefiltert.append((index, u))

        for original_index, u in gefiltert:
            row = ctk.CTkFrame(self.u_list_frame)
            row.pack(fill="x", pady=2)
            txt = f"{u['von']} bis {u['bis']}"
            ctk.CTkLabel(row, text=txt, width=300).pack(side="left", padx=10)

            btn_del = ctk.CTkButton(
                row,
                text="Löschen",
                width=60,
                fg_color="red",
                command=lambda i=original_index: self.delete_urlaub(i),
            )
            btn_del.pack(side="right", padx=10)

    def delete_urlaub(self, index):
        raw = lade_abwesenheiten_raw()
        if 0 <= index < len(raw["urlaub_raw"]):
            del raw["urlaub_raw"][index]
            speichere_abwesenheiten_raw(raw)
            self.refresh_urlaub_list()
            self.load_and_refresh()

    def setup_krankheit_tab(self):
        input_frame = ctk.CTkFrame(self.tab_krank)
        input_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(input_frame, text="Krank von:").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.entry_k_von = self.create_date_entry(input_frame)
        self.entry_k_von.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(input_frame, text="bis:").grid(row=0, column=2, padx=10, pady=10)
        self.entry_k_bis = self.create_date_entry(input_frame)
        self.entry_k_bis.grid(row=0, column=3, padx=5)
        ctk.CTkLabel(input_frame, text="Trotzdem gearbeitet (h):").grid(
            row=1, column=0, padx=10, pady=10
        )
        self.entry_k_ist = ctk.CTkEntry(input_frame, placeholder_text="0.0", width=80)
        self.entry_k_ist.grid(row=1, column=1, padx=5, sticky="w")
        ctk.CTkButton(
            input_frame,
            text="Krankheit speichern",
            fg_color="#E11D48",
            command=self.add_krankheit,
        ).grid(row=1, column=3, padx=20, pady=10)
        self.k_list_frame = ctk.CTkScrollableFrame(
            self.tab_krank, height=300, label_text="Erfasste Krankmeldungen"
        )
        self.k_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_krank_list()

    def add_krankheit(self):
        von_str = self.entry_k_von.get().strip()
        bis_str = self.entry_k_bis.get().strip() or von_str
        ist_stunden = self.entry_k_ist.get().strip()
        try:
            von_dt = datetime.strptime(von_str, "%d.%m.%Y")
            bis_dt = datetime.strptime(bis_str, "%d.%m.%Y")
            gearbeitet_dict = {}
            if ist_stunden:
                std_float = float(ist_stunden.replace(",", "."))
                if std_float > 0:
                    gearbeitet_dict[von_dt.strftime("%Y-%m-%d")] = std_float
            raw = lade_abwesenheiten_raw()
            raw["krankheit_raw"].append(
                {
                    "von": von_dt.strftime("%Y-%m-%d"),
                    "bis": bis_dt.strftime("%Y-%m-%d"),
                    "gearbeitete_stunden": gearbeitet_dict,
                }
            )
            raw["krankheit_raw"].sort(key=lambda x: x["von"])
            speichere_abwesenheiten_raw(raw)
            self.entry_k_von.delete(0, "end")
            self.entry_k_bis.delete(0, "end")
            self.entry_k_ist.delete(0, "end")
            self.refresh_krank_list()
            self.load_and_refresh()
        except ValueError:
            messagebox.showerror("Fehler", "Datum im Format TT.MM.JJJJ angeben.")

    def refresh_krank_list(self):
        from abwesenheiten import lade_abwesenheiten_raw

        for child in self.k_list_frame.winfo_children():
            child.destroy()

        raw = lade_abwesenheiten_raw()
        krankheiten = raw.get("krankheit_raw", [])
        jahr = self.aktuelles_jahr

        gefiltert = []
        for index, k in enumerate(krankheiten):
            von = datetime.strptime(k["von"], "%Y-%m-%d").date()
            bis = datetime.strptime(k["bis"], "%Y-%m-%d").date()
            if von.year <= jahr <= bis.year:
                gefiltert.append((index, k))

        for original_index, k in gefiltert:
            row = ctk.CTkFrame(self.k_list_frame)
            row.pack(fill="x", pady=2, padx=5)

            v = datetime.strptime(k["von"], "%Y-%m-%d").strftime("%d.%m.%Y")
            b = datetime.strptime(k["bis"], "%Y-%m-%d").strftime("%d.%m.%Y")
            anzeige = f"Krank: {v} bis {b}"
            ctk.CTkLabel(row, text=anzeige, width=300, anchor="w").pack(
                side="left", padx=10
            )

            btn_del = ctk.CTkButton(
                row,
                text="Löschen",
                width=60,
                fg_color="red",
                command=lambda i=original_index: self.delete_krankheit(i),
            )
            btn_del.pack(side="right", padx=10)

    def delete_krankheit(self, index):
        raw = lade_abwesenheiten_raw()
        if 0 <= index < len(raw.get("krankheit_raw", [])):
            del raw["krankheit_raw"][index]
            speichere_abwesenheiten_raw(raw)
            self.refresh_krank_list()
            self.load_and_refresh()

    def setup_arzt_tab(self):
        input_frame = ctk.CTkFrame(self.tab_arzt)
        input_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(input_frame, text="Datum:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_a_datum = self.create_date_entry(input_frame)
        self.entry_a_datum.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(input_frame, text="Dauer (h):").grid(
            row=0, column=2, padx=10, pady=10
        )
        self.entry_a_dauer = ctk.CTkEntry(
            input_frame, placeholder_text="z.B. 2.5", width=80
        )
        self.entry_a_dauer.grid(row=0, column=3, padx=5)
        ctk.CTkButton(
            input_frame, text="Termin speichern", command=self.add_arzttermin
        ).grid(row=0, column=4, padx=20)
        self.a_list_frame = ctk.CTkScrollableFrame(
            self.tab_arzt, height=300, label_text="Erfasste Arzttermine"
        )
        self.a_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_arzt_list()

    def add_arzttermin(self):
        try:
            datum_iso = datetime.strptime(
                self.entry_a_datum.get(), "%d.%m.%Y"
            ).strftime("%Y-%m-%d")
            dauer = float(self.entry_a_dauer.get().replace(",", "."))
            raw = lade_abwesenheiten_raw()
            raw["arzttermine_raw"].append({"datum": datum_iso, "dauer": dauer})
            raw["arzttermine_raw"].sort(key=lambda x: x["datum"])
            speichere_abwesenheiten_raw(raw)
            self.entry_a_datum.delete(0, "end")
            self.entry_a_dauer.delete(0, "end")
            self.refresh_arzt_list()
            self.load_and_refresh()
        except ValueError:
            messagebox.showerror(
                "Fehler", "Bitte Datum (TT.MM.JJJJ) und Dauer (Zahl) korrekt angeben."
            )

    def refresh_arzt_list(self):
        from abwesenheiten import lade_abwesenheiten_raw

        for child in self.a_list_frame.winfo_children():
            child.destroy()

        raw = lade_abwesenheiten_raw()
        termine = raw.get("arzttermine_raw", [])
        jahr = self.aktuelles_jahr

        gefiltert = []
        for index, a in enumerate(termine):
            datum = datetime.strptime(a["datum"], "%Y-%m-%d").date()
            if datum.year == jahr:
                gefiltert.append((index, a))

        for original_index, a in gefiltert:
            row = ctk.CTkFrame(self.a_list_frame)
            row.pack(fill="x", pady=2, padx=5)
            d = datetime.strptime(a["datum"], "%Y-%m-%d").strftime("%d.%m.%Y")
            ctk.CTkLabel(
                row, text=f"Arztbesuch am {d}: {a['dauer']}h", width=300, anchor="w"
            ).pack(side="left", padx=10)
            ctk.CTkButton(
                row,
                text="Löschen",
                width=60,
                fg_color="red",
                command=lambda i=original_index: self.delete_arzt(i),
            ).pack(side="right", padx=10)

    def delete_arzt(self, index):
        raw = lade_abwesenheiten_raw()
        if 0 <= index < len(raw.get("arzttermine_raw", [])):
            del raw["arzttermine_raw"][index]
            speichere_abwesenheiten_raw(raw)
            self.refresh_arzt_list()
            self.load_and_refresh()

    def setup_modelle_tab(self):
        input_frame = ctk.CTkFrame(self.tab_modelle)
        input_frame.pack(padx=20, pady=20, fill="x")
        ctk.CTkLabel(input_frame, text="Ab Datum (JJJJ-MM-TT):").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.ent_modell_start = ctk.CTkEntry(input_frame, placeholder_text="2024-01-01")
        self.ent_modell_start.insert(0, f"{date.today().year}-01-01")
        self.ent_modell_start.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(input_frame, text="Bundesland:").grid(
            row=0, column=2, padx=10, pady=10
        )
        self.cb_bundesland = ctk.CTkComboBox(
            input_frame, values=list(BUNDESLAENDER.keys())
        )
        self.cb_bundesland.set("Sachsen")
        self.cb_bundesland.grid(row=0, column=3, padx=10, pady=10)
        tage_container = ctk.CTkFrame(input_frame, fg_color="transparent")
        tage_container.grid(row=1, column=0, columnspan=4, pady=20)
        self.tag_entries = {}
        for i, name in enumerate(["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]):
            v_frame = ctk.CTkFrame(tage_container, fg_color="transparent")
            v_frame.pack(side="left", padx=5)
            ctk.CTkLabel(v_frame, text=name, font=("Roboto", 10)).pack()
            ent = ctk.CTkEntry(v_frame, width=50)
            ent.insert(0, "8.0" if i < 5 else "0.0")
            ent.pack()
            self.tag_entries[str(i)] = ent
        ctk.CTkButton(
            input_frame,
            text="Neues Modell speichern",
            fg_color="green",
            command=self.add_zeitmodell,
        ).grid(row=2, column=0, columnspan=4, pady=20)
        self.modelle_list_frame = ctk.CTkScrollableFrame(
            self.tab_modelle, label_text="Gespeicherte Arbeitszeit-Historie"
        )
        self.modelle_list_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.refresh_modelle_list()

    def add_zeitmodell(self):
        start_datum = self.ent_modell_start.get().strip()
        land_name = self.cb_bundesland.get()
        land_iso = BUNDESLAENDER.get(land_name, "SN")
        try:
            datetime.strptime(start_datum, "%Y-%m-%d")
            tagessoll = {}
            for i in range(7):
                val = self.tag_entries[str(i)].get().replace(",", ".")
                tagessoll[str(i)] = float(val)
            if "zeitmodelle" not in self.cfg:
                self.cfg["zeitmodelle"] = []
            self.cfg["zeitmodelle"] = [
                m for m in self.cfg["zeitmodelle"] if m["gueltig_ab"] != start_datum
            ]
            self.cfg["zeitmodelle"].append(
                {
                    "gueltig_ab": start_datum,
                    "bundesland": land_iso,
                    "tagessoll": tagessoll,
                }
            )
            self.cfg["zeitmodelle"].sort(key=lambda x: x["gueltig_ab"])
            speichere_config(self.cfg)
            self.refresh_modelle_list()
            self.load_and_refresh()
            messagebox.showinfo("Erfolg", f"Modell ab {start_datum} gespeichert!")
        except ValueError:
            messagebox.showerror("Fehler", "Ungültige Eingabe.")

    def refresh_modelle_list(self):
        for child in self.modelle_list_frame.winfo_children():
            child.destroy()
        modelle = self.cfg.get("zeitmodelle", [])
        for index, m in enumerate(modelle):
            row = ctk.CTkFrame(self.modelle_list_frame)
            row.pack(fill="x", pady=2, padx=5)
            info = f"Ab {m['gueltig_ab']} | {m['bundesland']} | Mo-Fr: {m['tagessoll']['0']}h..."
            ctk.CTkLabel(row, text=info, anchor="w").pack(
                side="left", padx=10, expand=True
            )
            ctk.CTkButton(
                row,
                text="Löschen",
                width=60,
                fg_color="#7F1D1D",
                command=lambda i=index: self.delete_modell(i),
            ).pack(side="right", padx=10)

    def delete_modell(self, index):
        if "zeitmodelle" in self.cfg and len(self.cfg["zeitmodelle"]) > index:
            del self.cfg["zeitmodelle"][index]
            speichere_config(self.cfg)
            self.refresh_modelle_list()
            self.load_and_refresh()

    def choose_folder(self):
        pfad = filedialog.askdirectory()
        if pfad:
            self.entry_ordner.delete(0, "end")
            self.entry_ordner.insert(0, pfad)

    def save_and_reload(self):
        datum_roh = self.entry_start.get()
        datum_sauber = datum_roh.replace("/", ".").replace("-", ".").replace(",", ".")
        self.entry_start.delete(0, "end")
        self.entry_start.insert(0, datum_sauber)
        datum_str = self.entry_start.get().strip()
        try:
            gewaehltes_datum = datetime.strptime(datum_str, "%d.%m.%Y").date()
            wochentag = gewaehltes_datum.weekday()
            if wochentag != 0:
                korrigiertes_datum = gewaehltes_datum - timedelta(days=wochentag)
                neuer_str = korrigiertes_datum.strftime("%d.%m.%Y")
                messagebox.showinfo(
                    "Startdatum angepasst",
                    f"Das Datum wurde auf den vorherigen Montag ({neuer_str}) gesetzt.",
                )
                self.entry_start.delete(0, "end")
                self.entry_start.insert(0, neuer_str)
                datum_str = neuer_str
        except ValueError:
            messagebox.showerror(
                "Fehler", "Ungültiges Datumsformat! Bitte TT.MM.JJJJ nutzen."
            )
            return
        try:
            self.cfg["ordner"] = self.entry_ordner.get()
            self.cfg["start_montag"] = self.entry_start.get()
            soll_wert = float(self.entry_soll.get().replace(",", "."))
            self.cfg["soll_wochenstunden"] = soll_wert
            # self.cfg["start_saldo"] = float(self.entry_vortrag.get().replace(",", "."))
            if not self.cfg.get("zeitmodelle"):
                start_iso = datetime.strptime(datum_str, "%d.%m.%Y").strftime(
                    "%Y-%m-%d"
                )
                tagessoll_wert = round(soll_wert / 5, 2)
                self.cfg["zeitmodelle"] = [
                    {
                        "gueltig_ab": start_iso,
                        "bundesland": "SN",
                        "tagessoll": {
                            str(i): tagessoll_wert if i < 5 else 0.0 for i in range(7)
                        },
                    }
                ]
            speichere_config(self.cfg)
            if hasattr(self, "refresh_modelle_list"):
                self.refresh_modelle_list()
            self.load_and_refresh()
            self.focus_set()
        except Exception as e:
            logging.error(f"Fehler beim Speichern: {e}")

    def fill_list(self, wochen_dict):
        for child in self.scroll_frame.winfo_children():
            child.destroy()
        if not wochen_dict:
            ctk.CTkLabel(
                self.scroll_frame, text="Keine Daten für diesen Zeitraum gefunden."
            ).pack(pady=20)
            return
        for montag in sorted(wochen_dict.keys()):
            zeile = WochenZeile(
                self.scroll_frame,
                montag,
                wochen_dict[montag],
                self.handle_payment_action,
            )
            zeile.pack(fill="x", pady=2, padx=5)

    def on_jahr_changed(self, choice):
        jahr = int(choice)
        self.setze_jahr(jahr)
        # self.aktuelles_jahr = jahr
        self.cfg["aktuelles_jahr"] = jahr
        speichere_config(self.cfg)
        # Startdatum auf ersten Montag des Jahres setzen
        erster = date(jahr, 1, 1)
        erster_montag = erster + timedelta(days=(7 - erster.weekday()) % 7)
        self.entry_start.delete(0, "end")
        self.entry_start.insert(0, erster_montag.strftime("%d.%m.%Y"))
        self.load_and_refresh()

    def setze_jahr(self, jahr: int):
        """Aktualisiert das Jahr, setzt den ersten Montag und lädt die Daten."""
        self.aktuelles_jahr = jahr
        self.cfg["aktuelles_jahr"] = jahr
        speichere_config(self.cfg)

        # Ersten Montag des Jahres berechnen
        erster = date(jahr, 1, 1)
        erster_montag = erster + timedelta(days=(7 - erster.weekday()) % 7)

        # UI- Felder aktualisieren
        self.entry_start.delete(0, "end")
        self.entry_start.insert(0, erster_montag.strftime("%d.%m.%Y"))

        if self.combo_jahr.get() != str(jahr):
            self.combo_jahr.set(str(jahr))

        # Daten neu laden
        self.load_and_refresh()

    def load_and_refresh(self):
        try:
            aktueller_pfad = self.entry_ordner.get()
            jahres_start_str = self.entry_start.get()
            jahres_start = datetime.strptime(jahres_start_str, "%d.%m.%Y").date()
            if jahres_start.weekday() != 0:
                jahres_start -= timedelta(days=jahres_start.weekday())

            soll_stunden = float(self.entry_soll.get().replace(",", "."))
            zuschlaege = self.cfg.get("zuschlaege", {})
            feiertags_faktor = float(zuschlaege.get("feiertag", 1.0))
            zeitmodelle_liste = self.cfg.get("zeitmodelle", [])

            # Vortrag-Fallback immer 0 – die automatische Berechnung hat Vorrang
            fallback_saldo = 0.0

            ergebnis = run_auswertung(
                pdf_datei=aktueller_pfad,
                jahres_start=jahres_start,
                sollstunden=soll_stunden,
                start_saldo_fallback=fallback_saldo,
                zeitmodelle_liste=zeitmodelle_liste,
                feiertags_zuschlag_faktor=feiertags_faktor,
            )

            # Automatischen Vortrag nur anzeigen, nicht in Config speichern
            self.entry_vortrag.delete(0, "end")
            self.entry_vortrag.insert(0, f"{ergebnis['vortrag']:.2f}")

            self.fill_list(ergebnis["wochen"])
            self.lbl_gesamt_saldo.configure(
                text=f"Gesamt-Saldo: {ergebnis['saldo']:.2f} h", text_color="#E3E66A"
            )
            #  copyright-Label
            self.lbl_copy_right = ctk.CTkLabel(
                self.footer,
                text=f"© {date.today().year} Gerald Günther",
                font=("Roboto", 10),
                text_color="gray60",
            )
            self.lbl_copy_right.pack(side="right", padx=20)

            self.focus_set()

        except Exception as e:
            logging.error(f"UI Load Error: {e}")
            self.fill_list({})
            self.lbl_gesamt_saldo.configure(
                text=f"Fehler: {str(e)}", text_color="#F87171"
            )

    def handle_payment_action(self, montag: date, stunden: float, kategorie: str):
        speichere_auszahlung(montag, kategorie, stunden)
        self.load_and_refresh()


if __name__ == "__main__":
    app = ZeiterfassungApp()
    app.mainloop()
