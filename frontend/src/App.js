import React, { useState } from "react";
import CurrentSensorData from "./components/CurrentSensorData";
import SensorGraph from "./components/SensorGraph";
import LedStatus from "./components/LedStatus";
import MqttListener from "./components/MqttListener";
import Login from "./components/Login";
import "./styles.css";

const App = () => {
  //const [liveSensor, setLiveSensor] = useState(null);
  const [liveSensor, setLiveSensor] = useState(null);
  const [liveLed, setLiveLed] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  // If not authenticated → show login screen
  if (!token) {
    return <Login onLogin={(tok) => setToken(tok)} />;
  }

  return (
    <>
      {/* Invisible MQTT subscription */}
      {/*<MqttListener onData={(data) => setLiveSensor(data)} />*/}
        <MqttListener onData={(d) => setLiveSensor(d)}onLed={(l) => setLiveLed(l)}/>

      {/* Top header */}
      <div className="header">
        <h1>🏠 Home Automation</h1>
        <button onClick={logout}>Logout</button>
      </div>

      {/* Responsive Grid Layout */}
      <div className="grid">
        {/* Left column (sensor data + graph) */}
        <div className="section-column">
          <CurrentSensorData liveData={liveSensor} />
          <SensorGraph liveData={liveSensor} />
        </div>

        {/* Right column (LED control) */}
        <div className="centered">
          <LedStatus  liveLed={liveLed}/>
        </div>
      </div>
    </>
  );
};

export default App;
