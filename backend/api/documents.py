from fastapi import APIRouter,UploadFile,File,HTTPException
from pathlib import Path
import uuid
from backend.config import settings
from backend.services.document_ai import DocumentAI
from backend.core.rag import RAGStore
from backend.security import validate_upload
router=APIRouter(prefix="/api/documents",tags=["documents"]);ingest=DocumentAI();rag=RAGStore(settings.db_path)
ALLOWED={".pdf",".txt",".md",".csv",".docx",".xlsx",".png",".jpg",".jpeg",".webp"}
@router.post("/upload")
async def upload(file:UploadFile=File(...)):
    data=await file.read();name=validate_upload(data,file.filename or "",settings.max_upload_mb,ALLOWED)
    did=str(uuid.uuid4());path=Path(settings.upload_dir)/(did+"_"+name);path.write_bytes(data)
    if Path(name).suffix.lower() in {".png",".jpg",".jpeg",".webp"}:return {"document_id":did,"text":"","ocr_required":True}
    try:
        result=ingest.extract(path);rag.add(did,result["text"]);return {"document_id":did,**result}
    except Exception as e:raise HTTPException(422,f"Document extraction failed: {type(e).__name__}")
@router.get("/search")
def search(q:str,limit:int=5):
    if not q.strip():raise HTTPException(400,"Query required")
    limit=max(1,min(limit,20));return {"results":rag.search(q,limit)}
