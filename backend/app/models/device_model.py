import sqlite3
from app.config import Config

DB_PATH = Config.DB_PATH

class DeviceModel:

    @staticmethod
    def create_table():
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT DEFAULT 'off',
                    mqtt_topic TEXT
                )
            """)

    @staticmethod
    def get_led_status():
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute("""
                SELECT status FROM devices
                WHERE type='led'
                LIMIT 1
            """).fetchone()
            return row[0] if row else "off"

    @staticmethod
    def update_led_state(status):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                UPDATE devices
                SET status=?
                WHERE type='led'
            """, (status, ))
            conn.commit()   # <-- FIXED
