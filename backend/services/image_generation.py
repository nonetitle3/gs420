"""Replaceable Hugging Face Diffusers image backend."""
from pathlib import Path
class ImageGenerationService:
    def __init__(self,model_id=None):
        self.model_id=model_id
        self._pipe=None
    def _load(self):
        if not self.model_id:raise RuntimeError("Image model is not configured")
        if self._pipe is None:
            from diffusers import DiffusionPipeline
            import torch
            self._pipe=DiffusionPipeline.from_pretrained(self.model_id,torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
            self._pipe.to("cuda" if torch.cuda.is_available() else "cpu")
        return self._pipe
    def generate(self,prompt,output_path):
        if not prompt.strip():raise ValueError("Prompt is required")
        image=self._load()(prompt).images[0]
        out=Path(output_path);out.parent.mkdir(parents=True,exist_ok=True);image.save(out)
        return {"path":str(out),"model":self.model_id}
    def image_to_image(self,image_path,prompt,output_path):
        if not prompt.strip():raise ValueError("Prompt is required")
        from PIL import Image
        image=self._load()(prompt,image=Image.open(image_path)).images[0]
        out=Path(output_path);out.parent.mkdir(parents=True,exist_ok=True);image.save(out)
        return {"path":str(out),"model":self.model_id}
