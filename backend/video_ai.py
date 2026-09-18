"""Phase 8 video AI adapter interface.

Provider-agnostic foundation for text-to-video and image-to-video backends.
Heavy video models are intentionally optional.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


class VideoAIService:
    provider = "none"

    def generate(
        self,
        prompt: str,
        duration_seconds: int = 4,
        width: int = 512,
        height: int = 512,
        fps: int = 8,
        seed: int | None = None,
    ) -> dict[str, Any]:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        raise RuntimeError(
            "No video provider is configured. Install/configure a video "
            "generation adapter."
        )

    def image_to_video(
        self,
        image_path: str,
        prompt: str = "",
        duration_seconds: int = 4,
        fps: int = 8,
    ) -> dict[str, Any]:
        if not Path(image_path).exists():
            raise FileNotFoundError("Source image not found.")
        raise RuntimeError(
            "No video provider is configured. Install/configure an "
            "image-to-video adapter."
        )
