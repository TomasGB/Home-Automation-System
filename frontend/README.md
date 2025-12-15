# 🖥 Home Automation System – Frontend (React)

This is the **React frontend** for the Home Automation System.  
It provides a real-time dashboard to monitor sensor data and control devices connected through the backend API.

The frontend **does NOT connect directly to MQTT**.  
All data flows through the Flask backend via REST APIs.

---

## 🚀 Features

### ✔ Live Sensor Dashboard
- Displays latest temperature and humidity
- Automatically updates by polling the backend API
- Ready for historical charts integration

### ✔ LED Control
- Toggle LED ON / OFF
- Sends commands to backend API
- UI stays synchronized with physical device state

### ✔ Secure Authentication
- JWT-based login
- Token stored in browser (localStorage)
- Protected routes

---

## 📁 Project Structure

```
frontend/
│
├── src/
│   ├── api/
│   │   ├── auth.js
│   │   ├── devices.js
│   │   └── sensors.js
│   │
│   ├── components/
│   │   ├── Dashboard.jsx
│   │   ├── LedControl.jsx
│   │   └── SensorCard.jsx
│   │
│   ├── pages/
│   │   ├── Login.jsx
│   │   └── Home.jsx
│   │
│   ├── context/
│   │   └── AuthContext.jsx
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── config.js
│
├── public/
└── package.json
```

---

## 🔗 Backend API Integration

The frontend communicates with the backend using HTTP requests.

### API Base URL
Configured in:
```
src/api/config.js
```

Example:
```js
export const API_BASE = "http://127.0.0.1:5000/api/v1";
```

---

## 📡 Sensor Data

### Get latest sensor reading
```
GET /api/v1/sensors/latest
```

Example response:
```json
{
  "temperature": 24.5,
  "humidity": 55,
  "timestamp": 14-12-2025 11:24
}
```

---

## 💡 DEVICE Control

### Get DEVICES
```
GET /api/v1/devices
```

### Set DEVICE state
```
POST /api/v1/devices/id/state
```

Request body:
```json
{
  "state": "on"
}
```

Backend publishes MQTT messages to the ESP32 automatically.

---

## 🔐 Authentication Flow

1. User logs in via `/auth/login`
2. Backend returns a JWT
3. Token is stored in `localStorage`
4. Token is sent in headers:
```
Authorization: Bearer <token>
```

---

## ⏱ Auto Refresh Strategy

- Sensor values are fetched periodically using `setInterval`
- Devices state is refreshed after every toggle
- Backend ensures consistency with MQTT device state

---

## 🛠 Running the Frontend

### Install dependencies
```bash
npm install
```

### Start development server
```bash
npm run dev
```

Default URL:
```
http://localhost:5000
```

---

## 📘 Summary

This frontend acts as:
- A clean visualization layer
- A secure control panel
- A consumer of backend REST APIs

All device logic and real-time communication are handled by the backend.
