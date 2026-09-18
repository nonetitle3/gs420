"""Phase 15 document extraction, chunking, embeddings, and vector search."""
from __future__ import annotations
import json, re, sqlite3, uuid
from pathlib import Path
from typing import Any

try:
    import numpy as np
except ImportError:
    np = None

class EmbeddingProvider:
    """Optional local Transformer embedding provider."""
    def __init__(self, model_id: str | None = None):
        self.model_id = model_id or "sentence-transformers/all-MiniLM-L6-v2"
        self._tokenizer = None
        self._model = None

    def _load(self):
        if self._model is not None: return
        if np is None: raise RuntimeError("numpy is required for vector search.")
        from transformers import AutoModel, AutoTokenizer
        import torch
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self._model = AutoModel.from_pretrained(self.model_id)
        self._model.eval()

    def encode(self, text: str) -> list[float]:
        self._load()
        import torch
        inputs = self._tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.inference_mode():
            out = self._model(**inputs).last_hidden_state
            mask = inputs["attention_mask"].unsqueeze(-1)
            vec = (out * mask).sum(1) / mask.sum(1).clamp(min=1)
        arr = vec[0].cpu().numpy()
        norm = float(np.linalg.norm(arr))
        return (arr / norm if norm else arr).astype(float).tolist()

def chunk_text(text: str, size: int = 1200, overlap: int = 150) -> list[str]:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean: return []
    step = max(1, size - overlap)
    return [clean[i:i+size] for i in range(0, len(clean), step)]

class DocumentStore:
    def __init__(self, database_path: str = "./data/gs420_rag.db", embedder: EmbeddingProvider | None = None):
        self.database_path = database_path
        self.embedder = embedder
        Path(database_path).expanduser().parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _conn(self):
        c = sqlite3.connect(self.database_path)
        c.row_factory = sqlite3.Row
        return c

    def _init(self):
        with self._conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS documents(
                id TEXT PRIMARY KEY, filename TEXT NOT NULL, content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
            c.execute("""CREATE TABLE IF NOT EXISTS chunks(
                id TEXT PRIMARY KEY, document_id TEXT NOT NULL, chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL, embedding TEXT)""")
            try:
                c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS document_fts USING fts5(document_id UNINDEXED, filename, content)")
            except sqlite3.OperationalError:
                pass

    def add(self, filename: str, content: str, create_embeddings: bool = False) -> dict[str, Any]:
        if not content.strip(): raise ValueError("Document content cannot be empty.")
        document_id = str(uuid.uuid4())
        chunks = chunk_text(content)
        with self._conn() as c:
            c.execute("INSERT INTO documents(id,filename,content) VALUES(?,?,?)",(document_id,filename[:255],content))
            try: c.execute("INSERT INTO document_fts(document_id,filename,content) VALUES(?,?,?)",(document_id,filename[:255],content))
            except sqlite3.OperationalError: pass
            for i, chunk in enumerate(chunks):
                emb = self.embedder.encode(chunk) if create_embeddings and self.embedder else None
                c.execute("INSERT INTO chunks(id,document_id,chunk_index,content,embedding) VALUES(?,?,?,?,?)",
                          (str(uuid.uuid4()),document_id,i,chunk,json.dumps(emb) if emb else None))
        return {"id":document_id,"filename":filename[:255],"chunks":len(chunks),"embeddings":bool(create_embeddings and self.embedder)}

    def search(self, query: str, limit: int = 5, semantic: bool = False) -> list[dict[str, Any]]:
        if not query.strip(): return []
        limit=max(1,min(limit,20))
        if semantic and self.embedder:
            q=np.array(self.embedder.encode(query),dtype=float)
            with self._conn() as c: rows=c.execute("SELECT c.document_id,d.filename,c.content,c.embedding FROM chunks c JOIN documents d ON d.id=c.document_id WHERE c.embedding IS NOT NULL").fetchall()
            scored=[]
            for r in rows:
                v=np.array(json.loads(r["embedding"]),dtype=float)
                scored.append((float(np.dot(q,v)),dict(document_id=r["document_id"],filename=r["filename"],snippet=r["content"][:500],score=round(float(np.dot(q,v)),6))))
            return [x[1] for x in sorted(scored,key=lambda x:x[0],reverse=True)[:limit]]
        with self._conn() as c:
            try:
                rows=c.execute("SELECT document_id,filename,snippet(document_fts,2,'','', ' … ',30) AS snippet FROM document_fts WHERE document_fts MATCH ? LIMIT ?",(query,limit)).fetchall()
                return [dict(r) for r in rows]
            except sqlite3.OperationalError:
                terms=[t for t in re.split(r"\s+",query.strip()) if t]
                if not terms:return []
                sql=" OR ".join("content LIKE ?" for _ in terms)
                rows=c.execute(f"SELECT id AS document_id,filename,substr(content,1,500) AS snippet FROM documents WHERE {sql} LIMIT ?",tuple(f"%{t}%" for t in terms)+(limit,)).fetchall()
                return [dict(r) for r in rows]

    def get(self, document_id: str):
        with self._conn() as c:
            row=c.execute("SELECT id,filename,content,created_at FROM documents WHERE id=?",(document_id,)).fetchone()
            return dict(row) if row else None

    def delete(self, document_id: str) -> bool:
        with self._conn() as c:
            c.execute("DELETE FROM documents WHERE id=?",(document_id,))
            c.execute("DELETE FROM chunks WHERE document_id=?",(document_id,))
            try:c.execute("DELETE FROM document_fts WHERE document_id=?",(document_id,))
            except sqlite3.OperationalError:pass
            return c.total_changes>0

    def stats(self):
        with self._conn() as c:
            return {"documents":int(c.execute("SELECT COUNT(*) FROM documents").fetchone()[0]),
                    "chunks":int(c.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]),
                    "embedded_chunks":int(c.execute("SELECT COUNT(*) FROM chunks WHERE embedding IS NOT NULL").fetchone()[0])}
