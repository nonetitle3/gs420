from fastapi.testclient import TestClient
from backend.main import app

def test_health():
 assert TestClient(app).get("/health").json()["status"]=="ok"

def test_router():
 from backend.core.model_router import ModelRouter
 assert ModelRouter().classify("write python code")=="coding"

def test_calculator():
 from backend.tools.calculator import calculate
 assert calculate("2+3*4")==14
