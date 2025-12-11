import sqlite3
from app.config import Config

DB_PATH = Config.DB_PATH

class SensorModel:
    @staticmethod
    def create_table():
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    temperature REAL,
                    humidity REAL
                )
            """)

    @staticmethod
    def insert(temperature, humidity):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO sensor_data (temperature, humidity)
                VALUES (?, ?)
            """, (temperature, humidity))

    @staticmethod
    def get_latest():
        with sqlite3.connect(DB_PATH) as conn:
            return conn.execute("""
                SELECT * FROM sensor_data
                ORDER BY timestamp DESC
                LIMIT 1
            """).fetchone()

    @staticmethod
    def get_history(limit=50):
        with sqlite3.connect(DB_PATH) as conn:
            return conn.execute("""
                SELECT * FROM sensor_data
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit, )).fetchall()
