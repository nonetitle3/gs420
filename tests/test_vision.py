def test_ocr_service_default():
 from backend.services.ocr import OCRService
 assert OCRService().lang=="ben+eng"
def test_vision_graceful_without_model():
 from backend.services.vision import VisionService
 assert VisionService().analyze("/missing.jpg")["ok"] is False
