import os
from flask import Flask
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logging
from .utils.error_handlers import register_error_handlers
from .mqtt_client import mqtt_client
from .routes.sensors import sensors_bp
from .routes.devices import devices_bp
from .routes.auth import auth_bp
from .utils.db_initializer import init_db



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Basic setup
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"],
        }
    })

    setup_logging(app)
    init_db()

    # Register blueprints
    app.register_blueprint(sensors_bp, url_prefix="/api/v1/sensors")
    app.register_blueprint(devices_bp, url_prefix="/api/v1/devices")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    
    # Register global error handlers
    register_error_handlers(app)

    # Start MQTT client (non-blocking)
    mqtt_client.start()

    return app
