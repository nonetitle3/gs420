# GS420 AI
Open-source-first AI hub for Bengali + English chat, memory, vision, image, video, agents, tools, documents, PWA and Android.

## Phase 16 — Model Management
Adds a persistent model registry with task, size, hardware, quantization, enabled state, priority and local-availability metadata. Models can be enabled/disabled through the API and the React Settings view can display the registry.

Model directories:
- data/models/general
- data/models/coding
- data/models/vision
- data/models/speech
- data/models/image
- data/models/video

Run:
python -m uvicorn backend.main:app --reload
