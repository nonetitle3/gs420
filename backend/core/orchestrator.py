import uuid
from backend.config import settings
from backend.core.model_router import ModelRouter
from backend.core.memory_manager import MemoryManager
from backend.models.hf import HuggingFaceModel

class Orchestrator:
    def __init__(self):
        self.router=ModelRouter();self.memory=MemoryManager();self.models={}
    def _model(self,model_id):
        if model_id not in self.models:self.models[model_id]=HuggingFaceModel(model_id,settings.device)
        return self.models[model_id]
    def build_messages(self,message,session_id):
        return [{"role":"system","content":"You are GS420 AI. Answer in Bengali or English matching the user."}]+self.memory.history(session_id,settings.max_history_messages)+[{"role":"user","content":message}]
    def chat(self,message,session_id=None,task=None):
        sid=session_id or str(uuid.uuid4());route=self.router.route(message,task);last=None
        for model_id in route.candidates:
            try:
                answer=self._model(model_id).generate(self.build_messages(message,sid),max_new_tokens=settings.max_new_tokens,temperature=settings.temperature,top_p=settings.top_p)
                self.memory.add_message(sid,"user",message);self.memory.add_message(sid,"assistant",answer)
                return {"session_id":sid,"answer":answer,"task":route.task,"model":model_id,"fallback_candidates":list(route.candidates)}
            except Exception as e:last=e
        answer=f"Model unavailable: {type(last).__name__ if last else 'UnknownError'}. Configure a compatible Hugging Face/local model."
        self.memory.add_message(sid,"user",message);self.memory.add_message(sid,"assistant",answer)
        return {"session_id":sid,"answer":answer,"task":route.task,"model":None,"fallback_candidates":list(route.candidates)}
    def stream(self,message,session_id=None,task=None):
        result=self.chat(message,session_id,task)
        answer=result["answer"];step=max(1,len(answer)//20)
        for i in range(step,len(answer)+step,step):yield {**result,"answer":answer[:i]}
