def test_local_image_tools(tmp_path):
 from PIL import Image
 from backend.services.image_tools import enhance,upscale
 src=tmp_path/"a.png";Image.new("RGB",(10,10),"white").save(src)
 assert Path(enhance(src,tmp_path/"e.png")["path"]).exists()
 assert Path(upscale(src,tmp_path/"u.png",2)["path"]).exists()
def test_generator_without_model():
 from backend.services.image_generation import ImageGenerationService
 try:ImageGenerationService().generate("test","/tmp/x.png")
 except RuntimeError as e:assert "not configured" in str(e)
