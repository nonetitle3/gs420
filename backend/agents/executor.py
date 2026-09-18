"""Permission-aware agent executor; no unrestricted shell access."""
class ExecutorAgent:
    ALLOWED={"reasoning","vision","memory","research"}
    def execute(self,steps,agents):
        results=[]
        for step in steps:
            name=step.get("agent")
            if name not in self.ALLOWED:results.append({"step":step,"status":"blocked"});continue
            agent=agents.get(name)
            if agent is None:results.append({"step":step,"status":"unavailable"});continue
            method=getattr(agent,"solve",None) or getattr(agent,"research",None) or getattr(agent,"recall",None)
            if method is None:results.append({"step":step,"status":"unsupported"});continue
            results.append({"step":step,"status":"ok","result":method(step.get("task",""))})
        return results
