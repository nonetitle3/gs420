"""Tool registry with explicit schemas and permission levels."""
from dataclasses import dataclass
from typing import Any,Callable
@dataclass(frozen=True)
class ToolSpec:
    name:str
    description:str
    input_schema:dict
    permission:str
    handler:Callable[...,Any]
class ToolRegistry:
    def __init__(self):self._tools={}
    def register(self,spec):self._tools[spec.name]=spec
    def get(self,name):return self._tools.get(name)
    def list(self):return [{"name":x.name,"description":x.description,"input_schema":x.input_schema,"permission":x.permission} for x in self._tools.values()]
    def execute(self,name,**kwargs):
        spec=self.get(name)
        if not spec:raise KeyError(f"Unknown tool: {name}")
        return spec.handler(**kwargs)
