import React, { useState, useEffect } from "react";
import axios from "axios";

const CurrentSensorData = ({ liveData }) => {
  const [latest, setLatest] = useState(null);

  // 1. Load latest data from backend once at startup
  useEffect(() => {
    const fetchLatest = async () => {
      try {
        const res = await axios.get("http://localhost:5000/api/v1/sensors/latest");
        const arr = res.data.data || [];
        if (arr.length > 0) {
          setLatest(arr[0]);        // backend already returns sorted desc
        }
      } catch (err) {
        console.error("Failed to fetch latest sensor data:", err);
      }
    };

    fetchLatest();
    const interval = setInterval(fetchLatest, 5000); // optional refresher
    return () => clearInterval(interval);
  }, []);

  // 2. Inject real-time MQTT live updates
  useEffect(() => {
    if (!liveData) return;

    const withTimestamp = {
      ...liveData,
      timestamp: liveData.timestamp || new Date().toISOString(),
    };

    setLatest(withTimestamp);
  }, [liveData]);

   // Helper function to format timestamp
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return "";

    // Create a Date object from the timestamp
    const date = new Date(timestamp);

    // Format the date to the desired format: DD-MM-YYYY HH:mm
    return date.toLocaleString("en-GB", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,  // 24-hour format
    });
  };

  return (
    <div className="card" style={{ textAlign: "center", padding: "15px" }}>
      <h2>Current Sensor Data</h2>

      {!latest ? (
        <p className="label">Waiting for data...</p>
      ) : (
        <>
          {/* Header */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-around",
              fontWeight: "700",
              marginTop: "5px",
              marginBottom: "5px",
              fontSize: "18px",
            }}
          >
            <span>Temperature</span>
            <span>Humidity</span>
          </div>

          {/* Values */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-around",
              fontSize: "24px",
              fontWeight: "600",
              marginBottom: "10px",
            }}
          >
            <span>{latest.temperature} °C</span>
            <span>{latest.humidity} %</span>
          </div>

          {/* Timestamp */}
          <p className="label">{formatTimestamp(latest.timestamp)}</p>
        </>
      )}
    </div>
  );
};

export default CurrentSensorData;

