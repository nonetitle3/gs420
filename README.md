# GS420 AI
Open-source-first AI hub for Bengali + English chat, coding, memory, voice, vision, image, video, agents and tools.

## Phase 10 — Tools System
Adds a schema/permission-aware Tool Registry, safe arithmetic calculator and optional web-search adapter. Calculator and tool APIs are mounted under /api/tools. External search providers remain optional.

Run:
python -m uvicorn backend.main:app --reload

Full test command:
python scripts/test_all.py
