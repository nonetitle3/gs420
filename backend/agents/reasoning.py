class ReasoningAgent:
    def solve(self,task,orchestrator=None):
        if orchestrator:return orchestrator.chat(task,task="reasoning")
        return {"task":task,"status":"ready"}
