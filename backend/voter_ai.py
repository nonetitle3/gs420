"""GS420 Phase 24-28 Bengali voter document intelligence."""
from __future__ import annotations
import re, sqlite3, uuid
from pathlib import Path
from typing import Any

BN_DIGITS=str.maketrans("০১২৩৪৫৬৭৮৯","0123456789")
FIELD_ALIASES={
 "voter_id":["voter id","voter_id","ভোটার আইডি","ভোটার নং","ভোটার নম্বর"],
 "serial_no":["serial","ক্রমিক","ক্রমিক নং","ক্রমিক নম্বর","সিরিয়াল"],
 "name":["name","নাম"],
 "father_name":["father","father name","পিতা","পিতার নাম"],
 "mother_name":["mother","mother name","মাতা","মাতার নাম"],
 "birth_date":["birth","date of birth","জন্ম","জন্ম তারিখ"],
 "gender":["gender","লিঙ্গ"],
 "occupation":["occupation","পেশা"],
 "address":["address","ঠিকানা"],
 "village":["village","গ্রাম"],
 "ward":["ward","ওয়ার্ড","ওয়ার্ড"],
 "union_name":["union","ইউনিয়ন","ইউনিয়ন"],
 "upazila":["upazila","উপজেলা"],
 "district":["district","জেলা"],
 "division":["division","বিভাগ"],
 "post_code":["post code","postcode","পোস্ট কোড"],
}

def normalize_digits(value:str)->str:
 return value.translate(BN_DIGITS)

def clean(value:str|None)->str|None:
 if value is None:return None
 value=re.sub(r"[\t\r ]+"," ",value)
 value=re.sub(r"\n+"," ",value)
 return value.strip(" :-|,") or None

def normalize_value(value:str|None)->str|None:
 value=clean(value)
 if not value:return None
 return normalize_digits(value)

def parse_label_lines(text:str)->list[dict[str,Any]]:
 lines=[clean(x) for x in text.splitlines()]
 lines=[x for x in lines if x]
 records=[]; current={}
 for line in lines:
  found=None
  for field,aliases in FIELD_ALIASES.items():
   for alias in aliases:
    if re.match(r"^\s*"+re.escape(alias)+r"\s*(?:[:：\-]|\s{2,})",line,re.I):
     found=field; break
   if found: break
  if found:
   pattern=r"^\s*"+r"(?:"+ "|".join(re.escape(a) for a in FIELD_ALIASES[found]) + r")\s*(?:[:：\-]|\s{2,})\s*(.*)$"
   m=re.match(pattern,line,re.I)
   if m: current[found]=normalize_value(m.group(1))
  elif ("voter_id" in current or "name" in current) and len(current)>=2 and re.search(r"\d",line):
   current.setdefault("raw_line",line)
 if current: records.append(current)
 return records

class VoterStore:
 def __init__(self,path="./data/gs420_voters.db"):
  self.path=path; Path(path).parent.mkdir(parents=True,exist_ok=True); self._init()
 def _conn(self):
  c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c
 def _init(self):
  with self._conn() as c:
   c.execute("""CREATE TABLE IF NOT EXISTS voters(
    id TEXT PRIMARY KEY, document_id TEXT, voter_id TEXT, serial_no TEXT, name TEXT,
    father_name TEXT, mother_name TEXT, birth_date TEXT, gender TEXT, occupation TEXT,
    address TEXT, village TEXT, ward TEXT, union_name TEXT, upazila TEXT, district TEXT,
    division TEXT, post_code TEXT, raw_text TEXT, source_page INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
   c.execute("CREATE INDEX IF NOT EXISTS idx_voter_id ON voters(voter_id)")
   c.execute("CREATE INDEX IF NOT EXISTS idx_name ON voters(name)")
   c.execute("CREATE INDEX IF NOT EXISTS idx_district ON voters(district)")
 def add_records(self,document_id:str,records:list[dict[str,Any]],raw_text:str="",page:int|None=None):
  inserted=0; duplicates=0
  with self._conn() as c:
   for r in records:
    key=r.get("voter_id") or "|".join(str(r.get(k) or "") for k in ("name","father_name","birth_date"))
    if not key: continue
    exists=c.execute("SELECT id FROM voters WHERE voter_id=? OR (voter_id IS NULL AND ?<>'' AND name=? AND father_name=? AND birth_date=?)",
      (r.get("voter_id"),r.get("voter_id") or "",r.get("name"),r.get("father_name"),r.get("birth_date"))).fetchone()
    if exists: duplicates+=1; continue
    c.execute("""INSERT INTO voters(id,document_id,voter_id,serial_no,name,father_name,mother_name,birth_date,gender,occupation,address,village,ward,union_name,upazila,district,division,post_code,raw_text,source_page)
      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
      (str(uuid.uuid4()),document_id,r.get("voter_id"),r.get("serial_no"),r.get("name"),r.get("father_name"),r.get("mother_name"),r.get("birth_date"),r.get("gender"),r.get("occupation"),r.get("address"),r.get("village"),r.get("ward"),r.get("union_name"),r.get("upazila"),r.get("district"),r.get("division"),r.get("post_code"),raw_text[:4000],page))
    inserted+=1
  return {"inserted":inserted,"duplicates":duplicates}
 def search(self,q:str,limit=50):
  terms=[x for x in re.split(r"\s+",normalize_digits(q).strip()) if x]
  if not terms:return []
  clauses=[];params=[]
  cols=["voter_id","serial_no","name","father_name","mother_name","birth_date","gender","occupation","address","village","ward","union_name","upazila","district","division","post_code"]
  for t in terms:
   clauses.append("("+" OR ".join(f"COALESCE({c},'') LIKE ?" for c in cols)+")")
   params.extend([f"%{t}%"]*len(cols))
  with self._conn() as c:
   rows=c.execute("SELECT * FROM voters WHERE "+" AND ".join(clauses)+" LIMIT ?",(*params,min(max(limit,1),200))).fetchall()
   return [dict(x) for x in rows]
 def stats(self):
  with self._conn() as c:return {"records":c.execute("SELECT COUNT(*) FROM voters").fetchone()[0],"with_voter_id":c.execute("SELECT COUNT(*) FROM voters WHERE voter_id IS NOT NULL AND voter_id<>''").fetchone()[0]}

def extract_and_store(document_id:str,text:str,store:VoterStore)->dict[str,Any]:
 records=parse_label_lines(text)
 result=store.add_records(document_id,records,text)
 result["parsed"]=len(records); return result
