"""Phase 13 management endpoints."""
from fastapi import APIRouter, Request

from backend.admin import dashboard_snapshot, require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard")
def dashboard(request: Request) -> dict:
    require_admin(request)
    return dashboard_snapshot()


@router.get("/health")
def admin_health(request: Request) -> dict:
    require_admin(request)
    return {"status": "ok", "service": "gs420-ai", "phase": 13}


@router.get("/environment")
def environment(request: Request) -> dict:
    require_admin(request)
    return {"environment": dashboard_snapshot()["environment"]}
