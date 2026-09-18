"""Phase 9 secure, permission-aware AI agent foundation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class ToolPermission:
    name: str
    description: str
    enabled: bool = False


@dataclass
class AgentStep:
    action: str
    status: str
    result: Any = None


@dataclass
class AgentResult:
    goal: str
    status: str
    steps: list[AgentStep] = field(default_factory=list)


class AgentToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[ToolPermission, Callable[..., Any]]] = {}

    def register(
        self,
        name: str,
        description: str,
        handler: Callable[..., Any],
        enabled: bool = False,
    ) -> None:
        self._tools[name] = (ToolPermission(name, description, enabled), handler)

    def list_tools(self) -> list[dict[str, Any]]:
        return [
            {
                "name": permission.name,
                "description": permission.description,
                "enabled": permission.enabled,
            }
            for permission, _ in self._tools.values()
        ]

    def execute(self, name: str, **kwargs: Any) -> Any:
        item = self._tools.get(name)
        if item is None:
            raise KeyError(f"Unknown agent tool: {name}")
        permission, handler = item
        if not permission.enabled:
            raise PermissionError(f"Agent tool '{name}' is disabled.")
        return handler(**kwargs)


class AgentEngine:
    """Small deterministic agent loop.

    Phase 9 establishes planning/tool-permission boundaries. It intentionally
    does not grant arbitrary shell, filesystem, network, or browser access.
    """

    def __init__(self, registry: AgentToolRegistry, max_steps: int = 5) -> None:
        self.registry = registry
        self.max_steps = max_steps

    def run(self, goal: str, actions: list[dict[str, Any]]) -> AgentResult:
        if not goal.strip():
            raise ValueError("Goal cannot be empty.")
        if len(actions) > self.max_steps:
            raise ValueError(f"Maximum agent steps is {self.max_steps}.")

        result = AgentResult(goal=goal, status="completed")
        for action in actions:
            name = str(action.get("tool", "")).strip()
            args = action.get("args", {})
            if not isinstance(args, dict):
                raise ValueError("Tool args must be an object.")
            try:
                value = self.registry.execute(name, **args)
                result.steps.append(AgentStep(name, "success", value))
            except Exception as exc:
                result.steps.append(AgentStep(name, "error", str(exc)))
                result.status = "partial"
        return result
