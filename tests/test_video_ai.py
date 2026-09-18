def test_video_generation_requires_model():
 from backend.services.video_generation import VideoGenerationService
 try:VideoGenerationService().generate("test","/tmp/x.mp4")
 except RuntimeError as e:assert "not configured" in str(e)
def test_video_api_exists():
 from backend.api.video import router
 assert any(r.path=="/generate" for r in router.routes)
