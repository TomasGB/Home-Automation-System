import { useEffect, useState } from "react";
import mqtt from "mqtt";
import { TOPIC_BASE } from "../api/config";
import { authFetch } from "../api/authFetch";

const SENSOR_TOPIC = `${TOPIC_BASE}/sensor/data`;

const MqttListener = ({ onData, onDevice }) => {
  const [deviceTopics, setDeviceTopics] = useState([]);

  useEffect(() => {
    // Fetch devices list from API (async)
    const fetchDevices = async () => {
      try {
        const response = await authFetch("devices");
        const mqttTopics = response.data.map(device => device.mqtt_topic);
        // Dynamically generate topics for each device
        const deviceNames = mqttTopics.map(topic => topic.split('/')[2]); // Extract device names
        const topics = deviceNames.map(name => `${TOPIC_BASE}/${name}/state`); // Create topics like: 'mqtt-explorer-ba30a458/home/lights/state'
        setDeviceTopics(topics); // Set the dynamic topics to state
      } catch (error) {
        console.error("Failed to fetch devices:", error);
      }
    };

    fetchDevices();

  }, []); // Empty dependency array means it runs once after initial render

  useEffect(() => {
    if (deviceTopics.length === 0) return; // No topics to subscribe to yet

    const client = mqtt.connect("wss://test.mosquitto.org:8081");

    client.on("connect", () => {
      console.log("MQTT WebSocket connected!");
      client.subscribe(SENSOR_TOPIC); // Subscribe to the sensor topic

      // Subscribe to each device topic dynamically
      deviceTopics.forEach(topic => {
        client.subscribe(topic, (err) => {
          if (err) {
            console.error(`Failed to subscribe to ${topic}`);
          } else {
            console.log(`Subscribed to ${topic}`);
          }
        });
      });
    });

    client.on("message", (topic, msg) => {
      const raw = msg.toString();
      try {
        // Try to parse JSON payload
        const parsed = JSON.parse(raw);

        if (topic === SENSOR_TOPIC && onData) onData(parsed);
        if (deviceTopics.includes(topic) && onDevice) onDevice(parsed); // Check if topic is one of the device topics
      } catch (err) {
        // Handle non-JSON payloads (e.g., "on", "off")
        if (topic === SENSOR_TOPIC && onData) {
          onData({ raw: raw });
        }
        if (deviceTopics.includes(topic) && onDevice) {
          const normalized = raw.trim().toLowerCase();
          if (["on", "off", "1", "0"].includes(normalized)) {
            onDevice({ status: normalized === "1" ? "on" : (normalized === "0" ? "off" : normalized) });
          } else {
            onDevice({ raw: raw });
          }
        }
      }
    });

    client.on("error", (e) => console.error("MQTT error (frontend):", e));

    return () => client.end(); // Clean up on unmount
  }, [deviceTopics, onData, onDevice]); // This effect depends on deviceTopics

  return null;
};

export default MqttListener;
