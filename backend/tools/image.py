from PIL import Image,ImageEnhance
def enhance(path,out):
 im=Image.open(path).convert("RGB");im=ImageEnhance.Sharpness(im).enhance(1.2);im.save(out,quality=95);return out
