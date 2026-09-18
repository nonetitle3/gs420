# GS420 AI

Open-source-first modular AI hub: chat, coding, vision, OCR, image/video adapters, voice, agents, tools, documents, memory, PWA and Android/Colab/Hugging Face deployment paths.

## Quick start
pip install -r requirements.txt
python app.py

## API
uvicorn backend.main:app --host 0.0.0.0 --port 8000

## Observability
Phase 21 provides structured request logs, request IDs, latency metrics, error counts, inference latency logging, and runtime resource monitoring.
- GET /api/system/observability
- GET /api/system/metrics

Pass X-Request-ID to correlate a client request with server logs. If omitted, GS420 generates one.
