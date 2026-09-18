"""GS420 AI FastAPI application."""
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router
from backend.core.orchestrator import AIOrchestrator
from backend.dependencies import get_orchestrator
from backend.api.voice import router as voice_router
from backend.api.vision import router as vision_router
from backend.api.image import router as image_router
from backend.api.video import router as video_router
from backend.api.agents import router as agents_router
from backend.api.tools import router as tools_router
from backend.api.rag import router as rag_router

app = FastAPI(
    title="GS420 AI",
    description="Modular open-model AI platform foundation.",
    version="0.9.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(voice_router)
app.include_router(vision_router)
app.include_router(image_router)
app.include_router(video_router)
app.include_router(agents_router)
app.include_router(tools_router)
app.include_router(rag_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "message": "GS420 AI API", "version": "0.9.0"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "gs420-ai", "phase": "11"}


@app.get("/api/models")
def models(orchestrator: AIOrchestrator = Depends(get_orchestrator)) -> dict:
    return {"models": orchestrator.model_info()}


@app.get("/api/system")
def system_info(orchestrator: AIOrchestrator = Depends(get_orchestrator)) -> dict:
    return {"status": "ok", "model": orchestrator.model_info(), "phase": 11}
