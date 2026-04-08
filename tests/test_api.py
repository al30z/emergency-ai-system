from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict_critical():
    r = client.post("/predict", json={"message": "I am trapped under rubble"})
    assert r.status_code == 200
    data = r.json()
    assert data["priority"] == "critical"
    assert data["confidence"] > 50

def test_predict_low():
    r = client.post("/predict", json={"message": "Any updates on the situation?"})
    assert r.status_code == 200
    data = r.json()
    assert data["priority"] in ["low", "medium"]

def test_batch_predict():
    r = client.post("/predict/batch", json={
        "messages": ["trapped and injured", "need food", "any updates?"]
    })
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 3

def test_empty_message():
    r = client.post("/predict", json={"message": "   "})
    assert r.status_code == 400

def test_demo():
    r = client.get("/demo")
    assert r.status_code == 200
    assert len(r.json()["results"]) == 4