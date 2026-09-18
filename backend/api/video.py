"""Phase 8 video generation API."""
from __future__ import annotations

import os
import tempfile
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.video_ai import VideoAIService

router = APIRouter(prefix="/api/video", tags=["video"])
video_ai = VideoAIService()
MAX_IMAGE_BYTES = 15 * 1024 * 1024


class GenerateVideoRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10000)
    duration_seconds: int = Field(default=4, ge=1, le=30)
    width: int = Field(default=512, ge=256, le=1536)
    height: int = Field(default=512, ge=256, le=1536)
    fps: int = Field(default=8, ge=1, le=30)
    seed: int | None = Field(default=None, ge=0)


@router.get("/providers")
def providers() -> dict[str, str]:
    return {"video": video_ai.provider}


@router.post("/generate")
def generate(request: GenerateVideoRequest) -> dict[str, Any]:
    try:
        return video_ai.generate(
            request.prompt,
            request.duration_seconds,
            request.width,
            request.height,
            request.fps,
            request.seed,
        )
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/image-to-video")
async def image_to_video(
    file: UploadFile = File(...),
    prompt: str = Form(default=""),
    duration_seconds: int = Form(default=4, ge=1, le=30),
    fps: int = Form(default=8, ge=1, le=30),
) -> dict[str, Any]:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Image file is empty.")
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image file is too large.")
    suffix = os.path.splitext(file.filename or "")[1].lower() or ".img"
    handle = tempfile.NamedTemporaryFile(delete=False, prefix="gs420-video-", suffix=suffix)
    try:
        handle.write(data)
        path = handle.name
    finally:
        handle.close()

    try:
        return video_ai.image_to_video(path, prompt, duration_seconds, fps)
    except (FileNotFoundError, RuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
