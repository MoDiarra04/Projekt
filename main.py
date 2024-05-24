import tkinter as tk
from GUI1 import create_main_page, display_profiles, create_profile_page, show_profiles_page
from Datenbank import create_table, connect_db

class IrrigationSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bewässerungssystem")
        self.geometry("800x480")

        # Datenbankverbindung herstellen und Tabelle erstellen
        self.conn = connect_db('profiles.db')
        create_table(self.conn)

        # Hauptseite erstellen
        create_main_page(self)
        display_profiles(self)

if __name__ == "__main__":
    app = IrrigationSystemApp()
    app.mainloop()
