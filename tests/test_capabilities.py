from fastapi.testclient import TestClient
from backend.main import app
c=TestClient(app)
def test_health():assert c.get("/health").status_code==200
def test_capability_routes():
 assert c.get("/api/image/status").json()["backend"]
 assert c.get("/api/video/status").json()["backend"]
