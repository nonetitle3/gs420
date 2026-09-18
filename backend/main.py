import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.observability import observability, logger
from backend.api import chat, memory, documents, agents, voice, vision, image, video, tools, models, system

app = FastAPI(title=settings.app_name, version="2.0.0", description="GS420 AI Master Prompt Phase 0-23")
_origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()] or ["*"]
app.add_middleware(CORSMiddleware, allow_origins=_origins, allow_methods=["GET","POST","DELETE","OPTIONS"], allow_headers=["*"])

@app.middleware("http")
async def request_observer(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or observability.new_request_id()
    started = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        response.headers["X-Request-ID"] = rid
        return response
    except Exception:
        logger.exception("request failed request_id=%s path=%s", rid, request.url.path)
        raise
    finally:
        duration = (time.perf_counter() - started) * 1000
        observability.record(request_id=rid, method=request.method, path=request.url.path, status_code=status, duration_ms=round(duration,2), timestamp=time.time())
        logger.info("request_id=%s method=%s path=%s status=%s duration_ms=%.2f", rid, request.method, request.url.path, status, duration)

for r in (chat.router,memory.router,documents.router,agents.router,voice.router,vision.router,image.router,video.router,tools.router,models.router,system.router):
    app.include_router(r)

@app.get("/")
def root():
    return {"status":"ok","name":settings.app_name,"environment":settings.app_env,"roadmap":"Phase 0-23"}

@app.get("/health")
def health():
    return {"status":"ok","environment":settings.app_env}
