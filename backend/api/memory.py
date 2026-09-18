from fastapi import APIRouter
from pydantic import BaseModel,Field
from backend.core.memory_manager import MemoryManager
router=APIRouter(prefix="/api/memory",tags=["memory"]);m=MemoryManager()
class M(BaseModel):content:str=Field(min_length=1,max_length=20000);kind:str="fact"
class P(BaseModel):key:str=Field(min_length=1,max_length=200);value:str=Field(max_length=5000)
class SP(BaseModel):title:str=Field(min_length=1,max_length=200);prompt:str=Field(min_length=1,max_length=20000)
@router.get("")
def get():return {"memories":m.memories(),"preferences":m.preferences(),"saved_prompts":m.saved_prompts()}
@router.post("")
def add(x:M):m.add_memory(x.content,x.kind);return {"ok":True}
@router.delete("/{i}")
def delete(i:int):m.delete_memory(i);return {"ok":True}
@router.get("/search")
def search(q:str,limit:int=10):return {"results":m.search(q,max(1,min(limit,50)))}
@router.post("/preferences")
def preference(x:P):m.set_preference(x.key,x.value);return {"ok":True}
@router.post("/prompts")
def prompt(x:SP):return {"id":m.save_prompt(x.title,x.prompt)}
@router.delete("/session/{session_id}")
def clear_session(session_id:str):m.clear_session(session_id);return {"ok":True}
@router.delete("/all")
def delete_all():m.delete_all();return {"ok":True}
