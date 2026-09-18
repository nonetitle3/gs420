# GS420 AI
Open-source-first AI hub for Bengali + English chat, coding, memory, voice and multimodal workflows.

## Phase 5 — Voice AI
STT uses a replaceable Whisper-compatible Hugging Face pipeline. TTS uses a replaceable Piper adapter. Heavy speech models are loaded only when the voice endpoint is used; no paid API key is required.

Run:
python -m uvicorn backend.main:app --reload
