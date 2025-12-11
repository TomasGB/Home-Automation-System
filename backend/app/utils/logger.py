import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app=None):
    log_dir = os.getenv("LOG_DIR", "/tmp")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    handler = RotatingFileHandler(os.path.join(log_dir, "app.log"), maxBytes=10*1024*1024, backupCount=3)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)

    root = logging.getLogger()
    if not root.handlers:
        root.setLevel(logging.INFO)
        root.addHandler(handler)

    if app:
        app.logger.handlers = root.handlers
        app.logger.setLevel(root.level)
