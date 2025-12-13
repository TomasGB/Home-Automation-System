import React, { useState } from "react";
import { authFetch } from "../api/authFetch";

const AddDeviceModal = ({ onClose, onAdded }) => {
  const [name, setName] = useState("");
  const [type, setType] = useState("switch");
  const [topic, setTopic] = useState("");

  const save = async () => {
    const res = await authFetch("devices", {
      method: "POST",
      body: JSON.stringify({
        name,
        type,
        mqtt_topic: topic
      })
    });

    if (res.success) {
      onAdded();     // reload device list
      onClose();      // close modal
    } else {
      console.error("Device creation failed:", res.error);
    }
  };

  return (
    <div className="modal">
      <div className="card" style={{ width: "300px" }}>
        <h2>Add New Device</h2>

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
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />

        <button onClick={save}>Add Device</button>
        <button onClick={onClose} style={{ marginTop: "10px" }}>Cancel</button>
      </div>
    </div>
  );
};

export default AddDeviceModal;
