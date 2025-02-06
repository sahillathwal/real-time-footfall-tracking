from deepface import DeepFace
import cv2

def extract_embedding(face_img):
    embedding = DeepFace.represent(face_img, model_name="Facenet")
    return embedding