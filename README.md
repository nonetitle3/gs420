# GS420 AI

Modular open-model AI platform.

## Phase 14 — Production Observability + Monitoring\n- Request metrics and latency tracking\n- 5xx error counters\n- Recent request event buffer with request IDs\n- Structured exception logging\n- Admin-protected metrics API at `/api/metrics/summary`\n- Monitoring UI at `/pwa/monitor.html`\n- API release version `1.2.0`\n\n## Phase 14 — Production Observability + Monitoring\nPhase 13 — Management Dashboard + Admin Security\n- Admin dashboard at `/pwa/admin.html`\n- Token-protected management endpoints under `/api/admin`\n- `GS420_ADMIN_TOKEN` is never returned by the API\n- Redacted GS420 environment view\n- Runtime model/device/configuration snapshot\n- API release version `1.1.0`\n\n## Phase 12 — PWA + Management/Security Foundation
- Installable PWA shell at `/pwa/`
- Web App Manifest
- Service worker with basic offline shell caching
- FastAPI serves the PWA
- Security helpers for generating secrets and redacting `GS420_*` environment values
- API release version `1.0.0`
- Android packaging with Capacitor and full production observability remain future work

## Phase 11 — RAG + Documents
- SQLite-backed document store
- Full-text search with SQLite FTS5 when available
- Safe fallback text search
- Upload support for TXT, Markdown, CSV, and JSON
- `GET /api/rag/stats`
- `POST /api/rag/documents`
- `POST /api/rag/search`
- `GET /api/rag/documents/{document_id}`
- `DELETE /api/rag/documents/{document_id}`
- 20 MB document upload limit
- PDF/DOCX extraction and vector embeddings are reserved for the next RAG enhancement

## Phase 10 — Tools System
- Permission-aware built-in tool registry
- Safe arithmetic calculator using AST validation (no eval/imports)
- Current UTC time tool
- Optional HTTP(S) text/JSON fetch tool, disabled by default
- `GET /api/tools`
- `POST /api/tools/execute`
- Conservative URL, timeout, content-type, and response-size limits
- Tools are separate from arbitrary shell/filesystem access

## Phase 9 — AI Agents
- Permission-aware agent tool registry
- Deterministic bounded agent execution loop
- Maximum 5 actions per run
- Explicit tool enable/disable boundary
- `GET /api/agents/tools`
- `POST /api/agents/run`
- No arbitrary shell, filesystem, network, or browser access is granted by default

## Phase 8 — Video AI
- Provider-agnostic text-to-video API
- Image-to-video API foundation
- `GET /api/video/providers`
- `POST /api/video/generate`
- `POST /api/video/image-to-video`
- Duration, resolution, FPS, and optional seed controls
- Image upload limit: 15 MB
- Heavy video models remain optional; a local video adapter can be plugged in later

## Phase 7 — Image AI
- Provider-agnostic image generation API
- Image editing API with optional mask upload
- `GET /api/image/providers`
- `POST /api/image/generate`
- `POST /api/image/edit`
- Prompt, size, steps, and optional seed controls
- Image upload limit: 15 MB
- The base installation does not download a large image model; a Diffusers/SDXL/FLUX adapter can be plugged in later

## Phase 6 — Vision + OCR
- Image upload API for vision analysis
- OCR API with Bengali + English language selection
- `GET /api/vision/providers`
- `POST /api/vision/ocr`
- `POST /api/vision/analyze`
- Image upload limit: 15 MB
- Provider adapters remain optional so the base installation stays lightweight
- OCR/vision engines can be added later without changing the API contract

## Phase 5 — Voice / STT / TTS
- Voice API foundation for speech-to-text and text-to-speech
- `POST /api/voice/transcribe` accepts audio uploads
- `POST /api/voice/synthesize` accepts text and language
- `GET /api/voice/providers` reports configured providers
- Provider adapters are optional; the base installation does not download a large audio model
- STT/TTS adapters can later be backed by local models such as faster-whisper/Piper

## Phase 4 — Coding AI + Secure Sandbox
- Restricted Python execution endpoint: `POST /api/code/execute`
- Isolated temporary working directory per execution
- Python isolated mode (`-I`)
- Execution timeout and output-size limits
- No inherited application environment variables except a minimal runtime environment
- Sandbox limits configurable with `GS420_SANDBOX_TIMEOUT_SECONDS` and `GS420_SANDBOX_MAX_OUTPUT_CHARS`
- Important: this is defense-in-depth for local use; truly untrusted multi-user execution should run inside a container or VM with OS-level isolation.

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
- POST /api/code/execute
- GET /api/voice/providers
- POST /api/voice/transcribe
- POST /api/voice/synthesize
- GET /api/vision/providers
- POST /api/vision/ocr
- POST /api/vision/analyze
- GET /api/image/providers
- POST /api/image/generate
- POST /api/image/edit
- GET /api/video/providers
- POST /api/video/generate
- POST /api/video/image-to-video
- GET /api/agents/tools
- POST /api/agents/run
- GET /api/tools
- POST /api/tools/execute
- GET /pwa/
- GET /api/rag/stats
- POST /api/rag/documents
- POST /api/rag/search
- GET /api/rag/documents/{document_id}
- DELETE /api/rag/documents/{document_id}

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
Phase 12 — PWA + management/security foundation
