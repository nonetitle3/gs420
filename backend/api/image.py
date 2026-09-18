from fastapi import APIRouter
router=APIRouter(prefix="/api/image",tags=["image"])
@router.get("/status")
def status():return {"available":False,"backend":"optional Diffusers"}
