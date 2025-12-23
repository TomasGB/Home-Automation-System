
import json
import threading
import paho.mqtt.client as mqtt
import logging
from app.config import Config
from app.services.sensor_service import SensorService
from app.models.device_model import DeviceModel
from app.models.device_action_model import DeviceActionModel

logger = logging.getLogger(__name__)

# Topics
BASE = Config.MQTT_BASE_TOPIC

SENSOR_TOPIC = f"{BASE}/sensor/data"
DEVICE_WILDCARD = f"{BASE}/+/state"
LEARN_RESULT_TOPIC = f"{BASE}/ir/learn/result"


class MQTTClientWrapper:

    def __init__(self):
        logger.info("🔥 MQTT: Initializing MQTTClientWrapper")

        self.client = mqtt.Client()

        self.broker = Config.MQTT_BROKER
        self.port = Config.MQTT_PORT

        # Subscribe to sensor + ALL devices
        self.topics = [
            (SENSOR_TOPIC, 0),
            (DEVICE_WILDCARD, 0),
            (LEARN_RESULT_TOPIC, 0),
        ]

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.sensor_service = SensorService()

        self._thread = None

    # ----------------------------------------------------------
    # MQTT CONNECT
    # ----------------------------------------------------------
    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"✔ MQTT connected to {self.broker}:{self.port} (rc={rc})")

        for topic, qos in self.topics:
            client.subscribe(topic, qos)
            logger.info(f"📡 Subscribed to: {topic}")

    # ----------------------------------------------------------
    # MQTT MESSAGE
    # ----------------------------------------------------------
    def on_message(self, client, userdata, message):

        raw = message.payload.decode()
        topic = message.topic

        logger.info(f"📥 MQTT message: {topic} → {raw}")

        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = raw.strip().lower()
        
        # ------------------------------
        # IR LEARN RESULT
        # ------------------------------
        if topic == LEARN_RESULT_TOPIC:
            try:
                if not isinstance(parsed, dict):
                    logger.error("Invalid learn result payload format")
                    return

                self.handle_learn_result(parsed)
                return

            except Exception as e:
                logger.exception("❌ Learn result error", exc_info=e)

            return
        # ------------------------------
        # SENSOR DATA
        # ------------------------------
        elif topic == SENSOR_TOPIC:
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
                logger.exception("❌ Sensor MQTT error", exc_info=e)

            return
        # ------------------------------
        # GENERIC DEVICE STATE
        # ------------------------------
        elif topic.startswith(f"{BASE}/") and topic.endswith("/state"):
            try:
                if isinstance(parsed, dict):
                    value = parsed.get("state") or parsed.get("status")
                else:
                    value = parsed

                if value is None:
                    logger.warning(f"⚠ No usable payload for {topic}")
                    return

                value = str(value).lower().strip()

                if value not in ("on", "off", "1", "0"):
                    logger.warning(f"⚠ Invalid device payload '{value}' on {topic}")
                    return

                final = "on" if value in ("on", "1") else "off"

                # 🔍 Find device by topic
                device = DeviceModel.get_by_mqtt_topic(topic)

                if not device:
                    logger.warning(f"📨 No device registered for topic: {topic}")
                    return

                # 💾 Update DB
                DeviceModel.update_status(device["id"], final)

                logger.info(f"🔄 Device '{device['name']}' updated → {final}")

            except Exception as e:
                logger.exception("❌ Device MQTT error", exc_info=e)
            
            return

    # ----------------------------------------------------------
    # START LOOP
    # ----------------------------------------------------------
    def start(self):
        if self._thread and self._thread.is_alive():
            return

        def run():
            try:
                logger.info("🚀 Starting MQTT loop…")
                self.client.connect(self.broker, self.port, 60)
                self.client.loop_forever()
            except Exception as e:
                logger.exception("❌ MQTT loop stopped", exc_info=e)

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    # ----------------------------------------------------------
    # PUBLISH
    # ----------------------------------------------------------
    def publish(self, topic, payload, qos=0, retain=True):
        try:
            if topic == LEARN_RESULT_TOPIC:
                retain=False
                
            logger.info(f"📤 Publishing → {topic}: {payload}")
            self.client.publish(topic, payload, qos=qos, retain=retain)
        except Exception as e:
            logger.exception("❌ MQTT publish failed", exc_info=e)

    # ----------------------------------------------------------
    # LEARN IR CODE
    # ----------------------------------------------------------

    def handle_learn_result(self, data):
        """
        Expected payload:
        {
          device_id: int,
          action: str,
          protocol: str,
          code: list
        }
        """
        logger.info(f"🧠 Handling IR learn result: {data}")

        if data.get("error"):
            logger.warning(f"IR learn failed: {data}")
            return

        device_id = data.get("device_id")
        action = data.get("action")
        protocol = data.get("protocol")
        code = data.get("code")

        if not all([device_id, action, protocol, code]):
            logger.error("Invalid learn result payload")
            return

        DeviceActionModel.create(
            device_id=device_id,
            action=action,
            protocol=protocol,
            code=json.dumps(code)
        )

        logger.info(
            f"Saved IR action '{action}' for device {device_id}"
        )


mqtt_client = MQTTClientWrapper()

