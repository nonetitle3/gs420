"""GS420 vision and OCR adapters."""
from __future__ import annotations
from pathlib import Path
from typing import Any

class VisionService:
    provider="none"
    def analyze(self,image_path:str,prompt:str="")->dict[str,Any]:
        if not Path(image_path).exists(): raise FileNotFoundError("Image file not found.")
        raise RuntimeError("No vision provider is configured.")

class OCRService:
    provider="tesseract"
    def extract_text(self,image_path:str,language:str="ben+eng")->dict[str,Any]:
        try:
            import pytesseract
            from PIL import Image
            text=pytesseract.image_to_string(Image.open(image_path),lang=language)
            return {"text":text,"language":language,"provider":self.provider}
        except ImportError as exc:
            raise RuntimeError("Install pytesseract and Pillow for OCR.") from exc
        except Exception as exc:
            raise RuntimeError(f"OCR failed: {exc}") from exc
