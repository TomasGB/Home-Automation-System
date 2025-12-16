import React, { useState, useEffect } from "react";
import { TOPIC_BASE } from "../api/config";
import { updateDevice, createDevice } from "../api/devices";

const AddDeviceModal = ({ device, onClose, onAdded }) => {
  const isEdit = !!device;

  const [name, setName] = useState("");
  const [type, setType] = useState("switch");
  const [topic, setTopic] = useState("");

  // ----------------------------------------
  // Initialize form when editing
  // ----------------------------------------
  useEffect(() => {
    if (device) {
      setName(device.name || "");
      setType(device.type || "switch");

      // Remove base topic if present
      if (device.mqtt_topic?.startsWith(TOPIC_BASE)) {
        setTopic(device.mqtt_topic.slice(TOPIC_BASE.length));
      } else {
        setTopic(device.mqtt_topic || "");
      }
    }
  }, [device]);

  // ----------------------------------------
  // Save (create or update)
  // ----------------------------------------
  const save = async () => {
    const payload = {
      name,
      type,
      mqtt_topic: `${TOPIC_BASE}${topic}`
    };

    const res = isEdit
      ? await updateDevice(device.id, payload)
      : await createDevice(payload);

    if (res?.success) {
      onAdded();
      onClose();
    } else {
      console.error("Device save failed:", res?.error);
    }
  };

  return (
    <div className="modal" style={{textAlign: "center" }}>
      <div className="card" style={{ width: "300px"}}>
        <h2>{isEdit ? "Edit Device" : "Add New Device"}</h2>

        <input
          className="input"
          placeholder="Device Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <select
          className="input"
          value={type}
          onChange={(e) => setType(e.target.value)}
        >
          <option value="switch">Switch / LED</option>
          <option value="sensor">Sensor</option>
        </select>

        <input
          className="input"
          placeholder="MQTT Topic"
          value={`${TOPIC_BASE}${topic}`}
          onChange={(e) => {
            const value = e.target.value;
            setTopic(
              value.startsWith(TOPIC_BASE)
                ? value.slice(TOPIC_BASE.length)
                : value
            );
          }}
        />

        <button onClick={save}>
          {isEdit ? "Update Device" : "Add Device"}
        </button>

        <button onClick={onClose} style={{ margin: "10px 5px" }}>
          Cancel
        </button>
      </div>
    </div>
  );
};

export default AddDeviceModal;
