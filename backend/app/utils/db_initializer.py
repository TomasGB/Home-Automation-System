import sqlite3
import os
from app.config import Config

#DB_PATH = "database.db"

def init_db():
    assert "test" in Config.DB_PATH.lower() or not Config.TESTING, \
        "❌ init_db is using a NON-test database during tests!"

    conn = sqlite3.connect(Config.DB_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")
    #conn = sqlite3.connect(DB_PATH)
    #cur = conn.cursor()

    #cur.execute("PRAGMA foreign_keys = ON;")

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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS device_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            protocol TEXT NOT NULL,
            code TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(device_id, action),
            FOREIGN KEY (device_id) 
            REFERENCES devices(id)
            ON DELETE CASCADE
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
