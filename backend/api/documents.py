from fastapi import APIRouter,UploadFile,File,HTTPException
from pathlib import Path
import uuid
from backend.config import settings
from backend.services.document_ai import DocumentAI
from backend.core.rag import RAGStore
router=APIRouter(prefix="/api/documents",tags=["documents"]);ingest=DocumentAI();rag=RAGStore(settings.db_path)
ALLOWED={".pdf",".txt",".md",".csv",".docx",".xlsx",".png",".jpg",".jpeg",".webp"}
@router.post("/upload")
async def upload(file:UploadFile=File(...)):
    ext=Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED:raise HTTPException(400,"Unsupported document format")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024:raise HTTPException(413,"File too large")
    did=str(uuid.uuid4());safe=Path(file.filename or "document").name.replace("..","_");path=Path(settings.upload_dir)/(did+"_"+safe);path.write_bytes(data)
    if ext in {".png",".jpg",".jpeg",".webp"}:return {"document_id":did,"text":"","ocr_required":True,"path":str(path)}
    try:
        result=ingest.extract(path);rag.add(did,result["text"])
        return {"document_id":did,**result}
    except Exception as e:raise HTTPException(422,f"Document extraction failed: {type(e).__name__}")
@router.get("/search")
def search(q:str,limit:int=5):
    if not q.strip():raise HTTPException(400,"Query required")
    return {"results":rag.search(q,limit)}
