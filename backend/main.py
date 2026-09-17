"""GS420 AI FastAPI application."""
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat import router as chat_router
from backend.dependencies import get_orchestrator
from backend.core.orchestrator import AIOrchestrator

app = FastAPI(
    title="GS420 AI",
    description="Modular open-model AI platform foundation.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "message": "GS420 AI API", "version": "0.1.0"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "gs420-ai"}

@app.get("/api/models")
def models(
    orchestrator: AIOrchestrator = Depends(get_orchestrator),
) -> dict:
    return {"models": orchestrator.model_info()}

@app.get("/api/system")
def system_info(
    orchestrator: AIOrchestrator = Depends(get_orchestrator),
) -> dict:
    return {"status": "ok", "model": orchestrator.model_info(), "phase": 1}
