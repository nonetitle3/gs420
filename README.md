# GS420 AI

Open-source-first modular AI hub: chat, coding, vision, OCR, image/video adapters, voice, agents, tools, documents, memory, PWA and Android/Colab/Hugging Face deployment paths.

## Quick start
pip install -r requirements.txt
python app.py

## API
uvicorn backend.main:app --host 0.0.0.0 --port 8000

## Testing
Phase 22:
python scripts/test_all.py

Equivalent:
python -m pytest -q tests

The suite covers core API, routing, memory, tools, agents, documents, multimodal adapters, security, resources, deployment scaffolds and observability. GPU/OCR/Android/deployment checks may require their target environment.
