"""Controlled task planner."""
class PlannerAgent:
    def plan(self,task):
        task=task.strip()
        if not task:return []
        return [{"step":1,"agent":"reasoning","task":task}]
