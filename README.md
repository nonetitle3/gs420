# GS420 AI
Open-source-first AI hub for Bengali + English chat, coding, memory, voice, vision, image and multimodal workflows.

## Phase 7 — Image AI
Includes an optional Diffusers text/image-to-image backend plus local enhancement and 2x/3x/4x upscaling utilities. Generative image models are intentionally optional because model size and hardware requirements vary; no free-tier GPU capacity is assumed.

Run:
python -m uvicorn backend.main:app --reload

Test:
python scripts/test_all.py
