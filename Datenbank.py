import sqlite3

def connect_db(db_name):
    # Verbindet sich mit der SQLite-Datenbank
    return sqlite3.connect(db_name)

def create_table(conn):
    # Erstellt die Tabelle für Profile, falls sie nicht existiert
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            wochentag TEXT,
            uhrzeit TEXT,
            bewaessungsdauer TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()

def save_profile(conn, name, wochentag, uhrzeit, bewaessungsdauer, image_path):
    # Speichert ein neues Profil in der Datenbank
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO profiles (name, wochentag, uhrzeit, bewaessungsdauer, image_path) 
        VALUES (?, ?, ?, ?, ?)
    ''', (name, wochentag, uhrzeit, bewaessungsdauer, image_path))
    conn.commit()

def get_profiles(conn):
    # Ruft alle gespeicherten Profile aus der Datenbank ab
    cursor = conn.cursor()
    cursor.execute('SELECT name, wochentag, uhrzeit, bewaessungsdauer, image_path FROM profiles')
    return cursor.fetchall()

def delete_profile(conn, name):
    # Löscht ein Profil aus der Datenbank
    cursor = conn.cursor()
    cursor.execute('DELETE FROM profiles WHERE name=?', (name,))
    conn.commit()
