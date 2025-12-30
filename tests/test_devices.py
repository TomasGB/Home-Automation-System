"""import json

def test_led_status_default(client):
    response = client.get("/api/v1/devices/led/status")
    assert response.status_code == 200
    assert "state" in response.json

def test_led_control_on(client):
    response = client.post(
        "/api/v1/devices/led",
        json={"state": "on"}
    )
    assert response.status_code == 200
    assert response.json["state"] == "on"

    # Check persistence
    get_res = client.get("/api/v1/devices/led/status")
    assert get_res.json["state"] == "on"

"""

def test_register_device(client, auth_headers):
    res = client.post("/api/v1/devices", json={
        "name": "Living Room ESP32",
        "type": "esp32"
    }, headers=auth_headers)

    assert res.status_code == 200


def test_list_devices(client, auth_headers):
    res = client.get("/api/v1/devices", headers=auth_headers)
    assert "data" in res.json
    assert isinstance(res.json["data"], list)


def test_duplicate_device(client, auth_headers):
    payload = {"name": "ESP32-1", "type": "esp32"}
    client.post("/api/v1/devices", json=payload, headers=auth_headers)
    res = client.post("/api/v1/devices", json=payload, headers=auth_headers)

    assert res.status_code == 200


def test_missing_fields(client, auth_headers):
    res = client.post("/api/v1/devices", json={}, headers=auth_headers)
    assert res.status_code == 400
