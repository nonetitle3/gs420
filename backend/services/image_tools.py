"""Local image enhancement utilities that do not require a generative model."""
from PIL import Image,ImageEnhance,ImageFilter
from pathlib import Path
def enhance(input_path,output_path,sharpness=1.4,contrast=1.08):
    image=Image.open(input_path).convert("RGB")
    image=ImageEnhance.Contrast(image).enhance(contrast)
    image=ImageEnhance.Sharpness(image).enhance(sharpness)
    out=Path(output_path);out.parent.mkdir(parents=True,exist_ok=True);image.save(out,quality=95)
    return {"path":str(out)}
def upscale(input_path,output_path,scale=2):
    image=Image.open(input_path).convert("RGB");image=image.resize((image.width*scale,image.height*scale),Image.Resampling.LANCZOS)
    out=Path(output_path);out.parent.mkdir(parents=True,exist_ok=True);image.save(out,quality=95)
    return {"path":str(out),"scale":scale}
def remove_background(input_path,output_path):
    raise RuntimeError("Background removal requires an optional configured segmentation backend")
