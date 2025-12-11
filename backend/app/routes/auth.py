#from flask import Blueprint, request, jsonify
#import jwt, datetime
#from ..config import Config
#from ..services.user_service import UserService
#
#auth_bp = Blueprint("auth", __name__)
#user_service = UserService()
#
## -------------------------------
##  REGISTER
## -------------------------------
#@auth_bp.post("/register")
#def register():
#    data = request.json
#    username = data.get("username")
#    password = data.get("password")
#    role = data.get("role", "user")
#
#    if user_service.user_exists(username):
#        return jsonify({"error": "User already exists"}), 400
#
#    created = user_service.create_user(username, password, role)
#    if created:
#        return jsonify({"message": "User created"}), 201
#    else:
#        return jsonify({"error": "Failed to create user"}), 500
#
#
## -------------------------------
##  LOGIN
## -------------------------------
#@auth_bp.post("/login")
#def login():
#    data = request.json
#    username = data.get("username")
#    password = data.get("password")
#
#    user = user_service.authenticate_user(username, password)
#    if not user:
#        return jsonify({"error": "Invalid credentials"}), 401
#
#    payload = {
#        "user_id": user["id"],
#        "username": username,
#        "role": user["role"],
#        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8),
#    }
#    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
#
#    return jsonify({"token": token})
#

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
