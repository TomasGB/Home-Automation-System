import React, { useState, useEffect } from "react";
import { setDeviceState, deleteDevice, onDeleted } from "../api/devices";

const DeviceCard = ({ device, liveUpdate, onDeleted, onEdit }) => {
  const [state, setState] = useState(device.status);

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

  return (
    <div className="card" style={{ width: "280px", textAlign: "center", margin: "0px 0px 15px 0px"}}>
      <div style={{margin: "0px 0px 0px 0px", display: "flex", gap: "70%", justifyContent: "center" }}>
        <button style={{ backgroundColor:"white", fontSize:"20px"}} onClick={() => onEdit(device)}>✏️</button>
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
