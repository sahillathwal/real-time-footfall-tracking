import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
from embedding.face_embedding import get_face_embedding, extract_face
from database.mongo_handler import store_person_embedding, get_matching_person

# Initialize DeepSORT Tracker
tracker = DeepSort(max_age=60, n_init=3, nms_max_overlap=1.0, max_cosine_distance=0.1)

def track_people(frame, boxes):
    """Track people using DeepSORT and store data in MongoDB."""
    detections = []
    for box in boxes:
        x1, y1, x2, y2, conf = box
        face = extract_face(frame, (x1, y1, x2, y2))
        face_embedding = get_face_embedding(face) if face is not None else None
        person_id = get_matching_person(face_embedding) if face_embedding is not None else None
        
        if person_id is None:
            person_id = f"P{int(conf * 100000)}"  # Generate a unique ID if not found
        
        detections.append(([x1, y1, x2 - x1, y2 - y1], conf, None))
        store_person_embedding(person_id, conf, face_embedding, "main_gate")
    
    tracks = tracker.update_tracks(detections, frame=frame)
    
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        ltrb = track.to_ltrb()
        x1, y1, x2, y2 = map(int, ltrb)
        
        # Draw bounding box and track ID
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame, tracks