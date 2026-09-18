from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from backend.models.registry import ModelRegistry,ModelInfo
router=APIRouter(prefix="/api/models",tags=["models"]);registry=ModelRegistry()
class RegisterRequest(BaseModel):
 id:str;task:str;size_gb:float=0;hardware:str="CPU";quantization:str="none";enabled:bool=True;priority:int=100
@router.get("")
def models():return registry.status()
@router.post("")
def register(x:RegisterRequest):return registry.register(ModelInfo(**x.model_dump()))
@router.post("/{model_id}/enable")
def enable(model_id:str):
 if model_id not in registry.items:raise HTTPException(404,"Model not found")
 registry.set_enabled(model_id,True);return {"ok":True}
@router.post("/{model_id}/disable")
def disable(model_id:str):
 if model_id not in registry.items:raise HTTPException(404,"Model not found")
 registry.set_enabled(model_id,False);return {"ok":True}
