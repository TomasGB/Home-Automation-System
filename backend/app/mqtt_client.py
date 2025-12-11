import json
import threading
import paho.mqtt.client as mqtt
import logging

from app.config import Config
from app.services.sensor_service import SensorService
from app.services.device_service import DeviceService

logger = logging.getLogger(__name__)

# Single set of topics
SENSOR_TOPIC = Config.MQTT_TOPIC_SENSOR         # "home/sensor/data"
LED_TOPIC = Config.MQTT_TOPIC_LED               # "home/led/state"


class MQTTClientWrapper:
    
    def __init__(self):
        
        logger.info("🔥 MQTT: Initializing MQTTClientWrapper")

        self.client = mqtt.Client()

        self.broker = Config.MQTT_BROKER
        self.port = Config.MQTT_PORT

        # Subscribe to ONLY 2 topics now
        self.topics = [
            (SENSOR_TOPIC, 0),
            (LED_TOPIC, 0)
        ]

        # Bind callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Services (NO DB_PATH)
        self.sensor_service = SensorService()
        self.device_service = DeviceService()

        self._thread = None


    # ----------------------------------------------------------
    # MQTT CONNECT CALLBACK
    # ----------------------------------------------------------
    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"✔ MQTT connected to {self.broker}:{self.port} (rc={rc})")

        for topic, qos in self.topics:
            client.subscribe(topic, qos)
            logger.info(f"📡 Subscribed to: {topic}")


    # ----------------------------------------------------------
    # MQTT MESSAGE CALLBACK
    # ----------------------------------------------------------
    def on_message(self, client, userdata, message):

        raw = message.payload.decode()
        topic = message.topic

        logger.info(f"📥 MQTT message: {topic} → {raw}")

        # Try parsing JSON
        try:
            parsed = json.loads(raw)
        except:
            parsed = raw.strip().lower()

        # ------------------------------
        # SENSOR DATA
        # ------------------------------
        if topic == SENSOR_TOPIC:
            try:
                if isinstance(parsed, dict) and \
                   "temperature" in parsed and \
                   "humidity" in parsed:

                    temp = parsed["temperature"]
                    humid = parsed["humidity"]

                    self.sensor_service.insert_sensor_data(temp, humid)
                    logger.info(f"💾 Stored sensor data: T={temp} H={humid}")

                else:
                    logger.warning(f"⚠ Invalid sensor payload: {parsed}")

            except Exception as e:
                logger.exception("❌ Failed to process sensor MQTT message", exc_info=e)

        # ------------------------------
        # LED CONTROL (ONE TOPIC)
        # ------------------------------
        elif topic == LED_TOPIC:
            try:
                # Expected: {"status": "on"} OR {"state": "off"}
                status = None

                if isinstance(parsed, dict):
                    status = parsed.get("status") or parsed.get("state")
                else:
                    status = parsed  # raw string

                if status in ("on", "off", "1", "0"):
                    final = "on" if status in ("on", "1") else "off"
                    self.device_service.update_led_status(final)
                    logger.info(f"💡 LED updated → {final}")
                else:
                    logger.warning(f"⚠ Unknown LED payload: {raw}")

            except Exception as e:
                logger.exception("❌ Failed to process LED MQTT message", exc_info=e)

        else:
            logger.warning(f"📨 Unknown MQTT topic received: {topic}")


    # ----------------------------------------------------------
    # START MQTT LOOP
    # ----------------------------------------------------------
    def start(self):
        if self._thread and self._thread.is_alive():
            return

        def run_loop():
            try:
                logger.info("🚀 Starting MQTT loop…")
                self.client.connect(self.broker, self.port, 60)
                self.client.loop_forever()
            except Exception as e:
                logger.exception("❌ MQTT loop terminated", exc_info=e)

        self._thread = threading.Thread(target=run_loop, daemon=True)
        self._thread.start()


    # ----------------------------------------------------------
    # PUBLISH HELPER
    # ----------------------------------------------------------
    def publish(self, topic, payload, qos=0, retain=False):
        try:
            logger.info(f"📤 Publishing → {topic}: {payload}")
            self.client.publish(topic, payload, qos=qos, retain=retain)
        except Exception as e:
            logger.exception("❌ Failed to publish MQTT message", exc_info=e)


# Global singleton
mqtt_client = MQTTClientWrapper()
