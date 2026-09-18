from fastapi import APIRouter,UploadFile,File,Form,HTTPException
from pathlib import Path
from backend.config import settings
from backend.services.video_generation import VideoGenerationService
from backend.services.video_tools import extract_frames
router=APIRouter(prefix="/api/video",tags=["video"]);generator=VideoGenerationService(None)
@router.post("/generate")
async def generate(prompt:str=Form(...)):
    try:return generator.generate(prompt,Path(settings.upload_dir)/"generated.mp4")
    except Exception as e:raise HTTPException(503,f"Video generation unavailable: {type(e).__name__}")
@router.post("/frames")
async def frames(file:UploadFile=File(...),interval:int=Form(1)):
    ext=Path(file.filename or "").suffix.lower()
    if ext not in {".mp4",".mov",".avi",".mkv",".webm"}:raise HTTPException(400,"Unsupported video format")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"File too large")
    src=Path(settings.upload_dir)/("video_"+Path(file.filename).name.replace("..","_"));src.write_bytes(data)
    try:return extract_frames(src,Path(settings.upload_dir)/("frames_"+src.stem),interval)
    except Exception as e:raise HTTPException(500,f"Frame extraction failed: {type(e).__name__}")
