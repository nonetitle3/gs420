"""Phase 14 observability endpoints."""
from fastapi import APIRouter, Request

from backend.admin import require_admin
from backend.observability import observability

router = APIRouter(prefix="/api/metrics", tags=["observability"])

@router.get("/summary")
def summary(request: Request) -> dict:
    require_admin(request)
    return observability.snapshot()

@router.get("/health")
def metrics_health(request: Request) -> dict:
    require_admin(request)
    data = observability.snapshot()
    return {
        "status": "ok",
        "uptime_seconds": data["uptime_seconds"],
        "requests_total": data["requests_total"],
        "errors_5xx": data["errors_5xx"],
    }
