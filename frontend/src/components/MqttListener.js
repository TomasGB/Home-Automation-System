
import { useEffect } from "react";
import mqtt from "mqtt";

const SENSOR_TOPIC = "home/sensor/data";
const LED_TOPIC = "home/led/status";

const MqttListener = ({ onData, onLed }) => {
  useEffect(() => {
    const client = mqtt.connect("wss://test.mosquitto.org:8081");

    client.on("connect", () => {
      console.log("MQTT WebSocket connected!");
      client.subscribe(SENSOR_TOPIC);
      client.subscribe(LED_TOPIC);
    });

    client.on("message", (topic, msg) => {
      const raw = msg.toString();
      try {
        // try JSON first
        const parsed = JSON.parse(raw);

        if (topic === SENSOR_TOPIC && onData) onData(parsed);
        if (topic === LED_TOPIC && onLed) onLed(parsed);
      } catch (err) {
        // not JSON — handle simple payloads (e.g. "on" / "off")
        if (topic === SENSOR_TOPIC && onData) {
          // If sensor sends plain values (unlikely) we still forward as raw
          onData({ raw: raw });
        }
        if (topic === LED_TOPIC && onLed) {
          const normalized = raw.trim().toLowerCase();
          // Support "on", "off", "1", "0" and also "{"status":"on"}" handled above
          if (["on", "off", "1", "0"].includes(normalized)) {
            onLed({ status: normalized === "1" ? "on" : (normalized === "0" ? "off" : normalized) });
          } else {
            // forward as raw if unknown format
            onLed({ raw: raw });
          }
        }
      }
    });

    client.on("error", (e) => console.error("MQTT error (frontend):", e));

    return () => client.end();
  }, [onData, onLed]);

  return null;
};

export default MqttListener;
