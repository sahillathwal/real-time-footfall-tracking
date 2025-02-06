from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")  # Download YOLOv8 if not available

def detect_faces(frame):
    results = model(frame)
    for result in results:
        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    return frame