# GS420 AI
Open-source-first AI hub for Bengali + English chat, memory, vision, image, video, agents, tools, documents and offline-first web use.

## Phase 12 — PWA / Offline-first
The frontend now has responsive mobile UI, installable web-app metadata, a service worker cache, local chat persistence and online/offline status. Backend inference still requires a reachable API unless an offline model is configured.

Run frontend:
cd frontend
npm install
npm run build

Run backend:
python -m uvicorn backend.main:app --reload
