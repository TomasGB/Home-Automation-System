from flask import Blueprint, jsonify, request
from app.services.device_service import DeviceService
from ..utils.auth_middleware import require_auth


devices_bp = Blueprint("devices", __name__)

# ------------------------------------------------------
#  GET LED STATUS (any logged-in user)
# ------------------------------------------------------
@devices_bp.get("/led/state")
@require_auth()
def led_status():
    status = DeviceService.get_led_status()
    return jsonify({
        "success": True,
        "data": { "state": status }
    })

# ------------------------------------------------------
#  SET LED STATE (ADMIN only)
# ------------------------------------------------------
@devices_bp.post("/led")
@require_auth(role="admin")
def led_set():
    from app.mqtt_client import mqtt_client
    from app.config import Config
    import json
    
    body = request.get_json() or {}
    state = body.get("state")

    print("🔥 LED POST ROUTE HIT — state =", state, flush=True)


    if state not in ["on", "off"]:
        return jsonify({
            "success": False,
            "error": "Invalid state"
        }), 400

    # DeviceService handles:
    # - DB update
    # - MQTT publish
    DeviceService.update_led_status(state)
    #print(">>> MQTT TOPIC LED =", Config.MQTT_TOPIC_LED)
    #print(">>> MQTT MESSAGE =", json.dumps({"status": state}))
    msg=str(state)

    mqtt_client.publish("home/led/state", state)
    #print("🔥 LED STATE UPDATED =", state, flush=True)

    return jsonify({
        "success": True,
        "data": { "state": state }
    })
