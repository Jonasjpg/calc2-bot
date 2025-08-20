from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json().get("ok") is True

def test_integral_basic():
    payload = {"type":"integral","input":"x*exp(2*x) dx"}
    r = client.post("/solve", json=payload)
    assert r.status_code == 200
    assert "result_latex" in r.json()