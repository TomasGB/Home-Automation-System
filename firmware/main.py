import time
import json
import network
from machine import Pin
from config import (
    WIFI_SSID, WIFI_PASSWORD,
    DHT_PIN, LED_PIN,
    TOPIC_SENSOR, TOPIC_AC, TOPIC_TV,
    SENSOR_PUBLISH_INTERVAL, WIFI_CONNECT_TIMEOUT
)
from drivers.dht_drivers import DHTDriver
from mqtt.mqtt_client import MQTTClientWrapper
from drivers.IR_Blaster import IRBlaster
from drivers.ir_codes import tv_on, tv_off, ac_on, ac_off

# -------------------------
# Hardware
# -------------------------
led = Pin(LED_PIN, Pin.OUT)
dht_drv = DHTDriver(DHT_PIN)

ir = IRBlaster()

# -------------------------
# State & Queue
# -------------------------
ir_queue = []

device_state = {
    "tv": None,
    "ac": None
}

TV_COOLDOWN_SEC = 2
AC_COOLDOWN_SEC = 3

last_tv_command_time = 0
last_ac_command_time = 0

# -------------------------
# MQTT
# -------------------------
mqtt_client = MQTTClientWrapper()

# -------------------------
# Wi-Fi
# -------------------------
def connect_wifi(timeout=WIFI_CONNECT_TIMEOUT):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        return True

    print("Connecting Wi-Fi...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            return False
        time.sleep(0.5)

    print("Wi-Fi connected:", wlan.ifconfig())
    return True

# -------------------------
# MQTT Message Handler
# -------------------------
def on_mqtt_message(topic, msg):
    global last_tv_command_time, last_ac_command_time

    t = topic.decode() if isinstance(topic, bytes) else topic
    payload = msg.decode() if isinstance(msg, bytes) else msg

    print("MQTT:", t, payload)

    try:
        data = json.loads(payload)
        state = data.get("state") or data.get("status")
    except Exception:
        state = payload.lower().strip()

    now = time.time()

    # ---------- TV ----------
    if t == (TOPIC_TV.decode() if isinstance(TOPIC_TV, bytes) else TOPIC_TV):
        if now - last_tv_command_time < TV_COOLDOWN_SEC:
            print("TV cooldown active")
            return

        if state == device_state["tv"]:
            print("TV already", state)
            return

        if state in ("on", "1"):
            ir_queue.append((tv_on, "tv", "on"))
            device_state["tv"] = "on"
            last_tv_command_time = now
            print("TV -> ON queued")

        elif state in ("off", "0"):
            ir_queue.append((tv_off, "tv", "off"))
            device_state["tv"] = "off"
            last_tv_command_time = now
            print("TV -> OFF queued")

    # ---------- AC ----------
    elif t == (TOPIC_AC.decode() if isinstance(TOPIC_AC, bytes) else TOPIC_AC):
        if now - last_ac_command_time < AC_COOLDOWN_SEC:
            print("AC cooldown active")
            return

        if state == device_state["ac"]:
            print("AC already", state)
            return

        if state in ("on", "1"):
            ir_queue.append((ac_on, "ac", "on"))
            device_state["ac"] = "on"
            last_ac_command_time = now
            print("AC -> ON queued")

        elif state in ("off", "0"):
            ir_queue.append((ac_off, "ac", "off"))
            device_state["ac"] = "off"
            last_ac_command_time = now
            print("AC -> OFF queued")

# -------------------------
# MQTT Connect
# -------------------------
def ensure_mqtt():
    if mqtt_client.connected:
        return True

    if not mqtt_client.connect():
        return False

    mqtt_client.subscribe(TOPIC_TV)
    mqtt_client.subscribe(TOPIC_AC)
    print("MQTT subscribed")

    return True

# -------------------------
# Sensor Publish
# -------------------------
def publish_sensor():
    t, h = dht_drv.read()
    if t is None or h is None:
        return

    payload = json.dumps({
        "temperature": t,
        "humidity": h
    })

    mqtt_client.publish(TOPIC_SENSOR, payload)

# -------------------------
# Main
# -------------------------
def main():
    mqtt_client.on_message_cb = on_mqtt_message

    if not connect_wifi():
        print("Wi-Fi failed, rebooting")
        time.sleep(5)
        import machine
        machine.reset()

    while not ensure_mqtt():
        time.sleep(2)

    last_sensor = time.time()

    while True:
        try:
            mqtt_client.check_msg()

            # ---- IR queue processing ----
            if ir_queue:
                item = ir_queue.pop(0)

                if isinstance(item, tuple) and len(item) == 3:
                    ir_cmd, dev, state = item
                    if dev == "ac":
                        ir.send(ir_cmd, repeats=3, gap_ms=180)
                    else:
                        ir.send(ir_cmd)
                    print(f"IR SENT: {dev} -> {state}")
                    time.sleep(0.2)
                else:
                    print("Invalid IR item:", item)


            # ---- Sensors ----
            if time.time() - last_sensor > SENSOR_PUBLISH_INTERVAL:
                publish_sensor()
                last_sensor = time.time()

            if not mqtt_client.connected:
                ensure_mqtt()

        except Exception as e:
            print("Main loop error:", e)
            mqtt_client.disconnect()
            time.sleep(2)
            ensure_mqtt()

        time.sleep(0.05)

# -------------------------
if __name__ == "__main__":
    main()

