# GS420 AI
Open-source-first AI hub for Bengali + English chat, coding, memory, voice, vision, image, video and multimodal workflows.

## Phase 8 — Video AI
Provides a replaceable GPU video-generation adapter and lightweight frame extraction. LTX/Wan-style generation remains optional because video inference is resource-intensive and hardware-dependent.

Run:
python -m uvicorn backend.main:app --reload

Test:
python scripts/test_all.py
