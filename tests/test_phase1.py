from fastapi.testclient import TestClient
from backend.main import app
def test_chat_validation():
    r=TestClient(app).post("/api/chat",json={"message":""})
    assert r.status_code==422
def test_stream_route_exists():
    r=TestClient(app).post("/api/chat/stream",json={"message":"hello"})
    assert r.status_code==200
    assert r.headers["content-type"].startswith("text/event-stream")
