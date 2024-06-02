import sys
import os

# Fügen Sie den Pfad zur Projektwurzel hinzu
sys.path.append(os.path.abspath('..'))
import unittest
import tkinter as tk
from GUI1 import create_main_page, create_profile_page, display_profiles
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

    def test_display_profiles(self):
        save_profile(self.app.conn, 'TestName', 'Montag', '08:00', '30', 'test_image_path.png')
        display_profiles(self.app)
        profiles_frame = self.app.wochenansicht_frame.winfo_children()
        self.assertGreater(len(profiles_frame), 1)

if __name__ == '__main__':
    unittest.main()
