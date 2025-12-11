# 🏠 Home Automation System – Backend (Flask + MQTT + SQLite)

This is the backend API for the **Home Automation System**, responsible for:

- User authentication (JWT)
- LED device control
- Recording and serving sensor data
- MQTT communication with the ESP32 and React frontend
- SQLite database for persistent storage

---

# 🚀 Features

### ✔ REST API  
You can control devices and retrieve sensor data via clean, versioned endpoints:

```
/api/v1/auth/login
/api/v1/devices/led
/api/v1/sensor/latest
/api/v1/sensor/history
```

### ✔ JWT Authentication  
Backend validates the JWT for protected routes.

### ✔ MQTT Integration  
- Subscribes to ESP32 sensor topic  
- Subscribes to LED state topic  
- Publishes LED control updates  
- Works with Mosquitto test broker

### ✔ SQLite Database  
Stores:
- Users
- Devices (LED)
- Sensor readings (temperature & humidity)

---

# 📁 Project Structure

```
backend/
│
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── devices.py
│   │   └── sensor.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── device_service.py
│   │   ├── sensor_service.py
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── device_model.py
│   │   └── sensor_model.py
│   │
│   ├── utils/
│   │   └── auth_middleware.py
│   │
│   ├── mqtt_client.py
│   ├── config.py
│   ├── __init__.py
│
├── database.db
├── run.py
└── requirements.txt
```

---

# 🔌 MQTT Topics

### Sensor data (ESP32 → Backend)
```
home/sensor/data
```
Example payload:
```json
{ "temperature": 25.3, "humidity": 60 }
```

### LED state updates (any → backend → frontend)
```
home/led/state
```

Payload:
```json
{ "status": "on" }
```

---

# 🔗 REST API Endpoints

## Auth

### **POST /api/v1/auth/login**
```json
{
  "username": "admin",
  "password": "1234"
}
```

Response (JWT):

```json
{ "token": "..." }
```

---

## LED Device

### **GET /api/v1/devices/led/status**
Requires JWT  
Returns:
```json
{ "success": true, "data": { "state": "on" } }
```

### **POST /api/v1/devices/led**
Admin-only  
Body:
```json
{ "state": "on" }
```

Backend will:
1. Update database  
2. Publish to MQTT  
3. Return new state  

---

## Sensor Data

### **GET /api/v1/sensor/latest**
Returns last stored sensor record.

### **GET /api/v1/sensor/history**
Returns the last N records for graphing.

---

# 🛠 Running the Backend

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Run Flask server
```
python run.py
```

Default URL:
```
http://localhost:5000
```

---

# ⚙️ Configuration

Environment variables supported in `Config`:

```
DB_PATH
MQTT_BROKER
MQTT_PORT
MQTT_TOPIC_SENSOR
MQTT_TOPIC_LED
SECRET_KEY
JWT_SECRET
```

Default broker:
```
test.mosquitto.org:1883
```

---

# 🧪 Testing MQTT Manually

Using MQTT Explorer or mosquitto_pub:

```
mosquitto_pub -h test.mosquitto.org -t home/led/state -m '{"status":"on"}'
```

Frontend updates instantly.

---

# 📘 Notes

- Backend publishes LED updates **only** when the API endpoint is hit.
- ESP32 reacts to MQTT messages from the same LED topic.
- Backend listens to the **same LED topic** so UI stays in sync.

---

