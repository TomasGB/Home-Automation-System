import React, { useState, useEffect } from "react";
import CurrentSensorData from "./components/CurrentSensorData";
import SensorGraph from "./components/SensorGraph";
import MqttListener from "./components/MqttListener";
import Login from "./components/Login";
import AddDeviceModal from "./components/AddDeviceModal";
import "./styles.css";

import DeviceCard from "./components/DeviceCard";
import { authFetch } from "./api/authFetch";



const App = () => {
  const [liveSensor, setLiveSensor] = useState(null);
  const [liveDevices, setLiveDevices] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));

  const [showAddDevice, setShowAddDevice] = useState(false);
  const [devices, setDevices] = useState([]);

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  // Load devices from backend
  const loadDevices = async () => {
    const res = await authFetch("devices");
    if (res.success) setDevices(res.data);
  };


  useEffect(() => {
    loadDevices();
  }, []);

  // Login screen
  if (!token) {
    return <Login onLogin={(tok) => setToken(tok)} />;
  }

  return (
    <>
      {/* Invisible MQTT listener */}
      <MqttListener
        onData={(d) => setLiveSensor(d)}
        onLed={(l) => setLiveDevices(l)}
      />

      {/* Modal for adding devices */}
      {showAddDevice && (
        <AddDeviceModal
          onClose={() => setShowAddDevice(false)}
          onAdded={loadDevices}
        />
      )}

      {/* Header */}
      <div className="header">
        <h1>🏠 Home Automation</h1>
        <div>
          <button onClick={() => setShowAddDevice(true)}>+ Add Device</button>
          <button onClick={logout}>Logout</button>
        </div>
      </div>

      {/* Main GRID */}
      <div className="grid">
        {/* Left: sensor information */}
        <div className="section-column">
          <CurrentSensorData liveData={liveSensor} />
          <SensorGraph liveData={liveSensor} />
        </div>

        {/* Right: cards for devices */}
        <div className="centered">
          {devices.map((dev) => (
            <DeviceCard
              key={dev.id}
              device={dev}
              liveUpdate={liveDevices}   // later: change to generic liveDevice system
            />
          ))}
        </div>
      </div>
    </>
  );
};

export default App;
