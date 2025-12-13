from flask import Blueprint, jsonify, request
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    body = request.get_json()
    username = body.get("username")
    password = body.get("password")

    token = AuthService.login(username, password)

    if not token:
        return jsonify({ "success": False, "error": "Invalid credentials" }), 401

    return jsonify({ "success": True, "token": token })

@auth_bp.post("/register")
def register():
    body = request.get_json()
    username = body.get("username")
    password = body.get("password")
    role = body.get("role", "user")

    try:
        AuthService.register(username, password, role)
    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 400

    return jsonify({ "success": True })
