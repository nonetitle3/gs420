"""Phase 14 lightweight production observability."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
import logging
import threading
import time
import uuid

logger = logging.getLogger("gs420")

@dataclass
class RequestEvent:
    request_id: str
    method: str
    path: str
    status_code: int
    duration_ms: float
    timestamp: str

class Observability:
    def __init__(self, max_events: int = 500) -> None:
        self._events: deque[RequestEvent] = deque(maxlen=max_events)
        self._lock = threading.Lock()
        self._started = time.time()
        self._total_requests = 0
        self._total_errors = 0
        self._total_duration_ms = 0.0

    def record(self, event: RequestEvent) -> None:
        with self._lock:
            self._events.append(event)
            self._total_requests += 1
            self._total_duration_ms += event.duration_ms
            if event.status_code >= 500:
                self._total_errors += 1

    def snapshot(self) -> dict:
        with self._lock:
            avg = self._total_duration_ms / self._total_requests if self._total_requests else 0.0
            return {
                "uptime_seconds": round(time.time() - self._started, 2),
                "requests_total": self._total_requests,
                "errors_5xx": self._total_errors,
                "average_latency_ms": round(avg, 2),
                "recent_events": [e.__dict__ for e in list(self._events)[-50:]],
            }

observability = Observability()

def log_exception(request_id: str, exc: Exception) -> None:
    logger.exception("request_id=%s error=%s", request_id, exc)
