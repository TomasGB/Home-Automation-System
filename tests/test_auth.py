"""
import jwt

def test_login_success(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "token" in response.json

def test_login_fail(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "wrong"
    })
    assert response.status_code == 401

def test_verify_token(client):
    # Get token first
    login = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    token = login.json["token"]

    response = client.get("/api/v1/auth/verify", headers={
        "Authorization": token
    })

    assert response.status_code == 200
    assert response.json["valid"] is True
"""
def test_login_success(client):
    res = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert res.status_code == 200
    assert "token" in res.json

def test_login_invalid_password(client):
    res = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "wrong"
    })
    assert res.status_code == 401

def test_protected_route_without_token(client):
    res = client.get("/api/v1/devices")
    assert res.status_code == 401

def test_forbidden_device_access(client, auth_headers):
    res = client.get("/api/v1/devices/999", headers=auth_headers)
    assert res.status_code in (403, 404, 405)

def test_invalid_jwt(client):
    headers = {"Authorization": "Bearer invalid.token.here"}
    res = client.get("/api/v1/devices", headers=headers)
    assert res.status_code == 401

def test_sql_injection_attempt(client, auth_headers):
    res = client.post("/api/v1/auth/login", json={
        "username": "' OR 1=1 --",
        "password": "test"
    })
    assert res.status_code == 401
