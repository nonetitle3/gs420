"""Phase 6 image vision/OCR adapters."""
from __future__ import annotations

import base64
from pathlib import Path
from typing import Any


class VisionService:
    provider = "none"

    def analyze(self, image_path: str, prompt: str = "") -> dict[str, Any]:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError("Image file not found.")
        raise RuntimeError(
            "No vision provider is configured. Set up a vision-model adapter."
        )


class OCRService:
    provider = "none"

    def extract_text(self, image_path: str, language: str = "ben+eng") -> dict[str, Any]:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError("Image file not found.")
        raise RuntimeError(
            "No OCR provider is configured. Set up an OCR adapter such as Tesseract."
        )
