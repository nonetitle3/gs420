"""Phase 2 API/core tests using fake routed models."""
from collections.abc import Generator

from fastapi.testclient import TestClient

from backend.main import app
from backend.dependencies import get_orchestrator
from backend.core.orchestrator import AIOrchestrator, ConversationStore
from backend.config import Settings


class FakeModel:
    def __init__(self, name: str):
        self.name = name

    def generate(self, messages, **kwargs) -> str:
        return f"Test response ({self.name})"

    def stream(self, messages, **kwargs) -> Generator[str, None, None]:
        yield "Test "
        yield f"response ({self.name})"

    def info(self):
        return {
            "provider": "fake",
            "model_id": self.name,
            "device": "cpu",
            "cuda_available": False,
            "gpu_name": None,
            "loaded": True,
        }


class FakeRouter:
    def __init__(self, settings):
        self.settings = settings
        self.models = {
            "general": FakeModel("general"),
            "reasoning": FakeModel("reasoning"),
            "coding": FakeModel("coding"),
            "vision": FakeModel("vision"),
        }

    def route(self, role="auto", message=""):
        if role == "auto":
            text = message.lower()
            if any(k in text for k in ("python", "code", "কোড")):
                role = "coding"
            elif any(k in text for k in ("math", "logic", "গণিত", "যুক্তি")):
                role = "reasoning"
            else:
                role = "general"
        if role == "chat":
            role = "general"
        return role, self.models[role]

    def list_routes(self):
        return [
            {"role": role, "model_id": role, "configured": True}
            for role in self.models
        ]


class FakeOrchestrator(AIOrchestrator):
    def __init__(self):
        settings = Settings()
        self.settings = settings
        self.router = FakeRouter(settings)
        self.conversations = ConversationStore(20)


def override_orchestrator():
    return FakeOrchestrator()


app.dependency_overrides[get_orchestrator] = override_orchestrator
client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["phase"] == "2"


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["version"] == "0.2.0"


def test_create_session():
    response = client.post("/api/sessions")
    assert response.status_code == 200
    assert "session_id" in response.json()


def test_chat_non_streaming_with_role():
    response = client.post(
        "/api/chat",
        json={"message": "Write Python code", "stream": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "coding"
    assert data["response"] == "Test response (coding)"


def test_chat_explicit_reasoning_role():
    response = client.post(
        "/api/chat",
        json={"message": "hello", "role": "reasoning", "stream": False},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "reasoning"


def test_chat_streaming():
    response = client.post(
        "/api/chat",
        json={"message": "Solve this math problem", "stream": True},
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")
    assert '"role": "reasoning"' in response.text
    assert "Test " in response.text
    assert "response (reasoning)" in response.text


def test_history():
    session_id = client.post("/api/sessions").json()["session_id"]
    response = client.post(
        "/api/chat",
        json={"session_id": session_id, "message": "Remember this", "stream": False},
    )
    assert response.status_code == 200
    messages = client.get(f"/api/sessions/{session_id}/history").json()["messages"]
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_clear_history():
    session_id = client.post("/api/sessions").json()["session_id"]
    client.post(
        "/api/chat",
        json={"session_id": session_id, "message": "Test", "stream": False},
    )
    response = client.delete(f"/api/sessions/{session_id}/history")
    assert response.status_code == 200
    assert client.get(f"/api/sessions/{session_id}/history").json()["messages"] == []
