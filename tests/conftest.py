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
    from app.config import Config

    Config.DB_PATH = test_db
    Config.TESTING = True

    from app import create_app
    from app.utils.db_initializer import init_db

    app = create_app()

    # Create tables in TEST DB
    init_db()

    print("✅ USING DB:", Config.DB_PATH)
    assert "test" in Config.DB_PATH.lower(), "❌ NOT using test database"

    return app

# ------------------------------------------------------------------
# User & auth fixtures
# ------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def seed_test_user(app):
    client = app.test_client()

    res = client.post("/api/v1/auth/register", json={
        "username": "admin",
        "password": "admin123"
    })

    assert res.status_code in (200, 201, 400)


@pytest.fixture(scope="session", autouse=True)
def promote_test_user_to_admin(seed_test_user, app):
    """⚠️ Must depend on seed_test_user to guarantee order"""
    from app.config import Config

    assert "test" in Config.DB_PATH.lower()

    with sqlite3.connect(Config.DB_PATH) as conn:
        conn.execute(
            "UPDATE users SET role = 'admin' WHERE username = 'admin'"
        )
        conn.commit()

        # Safety check
        role = conn.execute(
            "SELECT role FROM users WHERE username = 'admin'"
        ).fetchone()[0]

        assert role == "admin", "❌ Test user is NOT admin"


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    res = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert res.status_code == 200, (
        f"❌ Login failed during tests: {res.status_code} {res.json}"
    )

    token = res.json.get("token")
    assert token, "❌ Login response missing JWT token"

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
