# Wi-Fi
WIFI_SSID = "SSID"
WIFI_PASSWORD = "PASSWORD"

# MQTT (TCP)
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_CLIENT_ID_PREFIX = "esp32-mp-"



# Topics (must match backend/frontend)
TOPIC_SENSOR = b"home/sensor/data"
TOPIC_AC = b"home/AC/state"
TOPIC_TV = b"home/TV/state"
TOPIC_STATUS = b"home/device/status"
LEARN_REQUEST_TOPIC = b"home/ir/learn/request"
LEARN_RESULT_TOPIC = b"home/ir/learn/result"


# Hardware pins
LED_PIN = 32        # change if your LED is on a different pin
DHT_PIN = 14        # change to your DHT11 data pin
IR_LED_PIN = 26
IR_LED_PIN_RECEIVER = 27


# Timers
SENSOR_PUBLISH_INTERVAL = 10  # seconds
WIFI_CONNECT_TIMEOUT = 20     # seconds

