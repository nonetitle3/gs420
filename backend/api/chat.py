from fastapi import APIRouter
from pydantic import BaseModel,Field
from backend.core.orchestrator import Orchestrator
router=APIRouter(prefix="/api/chat",tags=["chat"]);orch=Orchestrator()
class ChatRequest(BaseModel):
 message:str=Field(min_length=1,max_length=20000);session_id:str|None=None;task:str|None=None
@router.post("")
def chat(x:ChatRequest):return orch.chat(x.message,x.session_id,x.task)
