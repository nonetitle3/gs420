"""Replaceable GPU video generation adapter.
Heavy video models are optional and never assumed on free CPU hosting.
"""
from pathlib import Path
class VideoGenerationService:
    def __init__(self,model_id=None):
        self.model_id=model_id
        self._pipeline=None
    def generate(self,prompt,output_path):
        if not self.model_id:raise RuntimeError("Video model is not configured")
        raise RuntimeError("Configure a compatible LTX/Wan GPU pipeline before generation")
    def image_to_video(self,image_path,prompt,output_path):
        if not self.model_id:raise RuntimeError("Video model is not configured")
        raise RuntimeError("Configure a compatible image-to-video GPU pipeline before generation")
