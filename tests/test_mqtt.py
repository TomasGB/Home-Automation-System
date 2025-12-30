from unittest.mock import patch

def test_mqtt_publish_called(client, auth_headers):
    # 1️⃣ Create a device with mqtt_topic
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

    # 2️⃣ Fetch devices to get the real ID
    list_res = client.get("/api/v1/devices", headers=auth_headers)
    assert list_res.status_code == 200
    assert list_res.json["success"] is True
    assert len(list_res.json["data"]) > 0

    device_id = list_res.json["data"][-1]["id"]

    # 3️⃣ Patch MQTT publish
    with patch("app.mqtt_client.mqtt_client.publish") as mock_publish:
        res = client.post(
            f"/api/v1/devices/{device_id}/learn-action",
            json={"action": "turn_on"},
            headers=auth_headers
        )

        assert res.status_code == 200
        mock_publish.assert_called_once()
