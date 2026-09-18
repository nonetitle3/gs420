"""GS420 AI Phase 2 model router.

Routes requests to general, reasoning, coding, or vision model roles while
keeping the application independent from any single model provider.
"""
from __future__ import annotations

from typing import Any

from backend.config import Settings
from backend.models.base import BaseModel
from backend.models.hf import HuggingFaceModel


class ModelRouter:
    """Lazy, role-based model router."""

    ROLES = ("general", "reasoning", "coding", "vision")

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._models: dict[str, BaseModel] = {}

    def _model_id_for(self, role: str) -> str:
        configured = {
            "general": self.settings.model_id,
            "reasoning": self.settings.reasoning_model_id or self.settings.model_id,
            "coding": self.settings.coding_model_id or self.settings.model_id,
            "vision": self.settings.vision_model_id or self.settings.model_id,
        }
        return configured.get(role, self.settings.model_id)

    def get_model(self, role: str = "general") -> BaseModel:
        normalized = role.lower().strip() or "general"
        if normalized == "chat":
            normalized = "general"
        if normalized not in self.ROLES:
            raise ValueError(f"Unknown model role: {role}")

        model_id = self._model_id_for(normalized)
        key = f"{normalized}:{model_id}:{self.settings.device}"
        if key not in self._models:
            model_settings = self.settings.model_copy(update={"model_id": model_id})
            self._models[key] = HuggingFaceModel(model_settings)
        return self._models[key]

    def route(self, role: str = "auto", message: str = "") -> tuple[str, BaseModel]:
        requested = (role or "auto").lower().strip()

        if requested == "chat":
            requested = "general"
        if requested in self.ROLES:
            return requested, self.get_model(requested)
        if requested != "auto":
            raise ValueError(f"Unknown model role: {role}")

        text = message.lower()
        coding_terms = (
            "python", "javascript", "typescript", "code", "debug",
            "programming", "কোড", "প্রোগ্রাম",
        )
        reasoning_terms = (
            "prove", "derive", "reason", "logic", "math",
            "প্রমাণ", "যুক্তি", "গণিত",
        )

        if any(term in text for term in coding_terms):
            return "coding", self.get_model("coding")
        if any(term in text for term in reasoning_terms):
            return "reasoning", self.get_model("reasoning")
        return "general", self.get_model("general")

    def list_routes(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for role in self.ROLES:
            model_id = self._model_id_for(role)
            result.append({
                "role": role,
                "model_id": model_id,
                "configured": role == "general" or model_id != self.settings.model_id,
            })
        return result
