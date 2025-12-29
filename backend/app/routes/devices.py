from flask import Blueprint, jsonify, request
from app.services.device_service import DeviceService
from app.models.device_model import DeviceModel
from app.models.device_action_model import DeviceActionModel
from app.models.device_action_model import DeviceActionModel
from ..utils.auth_middleware import require_auth
from app.config import Config
from app.mqtt_client import mqtt_client


devices_bp = Blueprint("devices", __name__)

@devices_bp.get("")
@require_auth()
def list_devices():
    devices = DeviceModel.get_all()
    return jsonify({"success": True, "data": devices})


@devices_bp.post("")
@require_auth(role="admin")
def create_device():
    body = request.get_json() or {}

    name = body.get("name")
    dev_type = body.get("type")
    mqtt_topic = body.get("mqtt_topic", None)

    if not name or not dev_type:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    DeviceModel.create_device(name, dev_type, mqtt_topic)

    return jsonify({"success": True, "message": "Device created"})

@devices_bp.post("/<int:device_id>/state")
@require_auth(role="admin")
def set_device_state(device_id):
    #from app.mqtt_client import mqtt_client
    import json

    body = request.get_json() or {}
    state = body.get("state")

    if state not in ["on", "off"]:
        return jsonify({"success": False, "error": "Invalid state"}), 400

    # Update DB
    updated = DeviceModel.update_status(device_id, state)
    if not updated:
        return jsonify({
            "success": False,
              "error": "Device not found"
              }), 404

    # Get device info (to know its topic)
    device = DeviceModel.get_by_id(device_id)

    # Publish MQTT message if device has topic
    if device and device.get("mqtt_topic"):
        mqtt_client.publish(device["mqtt_topic"], json.dumps({"status": state}), retain=True)

    return jsonify({"success": True, "data": {"state": state}})

@devices_bp.route("/<int:device_id>", methods=["DELETE"])
@require_auth()
def delete_device(device_id):
    try:
        if not device_id:
            return jsonify({
                "success": False,
                "error": "Device not found"
            }), 404
    
        # 1️⃣ Delete all actions first
        DeviceActionModel.delete_by_device(device_id)

        # 2️⃣ Delete the device
        DeviceModel.delete(device_id)

        return jsonify({
            "success": True,
            "message": "Device deleted"
        })

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500


@devices_bp.put("/<int:device_id>")
@require_auth(role="admin")
def update_device(device_id):
    body = request.get_json() or {}

    updated = DeviceModel.update(
        device_id,
        name=body.get("name"),
        dev_type=body.get("type"),
        mqtt_topic=body.get("mqtt_topic")
    )

    if not updated:
        return jsonify({
            "success": False,
            "error": "Device not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Device updated"
    })

@devices_bp.route("/<int:device_id>/learn-action", methods=["POST", "OPTIONS"])
@require_auth(role="admin")
def learn_action(device_id):
    #from app.mqtt_client import mqtt_client
    import json

    # Preflight
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json() or {}
    action = data.get("action")

    if not action:
        return jsonify({
            "success": False,
            "error": "Missing action name"
        }), 400

    device = DeviceModel.get_by_id(device_id)

    if not device:
        return jsonify({
            "success": False,
            "error": "Device not found"
        }), 404

    if not device.get("mqtt_topic"):
        return jsonify({
            "success": False,
            "error": "Device has no MQTT topic"
        }), 400

    mqtt_client.publish(
    f"{Config.MQTT_BASE_TOPIC}/ir/learn/request",
    json.dumps({
        "device_id": device_id,
        "action": action
    })
    )

    return jsonify({
        "success": True,
        "message": "Learning mode started. Point the remote and press the button"
    })

@devices_bp.route("/<int:device_id>/actions", methods=["GET"])
@require_auth()
def get_device_actions(device_id):
    #actions = DeviceActionModel.get_by_device(device_id=device_id)

    try:
        actions = DeviceActionModel.get_by_device(device_id)

        return jsonify({
            "success": True,
            "data": [
                {
                    "action": a["action"]
                } for a in actions
            ]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@devices_bp.route("/<int:device_id>/actions/<action>/trigger", methods=["POST"])
@require_auth()
def trigger_action(device_id, action):
    #from app.mqtt_client import mqtt_client

    mqtt_client.publish_ir_action(device_id, action)

    return jsonify({
        "success": True
    })

