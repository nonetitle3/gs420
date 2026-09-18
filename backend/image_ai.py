"""Phase 7 image generation/editing adapters.

The service is provider-agnostic. A deployment can later plug in Diffusers,
SDXL/SD3, FLUX, or another local/open-weight image backend without changing
the HTTP API.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


class ImageAIService:
    provider = "none"

    def generate(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        steps: int = 20,
        seed: int | None = None,
    ) -> dict[str, Any]:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        raise RuntimeError(
            "No image provider is configured. Install/configure an image "
            "generation adapter such as Diffusers."
        )

    def edit(
        self,
        image_path: str,
        prompt: str,
        mask_path: str | None = None,
    ) -> dict[str, Any]:
        if not Path(image_path).exists():
            raise FileNotFoundError("Source image not found.")
        if mask_path and not Path(mask_path).exists():
            raise FileNotFoundError("Mask image not found.")
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        raise RuntimeError(
            "No image provider is configured. Install/configure an image "
            "editing adapter."
        )
