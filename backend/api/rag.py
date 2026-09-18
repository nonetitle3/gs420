"""Phase 11 RAG document API."""
from __future__ import annotations

import io
import os
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.rag import DocumentStore

router = APIRouter(prefix="/api/rag", tags=["rag"])
store = DocumentStore()


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=5000)
    limit: int = Field(default=5, ge=1, le=20)


def _extract_text(filename: str, data: bytes) -> str:
    suffix = os.path.splitext(filename)[1].lower()
    if suffix in {".txt", ".md", ".csv", ".json"}:
        return data.decode("utf-8", errors="replace")
    raise ValueError("Phase 11 currently accepts TXT, MD, CSV, and JSON. PDF/DOCX extraction adapters are planned.")


@router.get("/stats")
def stats() -> dict[str, Any]:
    return store.stats()


@router.post("/documents")
async def upload_document(file: UploadFile = File(...)) -> dict[str, Any]:
    data = await file.read()
    if not data:
        raise HTTPException(400, "Document is empty.")
    if len(data) > 20 * 1024 * 1024:
        raise HTTPException(413, "Document is too large.")
    try:
        return store.add(file.filename or "document", _extract_text(file.filename or "", data))
    except ValueError as exc:
        raise HTTPException(415, str(exc)) from exc


@router.post("/search")
def search(request: SearchRequest) -> dict[str, Any]:
    return {"results": store.search(request.query, request.limit)}


@router.get("/documents/{document_id}")
def get_document(document_id: str) -> dict[str, Any]:
    item = store.get(document_id)
    if item is None:
        raise HTTPException(404, "Document not found.")
    return item


@router.delete("/documents/{document_id}")
def delete_document(document_id: str) -> dict[str, bool]:
    return {"deleted": store.delete(document_id)}
