import tkinter as tk
from GUI1 import create_main_page, display_profiles, create_profile_page, show_profiles_page, create_manual_page, start_countdown
from Datenbank import create_table, connect_db
from datetime import datetime, time

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
        
        self.bind('<Control-q>', self.quit_app)

        # Uhrzeit kontinuierlich überprüfen und ggf. Bewässerungsbefehl schicken
        self.check_time()

        # Erstellt die Hauptseite der Anwendung
        create_main_page(self)
        display_profiles(self,True)
        #get every selection = True and push it to old in start

    def create_manual_page(self):
        create_manual_page(self)

    def start_countdown(self, duration, window):
        start_countdown(self, duration, window)
        
    def quit_app(self, event=None):
        self.quit()

    # Zeit überprüfen, mit Terminen vergleichen und ggf. einen Bewässerungsbefehl schicken
    def check_time(self):
        
        # Volle Stunde erkennen
        if datetime.now().minute != 0:
            self.after(1000, self.check_time) # nochmal checken in 1 sekunde
            return
            
        global active_profiles
        if active_profiles:
            # Liste für Konvertierung: Montag->0; Dienstag->1 ...
            wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
                        
            # Wochentage und Stunden prüfen
            for profile in active_profiles:
                if wochentage.index(profile[1]) == datetime.weekday() and profile[2][0:2] == datetime.now().hour:
                    # TODO Bewässerungsbefehl abschicken
                    print("Bewässerungsbefehl!")

        # Schedule the next check
        self.after(1000*60*59, self.check_time) # nochmal checken in 59 minuten

    

if __name__ == "__main__":
    # Initialisiert und startet die Anwendung
    app = IrrigationSystemApp()
    app.mainloop()
