from fastapi import APIRouter
from pydantic import BaseModel
from backend.agents.planner import Planner
from backend.api.chat import orch
router=APIRouter(prefix="/api/agents",tags=["agents"])
class A(BaseModel):request:str
@router.post("/run")
def run(x:A):return {"plan":Planner().plan(x.request),"result":orch.chat(x.request)}
