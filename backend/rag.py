"""Phase 11 lightweight document/RAG store.

Uses SQLite FTS5 when available and stores extracted text locally.
PDF/DOCX extraction adapters can be added without changing the API.
"""
from __future__ import annotations

import re
import sqlite3
import uuid
from pathlib import Path
from typing import Any


class DocumentStore:
    def __init__(self, database_path: str = "./data/gs420_rag.db") -> None:
        self.database_path = database_path
        Path(database_path).expanduser().parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _conn(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.database_path)
        c.row_factory = sqlite3.Row
        return c

    def _init(self) -> None:
        with self._conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS documents(
                id TEXT PRIMARY KEY, filename TEXT NOT NULL,
                content TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
            try:
                c.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS document_fts
                    USING fts5(document_id UNINDEXED, filename, content)""")
            except sqlite3.OperationalError:
                pass

    def add(self, filename: str, content: str) -> dict[str, Any]:
        if not content.strip():
            raise ValueError("Document content cannot be empty.")
        document_id = str(uuid.uuid4())
        with self._conn() as c:
            c.execute("INSERT INTO documents(id,filename,content) VALUES(?,?,?)",
                      (document_id, filename[:255], content))
            try:
                c.execute("INSERT INTO document_fts(document_id,filename,content) VALUES(?,?,?)",
                          (document_id, filename[:255], content))
            except sqlite3.OperationalError:
                pass
        return {"id": document_id, "filename": filename[:255]}

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        if not query.strip():
            return []
        limit = max(1, min(limit, 20))
        with self._conn() as c:
            try:
                rows = c.execute("""SELECT document_id, filename, snippet(document_fts,2,'','', ' … ',30) AS snippet
                    FROM document_fts WHERE document_fts MATCH ? LIMIT ?""",
                    (query, limit)).fetchall()
                return [dict(r) for r in rows]
            except sqlite3.OperationalError:
                terms = [t for t in re.split(r"\s+", query.strip()) if t]
                if not terms:
                    return []
                sql = " OR ".join("content LIKE ?" for _ in terms)
                rows = c.execute(f"SELECT id AS document_id,filename,substr(content,1,500) AS snippet FROM documents WHERE {sql} LIMIT ?",
                                  tuple(f"%{t}%" for t in terms)+(limit,)).fetchall()
                return [dict(r) for r in rows]

    def get(self, document_id: str) -> dict[str, Any] | None:
        with self._conn() as c:
            row = c.execute("SELECT id,filename,content,created_at FROM documents WHERE id=?",
                            (document_id,)).fetchone()
            return dict(row) if row else None

    def delete(self, document_id: str) -> bool:
        with self._conn() as c:
            c.execute("DELETE FROM documents WHERE id=?", (document_id,))
            try:
                c.execute("DELETE FROM document_fts WHERE document_id=?", (document_id,))
            except sqlite3.OperationalError:
                pass
            return c.total_changes > 0

    def stats(self) -> dict[str, int]:
        with self._conn() as c:
            return {"documents": int(c.execute("SELECT COUNT(*) FROM documents").fetchone()[0])}
