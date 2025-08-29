from fastapi.testclient import TestClient
import os
import sys

# Asegurar que Python encuentre el paquete 'app' (carpeta hermana de 'tests')
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.main import app  # 👈 importamos la instancia FastAPI

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json().get("ok") is True

def test_integral_basic():
    payload = {"type": "integral", "input": "x*exp(2*x) dx"}
    r = client.post("/solve", json=payload)
    assert r.status_code == 200
    assert "result_latex" in r.json()
