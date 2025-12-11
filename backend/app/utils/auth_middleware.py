#import jwt
#from functools import wraps
#from flask import request, jsonify
#from ..config import Config
#
#def require_auth(role=None):
#    def decorator(f):
#        @wraps(f)
#        def wrapper(*args, **kwargs):
#            token = request.headers.get("Authorization")
#
#            if not token:
#                return jsonify({"error": "Missing token"}), 401
#
#            try:
#                token = token.replace("Bearer ", "")
#                decoded = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
#            except Exception:
#                return jsonify({"error": "Invalid or expired token"}), 401
#
#            # Role-based protection
#            if role and decoded.get("role") != role:
#                return jsonify({"error": "Forbidden"}), 403
#
#            request.user = decoded
#            return f(*args, **kwargs)
#        return wrapper
#    return decorator
#
import jwt
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
