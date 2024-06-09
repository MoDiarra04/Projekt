import unittest
import sqlite3
from Datenbank import connect_db, create_table, save_profile, get_profiles, delete_profile, update_selection, update_modulnummer

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        self.conn = connect_db(':memory:')  # Verwende eine In-Memory-Datenbank für Tests
        create_table(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_save_profile(self):
        save_profile(self.conn, 'TestName', 'Montag', '08:00', '30', 'test_image_path.png', 1, 1)
        profiles = get_profiles(self.conn)
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0][:7], ('TestName', 'Montag', '08:00', '30', 'test_image_path.png', 1, 1))

    def test_get_profiles(self):
        save_profile(self.conn, 'TestName', 'Montag', '08:00', '30', 'test_image_path.png', 1, 1)
        save_profile(self.conn, 'TestName2', 'Dienstag', '09:00', '20', 'test_image_path2.png', 0, 2)
        profiles = get_profiles(self.conn)
        self.assertEqual(len(profiles), 2)

    def test_update_selection(self):
        save_profile(self.conn, 'TestName', 'Montag', '08:00', '30', 'test_image_path.png', 0, 1)
        update_selection(self.conn, 'TestName', 1)
        profiles = get_profiles(self.conn)
        self.assertEqual(profiles[0][5], 1)

    def test_update_modulnummer(self):
        save_profile(self.conn, 'TestName', 'Montag', '08:00', '30', 'test_image_path.png', 1, 1)
        update_modulnummer(self.conn, 'TestName', 2)
        profiles = get_profiles(self.conn)
        self.assertEqual(profiles[0][6], 2)

if __name__ == '__main__':
    unittest.main()
