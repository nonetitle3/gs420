import subprocess,tempfile,pathlib,sys
def run_python(code,timeout=5):
 d=pathlib.Path(tempfile.mkdtemp(prefix="gs420-"));f=d/"main.py";f.write_text(code,encoding="utf8")
 try:
  p=subprocess.run([sys.executable,str(f)],cwd=d,text=True,capture_output=True,timeout=timeout)
  return {"returncode":p.returncode,"stdout":p.stdout[:10000],"stderr":p.stderr[:10000]}
 except subprocess.TimeoutExpired:return {"returncode":124,"stdout":"","stderr":"Execution timed out"}
