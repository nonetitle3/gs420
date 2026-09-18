"""Phase 7 image generation and editing API."""
from __future__ import annotations

import os
import tempfile
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.image_ai import ImageAIService

router = APIRouter(prefix="/api/image", tags=["image"])
image_ai = ImageAIService()
MAX_IMAGE_BYTES = 15 * 1024 * 1024


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10000)
    width: int = Field(default=512, ge=256, le=1536)
    height: int = Field(default=512, ge=256, le=1536)
    steps: int = Field(default=20, ge=1, le=100)
    seed: int | None = Field(default=None, ge=0)


async def _save_upload(file: UploadFile, prefix: str) -> str:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Image file is empty.")
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image file is too large.")
    suffix = os.path.splitext(file.filename or "")[1].lower() or ".img"
    handle = tempfile.NamedTemporaryFile(delete=False, prefix=prefix, suffix=suffix)
    try:
        handle.write(data)
        return handle.name
    finally:
        handle.close()


@router.get("/providers")
def providers() -> dict[str, str]:
    return {"image": image_ai.provider}


@router.post("/generate")
def generate(request: GenerateRequest) -> dict[str, Any]:
    try:
        return image_ai.generate(
            request.prompt, request.width, request.height, request.steps, request.seed
        )
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/edit")
async def edit(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    mask: UploadFile | None = File(default=None),
) -> dict[str, Any]:
    image_path = await _save_upload(file, "gs420-image-")
    mask_path = None
    try:
        if mask is not None:
            mask_path = await _save_upload(mask, "gs420-mask-")
        return image_ai.edit(image_path, prompt, mask_path)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        for path in (image_path, mask_path):
            if path:
                try:
                    os.unlink(path)
                except OSError:
                    pass
