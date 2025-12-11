def test_get_latest_sensors(client):
    # Nothing inserted yet → should return empty list
    response = client.get("/api/v1/sensors/latest")
    assert response.status_code == 200
    assert isinstance(response.json, list)
