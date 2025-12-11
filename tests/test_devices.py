import json

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
