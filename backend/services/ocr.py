def ocr_image(path,lang="ben+eng"):
 import pytesseract
 from PIL import Image
 return pytesseract.image_to_string(Image.open(path),lang=lang)
def extract_pdf(path):
 from pypdf import PdfReader
 r=PdfReader(path);return "\n".join((p.extract_text() or "") for p in r.pages),len(r.pages)
