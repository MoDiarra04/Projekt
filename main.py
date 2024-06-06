import tkinter as tk
from GUI1 import create_main_page, display_profiles, create_profile_page, show_profiles_page
from Datenbank import create_table, connect_db

class IrrigationSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Setzt den Titel des Hauptfensters
        self.title("Bewässerungssystem")
        # Setzt die Abmessungen des Hauptfensters
        self.geometry("800x480")

        # Stellt die Verbindung zur Datenbank her und erstellt die Tabelle
        self.conn = connect_db('profiles.db')
        create_table(self.conn)

        # Erstellt die Hauptseite der Anwendung
        create_main_page(self)
        display_profiles(self)
        #get every selection = True and push it to old in start
if __name__ == "__main__":
    # Initialisiert und startet die Anwendung
    app = IrrigationSystemApp()
    app.mainloop()
