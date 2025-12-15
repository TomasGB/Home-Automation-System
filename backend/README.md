# 🏠 Home Automation System – Backend (Flask + MQTT + SQLite)

This is the backend API for the **Home Automation System**.  
It acts as the central hub between the ESP32, the MQTT broker, and the frontend.

The backend is responsible for:

- Receiving sensor data via MQTT
- Storing sensor readings in SQLite
- Exposing REST endpoints for the frontend
- Handling LED device control
- Synchronizing device state through MQTT

---

# 🚀 Features

### ✔ REST API
Clean, versioned endpoints used by the frontend:

/api/v1/auth/login
/api/v1/devices/led
/api/v1/sensors/latest
/api/v1/sensors/history

---

### ✔ JWT Authentication
- Login endpoint issues JWT tokens
- Protected routes require `Authorization: Bearer <token>`

---

### ✔ MQTT Integration
- Subscribes to ESP32 sensor data topic
- Publishes LED control commands
- Listens to LED state updates to keep frontend in sync
- Uses Mosquitto test broker by default

---

### ✔ SQLite Database
Persistent storage for:

- Users
- Devices (LED)
- Sensor readings (temperature & humidity)

---

# 📁 Project Structure

```
backend/
│
├── app/
│ ├── routes/
│ │ ├── auth.py
│ │ ├── devices.py
│ │ └── sensors.py
│ │
│ ├── services/
│ │ ├── auth_service.py
│ │ ├── device_service.py
│ │ └── sensor_service.py
│ │
│ ├── models/
│ │ ├── user_model.py
│ │ ├── device_model.py
│ │ └── sensor_model.py
│ │
│ ├── utils/
│ │ └── auth_middleware.py
│ │
│ ├── mqtt_client.py
│ ├── config.py
│ ├── init.py
│
├── database.db
├── run.py
└── requirements.txt
```

---

# 🔌 MQTT Topics

### 📡 Sensor data (ESP32 → Backend)

The backend:

1. Receives the message via MQTT

2. Parses the JSON payload

3. Stores the data in SQLite


Payload example:
```json
{
  "temperature": 25.3,
  "humidity": 60
}
```

### 💡 DEVICE control (Backend → ESP32)

`
devices/id/state
`
```json
{
  "state": "on"
}
```

### 🔁 DEVICE state synchronization (ESP32 → Backend → Frontend)

`
devices/id/state
`
```json
{
  "state": "on"
}
```

Keeps UI state aligned with the physical device.

### 🔗 REST API Endpoints

### 🔐 Authentication

`POST /api/v1/auth/login`

Request:

```json
{
  "username": "admin",
  "password": "1234"
}
```

Response:

```json
{
  "token": "JWT_TOKEN"
}
```

### 💡 DEVICES

`GET /api/v1/devices`

Requires JWT

Response:

```json
{
  "success": true,
  "data": {
    "state": "on"
  }
}
```


`POST /api/v1/id/state`

Requires JWT

Request:

```json
{
  "state": "off"
}
```

Backend behavior:

1. Updates LED state in database

2. Publishes MQTT control message

3. Returns updated state

### 🌡 Sensor Data

`GET /api/v1/sensors/latest`

Returns the most recent sensor reading.

Response:

```json
{
  "temperature": 25.3,
  "humidity": 60,
  "timestamp": 14-12-2025 11:24
}
```

`GET /api/v1/sensors/history`

Optional query parameters:

```bash
?limit=50
```

Returns historical sensor data for charts.

### 🛠 Running the Backend

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Start the server
```bash
python run.py
```
Backend runs on:

```cpp
http://127.0.0.1:5000
```
### ⚙️ Configuration

Configured via the `Config` class:

```nginx
DB_PATH
MQTT_BROKER
MQTT_PORT
MQTT_TOPIC_SENSOR
MQTT_TOPIC_LED_CONTROL
MQTT_TOPIC_LED_STATE
SECRET_KEY
JWT_SECRET
```
Default MQTT broker:

```makefile
test.mosquitto.org:1883
```

### 🧪 MQTT Manual Testing

Publish DEVICE control command:

```bash
mosquitto_pub -h test.mosquitto.org -t home/device_name/state -m '{"state":"on"}'
```

Publish sensor data:

```bash
mosquitto_pub -h test.mosquitto.org -t home/sensor/data -m '{"temperature":24,"humidity":55}'
```

### 📘 Notes

* Backend reacts to MQTT messages, it does not poll

* Frontend never connects directly to MQTT

* All real-time communication flows through the backend

* UI sensor values are fetched from `/api/v1/sensors/latest`