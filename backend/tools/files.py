from pathlib import Path
ALLOWED={".txt",".md",".pdf",".docx",".csv",".xlsx",".png",".jpg",".jpeg",".webp"}
def safe_path(root,name):
 p=(Path(root)/Path(name).name).resolve()
 if p.suffix.lower() not in ALLOWED:raise ValueError("File type not allowed")
 return p
