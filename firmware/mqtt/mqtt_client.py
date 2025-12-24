# mqtt/mqtt_client.py
import time
import ubinascii
import machine
import json
from umqtt.simple import MQTTClient
from config import MQTT_BROKER, MQTT_PORT, MQTT_CLIENT_ID_PREFIX, TOPIC_AC, TOPIC_TV, TOPIC_STATUS

class MQTTClientWrapper:
    def __init__(self, on_message_cb=None):
        self.client = None
        self.on_message_cb = on_message_cb
        # create client id from unique id
        uid = ubinascii.hexlify(machine.unique_id()).decode()
        self.client_id = MQTT_CLIENT_ID_PREFIX + uid
        self.connected = False

    def _internal_cb(self, topic, msg):
        try:
            if self.on_message_cb:
                self.on_message_cb(topic, msg)
        except Exception as e:
            print("MQTT cb error:", e)


    def connect(self):
        """Create client and connect. Returns True on success."""
        try:
            self.client = MQTTClient(self.client_id,MQTT_BROKER,port=MQTT_PORT,keepalive=60)
            self.client.set_callback(self._internal_cb)
            self.client.connect()
            self.connected = True
            # Publish online status
            try:
                self.client.publish(TOPIC_STATUS, b'{"status":"online"}')
            except Exception:
                pass
            return True
        except Exception as e:
            print("MQTT connect failed:", e)
            self.connected = False
            self.client = None
            return False

    def subscribe(self, topic):
        if not self.connected:
            return False
        try:
            self.client.subscribe(topic)
            return True
        except Exception as e:
            print("Subscribe failed:", e)
            return False

    def check_msg(self):
        if not self.connected or not self.client:
            return
        try:
            self.client.check_msg()  # non-blocking; will call callback on message
        except OSError as e:
            print("MQTT check_msg OSError:", e)
            self.connected = False
            self.client = None

    def publish(self, topic, payload, retain=False):
        if not self.connected or not self.client:
            print("MQTT publish: client not connected")
            return False
        try:
            if isinstance(payload, str):
                payload = payload.encode()
            self.client.publish(topic, payload, retain=retain)
            return True
        except Exception as e:
            print("MQTT publish failed:", e)
            return False

    def disconnect(self):
        try:
            if self.client:
                self.client.disconnect()
        except Exception:
            pass
        self.connected = False
        self.client = None

