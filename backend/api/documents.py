from fastapi import APIRouter,UploadFile,File,HTTPException
from backend.config import settings
from backend.services.ocr import extract_pdf,ocr_image
from pathlib import Path
import uuid
router=APIRouter(prefix="/api/documents",tags=["documents"])
@router.post("/upload")
async def upload(file:UploadFile=File(...)):
 ext=Path(file.filename or "").suffix.lower()
 if ext not in {".pdf",".txt",".docx",".csv",".xlsx",".png",".jpg",".jpeg",".webp"}:raise HTTPException(400,"Unsupported file")
 data=await file.read()
 if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"File too large")
 p=Path(settings.upload_dir)/(uuid.uuid4().hex+ext);p.write_bytes(data);text="";pages=None
 if ext==".pdf":text,pages=extract_pdf(p)
 elif ext in {".png",".jpg",".jpeg",".webp"}:text=ocr_image(p)
 elif ext==".txt":text=data.decode("utf8","ignore")
 return {"filename":file.filename,"path":str(p),"pages":pages,"text":text[:100000]}
