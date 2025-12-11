from flask import jsonify

# -------------------------------
# Generic error response helper
# -------------------------------
def error_response(message: str, status: int = 400):
    return jsonify({"error": message}), status


# --------------------------------------
# Simple validation utilities (no libs)
# --------------------------------------
def require_fields(data: dict, fields: list):
    """
    Ensures all required fields exist in the incoming JSON.
    Returns (valid: bool, missing_fields: list[str])
    """
    missing = [f for f in fields if f not in data or data[f] in (None, "")]
    return (len(missing) == 0, missing)


def validate_enum(value, allowed: list):
    """
    Ensures value is inside a list of allowed options.
    Returns True/False.
    """
    return value in allowed


def validate_number(value, *, min=None, max=None):
    """
    Validates that a value is a number and optionally within a range.
    """
    try:
        num = float(value)
    except Exception:
        return False

    if min is not None and num < min:
        return False
    if max is not None and num > max:
        return False

    return True


# ----------------------------------------
# Decorator for validating request payloads
# ----------------------------------------
def validate_json(required_fields=None):
    """
    Usage:
        @validate_json(["state"])
        def endpoint():
            ...
    """
    if required_fields is None:
        required_fields = []

    def decorator(fn):
        from functools import wraps
        from flask import request

        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if not isinstance(data, dict):
                return error_response("Invalid or missing JSON body", 400)

            ok, missing = require_fields(data, required_fields)
            if not ok:
                return error_response(f"Missing required fields: {missing}", 400)

            return fn(*args, **kwargs)

        return wrapper

    return decorator
