import os
class ResourceManager:
 def info(self):
  d={"cpu":os.cpu_count()}
  try:
   import torch;d.update(cuda=torch.cuda.is_available(),gpu=torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
  except Exception:d.update(cuda=False,gpu=None)
  return d
