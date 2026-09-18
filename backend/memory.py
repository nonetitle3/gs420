"""SQLite-backed persistent conversation memory for GS420 AI."""
from __future__ import annotations

import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path


class SQLiteMemoryStore:
    """Thread-safe SQLite conversation store.

    The database is created automatically and survives application restarts.
    """

    def __init__(self, database_path: str, max_messages: int = 20) -> None:
        self.database_path = database_path
        self.max_messages = max_messages
        self._lock = threading.RLock()

        if database_path != ":memory:":
            Path(database_path).expanduser().parent.mkdir(parents=True, exist_ok=True)

        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path,
            timeout=30,
            check_same_thread=False,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        return connection

    def _initialize(self) -> None:
        with self._lock, self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_messages_session_id_id
                ON messages(session_id, id);
                """
            )

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def create_session(self, session_id: str | None = None) -> str:
        session_id = session_id or str(uuid.uuid4())
        now = self._now()
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO sessions(id, created_at, updated_at)
                VALUES (?, ?, ?)
                """,
                (session_id, now, now),
            )
        return session_id

    def get(self, session_id: str) -> list[dict[str, str]]:
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                """
                SELECT role, content
                FROM messages
                WHERE session_id = ?
                ORDER BY id ASC
                LIMIT ?
                """,
                (session_id, self.max_messages),
            ).fetchall()
            return [{"role": row["role"], "content": row["content"]} for row in rows]

    def append(self, session_id: str, role: str, content: str) -> None:
        if role not in {"user", "assistant", "system"}:
            raise ValueError(f"Unsupported message role: {role}")

        now = self._now()
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO sessions(id, created_at, updated_at)
                VALUES (?, ?, ?)
                """,
                (session_id, now, now),
            )
            connection.execute(
                """
                INSERT INTO messages(session_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (session_id, role, content, now),
            )
            connection.execute(
                "UPDATE sessions SET updated_at = ? WHERE id = ?",
                (now, session_id),
            )

            excess = connection.execute(
                """
                SELECT id FROM messages
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT -1 OFFSET ?
                """,
                (session_id, self.max_messages),
            ).fetchall()
            if excess:
                connection.executemany(
                    "DELETE FROM messages WHERE id = ?",
                    [(row["id"],) for row in excess],
                )

    def clear(self, session_id: str) -> None:
        with self._lock, self._connect() as connection:
            connection.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            connection.execute(
                "UPDATE sessions SET updated_at = ? WHERE id = ?",
                (self._now(), session_id),
            )

    def delete_session(self, session_id: str) -> None:
        with self._lock, self._connect() as connection:
            connection.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

    def session_exists(self, session_id: str) -> bool:
        with self._lock, self._connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM sessions WHERE id = ?", (session_id,)
            ).fetchone()
            return row is not None

    def stats(self) -> dict[str, int]:
        with self._lock, self._connect() as connection:
            sessions = connection.execute("SELECT COUNT(*) AS n FROM sessions").fetchone()["n"]
            messages = connection.execute("SELECT COUNT(*) AS n FROM messages").fetchone()["n"]
            return {"sessions": int(sessions), "messages": int(messages)}
