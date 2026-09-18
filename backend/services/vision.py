"""Replaceable image understanding adapter."""
class VisionService:
    def __init__(self,model_id=None):
        self.model_id=model_id
    def analyze(self,image_path,prompt="Describe this image."):
        if not self.model_id:
            return {"ok":False,"message":"Vision model is not configured","model":None}
        from transformers import pipeline
        pipe=pipeline("image-to-text",model=self.model_id)
        result=pipe(image_path)
        text=result[0].get("generated_text","") if result else ""
        return {"ok":True,"text":text,"model":self.model_id}
