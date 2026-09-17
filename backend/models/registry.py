"""Model registry for GS420 AI."""
from __future__ import annotations
from typing import Any
from backend.config import Settings
from backend.models.base import BaseModel
from backend.models.hf import HuggingFaceModel

class ModelRegistry:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._models: dict[str, BaseModel] = {}

    def get_text_model(self) -> BaseModel:
        key = f"text:{self.settings.model_id}"
        if key not in self._models:
            self._models[key] = HuggingFaceModel(self.settings)
        return self._models[key]

    def list_models(self) -> list[dict[str, Any]]:
        model = self.get_text_model()
        return [{"name": "default-text", **model.info()}]
