class STTService:
 def __init__(self,model):self.model=model;self.pipe=None
 def transcribe(self,path):
  if self.pipe is None:
   from transformers import pipeline;self.pipe=pipeline("automatic-speech-recognition",model=self.model)
  return self.pipe(path)["text"]
