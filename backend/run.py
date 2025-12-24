import os
import logging
from app import create_app

# Ensure logging works BEFORE Flask starts
logging.basicConfig(level=logging.INFO)

port = int(os.getenv("PORT", 5000))
debug = os.getenv("FLASK_DEBUG", "0") == "1"

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)
