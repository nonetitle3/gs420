"""Phase 15 RAG API with PDF/DOCX extraction and semantic search."""
from __future__ import annotations
import io, os
from typing import Any
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from backend.rag import DocumentStore, EmbeddingProvider
from backend.config import get_settings

router=APIRouter(prefix="/api/rag",tags=["rag"])
_embedding_id=get_settings().embedding_model_id
store=DocumentStore(embedder=EmbeddingProvider(_embedding_id) if _embedding_id else None)
class SearchRequest(BaseModel):
    query:str=Field(min_length=1,max_length=5000)
    limit:int=Field(default=5,ge=1,le=20)
    semantic:bool=False

def _extract_text(filename:str,data:bytes)->str:
    suffix=os.path.splitext(filename)[1].lower()
    if suffix in {".txt",".md",".csv",".json"}: return data.decode("utf-8",errors="replace")
    if suffix==".pdf":
        from pypdf import PdfReader
        reader=PdfReader(io.BytesIO(data))
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    if suffix==".docx":
        from docx import Document
        doc=Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Supported formats: TXT, MD, CSV, JSON, PDF, DOCX.")

@router.get("/stats")
def stats()->dict[str,Any]: return store.stats()

@router.post("/documents")
async def upload_document(file:UploadFile=File(...), embed:bool=Form(False))->dict[str,Any]:
    data=await file.read()
    if not data: raise HTTPException(400,"Document is empty.")
    if len(data)>20*1024*1024: raise HTTPException(413,"Document is too large.")
    try:return store.add(file.filename or "document",_extract_text(file.filename or "",data),create_embeddings=embed)
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
