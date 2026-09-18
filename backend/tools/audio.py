from backend.services.stt import STTService
def transcribe(path,model):return STTService(model).transcribe(path)
