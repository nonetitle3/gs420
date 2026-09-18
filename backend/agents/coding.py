"""Coding agent: generate, inspect and optionally test Python snippets."""
from backend.tools.code_runner import run_python
class CodingAgent:
    def __init__(self,orchestrator):self.orchestrator=orchestrator
    def generate(self,request,session_id=None):
        return self.orchestrator.chat(request,session_id=session_id,task="coding")
    def test_python(self,code):return run_python(code)
