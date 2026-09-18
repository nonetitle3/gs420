from fastapi import APIRouter
router=APIRouter(prefix="/api/video",tags=["video"])
@router.get("/status")
def status():return {"available":False,"backend":"GPU/Colab optional"}
