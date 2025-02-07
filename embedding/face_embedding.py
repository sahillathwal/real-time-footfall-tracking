import numpy as np
from deepface import DeepFace

def extract_face(frame, bbox):
    """Extracts the face region from the frame based on bounding box coordinates."""
    x1, y1, x2, y2 = bbox
    face = frame[y1:y2, x1:x2]
    return face

def get_face_embedding(face_image):
    """Generates a FaceNet embedding from a detected face image."""
    try:
        embedding = DeepFace.represent(face_image, model_name='Facenet', enforce_detection=False)[0]['embedding']
        return np.array(embedding)
    except Exception as e:
        print(f"Error extracting face embedding: {e}")
        return None