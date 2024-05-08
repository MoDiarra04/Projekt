import tkinter as tk
from tkinter import *

class IrrigationSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bewässerungssystem")
        self.geometry("800x600")

        # Variablen für Profilinformationen
        self.profiles = []

        self.create_main_page()

    def create_main_page(self):
        # Firmenname
        firmenname_label = tk.Label(self, text="Firmenname", font=("Helvetica", 20))
        firmenname_label.pack(side=tk.TOP)

        # Wochenansicht
        wochenansicht_frame = tk.Frame(self,bg='grey',bd=5,relief=RAISED,pady=2)
        wochenansicht_frame.pack(side=tk.LEFT, padx=10, pady=10)
        # Hier Wochenansicht implementieren
        #Wochentag
        tk.Label(wochenansicht_frame,text='Montag').grid(row=1,column=1)
        tk.Label(wochenansicht_frame,text='Dienstag').grid(row=1,column=2)
        tk.Label(wochenansicht_frame,text='Mittwoch').grid(row=1,column=3)
        tk.Label(wochenansicht_frame,text='Donnerstag').grid(row=1,column=4)
        tk.Label(wochenansicht_frame,text='Freitag').grid(row=1,column=5)
        tk.Label(wochenansicht_frame,text='Samstag').grid(row=1,column=6)
        tk.Label(wochenansicht_frame,text='Sonntag').grid(row=1,column=7)
        #Uhrzeit
        tk.Label(wochenansicht_frame,text='0-4 Uhr').grid(row=2,column=0)
        tk.Label(wochenansicht_frame,text='4-8 Uhr').grid(row=3,column=0)
        tk.Label(wochenansicht_frame,text='8-12 Uhr').grid(row=4,column=0)
        tk.Label(wochenansicht_frame,text='12-16 Uhr').grid(row=5,column=0)
        tk.Label(wochenansicht_frame,text='16-20 Uhr').grid(row=6,column=0)
        tk.Label(wochenansicht_frame,text='20-24 Uhr').grid(row=7,column=0)
    
        # Buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        profil_erstellen_button = tk.Button(buttons_frame, text="Profil erstellen", command=self.create_profile_page)
        profil_erstellen_button.pack(side=tk.TOP)
        profil_laden_button = tk.Button(buttons_frame, text="Profil laden", command=self.load_profile_page)
        profil_laden_button.pack(side=tk.TOP)
        # Weitere Buttons hinzufügen

    def create_profile_page(self):
        # Profil erstellen Seite
        create_profile_window = tk.Toplevel(self)
        create_profile_window.title("Profil erstellen")

        # Widgets für Profilerstellung
        name_label = tk.Label(create_profile_window, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(create_profile_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Implementiere weitere Widgets für die Profilerstellung

        # Button zum Speichern des Profils
        save_button = tk.Button(create_profile_window, text="Speichern", command=lambda: self.save_profile(name_entry.get()))
        save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def save_profile(self, name):
        # Speichert das erstellte Profil und schließt das Profil-Erstellungsfenster
        self.profiles.append({"name": name})
        print("Profil gespeichert:", name)
        # Optional: Aktualisiere Profil-Laden-Seite

    def load_profile_page(self):
        # Profil laden Seite
        load_profile_window = tk.Toplevel(self)
        load_profile_window.title("Profil laden")

        # Liste der Profile
        profile_listbox = tk.Listbox(load_profile_window)
        for profile in self.profiles:
            profile_listbox.insert(tk.END, profile["name"])
        profile_listbox.pack(padx=10, pady=10)

        # Button zum Laden des ausgewählten Profils
        load_button = tk.Button(load_profile_window, text="Laden", command=lambda: self.load_profile(profile_listbox.get(tk.ACTIVE)))
        load_button.pack(padx=10, pady=5)

    def load_profile(self, profile_name):
        # Lädt das ausgewählte Profil
        print("Profil geladen:", profile_name)
        # Implementiere das Laden des Profils in den Wochenplan und weitere Aktionen

if __name__ == "__main__":
    app = IrrigationSystemApp()
    app.mainloop()
