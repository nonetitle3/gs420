"""Restricted Python runner for coding tasks. No shell execution."""
import subprocess,sys,tempfile,os
from pathlib import Path
from backend.config import settings
def run_python(code:str,timeout=None)->dict:
    timeout=timeout or settings.sandbox_timeout
    if len(code)>20000:return {"ok":False,"error":"Code too large"}
    blocked=("os.system","subprocess","shutil.rmtree","socket.","requests.","urllib.")
    if any(x in code for x in blocked):return {"ok":False,"error":"Blocked operation"}
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"main.py";p.write_text(code,encoding="utf-8")
        try:
            r=subprocess.run([sys.executable,"-I",str(p)],cwd=d,input="",text=True,capture_output=True,timeout=timeout,env={"PATH":os.environ.get("PATH","")})
            return {"ok":r.returncode==0,"stdout":r.stdout[:settings.sandbox_output_chars],"stderr":r.stderr[:settings.sandbox_output_chars],"returncode":r.returncode}
        except subprocess.TimeoutExpired:return {"ok":False,"error":"Execution timed out"}
