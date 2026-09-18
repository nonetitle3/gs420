class MemoryAgent:
 def __init__(self,memory):self.memory=memory
 def save(self,text,kind="fact"):self.memory.add_memory(text,kind)
