# GS420 AI

Modular open-model AI platform.

## Phase 3 — Persistent Memory
- SQLite-backed conversation history that survives restarts
- Automatic session persistence
- Thread-safe database access with WAL mode
- Configurable database path via `GS420_MEMORY_DB_PATH`
- Memory statistics endpoint: `GET /api/memory/stats`

## Phase 2 — Model Router
- Role-based routing: general, reasoning, coding, vision
- Automatic routing for coding/reasoning keywords
- Optional specialized Hugging Face model IDs
- Explicit role selection through `POST /api/chat`

## Phase 1
- FastAPI backend
- Gradio UI at /ui
- Hugging Face text model
- Bengali + English chat
- Session-based conversation
- Streaming responses
- CPU/GPU detection
- Configurable model
- Tests

## Run locally
Python 3.11 or 3.12 is recommended.

```bash
python -m venv .venv
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Windows:
```powershell
.venv\\Scripts\\activate
```

Install:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then:
```bash
python start.py
```

Open:
- API: http://127.0.0.1:7860/
- Swagger: http://127.0.0.1:7860/docs
- Gradio UI: http://127.0.0.1:7860/ui

## Default model
`Qwen/Qwen2.5-0.5B-Instruct`

Change with:
```
GS420_MODEL_ID=your-huggingface-model
```

Device:
```
GS420_DEVICE=auto
```

## API
- GET /health
- GET /api/models
- GET /api/system
- POST /api/sessions
- POST /api/chat
- GET /api/sessions/{session_id}/history
- DELETE /api/sessions/{session_id}/history
- GET /api/memory/stats

## Tests
```bash
pytest -q
```

Tests use a fake model and do not download a Hugging Face model.

## Memory
By default, persistent memory is stored at `./data/gs420_memory.db`. The `data/` directory is ignored by Git so local conversation data is not committed.

## Roadmap
Phase 2 — Model Router
Phase 3 — Persistent Memory
Phase 4 — Coding AI + sandbox
Phase 5 — Voice/STT/TTS
Phase 6 — Vision/OCR
Phase 7 — Image AI
Phase 8 — Video AI
Phase 9 — Agents
Phase 10 — Tools
Phase 11 — RAG
Phase 12+ — PWA/Android/management/security/observability
