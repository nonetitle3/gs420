"""Phase 5 voice API."""
from __future__ import annotations

import os
import tempfile
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from backend.voice import SpeechToText, TextToSpeech

router = APIRouter(prefix="/api/voice", tags=["voice"])
stt = SpeechToText()
tts = TextToSpeech()


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)
    language: str = Field(default="en", min_length=2, max_length=10)


@router.get("/providers")
def providers() -> dict[str, str]:
    return {"stt": stt.provider, "tts": tts.provider}


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)) -> dict[str, Any]:
    suffix = os.path.splitext(file.filename or "")[1] or ".audio"
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Audio file is empty.")
    if len(data) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Audio file is too large.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as handle:
        handle.write(data)
        path = handle.name
    try:
        return stt.transcribe(path)
    except (FileNotFoundError, RuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


@router.post("/synthesize")
def synthesize(request: TTSRequest) -> Any:
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        result = tts.synthesize(request.text, path, request.language)
        return FileResponse(result["audio_path"], media_type="audio/wav", filename="gs420-tts.wav")
    except RuntimeError as exc:
        try:
            os.unlink(path)
        except OSError:
            pass
        raise HTTPException(status_code=503, detail=str(exc)) from exc
