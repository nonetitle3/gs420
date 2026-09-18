from dataclasses import dataclass
from backend.config import settings

@dataclass(frozen=True)
class Route:
 task:str
 model:str
 reason:str

class ModelRouter:
 TASKS={"general_chat","reasoning","coding","summarization","translation","vision","OCR","image_generation","video_generation","voice"}
 def classify(self,text="",task=None):
  if task in self.TASKS:return task
  t=(text or "").lower()
  rules={
   "coding":("python","code","debug","javascript","typescript","কোড"),
   "translation":("translate","অনুবাদ","translation"),
   "summarization":("summarize","summary","সারাংশ"),
   "reasoning":("reason","prove","logic","math","কেন","যুক্তি","গণিত"),
   "OCR":("ocr","text from image","লেখা পড়"),
  }
  for name,keys in rules.items():
   if any(k in t for k in keys):return name
  return "general_chat"
 def route(self,text="",task=None):
  role=self.classify(text,task)
  model={
   "reasoning":settings.reasoning_model_id,
   "coding":settings.coding_model_id,
   "vision":settings.vision_model_id,
  }.get(role) or settings.model_id
  return Route(role,model,"explicit task or keyword intent; configured specialist, otherwise general fallback")
