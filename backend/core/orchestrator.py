"""Central GS420 AI orchestration service."""
from __future__ import annotations

import threading
import uuid
from collections import defaultdict
from collections.abc import Generator
from typing import Any

from backend.config import Settings
from backend.models.router import ModelRouter
from backend.memory import SQLiteMemoryStore
from backend.sandbox import ExecutionResult, SandboxExecutor
from backend.rag import DocumentStore, EmbeddingProvider


class ConversationStore:
    def __init__(self, max_messages: int) -> None:
        self.max_messages = max_messages
        self._data: dict[str, list[dict[str, str]]] = defaultdict(list)
        self._lock = threading.Lock()

    def get(self, session_id: str) -> list[dict[str, str]]:
        with self._lock:
            return list(self._data.get(session_id, []))

    def append(self, session_id: str, role: str, content: str) -> None:
        with self._lock:
            self._data[session_id].append({"role": role, "content": content})
            self._data[session_id] = self._data[session_id][-self.max_messages:]

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._data.pop(session_id, None)


class AIOrchestrator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.router = ModelRouter(settings)
        self.memory = SQLiteMemoryStore(settings.memory_db_path, settings.max_history_messages)
        self.sandbox = SandboxExecutor(settings.sandbox_timeout_seconds, settings.sandbox_max_output_chars)
        self.rag = DocumentStore(embedder=EmbeddingProvider(settings.embedding_model_id) if settings.embedding_model_id else None)

    def new_session(self) -> str:
        return self.memory.create_session(str(uuid.uuid4()))

    def _prepare_messages(self, session_id: str, user_message: str) -> list[dict[str, str]]:
        return self.memory.get(session_id) + [{"role": "user", "content": user_message}]

    def resolve_role(self, role: str, message: str) -> str:
        selected_role, _ = self.router.route(role, message)
        return selected_role

    def _rag_context(self, query: str) -> str:\n        if not self.settings.rag_enabled: return ""\n        try:\n            results = self.rag.search(query, self.settings.rag_top_k, semantic=self.settings.rag_semantic and self.rag.embedder is not None)\n        except Exception:\n            return ""\n        if not results: return ""\n        parts = ["Relevant document context (use only when it helps answer the user):"]\n        for i, item in enumerate(results, 1):\n            parts.append(f"[{i}] {item.get(\"filename\", \"document\")}: {item.get(\"snippet\", \"\")}")\n        return "\\n".join(parts)\n\n    def chat(self, session_id: str, user_message: str, role: str = "auto", **generation_kwargs: Any) -> tuple[str, str]:
        cleaned = user_message.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")
        selected_role, model = self.router.route(role, cleaned)
        response = model.generate(self._prepare_messages(session_id, cleaned), **generation_kwargs)
        self.memory.append(session_id, "user", cleaned)
        self.memory.append(session_id, "assistant", response)
        return selected_role, response

    def stream_chat(self, session_id: str, user_message: str, role: str = "auto", **generation_kwargs: Any) -> Generator[str, None, None]:
        cleaned = user_message.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")
        _, model = self.router.route(role, cleaned)
        chunks: list[str] = []
        try:
            messages = self._prepare_messages(session_id, cleaned)\n            context = self._rag_context(cleaned)\n            if context: messages.insert(max(0, len(messages)-1), {"role": "system", "content": context})\n            for chunk in model.stream(messages, **generation_kwargs):
                chunks.append(chunk)
                yield chunk
        finally:
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
        return {"routes": self.router.list_routes(), "memory": self.memory.stats()}
