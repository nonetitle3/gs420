from fastapi import APIRouter,UploadFile,File,HTTPException
from backend.config import settings
from backend.services.ocr import ocr_image
router=APIRouter(prefix="/api/vision",tags=["vision"])
@router.post("/ocr")
async def ocr(file:UploadFile=File(...)):
 ext=(file.filename or "").lower()
 if not ext.endswith((".png",".jpg",".jpeg",".webp")):raise HTTPException(400,"Image required")
 p=settings.upload_dir+"/"+(file.filename or "image");open(p,"wb").write(await file.read())
 return {"text":ocr_image(p)}
