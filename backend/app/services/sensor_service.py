from app.models.sensor_model import SensorModel

class SensorService:

    def insert_sensor_data(self, temperature, humidity):
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
