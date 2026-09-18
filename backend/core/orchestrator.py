import uuid
from backend.config import settings
from backend.core.model_router import ModelRouter
from backend.core.memory_manager import MemoryManager
from backend.models.hf import HuggingFaceModel
class Orchestrator:
 def __init__(self):self.router=ModelRouter();self.memory=MemoryManager();self.models={}
 def chat(self,message,session_id=None,task=None):
  sid=session_id or str(uuid.uuid4());route=self.router.route(message,task);msgs=[{"role":"system","content":"You are GS420 AI. Answer in Bengali or English matching the user."}]+self.memory.history(sid)+[{"role":"user","content":message}]
  try:self.models.setdefault(route.model,HuggingFaceModel(route.model,settings.device));answer=self.models[route.model].generate(msgs,max_new_tokens=settings.max_new_tokens,temperature=settings.temperature)
  except Exception as e:answer=f"Model unavailable: {type(e).__name__}. Configure a compatible Hugging Face/local model."
  self.memory.add_message(sid,"user",message);self.memory.add_message(sid,"assistant",answer)
  return {"session_id":sid,"answer":answer,"task":route.task,"model":route.model}
