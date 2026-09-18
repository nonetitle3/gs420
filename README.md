# GS420 AI

Open-source-first modular AI hub for Bengali and English: chat, coding, voice, vision/OCR, image/video adapters, agents, tools, documents, memory, PWA, Android, Colab and Hugging Face.

## Deployment entry points

- Gradio/Hugging Face: `python app.py`
- FastAPI API: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Local helper: `python start.py`
- Docker: `docker build -t gs420-ai . && docker run --rm -p 7860:7860 gs420-ai`

No OpenAI API key is required.

## Local

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt
python start.py
```

## Hugging Face Spaces

Create a **Gradio Space**, import this repository, and configure:
```
GS420_MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct
GS420_DEVICE=auto
GS420_MAX_NEW_TOKENS=512
```
Use `GS420_HF_TOKEN` only as a Space Secret for private/gated models.

## FastAPI

Endpoints include `/`, `/health`, `/docs`, `/api/chat`, `/api/chat/stream`, documents, voice, vision, image/video, agents, tools, models and system routes.

## Frontend

```bash
cd frontend
npm install
npm run build
```
Set `VITE_API_URL` to the deployed FastAPI URL at build time. Never commit secrets or hard-code a localhost API URL.

## Validation

CI runs Python compilation/tests and the frontend production build. Hardware-dependent model inference and external Space deployment are only marked verified after their real environment has been exercised.
