"""OCR service using Tesseract with graceful availability checks."""
from pathlib import Path
class OCRService:
    def __init__(self,lang="ben+eng"):
        self.lang=lang
    def extract(self,image_path):
        from PIL import Image
        import pytesseract
        p=Path(image_path)
        if not p.exists():raise FileNotFoundError(str(p))
        text=pytesseract.image_to_string(Image.open(p),lang=self.lang)
        return {"text":text.strip(),"language":self.lang,"engine":"tesseract"}
