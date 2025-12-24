import time
import json
import network
from machine import Pin
from config import (
    WIFI_SSID, WIFI_PASSWORD,
    DHT_PIN, LED_PIN, IR_LED_PIN_RECEIVER,
    TOPIC_SENSOR, TOPIC_AC, TOPIC_TV, LEARN_REQUEST_TOPIC, LEARN_RESULT_TOPIC, IR_SEND_TOPIC,
    SENSOR_PUBLISH_INTERVAL, WIFI_CONNECT_TIMEOUT
)
from drivers.dht_drivers import DHTDriver
from mqtt.mqtt_client import MQTTClientWrapper
from drivers.IR_Blaster import IRBlaster
from drivers.IR_receiver import IRReceiver
from devices.tv import TV
from devices.ac import AC
import ujson


# -------------------------
# Hardware
# -------------------------
led = Pin(LED_PIN, Pin.OUT)
dht_drv = DHTDriver(DHT_PIN)

ir = IRBlaster()
ir_rx = IRReceiver(pin=IR_LED_PIN_RECEIVER)

learning_request = None

def load_codes(path):
    with open(path) as f:
        return ujson.load(f)

tv_codes = load_codes("IR_codes/TV/bedroom_tv.json")
ac_codes = load_codes("IR_codes/AC/bedroom_ac.json")

devices = {
    "tv": TV("tv", ir, tv_codes),
    "ac": AC("ac", ir, ac_codes)
}


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
    global last_tv_command_time, last_ac_command_time, learning_request

    t = topic.decode() if isinstance(topic, bytes) else topic
    payload = msg.decode() if isinstance(msg, bytes) else msg

    print("MQTT:", t, payload)

    try:
        data = json.loads(payload)
        state = data.get("state") or data.get("status")
    except Exception:
        state = payload.lower().strip()

    now = time.time()

    if t == (LEARN_REQUEST_TOPIC.decode() if isinstance(LEARN_REQUEST_TOPIC, bytes) else LEARN_REQUEST_TOPIC):
        try:
            data = json.loads(msg.decode())
            learning_request = data
            print("IR learning requested:", data)
        except Exception as e:
            print("Invalid learn request", e)
    
        # ---------- IR SEND (RAW) ----------
    if t == (IR_SEND_TOPIC.decode() if isinstance(IR_SEND_TOPIC, bytes) else IR_SEND_TOPIC):
        try:
            data = json.loads(payload)

            protocol = data.get("protocol")
            code = data.get("code")

            if protocol != "raw" or not code:
                print("Invalid IR send payload")
                return

            # Code may arrive as string → parse
            if isinstance(code, str):
                code = json.loads(code)

            ir_queue.append(("raw", code))
            print("RAW IR queued")

        except Exception as e:
            print("Failed to queue IR send:", e)

        return


    # ---------- TV ----------
    if t == (TOPIC_TV.decode() if isinstance(TOPIC_TV, bytes) else TOPIC_TV):
        if now - last_tv_command_time < TV_COOLDOWN_SEC:
            print("TV cooldown active")
            return

        if state == device_state["tv"]:
            print("TV already", state)
            return

        if state in ("on", "1"):
            ir_queue.append(("tv", "on"))
            device_state["tv"] = "on"
            last_tv_command_time = now
            print("TV -> ON queued")

        elif state in ("off", "0"):
            ir_queue.append(("tv", "off"))
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
            #ir_queue.append((ac_on, "ac", "on"))
            ir_queue.append(("ac", "on"))
            device_state["ac"] = "on"
            last_ac_command_time = now
            print("AC -> ON queued")

        elif state in ("off", "0"):
            #ir_queue.append((ac_off, "ac", "off"))
            ir_queue.append(("ac", "off"))
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
    mqtt_client.subscribe(LEARN_REQUEST_TOPIC)
    mqtt_client.subscribe(IR_SEND_TOPIC)

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
    
    global learning_request
    mqtt_client.on_message_cb = on_mqtt_message
    
    learning_request = None

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

            # ---- IR processing ----
            
            # ---- IR LEARNING MODE ----
            if learning_request:
                req = learning_request
                learning_request = None
                
                device_id = req["device_id"]
                action = req["action"]

                print("Learning IR for:", action)
                #time.sleep(1.5)
                print("👉 Point the remote and press the button NOW")
                
                led.value(1)
                pulses = ir_rx.capture(timeout_us=2000000)
                led.value(0)

                if pulses:
                    mqtt_client.publish(
                        LEARN_RESULT_TOPIC,
                        json.dumps({
                            "device_id": device_id,
                            "action": action,
                            "protocol": "raw",
                            "code": pulses
                        })
                    )
                    print("IR code captured & sent")
                else:
                    mqtt_client.publish(
                        LEARN_RESULT_TOPIC,
                        json.dumps({
                            "device_id": device_id,
                            "action": action,
                            "error": "timeout"
                        })
                    )
                    print("IR capture timeout")

                learning_request = None
                continue  

            if ir_queue:
                kind, payload = ir_queue.pop(0)

                if kind == "raw":
                    print("Sending RAW IR")
                    ir.send_raw(payload)
                    time.sleep(0.2)

                elif kind in devices:
                    devices[kind].send(payload)
                    print(f"IR SENT: {kind} -> {payload}")
                    time.sleep(0.2)

                else:
                    print("Unknown IR queue item:", kind)



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


