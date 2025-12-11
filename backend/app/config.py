import os

class Config:
    # Keep DB_PATH same as your current file
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "..", "database.db"))

    # MQTT
    MQTT_BROKER = os.getenv("MQTT_BROKER", "test.mosquitto.org")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    MQTT_TOPIC_SENSOR = os.getenv("MQTT_TOPIC_SENSOR", "home/sensor/data")
    #MQTT_TOPIC_LED = os.getenv("MQTT_TOPIC_LED", "home/led/control")

    # Only ONE LED topic – unified
    #MQTT_TOPIC_SENSOR = os.getenv("MQTT_TOPIC_SENSOR", "home/sensor/data")
    MQTT_TOPIC_LED = os.getenv("MQTT_TOPIC_LED", "home/led/state")


    # App
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")  # change in prod

    # Misc
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    JWT_SECRET = os.getenv("JWT_SECRET", "fallback_jwt_secret")

