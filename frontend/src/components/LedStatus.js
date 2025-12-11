import React, { useState, useEffect } from "react";
import { getLedStatus, setLedState } from "../api/devices";

const LedStatus = ({ liveLed }) => {
  const [led, setLed] = useState("off");
  const [loading, setLoading] = useState(true);

  // Normalize any LED value into "on" or "off"
  const normalizeLed = (value) => {
    if (!value) return null;

    if (value === "on" || value === "off") return value;

    const lower = String(value).trim().toLowerCase();

    if (["on", "1"].includes(lower)) return "on";
    if (["off", "0"].includes(lower)) return "off";

    return null;
  };

  // 1. Load LED status from backend
  useEffect(() => {
    const loadStatus = async () => {
      try {
        const res = await getLedStatus();

        let raw =
          res?.data?.state ??
          res?.state ??
          res?.status ??
          res ??
          null;

        const normalized = normalizeLed(raw);

        if (normalized) setLed(normalized);
      } catch (err) {
        console.error("Failed to load LED state:", err);
      } finally {
        setLoading(false);
      }
    };

    loadStatus();
  }, []);

  // 2. Live MQTT LED updates
  useEffect(() => {
    if (!liveLed) return;

    // liveLed may be: {status:"on"} OR {raw:"on"} OR {whatever}
    const raw =
      liveLed?.status ??
      liveLed?.state ??
      liveLed?.raw ??
      liveLed;

    const normalized = normalizeLed(raw);

    if (normalized) {
      setLed(normalized);
      console.log("Live LED update:", normalized);
    }
  }, [liveLed]);

  // 3. Toggle LED manually
  const toggleLed = async () => {
    const next = led === "on" ? "off" : "on";

    try {
      const res = await setLedState(next);

      let raw =
        res?.data?.state ??
        res?.state ??
        res?.status ??
        res ??
        null;

      const normalized = normalizeLed(raw);

      if (normalized) setLed(normalized);
    } catch (err) {
      console.error("Failed to toggle LED:", err);
    }
  };

  return (
    <div className="card" style={{ width: "280px", textAlign: "center" }}>
      <h2>LED Status</h2>

      {loading || !led ? (
        <p className="label">Loading...</p>
      ) : (
        <>
          <div
            className="value"
            style={{ color: led === "on" ? "green" : "red" }}
          >
            {led.toUpperCase()}
          </div>

          <button onClick={toggleLed}>
            Turn {led === "on" ? "off" : "on"}
          </button>
        </>
      )}
    </div>
  );
};

export default LedStatus;
