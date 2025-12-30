def test_create_device_action(client, auth_headers, monkeypatch):

    def mock_publish(topic, payload):
        return True

    monkeypatch.setattr(
        "app.routes.devices.mqtt_client.publish",
        mock_publish
    )

    create_res = client.post(
        "/api/v1/devices",
        json={
            "name": "Test IR Device",
            "type": "ir",
            "mqtt_topic": "home/test/ir"
        },
        headers=auth_headers
    )

    assert create_res.status_code in (200, 201)

    devices_res = client.get(
        "/api/v1/devices",
        headers=auth_headers
    )

    assert devices_res.status_code == 200
    device_id = devices_res.json["data"][-1]["id"]

    res = client.post(
        f"/api/v1/devices/{device_id}/learn-action",
        json={"action": "turn_on"},
        headers=auth_headers
    )

    assert res.status_code == 200
    assert res.json["success"] is True



def test_action_invalid_device(client, auth_headers):
    invalid_device_id = 999

    res = client.get(
        f"/api/v1/devices/{invalid_device_id}/actions",
        headers=auth_headers
    )

    assert res.status_code == 404

