"""Phase 9 agent API."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.agent import AgentEngine, AgentToolRegistry
from backend.core.orchestrator import AIOrchestrator
from backend.dependencies import get_orchestrator

router = APIRouter(prefix="/api/agents", tags=["agents"])


class AgentAction(BaseModel):
    tool: str = Field(min_length=1, max_length=100)
    args: dict[str, Any] = Field(default_factory=dict)


class AgentRunRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=10000)
    actions: list[AgentAction] = Field(default_factory=list, max_length=5)


_registry = AgentToolRegistry()
_engine = AgentEngine(_registry, max_steps=5)


@router.get("/tools")
def tools() -> dict[str, Any]:
    return {"tools": _registry.list_tools()}


@router.post("/run")
def run_agent(
    request: AgentRunRequest,
    orchestrator: AIOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    del orchestrator
    try:
        result = _engine.run(
            request.goal,
            [action.model_dump() for action in request.actions],
        )
        return {
            "goal": result.goal,
            "status": result.status,
            "steps": [
                {"action": step.action, "status": step.status, "result": step.result}
                for step in result.steps
            ],
        }
    except (ValueError, KeyError, PermissionError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
