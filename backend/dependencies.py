"""Shared FastAPI dependencies."""
from functools import lru_cache
from backend.config import Settings, get_settings
from backend.core.orchestrator import AIOrchestrator

@lru_cache
def get_orchestrator() -> AIOrchestrator:
    settings: Settings = get_settings()
    return AIOrchestrator(settings)
