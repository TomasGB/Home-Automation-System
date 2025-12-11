from flask import jsonify
import traceback
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):

    # ------------------------------
    # 404 – Not Found
    # ------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Resource not found",
            "status": 404
        }), 404

    # ------------------------------
    # 405 – Method Not Allowed
    # ------------------------------
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method not allowed",
            "status": 405
        }), 405

    # ------------------------------
    # 400 – Bad request
    # ------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad request",
            "status": 400
        }), 400

    # ------------------------------
    # 500 – Internal server error
    # ------------------------------
    @app.errorhandler(500)
    def internal_error(error):
        logger.error("Internal server error", exc_info=True)

        return jsonify({
            "error": "Internal server error",
            "status": 500
        }), 500

    # ------------------------------
    # Catch-all for exceptions not covered
    # ------------------------------
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error("Unhandled exception:", exc_info=True)

        return jsonify({
            "error": "Unexpected error",
            "details": str(error),
            "status": 500
        }), 500
