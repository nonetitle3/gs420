class ExecutorAgent:
 def __init__(self,allowed_tools=()):self.allowed=set(allowed_tools)
 def execute(self,name,fn,*args,**kwargs):
  if name not in self.allowed:raise PermissionError("Tool permission denied")
  return fn(*args,**kwargs)
