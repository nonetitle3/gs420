from .base import BaseModel
class GGUFModel(BaseModel):
 def __init__(self,path,n_ctx=4096):self.path=path;self.n_ctx=n_ctx;self.llm=None
 def generate(self,messages,**kw):
  if self.llm is None:
   from llama_cpp import Llama;self.llm=Llama(model_path=self.path,n_ctx=self.n_ctx,verbose=False)
  return self.llm.create_chat_completion(messages=messages,max_tokens=kw.get("max_new_tokens",256),temperature=kw.get("temperature",.7))["choices"][0]["message"]["content"]
