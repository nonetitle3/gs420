from fastapi import APIRouter,UploadFile,File,HTTPException
from backend.config import settings
from backend.services.stt import STTService
router=APIRouter(prefix="/api/voice",tags=["voice"])
@router.post("/transcribe")
async def transcribe(file:UploadFile=File(...)):
 data=await file.read()
 if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"File too large")
 p=settings.upload_dir+"/"+(file.filename or "audio")
 open(p,"wb").write(data)
 return {"text":STTService(settings.stt_model).transcribe(p)}
