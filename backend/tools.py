"""Phase 10 built-in tools with explicit permission boundaries."""
from __future__ import annotations

import ast
import math
import operator
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from backend.agent import AgentToolRegistry


_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}
_ALLOWED_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_ALLOWED_NAMES = {"pi": math.pi, "e": math.e}


def safe_calculate(expression: str) -> float | int:
    """Evaluate arithmetic only; function calls, attributes and imports are rejected."""
    tree = ast.parse(expression, mode="eval")

    def visit(node: ast.AST) -> float | int:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.Name) and node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[type(node.op)](visit(node.operand))
        raise ValueError("Only basic arithmetic expressions are allowed.")

    result = visit(tree)
    if not math.isfinite(float(result)):
        raise ValueError("Result is not finite.")
    return result


def current_time() -> dict[str, str]:
    return {"utc": datetime.now(timezone.utc).isoformat()}


def fetch_url(url: str, max_chars: int = 12000) -> dict[str, Any]:
    """Fetch public HTTP(S) text with conservative limits."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Only absolute HTTP(S) URLs are allowed.")
    if max_chars < 100 or max_chars > 30000:
        raise ValueError("max_chars must be between 100 and 30000.")
    request = Request(url, headers={"User-Agent": "GS420-Tool/1.0"})
    with urlopen(request, timeout=8) as response:
        content_type = response.headers.get("content-type", "")
        if "text/" not in content_type and "json" not in content_type:
            raise ValueError("URL did not return text or JSON content.")
        data = response.read(2_000_000).decode("utf-8", errors="replace")
        return {"url": url, "content_type": content_type, "text": data[:max_chars]}


def build_default_tool_registry() -> AgentToolRegistry:
    registry = AgentToolRegistry()
    registry.register(
        "calculator",
        "Evaluate basic arithmetic expressions.",
        lambda expression: safe_calculate(expression),
        enabled=True,
    )
    registry.register(
        "current_time",
        "Return the current UTC time.",
        lambda: current_time(),
        enabled=True,
    )
    registry.register(
        "fetch_url",
        "Fetch text/JSON from a specified HTTP(S) URL.",
        lambda url, max_chars=12000: fetch_url(url, max_chars),
        enabled=False,
    )
    return registry
