import time
import torch
from ultralytics import YOLO

device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO("models/person/yolov8n.pt").to(device)

# Load a test image
image_path = "data/raw/frame_001.jpg"

# Benchmarking
start_time = time.time()
results = model(image_path)
end_time = time.time()

print(f"✅ YOLOv8 Inference Completed in {end_time - start_time:.3f} seconds")