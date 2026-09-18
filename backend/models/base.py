from abc import ABC,abstractmethod
class BaseModel(ABC):
 @abstractmethod
 def generate(self,messages,**kwargs):raise NotImplementedError
 def stream(self,messages,**kwargs):yield self.generate(messages,**kwargs)
