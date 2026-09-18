"""Phase 19-20 OCR quality pipeline."""
from __future__ import annotations
from pathlib import Path
from typing import Any

class OCRService:
    provider="tesseract"

    def preprocess(self, image_path: str, mode: str = "balanced"):
        from PIL import Image, ImageOps, ImageEnhance, ImageFilter
        image=Image.open(image_path).convert("L")
        if mode in {"balanced","aggressive"}:
            image=ImageOps.autocontrast(image)
            image=ImageEnhance.Contrast(image).enhance(1.35 if mode=="balanced" else 1.7)
            image=ImageEnhance.Sharpness(image).enhance(1.25)
            if mode=="aggressive": image=image.filter(ImageFilter.MedianFilter(size=3))
        return image

    def extract_text(self,image_path:str,language:str="ben+eng",preprocess:str="balanced")->dict[str,Any]:
        try:
            import pytesseract
            image=self.preprocess(image_path,preprocess)
            data=pytesseract.image_to_data(image,lang=language,config="--psm 6",output_type=pytesseract.Output.DICT)
            words=[]; confs=[]
            for i,text in enumerate(data.get("text",[])):
                t=(text or "").strip()
                if t:
                    words.append(t)
                    try:
                        c=float(data["conf"][i])
                        if c>=0: confs.append(c)
                    except (ValueError,TypeError): pass
            text=" ".join(words)
            confidence=round(sum(confs)/len(confs),2) if confs else None
            return {"text":text,"language":language,"provider":self.provider,"preprocess":preprocess,
                    "confidence":confidence,"word_count":len(words),
                    "quality":"high" if confidence is not None and confidence>=80 else "medium" if confidence is not None and confidence>=55 else "low"}
        except ImportError as exc:
            raise RuntimeError("Install pytesseract and Pillow for OCR.") from exc
        except Exception as exc:
            raise RuntimeError(f"OCR failed: {exc}") from exc

class VisionService:
    provider="none"
    def analyze(self,image_path:str,prompt:str="")->dict[str,Any]:
        if not Path(image_path).exists(): raise FileNotFoundError("Image file not found.")
        raise RuntimeError("No vision provider is configured.")
