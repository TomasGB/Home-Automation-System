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
    def get_all():
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute("""
                SELECT id, name, type, status, mqtt_topic
                FROM devices
            """).fetchall()

        return [
            {
                "id": r[0],
                "name": r[1],
                "type": r[2],
                "status": r[3],
                "mqtt_topic": r[4]
            }
            for r in rows
        ]


    @staticmethod
    def create_device(name, dev_type, mqtt_topic):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO devices(name, type, status, mqtt_topic)
                VALUES (?, ?, 'off', ?)
            """, (name, dev_type, mqtt_topic))
    
    @staticmethod
    def delete(device_id):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                "DELETE FROM devices WHERE id = ?",
                (device_id,)
            )
            return cur.rowcount > 0
        
    @staticmethod
    def update(device_id, name=None, dev_type=None, mqtt_topic=None):
        fields = []
        values = []

        if name:
            fields.append("name = ?")
            values.append(name)

        if dev_type:
            fields.append("type = ?")
            values.append(dev_type)

        if mqtt_topic:
            fields.append("mqtt_topic = ?")
            values.append(mqtt_topic)

        if not fields:
            return False

        values.append(device_id)

        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                f"UPDATE devices SET {', '.join(fields)} WHERE id = ?",
                values
            )
            return cur.rowcount > 0


    
    @staticmethod
    def update_status(device_id, status):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                "UPDATE devices SET status=? WHERE id=?",
                (status, device_id)
            )
            return cur.rowcount > 0  # True if updated
        
    @staticmethod
    def get_device_status(device_id):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                "SELECT status FROM devices WHERE id=?",
                (device_id,)
            )
            row = cur.fetchone()
            if row:
                return row[0]  # The status is in the first column
            else:
                return None  # No device found with the given id

    
    @staticmethod
    def get_by_id(device_id):
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute(
                "SELECT id, name, type, status, mqtt_topic FROM devices WHERE id=?",
                (device_id,)
            ).fetchone()

            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "type": row[2],
                    "status": row[3],
                    "mqtt_topic": row[4],
                }
            return None
    
    @staticmethod
    def get_by_mqtt_topic(topic):
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT id, name, type, status, mqtt_topic FROM devices WHERE mqtt_topic = ?",
                (topic,)
            )
            row = cur.fetchone()
            return dict(row) if row else None




