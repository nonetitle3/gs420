from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.api import chat,memory,documents,agents,voice,vision,image,video,tools,models,system
app=FastAPI(title=settings.app_name,version="2.0.0",description="GS420 AI Master Prompt Phase 0-23")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["GET","POST","DELETE"],allow_headers=["*"])
for r in (chat.router,memory.router,documents.router,agents.router,voice.router,vision.router,image.router,video.router,tools.router,models.router,system.router):app.include_router(r)
@app.get("/")
def root():return {"status":"ok","name":settings.app_name,"roadmap":"Phase 0-23"}
@app.get("/health")
def health():return {"status":"ok"}
