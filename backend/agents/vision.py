class VisionAgent:
    def analyze(self,image_path,vision_service):
        return vision_service.analyze(image_path)
