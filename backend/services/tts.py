"""Piper TTS adapter. Piper executable/model are optional local dependencies."""
import subprocess
from pathlib import Path
class TTSService:
    def __init__(self,executable="piper",model_path=None):
        self.executable=executable;self.model_path=model_path
    def synthesize(self,text,output_path):
        if not self.model_path:raise RuntimeError("Configure PIPER_MODEL_PATH before TTS use")
        out=Path(output_path);out.parent.mkdir(parents=True,exist_ok=True)
        cmd=[self.executable,"--model",self.model_path,"--output_file",str(out)]
        try: subprocess.run(cmd,input=text,text=True,capture_output=True,check=True,timeout=120)
        except FileNotFoundError as e:raise RuntimeError("Piper executable not installed") from e
        return {"path":str(out)}
