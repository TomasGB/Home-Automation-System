/*
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
        <button onClick={onClose} style={{ margin: "10px 5px" }}>Cancel</button>
      </div>
    </div>
  );
};

export default AddDeviceModal;
*/

import React, { useState } from "react";
import { authFetch } from "../api/authFetch";
import { TOPIC_BASE } from "../api/config";

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
        mqtt_topic: TOPIC_BASE + topic, // Use the prefix when sending the topic
      }),
    });

    if (res.success) {
      onAdded();     // reload device list
      onClose();      // close modal
    } else {
      console.error("Device creation failed:", res.error);
    }
  };

  // Update the topic to include the prefix when the user types
  const handleTopicChange = (e) => {
    setTopic(e.target.value.replace(new RegExp(`^${TOPIC_BASE}`), "")); // Remove any existing prefix if the user deletes part of it
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
          value={TOPIC_BASE + topic} // Show the prefix and the user's input
          onChange={handleTopicChange} // Update the topic state correctly
        />

        <button onClick={save}>Add Device</button>
        <button onClick={onClose} style={{ margin: "10px 5px" }}>Cancel</button>
      </div>
    </div>
  );
};

export default AddDeviceModal;
