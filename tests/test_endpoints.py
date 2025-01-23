from fastapi.testclient import TestClient
import os

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_process_images_local(client):
    test_request = {
        "input_type": "local_folder",
        "path": "tests/test_data",
        "api_key": "test_key"
    }
    response = client.post("/api/v1/process-images", json=test_request)
    assert response.status_code == 200
    assert "excel_path" in response.json()