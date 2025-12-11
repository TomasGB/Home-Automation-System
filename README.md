# 🏠 Home Automation System  
A full-stack home automation platform featuring:

- 🚀 **Backend API (Python + Flask + SQLite + MQTT)**
- 🖥 **Frontend Dashboard (React + MQTT WebSockets)**
- 📡 **ESP32 Firmware (MicroPython)**
- 🔔 **Real-time communication using MQTT**
- 🔐 **JWT-based authentication**
- 💡 **LED control + live sensor monitoring**

This project provides a complete, expandable home automation solution suitable for learning, prototyping, or building real home features.

---

# 📂 Project Structure

```
Home-Automation-System/
│
├── backend/        → Flask API + MQTT client + SQLite database
├── frontend/       → React UI + MQTT WebSocket listener
├── esp32/          → MicroPython firmware (coming soon)
├── Docker/         → Docker environment (optional)
└── README.md       → Root documentation
```

---

# ⚙️ System Overview

## ✔ Backend (Flask)
Provides REST API endpoints for:

- User authentication (JWT)
- LED control (via MQTT + SQLite)
- Sensor data storage & retrieval
- MQTT bridge between ESP32 ↔ frontend

MQTT Messages:
- Sensor data: `home/sensor/data`
- LED state updates: `home/led/state`

The backend both **subscribes** to these topics and **publishes** state changes.

---

## ✔ Frontend (React)
The frontend dashboard includes:

- Live sensor readings  
- Historical graph  
- LED control panel  
- Login system  
- MQTT real-time updates (WebSockets)

Connects to:
```
wss://test.mosquitto.org:8081
```

---

## ✔ ESP32 (MicroPython)
Firmware responsibilities:

- Read temperature & humidity
- Publish sensor data to `home/sensor/data`
- Subscribe to `home/led/state` to toggle LED
- Send readings at configurable intervals

---

# 🔐 Authentication

The system uses **JWT tokens**:

1. Frontend sends login credentials  
2. Backend validates them (stored in SQLite)  
3. Returns JWT token  
4. Frontend stores token in `localStorage`  
5. Every API call includes `Authorization: Bearer <token>`  
6. Backend verifies via `auth_middleware`

---

# 📡 MQTT Topics

| Topic | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `home/sensor/data` | ESP32 → Backend/Frontend | `{ "temperature": X, "humidity": Y }` | Live sensor data |
| `home/led/state` | Backend → ESP32/Frontend | `{ "status": "on" }` | LED state updates |
| `home/led/control` | (deprecated) | — | Old topic, no longer used |

The system now uses **a single unified LED topic**:  
```
home/led/state
```

---

# 🛠 Installation & Setup

## 1️⃣ Clone the repository
```
git clone https://github.com/TomasGB/Home-Automation-System
cd Home-Automation-System
```

---

## 2️⃣ Backend Setup

### Install dependencies:
```
cd backend
pip install -r requirements.txt
```

### Start the server:
```
python run.py
```

Backend runs on:

```
http://localhost:5000
```

---

## 3️⃣ Frontend Setup

```
cd frontend
npm install
npm start
```

Runs on:

```
http://localhost:3000
```

---

## 4️⃣ ESP32 Firmware (MicroPython)

Firmware will:

- Connect to WiFi
- Connect to MQTT broker
- Publish sensor data periodically
- Listen for LED state changes

(Section will be updated when `esp32/` folder is added)

---

## 5️⃣ Optional: Docker Setup

Inside the `/Docker` folder you will find:

- `docker-compose.yml`
- Backend service container
- Frontend container
- Mosquitto broker (optional)
- Environment configs

Run:

```
docker-compose up --build
```

---

# 🧪 API Endpoints

### Authentication
```
POST /api/v1/auth/login
POST /api/v1/auth/register
```

### Devices
```
GET  /api/v1/devices/led/status
POST /api/v1/devices/led
```

### Sensors
```
GET /api/v1/sensors/latest
GET /api/v1/sensors/history
```

All protected routes require:

```
Authorization: Bearer <token>
```

---

# 📊 Dashboard Preview (Features)

### ✅ Live sensor cards  
### ✅ Temperature/Humidity graph  
### ❇ LED status indicator  
### ⚡ Real-time updates via MQTT  
### 🔒 JWT session persistence  
### 🚪 Logout support  

---

# 🧱 Technologies Used

### Backend
- Python 3.12
- Flask
- SQLite
- paho-mqtt
- JWT
- CORS

### Frontend
- React
- MQTT over WebSockets (`mqtt` package)
- Chart.js / Recharts (depending on implementation)
- Fetch API with JWT

### IoT
- ESP32 + MicroPython
- DHT22 / DHT11 sensor
- MQTT

---

# 📌 Future Improvements

- Add WebSocket backend relay option  
- Add multiple device types (relay, PIR, RGB LED, etc.)  
- Add user roles & permissions UI  
- Add device auto discovery  
- Add ESP32 OTA update support  

---

# 🎉 Final Notes

This project is fully modular — you can replace sensors, add new MQTT devices, or expand the API without breaking existing functionality.
