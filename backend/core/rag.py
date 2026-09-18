"""Small persistent lexical RAG index using SQLite FTS5."""
import sqlite3
from pathlib import Path
class RAGStore:
    def __init__(self,db_path):
        self.db_path=str(db_path);Path(self.db_path).parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(self.db_path) as c:c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(doc_id UNINDEXED, content)")
    def add(self,doc_id,content):
        with sqlite3.connect(self.db_path) as c:c.execute("DELETE FROM documents_fts WHERE doc_id=?",(doc_id,));c.execute("INSERT INTO documents_fts VALUES (?,?)",(doc_id,content))
    def search(self,query,limit=5):
        with sqlite3.connect(self.db_path) as c:
            rows=c.execute("SELECT doc_id,content FROM documents_fts WHERE documents_fts MATCH ? LIMIT ?",(query,limit)).fetchall()
        return [{"doc_id":r[0],"content":r[1]} for r in rows]
