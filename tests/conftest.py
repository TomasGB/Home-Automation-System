import os
import tempfile
import pytest
from app import create_app

@pytest.fixture
def client():
    # Create temporary DB file
    db_fd, db_path = tempfile.mkstemp()

    # Override environment variable so the app uses temp DB
    os.environ["DB_PATH"] = db_path

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.remove(db_path)
