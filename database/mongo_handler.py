from pymongo import MongoClient
import datetime
import numpy as np

def connect_db():
    """Establishes a connection to MongoDB."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["footfall_tracking"]
    return db

def store_person_embedding(person_id, track_id, face_embedding, camera_id):
    """Stores or updates a person's face embedding in MongoDB."""
    db = connect_db()
    collection = db["face_embeddings"]
    
    existing_person = collection.find_one({"person_id": person_id})
    
    if existing_person:
        collection.update_one(
            {"person_id": person_id},
            {"$set": {"last_seen": datetime.datetime.utcnow(), "track_id": track_id}}
        )
    else:
        person_data = {
            "person_id": person_id,
            "track_id": track_id,
            "face_embedding": face_embedding.tolist() if face_embedding is not None else None,
            "first_seen": datetime.datetime.utcnow(),
            "last_seen": datetime.datetime.utcnow(),
            "camera_id": camera_id,
            "entry_count": 1
        }
        collection.insert_one(person_data)

def get_matching_person(face_embedding, threshold=0.5):
    """Finds the closest matching person based on face embedding similarity."""
    db = connect_db()
    collection = db["face_embeddings"]
    
    people = collection.find()
    min_distance = float("inf")
    best_match = None
    
    for person in people:
        stored_embedding = np.array(person["face_embedding"])
        distance = np.linalg.norm(face_embedding - stored_embedding)
        
        if distance < min_distance and distance < threshold:
            min_distance = distance
            best_match = person["person_id"]
    
    return best_match