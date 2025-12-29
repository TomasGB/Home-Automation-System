import sqlite3
from app.config import Config

DB_PATH = Config.DB_PATH

class DeviceActionModel:

    @staticmethod
    def create(device_id, action, protocol, code):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO device_actions
            (device_id, action, protocol, code)
            VALUES (?, ?, ?, ?)
        """, (device_id, action, protocol, code))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_device(device_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT action, protocol, code
            FROM device_actions
            WHERE device_id = ?
        """, (device_id,))

        rows = cursor.fetchall()
        conn.commit()
        conn.close()

        return [
            {
                "action": r[0],
                "protocol": r[1],
                "code": r[2]
            }
            for r in rows
        ]

    @staticmethod
    def get(device_id, action):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT protocol, code
            FROM device_actions
            WHERE device_id = ? AND action = ?
        """, (device_id, action))

        row = cursor.fetchone()
        conn.commit()
        conn.close()

        if not row:
            return None

        return {
            "protocol": row[0],
            "code": row[1]
        }

    @staticmethod
    def delete_by_device(device_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM device_actions
            WHERE device_id = ?
        """, (device_id,))

        conn.commit()
        conn.close()