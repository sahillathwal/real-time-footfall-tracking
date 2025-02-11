import torch
import numpy as np
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
from ultralytics import YOLO

class MultiPersonTracker:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.yolo_model = YOLO("models/person/yolov8n.pt").to(self.device)

        # Initialize DeepSORT tracker
        self.tracker = DeepSort(
            max_age=30, n_init=3, max_iou_distance=0.7,
            nn_budget=100, use_cuda=torch.cuda.is_available()
        )

    def track_people(self, frame):
        """ Detect and track people in a frame. """
        results = self.yolo_model(frame)
        detections = results[0].boxes.data.cpu().numpy()

        bbox_xywh = []
        confs = []
        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            if int(cls) == 0:  # Class 0 is 'person'
                w, h = x2 - x1, y2 - y1
                bbox_xywh.append([x1, y1, w, h])
                confs.append(conf)

        tracks = self.tracker.update_tracks(np.array(bbox_xywh), np.array(confs), frame)

        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            x1, y1, x2, y2 = track.to_ltwh()
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"ID {track_id}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame
