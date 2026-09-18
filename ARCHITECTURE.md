# GS420 AI Architecture

User -> PWA/Android/Gradio -> FastAPI -> Orchestrator -> Model Router -> Resource Manager -> Model Adapter -> Tools/Agents -> Memory/RAG -> Result.

`backend/api` provides HTTP interfaces. `backend/core` provides orchestration, routing, memory, RAG, tasks and resources. `backend/models` contains replaceable model adapters and registry. `backend/services` contains OCR, STT, TTS, image/video/document services. `backend/agents` and `backend/tools` provide controlled automation.

SQLite stores persistent memory and FTS5 retrieval. Android/PWA primarily act as clients; Colab or suitable GPU services can host heavy inference. Hugging Face Spaces provides a Gradio deployment path.
