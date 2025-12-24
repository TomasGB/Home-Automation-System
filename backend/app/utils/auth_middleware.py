import jwt
from functools import wraps
from flask import request, jsonify, make_response
from app.services.auth_service import AuthService

def require_auth(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # Allow OPTIONS requests without auth
            if request.method == "OPTIONS":
                response = make_response(jsonify({"success": True}), 200)
                response.headers["Access-Control-Allow-Origin"] = "*"
                response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
                return response

            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"success": False, "error": "Missing token"}), 401

            user = AuthService.verify_token(token.replace("Bearer ", ""))
            if not user:
                return jsonify({"success": False, "error": "Invalid token"}), 401

            if role and user.get("role") != role:
                return jsonify({"success": False, "error": "Forbidden"}), 403

            return f(*args, **kwargs)

        return wrapper
    return decorator
