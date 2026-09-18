"""Model registry and local availability management."""
from dataclasses import dataclass,asdict
from pathlib import Path
import json
from backend.config import settings
@dataclass
class ModelInfo:
    id:str; task:str; size_gb:float=0.0; hardware:str="CPU"; quantization:str="none"; enabled:bool=True; priority:int=100
class ModelRegistry:
    def __init__(self,path=None):
        self.path=Path(path or Path(settings.upload_dir).parent/"models_registry.json")
        self.items={}
        self.load()
    def load(self):
        if self.path.exists():
            self.items={k:ModelInfo(**v) for k,v in json.loads(self.path.read_text()).items()}
    def save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True);self.path.write_text(json.dumps({k:asdict(v) for k,v in self.items.items()},ensure_ascii=False,indent=2))
    def register(self,info):self.items[info.id]=info;self.save();return info
    def set_enabled(self,model_id,enabled):
        self.items[model_id].enabled=enabled;self.save()
    def available(self,task=None):
        vals=[x for x in self.items.values() if x.enabled and (task is None or x.task==task)]
        return sorted(vals,key=lambda x:x.priority)
    def status(self):
        return [{**asdict(x),"local_path":str(Path("data/models")/x.id),"local_available":(Path("data/models")/x.id).exists()} for x in self.items.values()]
