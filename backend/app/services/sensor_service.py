#import sqlite3
#from typing import List, Dict
#import logging
#
#logger = logging.getLogger(__name__)
#
#class SensorService:
#    def __init__(self, db_path: str):
#        self.db_path = db_path
#
#    def _connect(self):
#        # Use row factory to return dict-like rows
#        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
#        conn.row_factory = sqlite3.Row
#        return conn
#
#    def insert_sensor_data(self, temperature: float, humidity: float):
#        try:
#            with self._connect() as conn:
#                conn.execute(
#                    "INSERT INTO sensor_data (timestamp, temperature, humidity) VALUES (datetime('now', 'localtime'), ?, ?)",
#                    (temperature, humidity)
#                )
#                conn.commit()
#        except Exception:
#            logger.exception("Failed to insert sensor data")
#
#    def get_latest(self, limit: int = 10) -> List[Dict]:
#        with self._connect() as conn:
#            cur = conn.execute("SELECT id, timestamp, temperature, humidity FROM sensor_data ORDER BY timestamp DESC LIMIT ?", (limit,))
#            rows = [dict(r) for r in cur.fetchall()]
#        return rows
#

from app.models.sensor_model import SensorModel

class SensorService:

    @staticmethod
    def insert_sensor_data(temperature, humidity):
        SensorModel.insert(temperature, humidity)

    @staticmethod
    def get_latest():
        row = SensorModel.get_latest()
        if not row:
            return None

        return {
            "id": row[0],
            "timestamp": row[1],
            "temperature": row[2],
            "humidity": row[3]
        }

    @staticmethod
    def get_history(limit=50):
        rows = SensorModel.get_history(limit)
        return [
            {
                "id": r[0],
                "timestamp": r[1],
                "temperature": r[2],
                "humidity": r[3],
            }
            for r in rows
        ]
