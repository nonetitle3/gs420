from fastapi import APIRouter,UploadFile,File,HTTPException
from pathlib import Path
from backend.config import settings
from backend.services.ocr import OCRService
from backend.services.vision import VisionService
router=APIRouter(prefix="/api/vision",tags=["vision"])
ocr=OCRService()
vision=VisionService(settings.vision_model_id)
@router.post("/ocr")
async def ocr_image(file:UploadFile=File(...)):
    ext=Path(file.filename or "image.bin").suffix.lower()
    if ext not in {".png",".jpg",".jpeg",".webp",".bmp",".tiff"}:raise HTTPException(400,"Unsupported image format")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"File too large")
    path=Path(settings.upload_dir)/("vision_"+Path(file.filename or "image").name.replace("..","_"));path.write_bytes(data)
    try:return ocr.extract(path)
    except Exception as e:raise HTTPException(503,f"OCR unavailable: {type(e).__name__}")
@router.post("/analyze")
async def analyze_image(file:UploadFile=File(...)):
    ext=Path(file.filename or "image.bin").suffix.lower()
    if ext not in {".png",".jpg",".jpeg",".webp",".bmp",".tiff"}:raise HTTPException(400,"Unsupported image format")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"File too large")
    path=Path(settings.upload_dir)/("vision_"+Path(file.filename or "image").name.replace("..","_"));path.write_bytes(data)
    try:return vision.analyze(path)
    except Exception as e:raise HTTPException(503,f"Vision model unavailable: {type(e).__name__}")
