from fastapi.testclient import TestClient
from backend.main import app
client=TestClient(app)
def test_health_and_root():
 assert client.get("/health").status_code==200
 assert client.get("/").json()["status"]=="ok"
def test_tools_calculator():
 r=client.post("/api/tools/calculator",json={"expression":"2+3*4"})
 assert r.status_code==200 and r.json()["result"]==14
def test_router_tasks():
 from backend.core.model_router import ModelRouter
 assert ModelRouter().TASKS
def test_memory_basic():
 from backend.core.memory_manager import MemoryManager
 m=MemoryManager();sid="suite";m.add_message(sid,"user","hello");assert m.history(sid)
def test_code_runner_rejects_shell():
 from backend.tools.code_runner import run_python
 try:run_python("import os; os.system('echo blocked')")
 except ValueError:assert True
 else:assert False
