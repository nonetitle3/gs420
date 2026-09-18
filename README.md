# GS420 AI
Open-source-first AI hub for Bengali + English chat, coding, memory, voice, vision and multimodal workflows.

## Phase 6 — Vision AI
Provides Bengali+English OCR through Tesseract and a replaceable Hugging Face image-to-text adapter. OCR accuracy depends on image quality, language data and engine/model; it is not guaranteed to be 100%.

Run:
python -m uvicorn backend.main:app --reload

Test everything:
python scripts/test_all.py
