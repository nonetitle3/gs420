from fastapi import APIRouter,UploadFile,File,HTTPException
from backend.services.stt import STTService
from backend.config import settings
from pathlib import Path
router=APIRouter(prefix="/api/voice",tags=["voice"]);stt=STTService()
@router.post("/transcribe")
async def transcribe(file:UploadFile=File(...)):
    ext=Path(file.filename or "audio.bin").suffix.lower()
    if ext not in {".wav",".mp3",".m4a",".ogg",".webm",".flac"}:raise HTTPException(400,"Unsupported audio format")
    if not file.content_type or not file.content_type.startswith("audio/"):raise HTTPException(400,"Audio file required")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"File too large")
    path=Path(settings.upload_dir)/("voice_"+Path(file.filename or "audio").name)
    path.write_bytes(data)
    try:return stt.transcribe(path)
    except Exception as e:raise HTTPException(503,f"STT unavailable: {type(e).__name__}")
