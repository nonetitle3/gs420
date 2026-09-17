"""Phase 1 API/core tests using a fake model."""
from collections.abc import Generator
from fastapi.testclient import TestClient
from backend.main import app
from backend.dependencies import get_orchestrator
from backend.core.orchestrator import AIOrchestrator, ConversationStore
from backend.config import Settings

class FakeModel:
    def generate(self, messages, **kwargs) -> str:
        return "Test response"
    def stream(self, messages, **kwargs) -> Generator[str, None, None]:
        yield "Test "
        yield "response"
    def info(self):
        return {"provider":"fake","model_id":"fake-model","device":"cpu","cuda_available":False,"gpu_name":None,"loaded":True}

class FakeRegistry:
    def __init__(self):
        self.model=FakeModel()
    def get_text_model(self): return self.model
    def list_models(self): return [{"name":"fake",**self.model.info()}]

class FakeOrchestrator(AIOrchestrator):
    def __init__(self):
        settings=Settings()
        self.settings=settings
        self.registry=FakeRegistry()
        self.conversations=ConversationStore(20)

def override_orchestrator():
    return FakeOrchestrator()

app.dependency_overrides[get_orchestrator]=override_orchestrator
client=TestClient(app)

def test_health():
    response=client.get("/health")
    assert response.status_code==200
    assert response.json()["status"]=="ok"

def test_root():
    response=client.get("/")
    assert response.status_code==200
    assert response.json()["message"]=="GS420 AI API"

def test_create_session():
    response=client.post("/api/sessions")
    assert response.status_code==200
    assert "session_id" in response.json()

def test_chat_non_streaming():
    response=client.post("/api/chat",json={"message":"Hello GS420","stream":False})
    assert response.status_code==200
    data=response.json()
    assert "session_id" in data
    assert data["response"]=="Test response"

def test_chat_streaming():
    response=client.post("/api/chat",json={"message":"Hello","stream":True})
    assert response.status_code==200
    assert "text/event-stream" in response.headers.get("content-type","")
    assert "Test " in response.text
    assert "response" in response.text

def test_history():
    session_id=client.post("/api/sessions").json()["session_id"]
    response=client.post("/api/chat",json={"session_id":session_id,"message":"Remember this","stream":False})
    assert response.status_code==200
    messages=client.get(f"/api/sessions/{session_id}/history").json()["messages"]
    assert len(messages)==2
    assert messages[0]["role"]=="user"
    assert messages[1]["role"]=="assistant"

def test_clear_history():
    session_id=client.post("/api/sessions").json()["session_id"]
    client.post("/api/chat",json={"session_id":session_id,"message":"Test","stream":False})
    response=client.delete(f"/api/sessions/{session_id}/history")
    assert response.status_code==200
    assert client.get(f"/api/sessions/{session_id}/history").json()["messages"]==[]
