from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.memory_manager import MemoryManager
router=APIRouter(prefix="/api/memory",tags=["memory"]);m=MemoryManager()
class M(BaseModel):content:str;kind:str="fact"
@router.get("")
def get():return m.memories()
@router.post("")
def add(x:M):m.add_memory(x.content,x.kind);return {"ok":True}
@router.delete("/{i}")
def delete(i:int):m.delete_memory(i);return {"ok":True}
