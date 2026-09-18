from fastapi import APIRouter,UploadFile,File,Form,HTTPException
from pathlib import Path
from backend.config import settings
from backend.services.image_generation import ImageGenerationService
from backend.services.image_tools import enhance,upscale
router=APIRouter(prefix="/api/image",tags=["image"]);generator=ImageGenerationService(None)
@router.post("/generate")
async def generate(prompt:str=Form(...)):
    try:return generator.generate(prompt,Path(settings.upload_dir)/"generated.png")
    except Exception as e:raise HTTPException(503,f"Image generation unavailable: {type(e).__name__}")
@router.post("/enhance")
async def enhance_image(file:UploadFile=File(...)):
    ext=Path(file.filename or "").suffix.lower()
    if ext not in {".png",".jpg",".jpeg",".webp"}:raise HTTPException(400,"Unsupported image format")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"File too large")
    src=Path(settings.upload_dir)/("src_"+Path(file.filename).name.replace("..","_"));src.write_bytes(data)
    try:return enhance(src,Path(settings.upload_dir)/("enhanced_"+src.name))
    except Exception as e:raise HTTPException(500,f"Enhancement failed: {type(e).__name__}")
@router.post("/upscale")
async def upscale_image(file:UploadFile=File(...),scale:int=Form(2)):
    if scale not in {2,3,4}:raise HTTPException(400,"Scale must be 2, 3 or 4")
    ext=Path(file.filename or "").suffix.lower()
    if ext not in {".png",".jpg",".jpeg",".webp"}:raise HTTPException(400,"Unsupported image format")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"File too large")
    src=Path(settings.upload_dir)/("src_"+Path(file.filename).name.replace("..","_"));src.write_bytes(data)
    try:return upscale(src,Path(settings.upload_dir)/("up_"+src.name),scale)
    except Exception as e:raise HTTPException(500,f"Upscale failed: {type(e).__name__}")
