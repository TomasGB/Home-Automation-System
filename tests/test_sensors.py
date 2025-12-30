def test_get_latest_sensors(client):
    
    response = client.get("/api/v1/sensors/latest")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
