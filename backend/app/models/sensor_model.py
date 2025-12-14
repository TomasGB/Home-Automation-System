import sqlite3
from app.config import Config
import time
from datetime import datetime

DB_PATH = Config.DB_PATH

class SensorModel:
    
    @staticmethod
    def create_table():
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp INTEGER NOT NULL,
                    temperature REAL,
                    humidity REAL
                )
            """)

    @staticmethod
    def insert(temperature, humidity, timestamp=None):
        # Get current timestamp or use provided timestamp
        if timestamp is None:
            timestamp = int(time.time())

        # Convert timestamp to a datetime object
        local_time = datetime.fromtimestamp(timestamp)

        # Format the datetime object to the desired format: day-month-year hour:minute
        formatted_time = local_time.strftime('%d-%m-%Y %H:%M')

        # Single connection block, no nested connects
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sensor_data (temperature, humidity, timestamp)
                VALUES (?, ?, ?)
            """, (temperature, humidity, formatted_time))
            conn.commit()


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
