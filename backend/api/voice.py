from fastapi import APIRouter,UploadFile,File,HTTPException
from pathlib import Path
import uuid
from backend.services.stt import STTService
from backend.config import settings
from backend.security import validate_upload
router=APIRouter(prefix="/api/voice",tags=["voice"]);stt=STTService()
ALLOWED={".wav",".mp3",".m4a",".ogg",".webm",".flac"}
@router.post("/transcribe")
async def transcribe(file:UploadFile=File(...)):
    data=await file.read();name=validate_upload(data,file.filename or "",settings.max_upload_mb,ALLOWED)
    path=Path(settings.upload_dir)/(str(uuid.uuid4())+"_"+name);path.write_bytes(data)
    try:return stt.transcribe(path)
    except Exception as e:raise HTTPException(503,f"STT unavailable: {type(e).__name__}")
