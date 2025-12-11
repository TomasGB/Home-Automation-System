from flask import jsonify

def success(data=None, message="OK", status=200, meta=None):
    """
    Standardized success response format.

    data: main payload (list, dict, etc.)
    message: optional description
    status: HTTP status code
    meta: extra metadata (pagination, counts, etc.)
    """
    payload = {
        "success": True,
        "message": message,
        "data": data
    }

    if meta is not None:
        payload["meta"] = meta

    return jsonify(payload), status
