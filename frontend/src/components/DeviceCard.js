/*
import React, { useState, useEffect } from "react";
import { setDeviceState, deleteDevice, onDeleted, learnDeviceAction  } from "../api/devices";

const DeviceCard = ({ device, liveUpdate, onDeleted, onEdit }) => {
  const [state, setState] = useState(device.status);
  const [learning, setLearning] = useState(false);
  const [actionName, setActionName] = useState("");

  // Normalize LED/switch values
  const normalize = (v) => {
    if (!v) return null;
    v = String(v).trim().toLowerCase();
    if (["on", "1", "true"].includes(v)) return "on";
    if (["off", "0", "false"].includes(v)) return "off";
    return null;
  };

  // Apply live MQTT updates
  useEffect(() => {
    if (!liveUpdate) return;

    const raw =
      liveUpdate?.status ??
      liveUpdate?.state ??
      liveUpdate?.raw ??
      liveUpdate;

    const normalized = normalize(raw);
    if (normalized) setState(normalized);
  }, [liveUpdate]);

  // Toggle device state
  const toggle = async () => {
    const next = state === "on" ? "off" : "on";
    const res = await setDeviceState(device.id, next);

    if (res.success) {
      setState(next);
    } else {
      console.error("Failed to toggle:", res.error);
    }
  };

  const remove = async () =>{
    if (!window.confirm("Delete this device?")) return;
    const res = await deleteDevice(device.id);
    if (res.success) onDeleted();
  }

  const startLearning = async () => {
    if (!actionName) return;

    try {
      await api.post(`/devices/${device.id}/learn-action`, {
        action: actionName
      });

      alert("Point the remote and press the button");
      setLearning(false);
      setActionName("");
    } catch (err) {
      console.error(err);
      alert("Failed to start learning");
    }
  };
  
  return (
    <div className="card" style={{ width: "280px", textAlign: "center", margin: "0px 0px 15px 0px"}}>
      <div style={{margin: "0px 0px 0px 0px", display: "flex", gap: "70%", justifyContent: "center" }}>
        <button style={{ backgroundColor:"white", fontSize:"20px"}} onClick={() => onEdit(device)}>✏️</button>
        <button style={{ backgroundColor:"white", fontSize:"20px"}} onClick={() => setLearning(true)}>
          Learn new action
        </button>
        {
          learning && (
          <div className="learn-panel">
            <input
              placeholder="Action name (e.g. volume_up)"
              value={actionName}
              onChange={(e) => setActionName(e.target.value)}
            />

            <button onClick={startLearning}>
              Start learning
            </button>

            <button onClick={() => setLearning(false)}>
              Cancel
            </button>
          </div>)
        }
        <button style={{ backgroundColor:"white", fontSize:"20px"}} onClick={remove}>🗑️</button>
      </div>
      <h2>{device.name}</h2>
      <div
        className="value"
        style={{ color: state === "on" ? "green" : "red" }}
      >
        {state.toUpperCase()}
      </div>

      <button onClick={toggle}>
        Turn {state === "on" ? "OFF" : "ON"}
      </button>
    </div>
  );
};

export default DeviceCard;

*/

import React, { useState, useEffect } from "react";
import {
  setDeviceState,
  deleteDevice,
  learnDeviceAction
} from "../api/devices";

const DeviceCard = ({ device, liveUpdate, onDeleted, onEdit }) => {
  const [state, setState] = useState(device.status);
  const [learning, setLearning] = useState(false);
  const [actionName, setActionName] = useState("");

  // Normalize LED/switch values
  const normalize = (v) => {
    if (!v) return null;
    v = String(v).trim().toLowerCase();
    if (["on", "1", "true"].includes(v)) return "on";
    if (["off", "0", "false"].includes(v)) return "off";
    return null;
  };

  // Apply live MQTT updates
  useEffect(() => {
    if (!liveUpdate) return;

    const raw =
      liveUpdate?.status ??
      liveUpdate?.state ??
      liveUpdate?.raw ??
      liveUpdate;

    const normalized = normalize(raw);
    if (normalized) setState(normalized);
  }, [liveUpdate]);

  // Toggle device state
  const toggle = async () => {
    const next = state === "on" ? "off" : "on";
    const res = await setDeviceState(device.id, next);

    if (res.success) {
      setState(next);
    } else {
      console.error("Failed to toggle:", res.error);
    }
  };

  const remove = async () => {
    if (!window.confirm("Delete this device?")) return;
    const res = await deleteDevice(device.id);
    if (res.success) onDeleted();
  };

  // ✅ Correct learning handler
  const startLearning = async () => {
  if (!actionName) return;

  try {
    await learnDeviceAction(device.id, actionName);

    alert(
      "Learning mode started.\n\n" +
      "👉 Point the remote at the ESP32\n" +
      "👉 Press the button ONCE\n" +
      "👉 Wait a few seconds"
    );
  } catch (err) {
    console.error(err);
    alert("Failed to start learning");
  }
  setActionName("");
  setLearning(false);
};


  return (
    <div
      className="card"
      style={{ width: "280px", textAlign: "center", marginBottom: "15px" }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "10px"
        }}
      >
        <button onClick={() => onEdit(device)}>✏️</button>

        <button onClick={() => setLearning(true)}>
          Learn new action
        </button>

        <button onClick={remove}>🗑️</button>
      </div>

      {learning && (
        <div className="learn-panel">
          <input style={{ margin: "5px", textAlign: "center" }}
            placeholder="Action name (e.g. volume_up)"
            value={actionName}
            onChange={(e) => setActionName(e.target.value)}
          />

          <button style={{ margin: "5px"}} onClick={startLearning}>
            Start learning
          </button>

          <button style={{ margin: "5px"}} onClick={() => setLearning(false)}>
            Cancel
          </button>
        </div>
      )}

      <h2>{device.name}</h2>

      <div
        className="value"
        style={{ color: state === "on" ? "green" : "red" }}
      >
        {state?.toUpperCase()}
      </div>

      <button onClick={toggle}>
        Turn {state === "on" ? "OFF" : "ON"}
      </button>
    </div>
  );
};

export default DeviceCard;
