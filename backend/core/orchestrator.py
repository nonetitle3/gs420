"""Central GS420 AI orchestration service."""
from __future__ import annotations

import uuid
from collections.abc import Generator
from typing import Any

from backend.config import Settings
from backend.models.router import ModelRouter
from backend.memory import SQLiteMemoryStore
from backend.sandbox import ExecutionResult, SandboxExecutor
from backend.rag import DocumentStore, EmbeddingProvider


class AIOrchestrator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.router = ModelRouter(settings)
        self.memory = SQLiteMemoryStore(settings.memory_db_path, settings.max_history_messages)
        self.sandbox = SandboxExecutor(settings.sandbox_timeout_seconds, settings.sandbox_max_output_chars)
        self.rag = DocumentStore(
            embedder=EmbeddingProvider(settings.embedding_model_id)
            if settings.embedding_model_id else None
        )

    def new_session(self) -> str:
        return self.memory.create_session(str(uuid.uuid4()))

    def _prepare_messages(self, session_id: str, user_message: str) -> list[dict[str, str]]:
        return self.memory.get(session_id) + [{"role": "user", "content": user_message}]

    def resolve_role(self, role: str, message: str) -> str:
        selected_role, _ = self.router.route(role, message)
        return selected_role

    def _rag_context(self, query: str) -> tuple[str, list[dict[str, Any]]]:
        if not self.settings.rag_enabled:
            return "", []
        try:
            results = self.rag.search(
                query,
                self.settings.rag_top_k,
                semantic=self.settings.rag_semantic and self.rag.embedder is not None,
            )
        except Exception:
            return "", []
        if not results:
            return "", []
        sources = []
        parts = ["Relevant document context. Use it only when it helps answer the user:"]
        for i, item in enumerate(results, 1):
            source = {
                "index": i,
                "document_id": item.get("document_id"),
                "filename": item.get("filename", "document"),
                "score": item.get("score"),
                "snippet": item.get("snippet", "")[:500],
            }
            sources.append(source)
            parts.append(
                f"[{i}] {source['filename']}: {source['snippet']}"
            )
        return "\n".join(parts), sources

    def chat(
        self, session_id: str, user_message: str, role: str = "auto", **generation_kwargs: Any
    ) -> tuple[str, str, list[dict[str, Any]]]:
        cleaned = user_message.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")
        selected_role, model = self.router.route(role, cleaned)
        messages = self._prepare_messages(session_id, cleaned)
        context, sources = self._rag_context(cleaned)
        if context:
            messages.insert(max(0, len(messages) - 1), {"role": "system", "content": context})
        response = model.generate(messages, **generation_kwargs)
        self.memory.append(session_id, "user", cleaned)
        self.memory.append(session_id, "assistant", response)
        return selected_role, response, sources

    def stream_chat(
        self, session_id: str, user_message: str, role: str = "auto", **generation_kwargs: Any
    ) -> Generator[tuple[str, list[dict[str, Any]]], None, None]:
        cleaned = user_message.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")
        _, model = self.router.route(role, cleaned)
        messages = self._prepare_messages(session_id, cleaned)
        context, sources = self._rag_context(cleaned)
        if context:
            messages.insert(max(0, len(messages) - 1), {"role": "system", "content": context})
        chunks: list[str] = []
        for chunk in model.stream(messages, **generation_kwargs):
            chunks.append(chunk)
            yield chunk, sources
        response = "".join(chunks).strip()
        if response:
            self.memory.append(session_id, "user", cleaned)
            self.memory.append(session_id, "assistant", response)

    def get_history(self, session_id: str) -> list[dict[str, str]]:
        return self.memory.get(session_id)

    def clear_history(self, session_id: str) -> None:
        self.memory.clear(session_id)

    def execute_python(self, code: str) -> ExecutionResult:
        return self.sandbox.execute_python(code)

    def model_info(self) -> dict[str, Any]:
        return {
            "routes": self.router.list_routes(),
            "memory": self.memory.stats(),
            "rag": self.rag.stats(),
        }
