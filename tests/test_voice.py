def test_stt_adapter_shape():
 from backend.services.stt import STTService
 s=STTService();assert s.model_id
def test_tts_requires_model():
 from backend.services.tts import TTSService
 try:TTSService().synthesize("hello","/tmp/x.wav")
 except RuntimeError as e:assert "PIPER_MODEL_PATH" in str(e)
