import unittest
import sqlite3
from Datenbank import connect_db, create_table, save_profile, get_profiles, delete_profile

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        self.conn = connect_db(':memory:')  # Verwende eine In-Memory-Datenbank für Tests
        create_table(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_save_profile(self):
        save_profile(self.conn, 'TestName', 'Montag', '08:00', '30', 'test_image_path.png')
        profiles = get_profiles(self.conn)
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0][:5], ('TestName', 'Montag', '08:00', '30', 'test_image_path.png'))

    def test_get_profiles(self):
        save_profile(self.conn, 'TestName', 'Montag', '08:00', '30', 'test_image_path.png')
        save_profile(self.conn, 'TestName2', 'Dienstag', '09:00', '20', 'test_image_path2.png')
        profiles = get_profiles(self.conn)
        self.assertEqual(len(profiles), 2)

    def test_delete_profile(self):
        save_profile(self.conn, 'TestName', 'Montag', '08:00', '30', 'test_image_path.png')
        delete_profile(self.conn, 1)
        profiles = get_profiles(self.conn)
        self.assertEqual(len(profiles), 0)

if __name__ == '__main__':
    unittest.main()
