from flask import Blueprint, jsonify, request
from app.services.device_service import DeviceService
from app.models.device_model import DeviceModel
from ..utils.auth_middleware import require_auth


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
    from app.mqtt_client import mqtt_client
    import json

    body = request.get_json() or {}
    state = body.get("state")

    if state not in ["on", "off"]:
        return jsonify({"success": False, "error": "Invalid state"}), 400

    # Update DB
    updated = DeviceModel.update_status(device_id, state)
    if not updated:
        return jsonify({"success": False, "error": "Device not found"}), 404

    # Get device info (to know its topic)
    device = DeviceModel.get_by_id(device_id)

    # Publish MQTT message if device has topic
    if device and device.get("mqtt_topic"):
        mqtt_client.publish(device["mqtt_topic"], json.dumps({"status": state}), retain=True)

    return jsonify({"success": True, "data": {"state": state}})
