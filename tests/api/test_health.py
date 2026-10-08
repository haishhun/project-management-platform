def test_database_health_endpoint(client):
    response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_health_endpoint(client):
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_ready_endpoint(client):
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
