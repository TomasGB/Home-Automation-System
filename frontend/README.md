# 🏠 Home Automation System – Frontend (React + MQTT)

This is the **React frontend** for the Home Automation System.  
It provides a clean UI to:

- View real-time sensor data  
- Visualize temperature/humidity history  
- Monitor and toggle LED state  
- Authenticate using JWT  
- Receive MQTT updates over WebSockets

---

# 🚀 Features

### ✔ Live Sensor Dashboard  
Real-time temperature & humidity displayed instantly using MQTT.

### ✔ Interactive LED Control  
- Toggles LED state via backend API  
- Listens to MQTT updates to stay synced

### ✔ Graphing  
Sensor history visualized using a clean line chart.

### ✔ Secure Authentication  
Users must log in to access the dashboard.

### ✔ MQTT WebSocket Client  
Connects to:
```
wss://test.mosquitto.org:8081
```

Subscribes to:
```
home/sensor/data
home/led/state
```

---

# 📁 Project Structure

```
frontend/
│
├── public/
├── src/
│   ├── api/
│   │   ├── authFetch.js
│   │   ├── auth.js
│   │   ├── devices.js
│   │   └── sensors.js
│   │
│   ├── components/
│   │   ├── Login.jsx
│   │   ├── LedStatus.jsx
│   │   ├── CurrentSensorData.jsx
│   │   ├── SensorGraph.jsx
│   │   └── MqttListener.jsx
│   │
│   ├── styles.css
│   ├── App.jsx
│   ├── config.js
│   └── index.js
│
├── package.json
└── README.md
```

---

# 🌐 API Base URL

Configured in **`src/config.js`**:

```javascript
export const API_BASE = "http://localhost:5000/api/v1";
```

Frontend sends authenticated requests through `authFetch.js`.

---

# 🔗 Backend Communication

The frontend interacts with the backend via:

### Auth  
```
POST /api/v1/auth/login
```

### LED  
```
GET /api/v1/devices/led/status
POST /api/v1/devices/led
```

### Sensor  
```
GET /api/v1/sensor/latest
GET /api/v1/sensor/history
```

All protected routes automatically attach JWT using `authFetch`.

---

# 📡 MQTT Integration

MQTT over WebSockets via `mqtt` npm package.  
Connection established in `MqttListener.jsx`:

```javascript
mqtt.connect("wss://test.mosquitto.org:8081");
```

### Subscribed topics

✔ `home/sensor/data`  
✔ `home/led/state`  

### Sensor message example:
```json
{ "temperature": 25.3, "humidity": 50 }
```

### LED message example:
```json
{ "status": "on" }
```

---

# 🧩 Key Components

## **Login.jsx**
Handles authentication and stores JWT in `localStorage`.

## **MqttListener.jsx**
Invisible component that:
- Subscribes to MQTT topics  
- Passes updates to the app via callbacks  

## **LedStatus.jsx**
- Fetches LED state from backend  
- Updates via MQTT  
- Sends toggle actions via API  

## **CurrentSensorData.jsx**
Displays latest sensor reading.

## **SensorGraph.jsx**
Renders graph of historical readings.

---

# 🛠 Setup & Installation

### 1. Install dependencies:
```
npm install
```

### 2. Start the development server:
```
npm start
```

Runs at:
```
http://localhost:3000
```

Make sure the backend is running at:
```
http://localhost:5000
```

---

# 🔑 Authentication Flow

1. User enters username/password  
2. Backend returns JWT  
3. Token is saved in `localStorage`  
4. `authFetch` attaches token to every request  
5. Backend validates token and sends data  

---

# 📡 Live Updates (MQTT Flow)

### LED Toggle  
1. User presses toggle button  
2. Frontend sends `POST /devices/led`  
3. Backend updates DB  
4. Backend publishes MQTT message  
5. Frontend receives it instantly  
6. UI updates without page reload  

### Sensor Data  
ESP32 publishes to:  
```
home/sensor/data
```

Frontend listens continuously.

---

# 📘 Notes

- UI automatically stays synchronized with ESP32 and backend via MQTT.
- WebSocket MQTT broker: `wss://test.mosquitto.org:8081`
- All data normalization handled inside UI components.

---

# 🎉 Frontend Ready!

This frontend is fully compatible with the backend and ESP32 firmware.

