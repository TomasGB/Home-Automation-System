from app.models.sensor_model import SensorModel
from app.models.device_model import DeviceModel
from app.models.user_model import UserModel

def migrate():
    print("Creating database tables...")
    SensorModel.create_table()
    DeviceModel.create_table()
    UserModel.create_table()
    print("✓ Migration complete")

if __name__ == "__main__":
    migrate()
