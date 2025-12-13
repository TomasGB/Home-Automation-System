import jwt
"""
from functools import wraps
from flask import request, jsonify
from ..config import Config

def require_auth(role=None):
    # This is the ONLY wrapper Flask will see
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Missing token"}), 401

            # Split "Bearer token"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({"error": "Malformed Authorization header"}), 401

            token = parts[1]

            # Decode token
            try:
                decoded = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            except Exception as e:
                return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401

            # Role verification (optional)
            if role and decoded.get("role") != role:
                return jsonify({"error": "Forbidden"}), 403

            # Attach user object
            request.user = decoded

            return f(*args, **kwargs)

        return decorated_function

    return decorator
"""

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
