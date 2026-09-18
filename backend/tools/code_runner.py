"""Defense-in-depth Python execution. Use an isolated container/VM for hostile multi-tenant workloads."""
import ast,subprocess,sys,tempfile,os
from pathlib import Path
from backend.config import settings

BLOCKED_IMPORTS={"os","subprocess","socket","shutil","requests","urllib","ctypes","multiprocessing"}
BLOCKED_CALLS={"eval","exec","compile","__import__","open"}

def _safe(code:str):
    if len(code)>20000:return False,"Code too large"
    try: tree=ast.parse(code)
    except SyntaxError:return True,None
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            if any(a.name.split(".")[0] in BLOCKED_IMPORTS for a in n.names): return False,"Blocked import"
        if isinstance(n,ast.ImportFrom) and (n.module or "").split(".")[0] in BLOCKED_IMPORTS:return False,"Blocked import"
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in BLOCKED_CALLS:return False,"Blocked operation"
    return True,None

def run_python(code:str,timeout=None)->dict:
    ok,error=_safe(code)
    if not ok:return {"ok":False,"error":error}
    timeout=timeout or settings.sandbox_timeout_seconds
    with tempfile.TemporaryDirectory(prefix="gs420-run-") as d:
        p=Path(d)/"main.py";p.write_text(code,encoding="utf-8")
        env={"PATH":os.environ.get("PATH",""),"PYTHONIOENCODING":"utf-8","PYTHONNOUSERSITE":"1","HOME":d}
        try:
            r=subprocess.run([sys.executable,"-I",str(p)],cwd=d,env=env,capture_output=True,text=True,timeout=timeout)
            limit=settings.sandbox_max_output_chars
            return {"ok":r.returncode==0,"stdout":r.stdout[:limit],"stderr":r.stderr[:limit],"returncode":r.returncode}
        except subprocess.TimeoutExpired:return {"ok":False,"error":"Execution timed out"}
