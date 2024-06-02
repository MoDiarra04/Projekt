import unittest
import tkinter as tk
from GUI1 import create_main_page, show_profiles_page, create_profile_page, display_profiles
from Datenbank import connect_db, create_table, save_profile

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.app = tk.Tk()
        self.app.conn = connect_db(':memory:')
        create_table(self.app.conn)
        create_main_page(self.app)

    def tearDown(self):
        self.app.destroy()

    def test_create_and_display_profile(self):
        create_profile_page(self.app)
        profile_window = self.app.winfo_children()[-1]

        # Simuliere die Eingabe des Benutzers und das Speichern des Profils
        name_entry = profile_window.children['!entry']
        name_entry.insert(0, 'TestName')
        duration_entry = profile_window.children['!entry2']
        duration_entry.insert(0, '30')
        save_button = profile_window.children['!button']
        save_button.invoke()

        # Überprüfen, ob das Profil gespeichert und angezeigt wird
        display_profiles(self.app)
        profiles_frame = self.app.wochenansicht_frame.winfo_children()
        self.assertGreater(len(profiles_frame), 1)

if __name__ == '__main__':
    unittest.main()
