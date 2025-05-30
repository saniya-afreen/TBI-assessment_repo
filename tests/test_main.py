from fastapi.testclient import TestClient
from serving.main import app

client = TestClient(app)

def test_deploy_model():
    response = client.post("/deploy", json={"model_name": "bert-base-uncased"})
    assert response.status_code == 200
    assert response.json()["status"] in ["PENDING", "STARTED"]

def test_status_before_deploy():
    response = client.get("/status/nonexistent-model")
    assert response.status_code == 404
    assert response.json()["detail"] == "Model not found"

def test_status_after_deploy():
    client.post("/deploy", json={"model_name": "distilbert-base-uncased"})
    
    response = client.get("/status/distilbert-base-uncased")
    assert response.status_code == 200
    assert response.json()["status"] in ["PENDING", "STARTED", "RUNNING"]

def test_invalid_payload():
    response = client.post("/deploy", json={"wrong_key": "value"})
    assert response.status_code == 422 
