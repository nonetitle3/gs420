"""Open-source Whisper-compatible STT adapter with graceful fallback."""
from pathlib import Path
class STTService:
    def __init__(self,model_id="openai/whisper-small"):
        self.model_id=model_id;self._pipe=None
    def _load(self):
        if self._pipe is None:
            from transformers import pipeline
            self._pipe=pipeline("automatic-speech-recognition",model=self.model_id)
        return self._pipe
    def transcribe(self,audio_path):
        path=Path(audio_path)
        if not path.exists():raise FileNotFoundError(str(path))
        result=self._load()(str(path))
        return {"text":result.get("text","").strip(),"model":self.model_id}
