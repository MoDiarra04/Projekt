import unittest
import tkinter as tk
from GUI1 import create_main_page, create_profile_page, display_profiles, set_image_path, show_profiles_page
from Datenbank import connect_db, create_table, save_profile

class TestGUIFunctions(unittest.TestCase):

    def setUp(self):
        self.app = tk.Tk()
        self.app.conn = connect_db(':memory:')
        create_table(self.app.conn)
        create_main_page(self.app)

    def tearDown(self):
        self.app.destroy()

    def test_create_profile_page(self):
        create_profile_page(self.app)
        profile_window = self.app.winfo_children()[-1]
        self.assertEqual(profile_window.title(), 'Profil erstellen')

        # Überprüfen, ob alle Widgets existieren
        name_label = profile_window.nametowidget(profile_window.winfo_children()[0])
        self.assertEqual(name_label.cget("text"), "Name:")
        upload_button = profile_window.nametowidget(profile_window.winfo_children()[2])
        self.assertEqual(upload_button.cget("text"), "Bild hochladen:")
        
        # Überprüfen des Wochentags-Labels
        weekday_label = profile_window.nametowidget(profile_window.winfo_children()[6])
        self.assertEqual(weekday_label.cget("text"), "Montag")
        
        # Überprüfen des Uhrzeit-Labels
        hour_label = profile_window.nametowidget(profile_window.winfo_children()[8])
        self.assertEqual(hour_label.cget("text"), "00:00")

        # Überprüfen der weiteren Widgets
        minuten_label = profile_window.nametowidget(profile_window.winfo_children()[10])
        self.assertEqual(minuten_label.cget("text"), "1")

    def test_display_profiles(self):
        save_profile(self.app.conn, 'TestName', 'Montag', '08:00', '30', 'test_image_path.png', False, 1)
        display_profiles(self.app, modulnummer=1)
        profiles_frame = self.app.wochenansicht_frame.winfo_children()
        self.assertGreater(len(profiles_frame), 1)

    def test_show_profiles_page(self):
        show_profiles_page(self.app)
        profiles_window = self.app.winfo_children()[-1]
        self.assertEqual(profiles_window.title(), 'Profiles')
        
        # Überprüfen, ob die Checkbuttons und OK-Button existieren
        module_checkbox1 = profiles_window.nametowidget(profiles_window.winfo_children()[1])
        self.assertEqual(module_checkbox1.cget("text"), "Pumpe: 1")
        module_checkbox2 = profiles_window.nametowidget(profiles_window.winfo_children()[2])
        self.assertEqual(module_checkbox2.cget("text"), "Pumpe: 2")
        ok_button = profiles_window.nametowidget(profiles_window.winfo_children()[-1].winfo_children()[-1])
        self.assertEqual(ok_button.cget("text"), "OK")

if __name__ == '__main__':
    unittest.main()
