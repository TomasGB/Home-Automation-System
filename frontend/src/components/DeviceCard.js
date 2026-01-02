import React, { useState, useEffect } from "react";
import {
  setDeviceState,
  deleteDevice,
  learnDeviceAction,
  getDeviceActions,
  triggerDeviceAction,
  getDevices
} from "../api/devices";

const DeviceCard = ({ device, liveUpdate, onDeleted, onEdit }) => {
  const [state, setState] = useState(device.status ?? "unknown");
  const [learning, setLearning] = useState(false);
  const [actionName, setActionName] = useState("");
  const [learningStatus, setLearningStatus] = useState("idle"); // idle | listening | success | error
  const [learningMessage, setLearningMessage] = useState("");
  const [actions, setActions] = useState([]);
  const [selectedAction, setSelectedAction] = useState("");
  const [actionStatus, setActionStatus] = useState("");


  // Normalize Devices/switch values
  const normalize = (v) => {
    if (!v) return null;
    v = String(v).trim().toLowerCase();
    if (["on", "1", "true"].includes(v)) return "on";
    if (["off", "0", "false"].includes(v)) return "off";
    return null;
  };

  // Set updated device status
  useEffect(() => {
    if (device.status) {
      setState(device.status);
    }
  }, [device.status]);


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

  // load actions on mount
  useEffect(() => {
    const loadActions = async () => {
      try {
        const res = await getDeviceActions(device.id);
        if (res.success) {
          setActions(res.data);
        }
      } catch (e) {
        console.error("Failed to load actions", e);
      }
    };

    loadActions();
  }, [device.id]);

  const triggerAction = async () => {
    if (!selectedAction) return;

    setActionStatus("Sending IR command...");

    try {
      const res = await triggerDeviceAction(device.id, selectedAction);

      if (res.success) {
        setActionStatus("Action sent successfully");
        if (["on", "off"].includes(selectedAction)) {
          setState(selectedAction);
        }
      } else {
        setActionStatus("Failed to send action");
      }
    } catch (e) {
      console.error(e);
      setActionStatus("ESP32 not responding");
    }
    setTimeout(() => setActionStatus(""), 2000);
    setSelectedAction("");
  };

  const remove = async () => {
    if (!window.confirm("Delete this device?")) return;
    const res = await deleteDevice(device.id);
    if (res.success) onDeleted();
  };

  // ✅ Correct learning handler
  const resetLearningUI = () => {
    setLearning(false);
    setLearningStatus("idle");
    setLearningMessage("");
    setActionName("");
  };

  const prepareLearning = () => {
    if (!actionName.trim()) return;

    setLearningStatus("ready");
    setLearningMessage("Get the remote ready, then click START");
  };


  const startLearning = async () => {
  if (!actionName) return;

  try {
    const res = await learnDeviceAction(device.id, actionName);

    alert(
      "Learning mode started.\n\n" +
      "👉 Point the remote at the ESP32\n" +
      "👉 Press the button ONCE\n" +
      "👉 Wait a few seconds\n" +
      "👉 Then click Ok"
    );

    if (res?.success !== false) {
        setLearningStatus("success");
        setLearningMessage("IR action learned successfully");
      } else {
        setLearningStatus("error");
        setLearningMessage("Failed to learn IR action");
      }
    } catch (err) {
      console.error(err);
      setLearningStatus("error");
      setLearningMessage("Timeout or communication error");
    }

    setTimeout(resetLearningUI, 2500);
  //}
  setActionName("");
  setLearning(false);
  };


  return (
    <div
      className="card"
      style={{ width: "280px", textAlign: "center", marginBottom: "15px" }}
    >
      
      <div className="status-container">
        <h2 style={{ margin: "4px 0px 10px 0px", fontSize: "1.2rem" }}>
        {device.name}
        </h2>
        <div
          className={`status-dot ${state === "on" ? "on" : "off"}`}
          title={state}
        />
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "8px"
        }}
      >
        

        <div style={{ display: "flex", width:"100%", gap: "6px", justifyContent: "space-evenly"}}>
          <button onClick={() => onEdit(device)}>✏️</button>
          <button onClick={() => setLearning(true)}>New Action ✨</button>
          <button onClick={remove}>🗑️</button>
        </div>
      </div>
      {learning && (
        <div className="learn-panel">

          <input
            placeholder="Action name (e.g. volume_up)"
            value={actionName}
            onChange={(e) => setActionName(e.target.value)}
            disabled={learningStatus === "listening"}
          />

          {learningStatus === "idle" && (
            <button onClick={prepareLearning}>
              Prepare
            </button>
          )}

          {learningStatus === "ready" && (
            <button onClick={startLearning}>
              START
            </button>
          )}

          {learningStatus === "listening" && (
            <div style={{ color: "orange", fontWeight: "bold" }}>
              ⏺ Listening…
            </div>
          )}

          {learningStatus === "success" && (
            <div style={{ color: "green" }}>
              ✅ {learningMessage}
            </div>
          )}

          {learningStatus === "error" && (
            <div style={{ color: "red" }}>
              ❌ {learningMessage}
            </div>
          )}

          <button
            onClick={resetLearningUI}
            disabled={learningStatus === "listening"}
          >
            Cancel
          </button>

        </div>
      )}

      <div style={{ marginTop: "10px" }}>
        <div style={{ marginTop: "14px" }}>
          <label style={{ fontSize: "0.75rem", color: "#9ca3af" }}>
            Action
          </label>

          <select
            value={selectedAction}
            onChange={(e) => setSelectedAction(e.target.value)}
          >
            <option value="">Select action</option>
            {actions.map((a) => (
              <option key={a.action} value={a.action}>
                {a.action}
              </option>
            ))}
          </select>

          <button
            onClick={triggerAction}
            disabled={!selectedAction}
            style={{ marginTop: "8px", width: "100%" }}
          >
            ▶ Send Command
          </button>
        </div>

      {actionStatus && (
        <div style={{ marginTop: "6px", fontSize: "0.85rem" }}>
          {actionStatus}
        </div>
      )}
    </div>

    </div>
  );
};

export default DeviceCard;
