from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk


class IrrigationSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bewässerungssystem")
        self.geometry("800x480")

        # Variablen für Profilinformationen
        self.profiles = []

        self.create_main_page()

    def create_main_page(self):
        # Firmenname
        firmenname_label = tk.Label(text="Firmenname", font=("Helvetica", 20))
        firmenname_label.pack(side=tk.TOP)

        # Wochenansicht
        wochenansicht_frame = tk.Frame(bg='grey',bd=5,relief=RAISED,pady=2)
        wochenansicht_frame.pack(side=tk.TOP)
        # Hier Wochenansicht implementieren
        #Wochentag
        tk.Label(wochenansicht_frame,text='Montag').grid(row=1,column=1)
        tk.Label(wochenansicht_frame,text='Dienstag').grid(row=1,column=2)
        tk.Label(wochenansicht_frame,text='Mittwoch').grid(row=1,column=3)
        tk.Label(wochenansicht_frame,text='Donnerstag').grid(row=1,column=4)
        tk.Label(wochenansicht_frame,text='Freitag').grid(row=1,column=5)
        tk.Label(wochenansicht_frame,text='Samstag').grid(row=1,column=6)
        tk.Label(wochenansicht_frame,text='Sonntag').grid(row=1,column=7)
 
    
        # Buttons
        buttons_frame = tk.Frame()
        buttons_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        profil_erstellen_button = tk.Button(buttons_frame, text="Profil erstellen", command=self.create_profile_page)
        profil_erstellen_button.pack(side=tk.TOP)
        profil_laden_button = tk.Button(buttons_frame, text="Profil laden", command=self.load_profile_page)
        profil_laden_button.pack(side=tk.TOP)
        # Weitere Buttons hinzufügen

    def create_profile_page(self):
        # Profil erstellen Seite
        create_profile_window = tk.Toplevel()
        create_profile_window.title("Profil erstellen")

        # Widgets für Profilerstellung
        name_label = tk.Label(create_profile_window, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(create_profile_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        bild_label = tk.Label(create_profile_window, text="Bild hochladen:")
        bild_label.grid(row=1, column=0, padx=10, pady=5)
        upload_button = tk.Button(create_profile_window,text="Bild hichladen")
        upload_button.grid(row=1, column=1, padx=10, pady=5)
        # Implementiere weitere Widgets für die Profilerstellung
        # Liste der Wochentage
        weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        weekday_label = tk.Label(create_profile_window, text="Wochentag: ")
        weekday_label.grid(row=2, column=0, padx=10, pady=5)
        # Dropdown-Menü für Wochentage
        selected_weekday = tk.StringVar()
        selected_weekday.set(weekdays[0])  # Standardmäßig den ersten Wochentag auswählen
        weekday_dropdown = tk.OptionMenu(create_profile_window,selected_weekday, *weekdays)
        weekday_dropdown.grid(row=2, column=1, padx=10, pady=5)
        # Liste der Stunden von 0 bis 23
        hours = [str(hour) for hour in range(24)]

        # Dropdown-Menü für Uhrzeit
        selected_hour_label = tk.Label(create_profile_window, text="Uhrzeit: ")
        selected_hour_label.grid(row=3, column=0, padx=10, pady=5)
        selected_hour = tk.StringVar()
        selected_hour.set(hours[0])  # Standardmäßig die erste Stunde auswählen
        hour_dropdown = tk.OptionMenu(create_profile_window, selected_hour, *hours)
        hour_dropdown.grid(row=3, column=1, padx=10, pady=5)
        # Dropdown Dauer
        minuten_label = tk.Label(create_profile_window, text="Dauer: ")
        minuten_label.grid(row=4, column=0, padx=10, pady=5)
        minutes = [str(minute) for minute in range(1, 21)]
        selected_minute = tk.StringVar()
        selected_minute.set(minutes[0])  # Standardmäßig die erste Minute auswählen
        minute_dropdown = tk.OptionMenu(create_profile_window, selected_minute, *minutes)
        minute_dropdown.grid(row=4, column=1, padx=10, pady=5)
        # Button zum Speichern des Profils
        save_button = tk.Button(create_profile_window, text="Speichern", command=lambda: self.save_profile(name_entry.get()))
        save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def save_profile(self, name):
        # Speichert das erstellte Profil und schließt das Profil-Erstellungsfenster
        self.profiles.append({"name": name})
        print("Profil gespeichert:", name)
        # Optional: Aktualisiere Profil-Laden-Seite

    def load_profile_page(self):
        # Profil laden Seite
        load_profile_window = tk.Toplevel()
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

    def upload_image(self):
        label = tk.Label()
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo

if __name__ == "__main__":
    app = IrrigationSystemApp()
    app.mainloop()
