import sqlite3
import os

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # -----------------------------------------------------
    # SENSOR DATA
    # -----------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)

    # -----------------------------------------------------
    # LED STATUS
    # -----------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS led_status (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        state TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    # Insert default LED row if missing
    cur.execute("SELECT COUNT(*) FROM led_status")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO led_status (id, state, updated_at) VALUES (1, 'off', CURRENT_TIMESTAMP)"
        )

    # -----------------------------------------------------
    # DEVICES
    # -----------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        status TEXT,
        last_update TEXT DEFAULT CURRENT_TIMESTAMP,
        mqtt_topic TEXT
    )
    """)

    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------------------------------
    # ALERTS
    # -----------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER,
        condition TEXT NOT NULL,
        current_value REAL,
        message TEXT,
        triggered_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------------------------------
    # AUTOMATION RULES
    # -----------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS automation_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        condition TEXT NOT NULL,
        action TEXT NOT NULL,
        enabled INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
