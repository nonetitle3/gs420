def test_coding_agent_api_shape():
 from backend.agents.coding import CodingAgent
 assert hasattr(CodingAgent,"generate") and hasattr(CodingAgent,"test_python")
def test_runner_blocks_shell():
 from backend.tools.code_runner import run_python
 assert run_python("import os; os.system('echo bad')")["ok"] is False
