def test_planner_creates_controlled_plan():
 from backend.agents.planner import PlannerAgent
 assert PlannerAgent().plan("hello")[0]["agent"]=="reasoning"
def test_executor_blocks_unapproved_agent():
 from backend.agents.executor import ExecutorAgent
 assert ExecutorAgent().execute([{"agent":"shell","task":"rm -rf /"}],{})[0]["status"]=="blocked"
