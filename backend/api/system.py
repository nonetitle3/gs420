from fastapi import APIRouter,Query
from backend.core.resource_manager import ResourceManager
from backend.observability import observability
router=APIRouter(prefix="/api/system",tags=["system"])
resources=ResourceManager()
@router.get("/resources")
def resource_info(): return resources.info()
@router.get("/profile")
def resource_profile(): return resources.profile()
@router.get("/can-load")
def can_load(model_gb:float,task:str="general_chat"): return resources.can_load(model_gb,task)
@router.get("/observability")
def observability_summary(): return observability.summary()
@router.get("/metrics")
def metrics(limit:int=Query(100,ge=1,le=1000)): return {"metrics":observability.metrics()[-limit:]}
