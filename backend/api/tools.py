"""Phase 10 tools API."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.tools import build_default_tool_registry

router = APIRouter(prefix="/api/tools", tags=["tools"])
_registry = build_default_tool_registry()


class ToolExecuteRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    args: dict[str, Any] = Field(default_factory=dict)


@router.get("")
def list_tools() -> dict[str, Any]:
    return {"tools": _registry.list_tools()}


@router.post("/execute")
def execute_tool(request: ToolExecuteRequest) -> dict[str, Any]:
    try:
        result = _registry.execute(request.name, **request.args)
        return {"tool": request.name, "success": True, "result": result}
    except (KeyError, PermissionError, ValueError, TypeError, OSError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
