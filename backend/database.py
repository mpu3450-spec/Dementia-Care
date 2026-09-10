import sqlite3

DB_NAME = "dementia_care.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            language TEXT,
            last_active TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            game TEXT,
            score INTEGER,
            accuracy REAL,
            response_time REAL,
            mistakes INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            reminder_type TEXT,
            reminder_text TEXT,
            reminder_time TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()
    