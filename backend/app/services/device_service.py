from app.models.device_model import DeviceModel


class DeviceService:
    
    @staticmethod
    def get_led_status():
        status = DeviceModel.get_led_status()
        return status if status in ["on", "off"] else "off"

    @staticmethod
    def update_led_status(state):
        if state not in ("on", "off"):
            raise ValueError("Invalid LED state")

        DeviceModel.update_led_state(state)
        return True
