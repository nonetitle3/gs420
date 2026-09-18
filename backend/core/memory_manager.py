import sqlite3
from pathlib import Path
from backend.config import settings
class MemoryManager:
 def __init__(self,path=None):
  self.path=path or settings.db_path;Path(self.path).parent.mkdir(parents=True,exist_ok=True)
  with sqlite3.connect(self.path) as c:c.executescript("CREATE TABLE IF NOT EXISTS conversations(id INTEGER PRIMARY KEY,session_id TEXT,role TEXT,content TEXT,created_at DATETIME DEFAULT CURRENT_TIMESTAMP);CREATE TABLE IF NOT EXISTS memories(id INTEGER PRIMARY KEY,kind TEXT,content TEXT,created_at DATETIME DEFAULT CURRENT_TIMESTAMP);CREATE VIRTUAL TABLE IF NOT EXISTS conversations_fts USING fts5(content,content='conversations',content_rowid='id');")
 def add_message(self,sid,role,content):
  with sqlite3.connect(self.path) as c:
   q=c.execute("INSERT INTO conversations(session_id,role,content) VALUES(?,?,?)",(sid,role,content));c.execute("INSERT INTO conversations_fts(rowid,content) VALUES(?,?)",(q.lastrowid,content))
 def history(self,sid,limit=20):
  with sqlite3.connect(self.path) as c:return [{"role":r[0],"content":r[1]} for r in c.execute("SELECT role,content FROM conversations WHERE session_id=? ORDER BY id DESC LIMIT ?",(sid,limit)).fetchall()][::-1]
 def add_memory(self,content,kind="fact"):
  with sqlite3.connect(self.path) as c:c.execute("INSERT INTO memories(kind,content) VALUES(?,?)",(kind,content))
 def memories(self):
  with sqlite3.connect(self.path) as c:return [{"id":r[0],"kind":r[1],"content":r[2]} for r in c.execute("SELECT id,kind,content FROM memories ORDER BY id DESC")]
 def delete_memory(self,i):
  with sqlite3.connect(self.path) as c:c.execute("DELETE FROM memories WHERE id=?",(i,))
