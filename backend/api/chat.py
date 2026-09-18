from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel,Field
import json
from backend.core.orchestrator import Orchestrator
router=APIRouter(prefix="/api/chat",tags=["chat"]);orch=Orchestrator()
class ChatRequest(BaseModel):
    message:str=Field(min_length=1,max_length=20000)
    session_id:str|None=None
    task:str|None=None
@router.post("")
def chat(x:ChatRequest): return orch.chat(x.message,x.session_id,x.task)
@router.post("/stream")
def stream(x:ChatRequest):
    def events():
        for item in orch.stream(x.message,x.session_id,x.task):
            yield "data: "+json.dumps(item,ensure_ascii=False)+"\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(events(),media_type="text/event-stream",headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})
