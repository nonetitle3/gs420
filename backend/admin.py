"""GS420 AI management dashboard API helpers."""
from __future__ import annotations

from datetime import datetime, timezone
import hmac

from fastapi import HTTPException, Request

from backend.config import get_settings
from backend.security import redacted_environment


def require_admin(request: Request) -> None:
    expected = get_settings().admin_token
    if not expected:
        raise HTTPException(
            status_code=503,
            detail="Admin access is not configured. Set GS420_ADMIN_TOKEN.",
        )
    supplied = request.headers.get("X-GS420-Admin-Token", "")
    if not supplied or not hmac.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="Invalid admin token.")


def dashboard_snapshot() -> dict:
    settings = get_settings()
    return {
        "service": "gs420-ai",
        "version": "1.1.0",
        "phase": 13,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "configuration": {
            "model_id": settings.model_id,
            "reasoning_model_id": settings.reasoning_model_id,
            "coding_model_id": settings.coding_model_id,
            "vision_model_id": settings.vision_model_id,
            "device": settings.device,
            "max_new_tokens": settings.max_new_tokens,
            "temperature": settings.temperature,
            "top_p": settings.top_p,
        },
        "environment": redacted_environment(),
    }
