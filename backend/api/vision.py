"""Phase 6 vision and OCR API."""
from __future__ import annotations

import os
import tempfile
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.vision import OCRService, VisionService

router = APIRouter(prefix="/api/vision", tags=["vision"])
vision = VisionService()
ocr = OCRService()

MAX_IMAGE_BYTES = 15 * 1024 * 1024


async def _save_image(file: UploadFile) -> str:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Image file is empty.")
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image file is too large.")
    suffix = os.path.splitext(file.filename or "")[1].lower() or ".img"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as handle:
        handle.write(data)
        return handle.name


@router.get("/providers")
def providers() -> dict[str, str]:
    return {"vision": vision.provider, "ocr": ocr.provider}


@router.post("/ocr")
async def extract_ocr(
    file: UploadFile = File(...),
    language: str = Form(default="ben+eng"),
) -> dict[str, Any]:
    path = await _save_image(file)
    try:
        return ocr.extract_text(path, language)
    except (FileNotFoundError, RuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form(default=""),
) -> dict[str, Any]:
    path = await _save_image(file)
    try:
        return vision.analyze(path, prompt)
    except (FileNotFoundError, RuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
