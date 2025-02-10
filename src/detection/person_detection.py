import torch
from ultralytics import YOLO

class PersonDetector:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = YOLO("models/person/yolov8n.pt").to(self.device)

    def detect_people(self, image):
        results = self.model(image)
        return results[0].boxes.data.cpu().numpy()
