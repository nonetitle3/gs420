"""SQLite-backed short/long-term memory with FTS5 search and deletion."""
import sqlite3
from pathlib import Path
from backend.config import settings

class MemoryManager:
    def __init__(self,path=None):
        self.path=str(path or settings.db_path);Path(self.path).parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(self.path) as c:
            c.executescript("""
            CREATE TABLE IF NOT EXISTS conversations(id INTEGER PRIMARY KEY,session_id TEXT NOT NULL,role TEXT NOT NULL,content TEXT NOT NULL,created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY,kind TEXT NOT NULL,content TEXT NOT NULL,created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS preferences(id INTEGER PRIMARY KEY,key TEXT UNIQUE NOT NULL,value TEXT NOT NULL,created_at DATETIME DEFAULT CURRENT_TIMESTAMP,updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS saved_prompts(id INTEGER PRIMARY KEY,title TEXT NOT NULL,prompt TEXT NOT NULL,created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
            CREATE VIRTUAL TABLE IF NOT EXISTS conversations_fts USING fts5(content,content='conversations',content_rowid='id');
            """)
    def _conn(self): return sqlite3.connect(self.path)
    def add_message(self,sid,role,content):
        with self._conn() as c:
            q=c.execute("INSERT INTO conversations(session_id,role,content) VALUES(?,?,?)",(sid,role,content))
            c.execute("INSERT INTO conversations_fts(rowid,content) VALUES(?,?)",(q.lastrowid,content))
    def history(self,sid,limit=20):
        with self._conn() as c:
            rows=c.execute("SELECT role,content FROM conversations WHERE session_id=? ORDER BY id DESC LIMIT ?",(sid,limit)).fetchall()
        return [{"role":r,"content":v} for r,v in reversed(rows)]
    def clear_session(self,sid):
        with self._conn() as c:
            ids=[r[0] for r in c.execute("SELECT id FROM conversations WHERE session_id=?",(sid,))]
            c.execute("DELETE FROM conversations WHERE session_id=?",(sid,))
            for i in ids:c.execute("DELETE FROM conversations_fts WHERE rowid=?",(i,))
    def search(self,query,limit=10):
        with self._conn() as c:
            return [{"session_id":r[0],"role":r[1],"content":r[2]} for r in c.execute("SELECT c.session_id,c.role,c.content FROM conversations c JOIN conversations_fts f ON f.rowid=c.id WHERE conversations_fts MATCH ? ORDER BY c.id DESC LIMIT ?",(query,limit))]
    def add_memory(self,content,kind="fact"):
        with self._conn() as c:c.execute("INSERT INTO memories(kind,content) VALUES(?,?)",(kind,content))
    def memories(self,kind=None):
        with self._conn() as c:
            q="SELECT id,kind,content FROM memories";args=()
            if kind:q+=" WHERE kind=?";args=(kind,)
            q+=" ORDER BY id DESC"
            return [{"id":r[0],"kind":r[1],"content":r[2]} for r in c.execute(q,args)]
    def delete_memory(self,i):
        with self._conn() as c:c.execute("DELETE FROM memories WHERE id=?",(i,))
    def set_preference(self,key,value):
        with self._conn() as c:c.execute("INSERT INTO preferences(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value,updated_at=CURRENT_TIMESTAMP",(key,value))
    def preferences(self):
        with self._conn() as c:return [{"key":r[0],"value":r[1]} for r in c.execute("SELECT key,value FROM preferences ORDER BY key")]
    def save_prompt(self,title,prompt):
        with self._conn() as c:
            q=c.execute("INSERT INTO saved_prompts(title,prompt) VALUES(?,?)",(title,prompt));return q.lastrowid
    def saved_prompts(self):
        with self._conn() as c:return [{"id":r[0],"title":r[1],"prompt":r[2]} for r in c.execute("SELECT id,title,prompt FROM saved_prompts ORDER BY id DESC")]
    def delete_all(self):
        with self._conn() as c:c.executescript("DELETE FROM conversations;DELETE FROM memories;DELETE FROM preferences;DELETE FROM saved_prompts;DELETE FROM conversations_fts;")
