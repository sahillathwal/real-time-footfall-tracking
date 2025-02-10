import torch
from ultralytics import YOLO
from insightface.app import FaceAnalysis

class FaceDetector:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load RetinaFace (InsightFace)
        self.face_detector = FaceAnalysis(name="buffalo_l")
        self.face_detector.prepare(ctx_id=0)  # GPU execution

        # Load YOLOv8-Face
        self.yolo_face = YOLO("models/face/yolov8-face.pt").to(self.device)

    def detect_faces(self, image):
        # Run RetinaFace first (GPU)
        faces = self.face_detector.get(image)
        if len(faces) == 0:  
            # If RetinaFace fails, use YOLOv8-Face
            results = self.yolo_face(image)
            faces = results[0].boxes.data.cpu().numpy()
        return faces
