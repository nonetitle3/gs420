def test_model_registry(tmp_path):
 from backend.models.registry import ModelRegistry,ModelInfo
 r=ModelRegistry(tmp_path/"m.json");r.register(ModelInfo("demo","general_chat",1.2,"CPU","GGUF",priority=1))
 assert r.available("general_chat")[0].id=="demo"
 r.set_enabled("demo",False);assert not r.available()
def test_model_api_exists():
 from backend.api.models import router
 assert any(r.path=="" for r in router.routes)
