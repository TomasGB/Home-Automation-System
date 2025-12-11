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
