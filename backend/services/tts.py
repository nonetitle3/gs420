import subprocess,tempfile
class TTSService:
 def __init__(self,voice):self.voice=voice
 def synthesize(self,text,out=None):
  if not self.voice:raise RuntimeError("Piper voice is not configured")
  out=out or tempfile.mktemp(suffix=".wav");p=subprocess.run(["piper","--model",self.voice,"--output_file",out],input=text,text=True,capture_output=True,timeout=30)
  if p.returncode:raise RuntimeError(p.stderr.strip() or "Piper failed")
  return out
