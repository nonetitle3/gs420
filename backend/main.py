"""GS420 AI FastAPI application."""
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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
from backend.api.admin import router as admin_router
from backend.api.metrics import router as metrics_router
from backend.observability import observability, RequestEvent, log_exception
import time
import uuid

app = FastAPI(
    title="GS420 AI",
    description="Modular open-model AI platform foundation.",
    version="1.5.0",
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
app.include_router(admin_router)
app.include_router(metrics_router)
@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    started = time.perf_counter()
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        log_exception(request_id, exc)
        raise
    finally:
        duration_ms = (time.perf_counter() - started) * 1000
        status_code = locals().get("response").status_code if "response" in locals() else 500
        observability.record(RequestEvent(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=status_code,
            duration_ms=round(duration_ms, 2),
            timestamp=__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        ))

app.mount("/pwa", StaticFiles(directory="pwa", html=True), name="pwa")


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "message": "GS420 AI API", "version": "1.5.0"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "gs420-ai", "phase": "18"}


@app.get("/api/models")
def models(orchestrator: AIOrchestrator = Depends(get_orchestrator)) -> dict:
    return {"models": orchestrator.model_info()}


@app.get("/api/system")
def system_info(orchestrator: AIOrchestrator = Depends(get_orchestrator)) -> dict:
    return {"status": "ok", "model": orchestrator.model_info(), "phase": 18}
