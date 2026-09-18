import uuid
from backend.config import settings
from backend.core.model_router import ModelRouter
from backend.core.memory_manager import MemoryManager
from backend.models.hf import HuggingFaceModel

class Orchestrator:
    def __init__(self):
        self.router=ModelRouter()
        self.memory=MemoryManager()
        self.models={}
    def _model(self, model_id):
        if model_id not in self.models:
            self.models[model_id]=HuggingFaceModel(model_id,settings.device)
        return self.models[model_id]
    def build_messages(self,message,session_id):
        return [{"role":"system","content":"You are GS420 AI. Answer in Bengali or English matching the user."}]+self.memory.history(session_id)+[{"role":"user","content":message}]
    def chat(self,message,session_id=None,task=None):
        sid=session_id or str(uuid.uuid4());route=self.router.route(message,task)
        try:
            answer=self._model(route.model).generate(self.build_messages(message,sid),max_new_tokens=settings.max_new_tokens,temperature=settings.temperature)
        except Exception as e:
            answer=f"Model unavailable: {type(e).__name__}. Configure a compatible Hugging Face/local model."
        self.memory.add_message(sid,"user",message);self.memory.add_message(sid,"assistant",answer)
        return {"session_id":sid,"answer":answer,"task":route.task,"model":route.model}
    def stream(self,message,session_id=None,task=None):
        result=self.chat(message,session_id,task)
        text=result["answer"]
        step=max(1,len(text)//20)
        for i in range(step,len(text)+step,step):
            yield {**result,"answer":text[:i]}
