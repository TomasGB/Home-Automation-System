import sys
import os
import pytest
import logging
import sqlite3

# ------------------------------------------------------------------
# Path setup
# ------------------------------------------------------------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
sys.path.insert(0, BACKEND_DIR)

# Silence MQTT noise during tests
logging.getLogger("app.mqtt_client").setLevel(logging.ERROR)

# ------------------------------------------------------------------
# Test database fixture
# ------------------------------------------------------------------

@pytest.fixture(scope="session")
def test_db(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("data") / "test.db"
    return str(db_path)

# ------------------------------------------------------------------
# App fixture
# ------------------------------------------------------------------

@pytest.fixture(scope="session")
def app(test_db):
    from app import create_app
    from app.config import Config

    # Point app to test database
    Config.DB_PATH = test_db

    app = create_app()

    # Ensure DB file exists
    sqlite3.connect(test_db).close()

    return app

# ------------------------------------------------------------------
# Client & auth fixtures
# ------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def seed_test_user(app):
    client = app.test_client()

    res = client.post("/api/v1/auth/register", json={
        "username": "admin",
        "password": "admin123"
    })

    # User may already exist if tests reuse DB
    assert res.status_code in (200, 201, 400)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    res = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })

    assert res.status_code == 200, res.json

    token = res.json["token"]
    return {"Authorization": f"Bearer {token}"}
