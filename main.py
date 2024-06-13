import tkinter as tk
from GUI1 import create_main_page, display_profiles, create_profile_page, show_profiles_page, create_manual_page, start_countdown
from Datenbank import create_table, connect_db

class IrrigationSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Entfernt die title bar des Hauptfensters.
        self.overrideredirect(True)
        
        # Setzt die Abmessungen des Hauptfensters
        self.geometry("800x480")

        # Initialisieren von smart_button_active
        self.smart_button_active = False

        # Datenbankverbindung herstellen und Tabelle erstellen
        self.conn = connect_db('profiles.db')
        create_table(self.conn)
        
        # Uhrzeit kontinuierlich überprüfen und ggf. wässern
        self.checked = True # Flag zum Überprüfen ob in dieser Stunde bereits gewässert wurde
        self.check_time()

        # Erstellt die Hauptseite der Anwendung
        create_main_page(self)
        display_profiles(self,True)
        #get every selection = True and push it to old in start

    def create_manual_page(self):
        create_manual_page(self)

    def start_countdown(self, duration, window):
        start_countdown(self, duration, window)

    

if __name__ == "__main__":
    # Initialisiert und startet die Anwendung
    app = IrrigationSystemApp()
    app.mainloop()
