"""Tests for the current GS420 Phase 1 chat API without loading a real model."""
from fastapi.testclient import TestClient
from backend.main import app

client=TestClient(app)

def test_health():
 r=client.get("/health");assert r.status_code==200 and r.json()["status"]=="ok"

def test_root():
 r=client.get("/");assert r.status_code==200 and r.json()["status"]=="ok"

def test_chat_validation():
 r=client.post("/api/chat",json={"message":""});assert r.status_code==422

def test_streaming_route():
 r=client.post("/api/chat/stream",json={"message":"hello"})
 assert r.status_code==200
 assert "text/event-stream" in r.headers.get("content-type","")
 assert "[DONE]" in r.text

def test_capability_routes():
 for p in ("/api/image/status","/api/video/status"):
  r=client.get(p);assert r.status_code==200
