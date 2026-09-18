"""Phase 21 observability: structured logs, request IDs and runtime metrics."""
from __future__ import annotations
import logging,time,uuid
from collections import deque
from dataclasses import asdict,dataclass
from threading import Lock

logger=logging.getLogger("gs420")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s %(message)s")

@dataclass
class RequestMetric:
    request_id:str
    method:str
    path:str
    status_code:int
    duration_ms:float
    timestamp:float

class Observability:
    def __init__(self,max_metrics=1000):
        self._metrics=deque(maxlen=max_metrics);self._lock=Lock()
    def new_request_id(self): return uuid.uuid4().hex
    def record(self,**kwargs):
        with self._lock:self._metrics.append(RequestMetric(**kwargs))
    def metrics(self):
        with self._lock:return [asdict(x) for x in self._metrics]
    def summary(self):
        with self._lock: vals=list(self._metrics)
        if not vals:return {"requests":0,"avg_latency_ms":0.0,"errors":0}
        return {"requests":len(vals),"avg_latency_ms":round(sum(x.duration_ms for x in vals)/len(vals),2),
                "errors":sum(x.status_code>=400 for x in vals)}
observability=Observability()
