from dataclasses import dataclass
from backend.config import settings
@dataclass
class Route: task:str; model:str; reason:str
class ModelRouter:
 TASKS={"general_chat","reasoning","coding","summarization","translation","vision","OCR","image_generation","video_generation","voice"}
 def classify(self,text="",task=None):
  if task in self.TASKS:return task
  t=(text or "").lower()
  if any(x in t for x in ("python","code","debug","javascript","typescript")):return "coding"
  if any(x in t for x in ("translate","অনুবাদ")):return "translation"
  if any(x in t for x in ("summarize","সারাংশ")):return "summarization"
  if any(x in t for x in ("reason","prove","কেন")):return "reasoning"
  return "general_chat"
 def route(self,text="",task=None):return Route(self.classify(text,task),settings.model_id,"intent classification + fallback")
