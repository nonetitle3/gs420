from concurrent.futures import ThreadPoolExecutor
class TaskManager:
 def __init__(self,max_workers=2):self.pool=ThreadPoolExecutor(max_workers=max_workers)
 def submit(self,fn,*a,**kw):return self.pool.submit(fn,*a,**kw)
