from app.models.device_model import DeviceModel


class DeviceService:
    
    @staticmethod
    def get_device_status():
        status = DeviceModel.get_device_status()
        return status if status in ["on", "off"] else "off"

    @staticmethod
    def update_device_status(state):
        if state not in ("on", "off"):
            raise ValueError("Invalid DEVICE state")

        DeviceModel.update_status(state)
        return True
