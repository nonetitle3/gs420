"""GS420 AI chat API."""
from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from backend.core.orchestrator import AIOrchestrator
from backend.dependencies import get_orchestrator

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    session_id: str | None = Field(default=None, min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=20000)
    stream: bool = True
    role: str = Field(default="auto", pattern="^(auto|general|chat|reasoning|coding|vision)$")
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    top_p: float | None = Field(default=None, gt=0.0, le=1.0)
    max_new_tokens: int | None = Field(default=None, ge=1, le=8192)


class ChatResponse(BaseModel):
    session_id: str
    response: str
    role: str


class SessionResponse(BaseModel):
    session_id: str


def _generation_kwargs(request: ChatRequest) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if request.temperature is not None:
        kwargs["temperature"] = request.temperature
    if request.top_p is not None:
        kwargs["top_p"] = request.top_p
    if request.max_new_tokens is not None:
        kwargs["max_new_tokens"] = request.max_new_tokens
    return kwargs


@router.post("/chat", response_model=None)
def chat(request: ChatRequest, orchestrator: AIOrchestrator = Depends(get_orchestrator)) -> Any:
    session_id = request.session_id or orchestrator.new_session()
    try:
        kwargs = _generation_kwargs(request)
        if request.stream:
            selected_role = orchestrator.resolve_role(request.role, request.message)

            def event_stream():
                try:
                    for chunk in orchestrator.stream_chat(
                        session_id, request.message, request.role, **kwargs
                    ):
                        yield (
                            "data: "
                            + json.dumps(
                                {"session_id": session_id, "role": selected_role, "text": chunk},
                                ensure_ascii=False,
                            )
                            + "\n\n"
                        )
                    yield "data: [DONE]\n\n"
                except Exception as exc:
                    yield "data: " + json.dumps({"error": str(exc)}, ensure_ascii=False) + "\n\n"

            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
            )

        selected_role, response = orchestrator.chat(
            session_id, request.message, request.role, **kwargs
        )
        return ChatResponse(session_id=session_id, response=response, role=selected_role)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {exc}") from exc


@router.post("/sessions", response_model=SessionResponse)
def create_session(orchestrator: AIOrchestrator = Depends(get_orchestrator)) -> SessionResponse:
    return SessionResponse(session_id=orchestrator.new_session())


@router.get("/sessions/{session_id}/history")
def history(session_id: str, orchestrator: AIOrchestrator = Depends(get_orchestrator)) -> dict[str, Any]:
    return {"session_id": session_id, "messages": orchestrator.get_history(session_id)}


@router.get("/memory/stats")
def memory_stats(orchestrator: AIOrchestrator = Depends(get_orchestrator)) -> dict[str, Any]:
    return {"status": "ok", "memory": orchestrator.memory.stats()}


@router.delete("/sessions/{session_id}/history")
def clear_history(session_id: str, orchestrator: AIOrchestrator = Depends(get_orchestrator)) -> dict[str, Any]:
    orchestrator.clear_history(session_id)
    return {"status": "ok", "session_id": session_id, "message": "Conversation history cleared."}
