from fastapi.testclient import TestClient
import os
import sys

# Asegurar que Python encuentre el paquete 'app' (carpeta hermana de 'tests')
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.main import app  # importamos la instancia FastAPI

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json().get("ok") is True

def test_integral_basic():
    payload = {"type": "integral", "input": "x*exp(2*x) dx"}
    r = client.post("/solve", json=payload)
    assert r.status_code == 200
    assert "result_latex" in r.json()



def test_integral_with_caret_power():
    payload = {"type": "integral", "input": "x^2 dx"}
    r = client.post("/solve", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["result_latex"].endswith("+ C")

def test_integral_with_integral_symbol_and_dx():
    payload = {"type": "integral", "input": "∫ (2x+1)*exp(x) dx"}
    r = client.post("/solve", json=payload)
    assert r.status_code == 200
    assert "result_latex" in r.json()

def test_wrong_type_returns_422():
    payload = {"type": "derivative", "input": "x^2"}
    r = client.post("/solve", json=payload)
    assert r.status_code == 422

def test_empty_input_returns_422():
    payload = {"type": "integral", "input": ""}
    r = client.post("/solve", json=payload)
    assert r.status_code == 422
