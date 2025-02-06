from ultralytics import YOLO
import cv2

# Load YOLOv8 Model for people detection
model = YOLO("yolov8n.pt")

def detect_people(frame):
    """Detect people in a frame using YOLOv8."""
    results = model(frame)
    boxes = []
    for result in results:
        for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
            if int(cls) == 0:  # Class 0 corresponds to 'person' in COCO dataset
                x1, y1, x2, y2 = map(int, box)
                boxes.append((x1, y1, x2, y2, float(conf)))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"{conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return frame, boxes