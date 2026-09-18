# GS420 AI
Open-source-first AI hub for Bengali + English chat, coding, memory, voice, vision, image, video, agents, tools, documents, PWA and Android.

## Phase 15 — React + FastAPI
The frontend is now a React/Vite application shell connected to FastAPI APIs. It includes canonical pages/tabs for Chat, Coding, Vision, Image, Video, Voice, Agents, Documents, Memory and Settings, with API-driven Chat, Agents and Document Search examples.

Build:
cd frontend
npm install
npm run build

Backend:
python -m uvicorn backend.main:app --reload
