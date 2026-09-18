class ImageGenerationService:
 def generate(self,prompt,out="data/cache/generated.png"):
  from diffusers import DiffusionPipeline
  pipe=DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell");pipe(prompt).images[0].save(out);return out
