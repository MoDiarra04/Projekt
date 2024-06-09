import unittest
import tkinter as tk
from GUI1 import create_main_page, show_profiles_page, create_profile_page, display_profiles
from Datenbank import connect_db, create_table, save_profile

class TestIntegration(unittest.TestCase):

    def setUp(self):
        # Setzt die Testumgebung auf, indem eine in-memory SQLite-Datenbank und die Hauptseite der GUI erstellt werden
        self.app = tk.Tk()
        self.app.conn = connect_db(':memory:')
        create_table(self.app.conn)
        create_main_page(self.app)

    def tearDown(self):
        # Zerstört die GUI nach jedem Test
        self.app.destroy()

    def test_create_and_display_profile(self):
        # Öffnet die Profil-Erstellungsseite
        create_profile_page(self.app)
        profile_window = self.app.winfo_children()[-1]

        # Simuliert die Eingabe des Benutzers und das Speichern des Profils
        name_entry = None
        duration_option_menu = None

        # Debug-Ausgabe der Widgets
        for widget in profile_window.winfo_children():
            print(widget, widget.winfo_class())

        for widget in profile_window.winfo_children():
            if isinstance(widget, tk.Entry) and not name_entry:
                name_entry = widget
            elif isinstance(widget, tk.OptionMenu) and not duration_option_menu:
                duration_option_menu = widget

        self.assertIsNotNone(name_entry, "Name entry not found")
        self.assertIsNotNone(duration_option_menu, "Duration option menu not found")

        name_entry.insert(0, 'TestName')

        # Setzen des Werts im OptionMenu
        menu = duration_option_menu.children["menu"]
        menu.invoke(10)  # Hier wird der 11. Eintrag im Menu ausgewählt (indexbasiert)

        save_button = None
        for widget in profile_window.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget('text') == 'Speichern':
                save_button = widget
                break

        self.assertIsNotNone(save_button, "Save button not found")
        save_button.invoke()

        # Überprüfen, ob das Profil gespeichert und angezeigt wird
        display_profiles(self.app)
        profiles_frame = self.app.wochenansicht_frame.winfo_children()
        self.assertGreater(len(profiles_frame), 1)

if __name__ == '__main__':
    unittest.main()
