from backend.observability import Observability
def test_metrics_summary():
    o=Observability();rid=o.new_request_id();o.record(request_id=rid,method="GET",path="/health",status_code=200,duration_ms=5.0,timestamp=1.0)
    s=o.summary()
    assert s["requests"]==1 and s["errors"]==0 and s["avg_latency_ms"]==5.0
