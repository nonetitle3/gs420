"""Phase 15 RAG API with PDF/DOCX extraction and semantic search."""
from __future__ import annotations
import io, os, tempfile
from typing import Any
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from backend.rag import DocumentStore, EmbeddingProvider\nfrom backend.vision import OCRService\nfrom backend.config import get_settings
from backend.config import get_settings

router=APIRouter(prefix="/api/rag",tags=["rag"])
_embedding_id=get_settings().embedding_model_id
store=DocumentStore(embedder=EmbeddingProvider(_embedding_id) if _embedding_id else None)\nocr=OCRService()
class SearchRequest(BaseModel):
    query:str=Field(min_length=1,max_length=5000)
    limit:int=Field(default=5,ge=1,le=20)
    semantic:bool=False

def _extract_text(filename:str,data:bytes,ocr_scanned:bool=False,language:str="ben+eng",preprocess:str="balanced")->tuple[str,dict[str,Any]]:
    suffix=os.path.splitext(filename)[1].lower()
    if suffix in {".txt",".md",".csv",".json"}: return data.decode("utf-8",errors="replace"), {"method":"text"}
    if suffix==".pdf":
        from pypdf import PdfReader
        reader=PdfReader(io.BytesIO(data))
        return "\n".join((p.extract_text() or "") for p in reader.pages), {"method":"pdf_text"}
    if suffix==".docx":
        from docx import Document
        doc=Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs), {"method":"docx_text"}
    raise ValueError("Supported formats: TXT, MD, CSV, JSON, PDF, DOCX.")

@router.get("/stats")
def stats()->dict[str,Any]: return store.stats()

@router.post("/documents")
async def upload_document(file:UploadFile=File(...), embed:bool=Form(False), ocr_scanned:bool=Form(False), language:str=Form("ben+eng"), preprocess:str=Form("balanced"))->dict[str,Any]:
    data=await file.read()
    if not data: raise HTTPException(400,"Document is empty.")
    if len(data)>20*1024*1024: raise HTTPException(413,"Document is too large.")
    try:filename=file.filename or "document"
        text=_extract_text(filename,data,ocr_scanned=ocr_scanned,language=language)
        if not text: raise ValueError("No extractable text found. For scanned PDFs, enable ocr_scanned=true.")
        return store.add(filename,text,create_embeddings=embed)\n
    except RuntimeError as exc: raise HTTPException(503,str(exc)) from exc
    except ValueError as exc: raise HTTPException(415,str(exc)) from exc

@router.post("/search")
def search(request:SearchRequest)->dict[str,Any]:
    if request.semantic and store.embedder is None:
        raise HTTPException(503,"Semantic search is not configured. Set GS420_EMBEDDING_MODEL_ID and restart.")
    return {"results":store.search(request.query,request.limit,request.semantic)}

@router.get("/documents/{document_id}")
def get_document(document_id:str)->dict[str,Any]:
    item=store.get(document_id)
    if item is None: raise HTTPException(404,"Document not found.")
    return item

@router.delete("/documents/{document_id}")
def delete_document(document_id:str)->dict[str,bool]: return {"deleted":store.delete(document_id)}
