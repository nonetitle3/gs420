"""Central GS420 AI orchestration service."""
from __future__ import annotations

import threading
import uuid
from collections import defaultdict
from collections.abc import Generator
from typing import Any

from backend.config import Settings
from backend.models.router import ModelRouter


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
        self.conversations = ConversationStore(settings.max_history_messages)

    def new_session(self) -> str:
        return str(uuid.uuid4())

    def _prepare_messages(self, session_id: str, user_message: str) -> list[dict[str, str]]:
        return self.conversations.get(session_id) + [{"role": "user", "content": user_message}]

    def resolve_role(self, role: str, message: str) -> str:
        selected_role, _ = self.router.route(role, message)
        return selected_role

    def chat(self, session_id: str, user_message: str, role: str = "auto", **generation_kwargs: Any) -> tuple[str, str]:
        cleaned = user_message.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")
        selected_role, model = self.router.route(role, cleaned)
        response = model.generate(self._prepare_messages(session_id, cleaned), **generation_kwargs)
        self.conversations.append(session_id, "user", cleaned)
        self.conversations.append(session_id, "assistant", response)
        return selected_role, response

    def stream_chat(self, session_id: str, user_message: str, role: str = "auto", **generation_kwargs: Any) -> Generator[str, None, None]:
        cleaned = user_message.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")
        _, model = self.router.route(role, cleaned)
        chunks: list[str] = []
        try:
            for chunk in model.stream(self._prepare_messages(session_id, cleaned), **generation_kwargs):
                chunks.append(chunk)
                yield chunk
        finally:
            response = "".join(chunks).strip()
            if response:
                self.conversations.append(session_id, "user", cleaned)
                self.conversations.append(session_id, "assistant", response)

    def get_history(self, session_id: str) -> list[dict[str, str]]:
        return self.conversations.get(session_id)

    def clear_history(self, session_id: str) -> None:
        self.conversations.clear(session_id)

    def model_info(self) -> dict[str, Any]:
        return {"routes": self.router.list_routes()}
