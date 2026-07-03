import sqlite3

DB = "patients.db"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name   TEXT    NOT NULL,
            dob         TEXT    NOT NULL,
            email       TEXT    NOT NULL,
            glucose     REAL    NOT NULL,
            haemoglobin REAL    NOT NULL,
            cholesterol REAL    NOT NULL,
            remarks     TEXT    DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()
