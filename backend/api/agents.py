from fastapi import APIRouter
from pydantic import BaseModel,Field
from backend.agents.planner import PlannerAgent
router=APIRouter(prefix="/api/agents",tags=["agents"]);planner=PlannerAgent()
class PlanRequest(BaseModel):
    task:str=Field(min_length=1,max_length=10000)
@router.post("/plan")
def plan(x:PlanRequest):return {"task":x.task,"steps":planner.plan(x.task)}
