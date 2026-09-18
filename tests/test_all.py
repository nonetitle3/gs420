"""Single-command integration smoke suite for the canonical GS420 foundations."""
from fastapi.testclient import TestClient
from backend.main import app

def test_all_core():
    c=TestClient(app)
    assert c.get("/health").status_code==200
    assert c.get("/").json()["name"]=="GS420 AI"
    r=c.post("/api/chat",json={"message":"hello"})
    assert r.status_code==200 and "session_id" in r.json()
    assert c.get("/api/memory").status_code==200
    assert c.post("/api/tools/python",json={"code":"print(2+3)"}).json()["ok"] is True
    assert c.post("/api/tools/python",json={"code":"import os; os.system('echo x')"}).json()["ok"] is False

def test_router_all_tasks():
    from backend.core.model_router import ModelRouter
    r=ModelRouter()
    for task in ["general_chat","reasoning","coding","summarization","translation","vision","OCR","image_generation","video_generation","voice"]:
        route=r.route("test",task)
        assert route.task==task and route.candidates

def test_memory_crud(tmp_path):
    from backend.core.memory_manager import MemoryManager
    m=MemoryManager(tmp_path/"test.db")
    m.add_message("s","user","hello")
    m.add_memory("fact")
    m.set_preference("language","bn")
    m.save_prompt("test","hello")
    assert m.history("s") and m.memories() and m.preferences() and m.saved_prompts()
    m.clear_session("s");assert not m.history("s")
