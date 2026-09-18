from .base import BaseModel
class HuggingFaceModel(BaseModel):
 def __init__(self,model_id,device="auto"):self.model_id=model_id;self.device=device;self.tokenizer=None;self.model=None
 def _load(self):
  if self.model:return
  from transformers import AutoTokenizer,AutoModelForCausalLM
  import torch
  self.tokenizer=AutoTokenizer.from_pretrained(self.model_id)
  self.model=AutoModelForCausalLM.from_pretrained(self.model_id,device_map="auto" if self.device=="auto" and torch.cuda.is_available() else None)
 def generate(self,messages,max_new_tokens=256,temperature=.7,**kw):
  self._load();import torch
  p=self.tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True);x=self.tokenizer(p,return_tensors="pt")
  if hasattr(self.model,"device"):x={k:v.to(self.model.device) for k,v in x.items()}
  with torch.no_grad():y=self.model.generate(**x,max_new_tokens=max_new_tokens,do_sample=temperature>0,temperature=max(.01,temperature),pad_token_id=self.tokenizer.eos_token_id)
  return self.tokenizer.decode(y[0][x["input_ids"].shape[1]:],skip_special_tokens=True).strip()
