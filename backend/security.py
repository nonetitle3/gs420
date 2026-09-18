"""Phase 20 security helpers."""
from __future__ import annotations
import os,secrets,re
from pathlib import Path
from fastapi import HTTPException

SAFE_NAME=re.compile(r"[^A-Za-z0-9._-]+")

def generate_secret(length:int=32)->str:
    if length<16: raise ValueError("Secret length must be at least 16.")
    return secrets.token_urlsafe(length)

def redacted_environment()->dict[str,str]:
    sensitive=("TOKEN","SECRET","PASSWORD","KEY")
    return {k:("***" if any(x in k.upper() for x in sensitive) else v)
            for k,v in os.environ.items() if k.startswith("GS420_")}

def safe_filename(name:str,default="upload.bin")->str:
    base=Path(name or default).name
    base=SAFE_NAME.sub("_",base).strip(". ")
    return (base or default)[:180]

def validate_upload(data:bytes,filename:str,max_mb:int,allowed:set[str]):
    ext=Path(filename).suffix.lower()
    if ext not in allowed: raise HTTPException(400,"Unsupported file type")
    if len(data)>max_mb*1024*1024: raise HTTPException(413,"File too large")
    return safe_filename(filename)
