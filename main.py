import tkinter as tk
from GUI1 import create_main_page, display_profiles, create_profile_page, show_profiles_page
from Datenbank import create_table, connect_db

class IrrigationSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Entfernt die title bar des Hauptfensters.
        self.overrideredirect(True)
        
        # Setzt die Abmessungen des Hauptfensters
        self.geometry("800x480")

        # Stellt die Verbindung zur Datenbank her und erstellt die Tabelle
        self.conn = connect_db('profiles.db')
        create_table(self.conn)

        # Erstellt die Hauptseite der Anwendung
        create_main_page(self)

if __name__ == "__main__":
    # Initialisiert und startet die Anwendung
    app = IrrigationSystemApp()
    app.mainloop()
