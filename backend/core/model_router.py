"""Task-aware model routing with ordered fallback candidates."""
from dataclasses import dataclass
from backend.config import settings

@dataclass(frozen=True)
class Route:
    task: str
    model: str
    candidates: tuple[str,...]
    reason: str

class ModelRouter:
    TASKS={"general_chat","reasoning","coding","summarization","translation","vision","OCR","image_generation","video_generation","voice"}
    def classify(self,text="",task=None):
        if task in self.TASKS:return task
        t=(text or "").lower()
        rules={
            "coding":("python","code","debug","javascript","typescript","কোড","প্রোগ্রাম"),
            "translation":("translate","অনুবাদ","translation"),
            "summarization":("summarize","summary","সারাংশ"),
            "reasoning":("reason","prove","logic","math","কেন","যুক্তি","গণিত"),
            "OCR":("ocr","text from image","ছবির লেখা"),
            "vision":("image","picture","ছবি","screenshot"),
            "image_generation":("generate image","create image","ছবি তৈরি"),
            "video_generation":("generate video","create video","ভিডিও তৈরি"),
            "voice":("speech","voice","কণ্ঠ","অডিও"),
        }
        for name,keys in rules.items():
            if any(k in t for k in keys):return name
        return "general_chat"

    def candidates(self,task):
        specialist={"reasoning":settings.reasoning_model_id,"coding":settings.coding_model_id,"vision":settings.vision_model_id}.get(task)
        values=[]
        if specialist:values.append(specialist)
        if settings.model_id not in values:values.append(settings.model_id)
        return tuple(values)

    def route(self,text="",task=None):
        role=self.classify(text,task)
        candidates=self.candidates(role)
        return Route(role,candidates[0],candidates,"specialist model when configured, then general fallback")
