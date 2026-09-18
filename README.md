# GS420 AI
Open-source-first AI hub for Bengali + English chat, memory, vision, image, video, agents, tools, documents, PWA and Android.

## Phase 13 — Android / Capacitor
The project now contains a Capacitor Android wrapper configuration targeting the built PWA. Heavy inference remains remote/local-backend rather than pretending large models run efficiently on phones.

Frontend:
cd frontend && npm install && npm run build

Android:
cd mobile/capacitor
npm install
npx cap add android
npm run sync
npx cap open android
