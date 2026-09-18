"""GS420 AI Google Colab bootstrap."""
from __future__ import annotations
import os, platform, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(cmd):
    print("$"," ".join(cmd))
    subprocess.check_call(cmd,cwd=ROOT)

def detect():
    info={"python":sys.version.split()[0],"platform":platform.platform(),"cuda":False,"gpu":None}
    try:
        import torch
        info["cuda"]=bool(torch.cuda.is_available())
        if info["cuda"]:
            info["gpu"]=torch.cuda.get_device_name(0)
            info["vram_gb"]=round(torch.cuda.get_device_properties(0).total_memory/(1024**3),2)
    except Exception as exc:
        info["torch_error"]=type(exc).__name__
    return info

def main():
    print("GS420 AI — Google Colab setup")
    print(detect())
    if os.environ.get("GS420_COLAB_SKIP_INSTALL")!="1":
        run([sys.executable,"-m","pip","install","-r","requirements-colab.txt"])
    print("Setup complete.")
    print("API: python start.py")
    print("Gradio: python app.py")
    print("Keep tokens in Colab secrets/environment variables.")

if __name__=="__main__":
    main()
