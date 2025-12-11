from flask import Blueprint, jsonify, request
from app.services.sensor_service import SensorService
from ..utils.auth_middleware import require_auth

sensors_bp = Blueprint("sensors", __name__)

@sensors_bp.get("/latest")
@require_auth()
def latest():
    data = SensorService.get_latest()
    return jsonify({ "success": True, "data": data })

@sensors_bp.get("/history")
@require_auth()
def history():
    limit = int(request.args.get("limit", 50))
    data = SensorService.get_history(limit)
    return jsonify({ "success": True, "data": data })
